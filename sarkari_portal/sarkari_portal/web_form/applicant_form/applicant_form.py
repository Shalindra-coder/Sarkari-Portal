# import frappe

# def get_context(context):
#     try:
#         # Single Doctype: QR Code
#         doc = frappe.get_doc("QR Code")

#         # QR field fetch
#         context.qr_code = doc.qr_code or ""

#     except Exception:
#         context.qr_code = ""



import frappe
from frappe.model.document import Document
import easyocr
import os
import re

class QRCode(Document):
    def validate(self):
        # Jab user web form submit karega, ye 'validate' function chalega
        if self.qr_code:
            self.verify_payment_receipt()

    def verify_payment_receipt(self):
        # 1. File ka path nikalna
        # self.qr_code mein file ka URL hota hai (e.g., /files/receipt.jpg)
        file_path = frappe.get_site_path('public', 'files', self.qr_code.split('/')[-1])

        if not os.path.exists(file_path):
            return

        try:
            # 2. EasyOCR use karke text read karna
            # Note: Pehli baar run hone par ye model download karega (thoda time lega)
            reader = easyocr.Reader(['en'])
            result = reader.readtext(file_path, detail=0)
            text = " ".join(result).lower()

            # 3. Validation Logic (Keywords)
            # Hum check kar rahe hain ki kya receipt mein 'success' ya 'paid' jaise shabd hain
            success_keywords = ["successful", "success", "paid", "completed", "transaction", "received"]
            
            is_valid = any(word in text for word in success_keywords)

            # 4. UTR/Transaction ID dhundna (Optional but Recommended)
            # Aksar UTR 12 digits ka hota hai
            utr_match = re.search(r"\b\d{12}\b", text)
            if utr_match:
                self.description = f"Auto-Detected UTR: {utr_match.group()}" # Kisi field mein save kar lo

            # 5. Agar receipt sahi nahi hai toh Error throw karein
            if not is_valid:
                # frappe.throw karne se Web Form submit nahi hoga aur user ko error dikhega
                frappe.throw("Aapne jo receipt upload ki hai wo valid nahi lag rahi hai. Kripya Successful Payment ka screenshot upload karein.")

        except Exception as e:
            # Agar OCR fail ho jaye toh error log karein par user ko block na karein (taaki manual check ho sake)
            frappe.log_error(title="OCR Verification Failed", message=frappe.get_traceback())
            frappe.msgprint("Receipt auto-verify nahi ho payi, hum ise manually check karenge.")