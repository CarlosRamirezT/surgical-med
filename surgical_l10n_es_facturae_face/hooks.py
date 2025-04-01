from odoo import api, SUPERUSER_ID

def check_and_fix_configurations(env):
    """
    This function runs automatically after installing/updating the module.
    """
    module = "l10n_es_facturae_face"

    # fix wrong backend type related to

    # facturae_backend_type

    backend_type = env["edi.backend.type"].search(
        [("code", "=", "l10n_es_facturae")], limit=1
    )

    # check if backend type has an external id related

    external_id = env["ir.model.data"].search(
        [
            # ("module", "=", module),
            ("name", "=", "facturae_backend_type"),
            # ("model", "=", "edi.backend.type"),
        ],
    )
    if external_id:
        external_id.unlink()

    env["ir.model.data"].create(
        {
            "module": module,
            "name": "facturae_backend_type",
            "model": "edi.backend.type",
            "res_id": backend_type.id,
        }
    )

    # facturae_exchange_type

    external_id = env["ir.model.data"].search(
        [
            # ("module", "=", module),
            ("name", "=", "facturae_exchange_type"),
            # ("model", "=", "edi.exchange.type"),
        ],
    )
    if external_id:
        external_id.unlink()

    exchange_type = env["edi.exchange.type"].search(
        [("code", "=", "l10n_es_facturae")], limit=1
    )
    if exchange_type:
        exchange_type.unlink()
    exchange_type = env["edi.exchange.type"].create(
        {
            "name": "Spanish Facturae",
            "code": "l10n_es_facturae",
            "backend_type_id": backend_type.id,
            "direction": "output",
            "exchange_filename_pattern": "{record_name}--{dt}",
            "exchange_file_ext": "xsig",
            "exchange_file_auto_generate": True,
        }
    )
    external_id = env["ir.model.data"].search(
        [
            # ("module", "=", module),
            ("name", "=", "facturae_exchange_type"),
            # ("model", "=", "edi.exchange.type"),
        ],
    )
    if external_id:
        external_id.unlink()
    env["ir.model.data"].create(
        {
            "module": module,
            "name": "facturae_exchange_type",
            "model": "edi.exchange.type",
            "res_id": exchange_type.id,
        }
    )

    # facturae_face_exchange_type_rule

    exchange_type_rule = env["edi.exchange.type.rule"].search(
        [("type_id", "=", exchange_type.id)], limit=1
    )
    if exchange_type_rule:
        exchange_type_rule.unlink()
    exchange_type_rule = env["edi.exchange.type.rule"].create(
        {
            "name": "Default",
            "type_id": exchange_type.id,
            "model_id": env.ref("account.model_account_move").id,
            "enable_domain": "[('state', '!=', 'draft'), ('partner_id', '!=', False), ('partner_id.l10n_es_facturae_sending_code', '=', \"face\"), ('move_type', 'in', ['out_invoice', 'out_refund'])]",
            "enable_snippet": "result = not record._has_exchange_record(exchange_type)",
        }
    )
    external_id = env["ir.model.data"].search(
        [
            ("module", "=", module),
            ("name", "=", "facturae_face_exchange_type_rule"),
            ("model", "=", "edi.exchange.type.rule"),
        ],
        limit=1,
    )
    if external_id:
        external_id.unlink()
    env["ir.model.data"].create(
        {
            "module": module,
            "name": "facturae_face_exchange_type_rule",
            "model": "edi.exchange.type.rule",
            "res_id": exchange_type_rule.id,
        }
    )

    # face_backend
    # nothing to do here

    face_backend = env["edi.backend"].search([("name", "=", "FACe")], limit=1)

    # facturae_face_update_exchange_type

    update_exchange_type = env["edi.exchange.type"].search(
        [("code", "=", "l10n_es_facturae_face_update")], limit=1
    )
    if update_exchange_type:
        update_exchange_type.unlink()
    update_exchange_type = env["edi.exchange.type"].create(
        {
            "name": "Update Facturae FACe",
            "code": "l10n_es_facturae_face_update",
            "backend_type_id": backend_type.id,
            "backend_id": face_backend.id,
            "direction": "input",
            "exchange_filename_pattern": "{record_name}--{dt}",
            "exchange_file_ext": "json",
        }
    )
    external_id = env["ir.model.data"].search(
        [
            ("module", "=", module),
            ("name", "=", "facturae_face_update_exchange_type"),
            ("model", "=", "edi.exchange.type"),
        ],
        limit=1,
    )
    if external_id:
        external_id.unlink()
    env["ir.model.data"].create(
        {
            "module": module,
            "name": "facturae_face_update_exchange_type",
            "model": "edi.exchange.type",
            "res_id": update_exchange_type.id,
        }
    )

    # facturae_face_update_exchange_type_rule

    update_exchange_rule = env["edi.exchange.type.rule"].search(
        [("type_id", "=", update_exchange_type.id)], limit=1
    )
    if update_exchange_rule:
        update_exchange_rule.unlink()
    update_exchange_rule = env["edi.exchange.type.rule"].create(
        {
            "name": "Default",
            "type_id": update_exchange_type.id,
            "model_id": env.ref("account.model_account_move").id,
            "enable_domain": "[('state', '!=', 'draft'), ('partner_id.l10n_es_facturae_sending_code', '=', \"face\")]",
            "enable_snippet": 'result = record._has_exchange_record(record.env.ref("l10n_es_facturae_face.facturae_exchange_type"), record.env.ref("l10n_es_facturae_face.face_backend"))',
        }
    )
    external_id = env["ir.model.data"].search(
        [
            ("module", "=", module),
            ("name", "=", "facturae_face_update_exchange_type_rule"),
            ("model", "=", "edi.exchange.type.rule"),
        ],
        limit=1,
    )
    if external_id:
        external_id.unlink()
    env["ir.model.data"].create(
        {
            "module": module,
            "name": "facturae_face_update_exchange_type_rule",
            "model": "edi.exchange.type.rule",
            "res_id": update_exchange_rule.id,
        }
    )

    # facturae_face_cancel_exchange_type

    cancel_exchange_type = env["edi.exchange.type"].search(
        [("code", "=", "l10n_es_facturae_face_cancel")], limit=1
    )
    if cancel_exchange_type:
        cancel_exchange_type.unlink()
    cancel_exchange_type = env["edi.exchange.type"].create(
        {
            "name": "Cancel Facturae FACe",
            "code": "l10n_es_facturae_face_cancel",
            "backend_type_id": backend_type.id,
            "backend_id": face_backend.id,
            "direction": "output",
            "exchange_filename_pattern": "{record_name}--{dt}",
            "exchange_file_ext": "txt",
        }
    )
    external_id = env["ir.model.data"].search(
        [
            ("module", "=", module),
            ("name", "=", "facturae_face_cancel_exchange_type"),
            ("model", "=", "edi.exchange.type"),
        ],
        limit=1,
    )
    if external_id:
        external_id.unlink()
    env["ir.model.data"].create(
        {
            "module": module,
            "name": "facturae_face_cancel_exchange_type",
            "model": "edi.exchange.type",
            "res_id": cancel_exchange_type.id,
        }
    )

    # facturae_output_template

    output_template = env["edi.exchange.template.output"].search(
        [("code", "=", "l10n_es_facturae.facturae_file")], limit=1
    )
    if output_template:
        output_template.unlink()
    output_template = env["edi.exchange.template.output"].create(
        {
            "name": "Facturae output",
            "backend_type_id": backend_type.id,
            "type_id": exchange_type.id,
            "code": "l10n_es_facturae.facturae_file",
            "output_type": "xsig",
            "generator": "report",
            "report_id": env.ref("l10n_es_facturae.report_facturae_signed").id,
            "code_snippet": "result = {'res_ids': record.ids}",
        }
    )
    external_id = env["ir.model.data"].search(
        [
            ("module", "=", module),
            ("name", "=", "facturae_output_template"),
            ("model", "=", "edi.exchange.template.output"),
        ],
        limit=1,
    )
    if external_id:
        external_id.unlink()
    env["ir.model.data"].create(
        {
            "module": module,
            "name": "facturae_output_template",
            "model": "edi.exchange.template.output",
            "res_id": output_template.id,
        }
    )

def post_init_hook(cr, registry=False):
    """
    This function runs automatically after installing/updating the module.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    check_and_fix_configurations(env)

