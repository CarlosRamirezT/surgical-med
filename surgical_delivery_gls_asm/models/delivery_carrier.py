# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from xml.sax.saxutils import escape

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

from odoo.addons.delivery_gls_asm.models.gls_asm_request import GlsAsmRequest


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    # def _prepare_gls_asm_shipping(self, picking):
    #     res = super(DeliveryCarrier, self)._prepare_gls_asm_shipping(picking)
        
    #     # update the customized values

    #     res["destinatario_observaciones"] = (
    #         picking.note and escape(picking.note) or ""
    #     )
    #     res["referencia_c"] = (
    #         picking.origin
    #         and escape(f"{picking.name}/{picking.origin}")
    #         or escape(picking.name),
    #     )  # Our unique reference

    #     # return updated shipping values
        
    #     return res
    
    def _prepare_gls_asm_shipping(self, picking):
        """Convert picking values for asm api
        :param picking record with picking to send
        :returns dict values for the connector
        """
        self.ensure_one()
        # A picking can be delivered from any warehouse
        sender_partner = (
            picking.picking_type_id.warehouse_id.partner_id
            or picking.company_id.partner_id
        )
        consignee = picking.partner_id
        consignee_entity = picking.partner_id.commercial_partner_id
        if not sender_partner.street:
            raise UserError(_("Couldn't find the sender street"))
        cash_amount = 0
        if self.gls_asm_cash_on_delivery:
            cash_amount = picking.sale_id.amount_total
        return {
            "fecha": fields.Date.today().strftime("%d/%m/%Y"),
            "portes": self.gls_asm_postage_type,
            "servicio": self.gls_asm_service,
            "horario": self.gls_asm_shiptime,
            "bultos": picking.number_of_packages,
            "peso": round(picking.shipping_weight, 3),
            "volumen": "",  # [optional] Volume, in m3
            "declarado": "",  # [optional]
            "dninomb": "0",  # [optional]
            "fechaentrega": "",  # [optional]
            "retorno": "1" if self.gls_asm_with_return else "0",  # [optional]
            "pod": "N",  # [optional]
            "podobligatorio": "N",  # [deprecated]
            "remite_plaza": "",  # [optional] Origin agency
            "remite_nombre": escape(
                sender_partner.name or sender_partner.parent_id.name
            ),
            "remite_direccion": escape(sender_partner.street or ""),
            "remite_poblacion": escape(sender_partner.city or ""),
            "remite_provincia": escape(sender_partner.state_id.name or ""),
            "remite_pais": "34",  # [mandatory] always 34=Spain
            "remite_cp": sender_partner.zip or "",
            "remite_telefono": sender_partner.phone or "",
            "remite_movil": sender_partner.mobile or "",
            "remite_email": escape(sender_partner.email or ""),
            "remite_departamento": "",
            "remite_nif": sender_partner.vat or "",
            "remite_observaciones": "",
            "destinatario_codigo": "",
            "destinatario_plaza": "",
            "destinatario_nombre": (
                escape(consignee.name or consignee.commercial_partner_id.name or "")
            ),
            "destinatario_direccion": escape(consignee.street or ""),
            "destinatario_poblacion": escape(consignee.city or ""),
            "destinatario_provincia": escape(consignee.state_id.name or ""),
            "destinatario_pais": consignee.country_id.phone_code or "",
            "destinatario_cp": consignee.zip,
            # For certain destinations the consignee mobile and email are required to
            # make the expedition. Try to fallback to the commercial entity one
            "destinatario_telefono": consignee.phone or consignee_entity.phone or "",
            "destinatario_movil": consignee.mobile or consignee_entity.mobile or "",
            "destinatario_email": escape(
                consignee.email or consignee_entity.email or ""
            ),
            "destinatario_observaciones": picking.gls_shipping_notes or "",
            "destinatario_att": "",
            "destinatario_departamento": "",
            "destinatario_nif": "",
            "referencia_c": 
                picking.origin and escape(f"{picking.name}/{picking.origin}".replace("\\", "/")) or picking.name.replace("\\", "/") # It errors with \ characters
            ,
            "referencia_0": "",  # Not used if the above is set
            "importes_debido": "0",  # The customer pays the shipping
            "importes_reembolso": cash_amount or "",
            "seguro": "0",  # [optional]
            "seguro_descripcion": "",  # [optional]
            "seguro_importe": "",  # [optional]
            "etiqueta": "PDF",  # Get Label in response
            "etiqueta_devolucion": "PDF",
            # [optional] GLS Customer Code
            # (when customer have several codes in GLS)
            "cliente_codigo": "",
            "cliente_plaza": "",
            "cliente_agente": "",
        }
    
    def gls_asm_send_shipping(self, pickings):
        """Send the package to GLS
        :param pickings: A recordset of pickings
        :return list: A list of dictionaries although in practice it's
        called one by one and only the first item in the dict is taken. Due
        to this design, we have to inject vals in the context to be able to
        add them to the message.
        """
        gls_request = GlsAsmRequest(self._gls_asm_uid())
        result = []
        for picking in pickings:
            if picking.carrier_id.gls_is_pickup_service:
                continue
            vals = self._prepare_gls_asm_shipping(picking)
            # force remove referencia_c length validation

            # if len(vals.get("referencia_c", "")) > 15:
            #     raise UserError(
            #         _(
            #             "GLS-ASM API doesn't admit a reference number higher than "
            #             "15 characters. In order to handle it, they trim the"
            #             "reference and as the reference is unique to every "
            #             "customer we soon would have duplicated reference "
            #             "collisions. To prevent this, you should edit your picking "
            #             "sequence to a max of 15 characters."
            #         )
            #     )

            vals.update({"tracking_number": False, "exact_price": 0})
            response = gls_request._send_shipping(vals)
            self.log_xml(
                response and response.get("gls_sent_xml", ""),
                "GLS ASM Shipping Request",
            )
            self.log_xml(response or "", "GLS ASM Shipping Response")
            if not response or response.get("_return", -1) < 0:
                result.append(vals)
                continue
            # For compatibility we provide this number although we get
            # two more codes: codbarras and uid
            vals["tracking_number"] = response.get("_codexp")
            gls_asm_picking_ref = ""
            try:
                references = response.get("Referencias", {}).get("Referencia", [])
                for ref in references:
                    if ref.get("_tipo", "") == "N":
                        gls_asm_picking_ref = ref.get("value", "")
                        break
            except Exception as e:
                _logger.warning(e)
            picking.write(
                {
                    "gls_asm_public_tracking_ref": response.get("_codbarras"),
                    "gls_asm_picking_ref": gls_asm_picking_ref,
                }
            )
            # We post an extra message in the chatter with the barcode and the
            # label because there's clean way to override the one sent by core.
            body = _("GLS Shipping extra info:\n" "barcode: %s") % response.get(
                "_codbarras"
            )
            attachment = []
            if response.get("gls_label"):
                attachment = [
                    (
                        "gls_label_{}.pdf".format(response.get("_codbarras")),
                        response.get("gls_label"),
                    )
                ]
            picking.message_post(body=body, attachments=attachment)
            result.append(vals)
        return result
