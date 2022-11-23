import os

from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action


@action(detail=False)
def generate_pdf(self, response, cart):
    '''Download shopping list as PDF-file.'''
    pdfmetrics.registerFont(
        TTFont('RadioVolna', (os.path.abspath('data/RadioVolna.ttf')))
        )
    pdf = canvas.Canvas(response)
    pdf.setFont('RadioVolna', 25)
    pdf.drawString(
        150, 800, f'{self.request.user.first_name}, remember to buy:'
        )
    pdf.setFont('RadioVolna', 20)
    pdf.translate(cm, 26.5*cm)
    for item in range(len(cart)):
        pdf.drawString(
            100, -item*cm,
            (f"{item+1} {cart[item].get('ingredients__name')} - "
             f"{cart[item].get('total')} "
             f"{cart[item].get('ingredients__measurement_unit')};")
            )
    pdf.showPage()
    pdf.save()
    return response
