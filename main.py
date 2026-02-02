from flask import Flask, request, send_file, jsonify
from weasyprint import HTML, CSS
import tempfile
import os

app = Flask(__name__)

@app.route("/html-to-pdf", methods=["POST"])
def html_to_pdf():
    data = request.get_json()
    html = data.get("html") if data else None

    if not html:
        return jsonify({"error": "HTML content required"}), 400

    # Temporary PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        pdf_path = f.name

    # A4 + margins (close to wkhtmltopdf)
    css = CSS(string="""
        @page {
            size: A4;
            margin: 15mm 10mm 15mm 10mm;
        }
        body {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 14px;
        }
    """)

    HTML(string=html).write_pdf(pdf_path, stylesheets=[css])

    return send_file(
        pdf_path,
        mimetype="application/pdf",
        download_name="invoice.pdf",
        as_attachment=False
    )

if __name__ == "__main__":
    app.run()
