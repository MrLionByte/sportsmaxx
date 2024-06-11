from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


def html_to_pdf(template_path, context=None):
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), dest=result)
    if pdf.err:
        return None
    result.seek(0)
    return result.getvalue()
