frappe.ready(function() {

    let payment_done = false;
    let qr_image = "";

    // HTML inject
    let html = `
        <div style="margin-top:30px; text-align:center;">
            
            <button type="button" id="start-payment" class="btn btn-primary" style="padding:10px 20px; font-size:16px;">
                Start Payment
            </button>

            <div id="qr-section" style="display:none; margin-top:30px;">
                
                <h3 style="margin-bottom:15px;">Scan QR Code to Pay</h3>

                <div style="display:flex; justify-content:center;">
                    <img id="qr-image" style="width:320px; height:320px; border:2px solid #ddd; padding:10px; border-radius:10px;">
                </div>

                <br>

                <button type="button" id="confirm-payment" class="btn btn-success" style="padding:10px 20px; font-size:16px;">
                    I Have Paid
                </button>

            </div>
        </div>
    `;

    $(".web-form").append(html);

    // QR fetch
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "QR Code",
            name: "QR Code"
        },
        callback: function(r) {
            if (r.message) {
                qr_image = r.message.qr_code;
            }
        }
    });

    // Start Payment
    $(document).on("click", "#start-payment", function () {
        if (qr_image) {
            $("#qr-image").attr("src", qr_image);
            $("#qr-section").show();
        } else {
            frappe.msgprint("QR Code load nahi hua, please refresh");
        }
    });

    // Confirm Payment
    $(document).on("click", "#confirm-payment", function () {
        payment_done = true;
        frappe.msgprint("Payment Confirmed ✅");
    });

    // Submit Block
    $(document).on("submit", ".web-form", function (e) {
        if (!payment_done) {
            e.preventDefault();
            frappe.msgprint("❌ Please complete payment first!");
            return false;
        }
    });

});