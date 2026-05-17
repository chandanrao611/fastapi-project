from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from io import BytesIO

templates = Environment(
    loader=FileSystemLoader("app/templates")
)

class PDFService:

    @staticmethod
    def generate_invoice_pdf(data: dict):

        template = templates.get_template("invoice.html")

        html_content = template.render(data)

        pdf_buffer = BytesIO()

        HTML(string=html_content).write_pdf(pdf_buffer)

        pdf_buffer.seek(0)

        return pdf_buffer

    @staticmethod
    def generate_template(data: dict):
        template = templates.get_template("invoice.html")
        html_content = template.render(data)
        return html_content