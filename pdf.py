from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Image
from reportlab.platypus import PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


def generate_pdf(file_name, trip, image_file):
    width, height = letter
    pdf = SimpleDocTemplate(file_name, pagesize=letter)

    data = [['Name', 'Confirmation Number', 'Total', 'Adults', 'Children', 'Seats']]
    total_adults = 0
    total_children = 0

    for group in trip.groups:

        name = "%s %s" % (group.first_name, group.last_name)
        total = group.adults + group.children
        seats = list()
        for passenger in group.passengers:
            seats.append(passenger.position)
        seats.sort()
        data.append([name, group.confirmation_number, total, group.adults, group.children, " ,".join(seats)])
        total_adults += group.adults
        total_children += group.children

    data.append(["TOTALS", "", total_adults + total_children, total_adults, total_children, ""])

    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ])
    table.setStyle(style)

    img = Image(image_file)
    img_width = img.drawWidth
    img_height = img.drawHeight

    new_height = 600
    img_scale = new_height/img_height
    new_width = img_scale * img_width
    img.drawWidth = new_width
    img.drawHeight = new_height
    img.hAlign = 'CENTER'

    elems = list()
    elems.append(table)
    elems.append(PageBreak())
    elems.append(img)

    pdf.build(elems)
