import frappe

def get_context(context):
    try:
        # Single Doctype: QR Code
        doc = frappe.get_doc("QR Code")

        # QR field fetch
        context.qr_code = doc.qr_code or ""

    except Exception:
        context.qr_code = ""