import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.conf import settings

def generate_bus_pass_pdf(application, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a365d'),
        alignment=1, # Center
        spaceAfter=15
    )

    normal_style = styles['Normal']

    # Pass Header
    story.append(Paragraph("COLLEGE BUS PASS SYSTEM - BENGALURU", title_style))
    story.append(Paragraph("<b>Official Digital Bus Pass</b>", ParagraphStyle('Sub', parent=normal_style, alignment=1, textColor=colors.HexColor('#4a5568'))))
    story.append(Spacer(1, 20))

    # Pass Details Table
    student = application.student
    route = application.route

    data = [
        [Paragraph("<b>Roll Number:</b>", normal_style), Paragraph(student.roll_number, normal_style)],
        [Paragraph("<b>Student Name:</b>", normal_style), Paragraph(student.user.get_full_name() or student.user.username, normal_style)],
        [Paragraph("<b>Department & Year:</b>", normal_style), Paragraph(f"{student.department} ({student.get_year_display()})", normal_style)],
        [Paragraph("<b>Route Number:</b>", normal_style), Paragraph(f"Route {route.route_number} - {route.route_name}", normal_style)],
        [Paragraph("<b>Pickup Point:</b>", normal_style), Paragraph(application.pickup_point, normal_style)],
        [Paragraph("<b>Duration:</b>", normal_style), Paragraph(f"{application.duration_months} Month(s)", normal_style)],
        [Paragraph("<b>Total Fee Paid:</b>", normal_style), Paragraph(f"₹{application.total_fee}", normal_style)],
        [Paragraph("<b>Valid Period:</b>", normal_style), Paragraph(f"{application.valid_from} to {application.valid_until}", normal_style)],
        [Paragraph("<b>Status:</b>", normal_style), Paragraph(f"<font color='green'><b>APPROVED</b></font>", normal_style)],
    ]

    t = Table(data, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    story.append(t)
    story.append(Spacer(1, 30))
    story.append(Paragraph("<i>Note: This is a system-generated pass. Please carry a digital or printed copy while boarding the bus.</i>", ParagraphStyle('Foot', parent=normal_style, fontSize=9, textColor=colors.HexColor('#718096'), alignment=1)))

    doc.build(story)