from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_filename = "Car_Service_Management_Speaking_Script.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=22,
    textColor=colors.HexColor("#FF5500"),
    alignment=1,
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'SubTitleStyle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor("#555555"),
    alignment=1,
    spaceAfter=20
)

name_style = ParagraphStyle(
    'NameStyle',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor("#D33F00"),
    spaceAfter=4
)

body_style = ParagraphStyle(
    'BodyStyle',
    parent=styles['Normal'],
    fontSize=11,
    leading=16,
    textColor=colors.HexColor("#222222")
)

story = []

story.append(Paragraph("Car Service Management System", title_style))
story.append(Paragraph("Official Team Presentation & Speaking Script", subtitle_style))

script_data = [
    ("1. Kartavya (Documentation & Business Analyst)", 
     "Namashte badhane, hu Kartavya chhu. Aaje amari team Car Service Management System project present kare chhe.<br/><br/>"
     "Aa project banavvano main Aim e chhe ke garage ma je loko ne lambi line ma ubha rehvu pade chhe ane phone karine appointment levi pade chhe, ene poori rite online ane automatic banavi shakaye.<br/><br/>"
     "Amari aa system thi car owner potana mobile thi j ghar bethe service book kari shake chhe, jethi eno ane garage walano—banne no time bache chhe.<br/><br/>"
     "Have amari team na baki members tamne aa system na Frontend, Backend ane Testing vishe vistar thi samjavshe. Thank you!"),
    
    ("2. Shivang Mistry (Frontend Lead & UI Designer)",
     "Hello, hu Shivang chhu. Me aa system nu Frontend ane UI/UX Design karyu chhe.<br/><br/>"
     "Amari website ma ame Brotomotiv jevi premium automotive dark theme apply kari chhe, jema glowing orange accents ane glassmorphism effect chhe.<br/><br/>"
     "Main feature e chhe ke customer ne koi lambu form bharva ni zaroorat nathi. Te jevuj koi service photo card (jema Paint Protection Film, Ceramic Coating, Wheel Alignment wagere) par click kare, etle tarat j ek sleek Modal Popup khule chhe ane tarat j booking thai jay chhe."),
    
    ("3. Rudra Goswami (Backend Lead & Cloud Architect)",
     "Hello, hu Rudra chhu. Me aa project nu Backend Architecture ane Cloud Integration develop karyu chhe.<br/><br/>"
     "Backend ma hu Python Flask no use kari ne REST APIs banavi chhe. GitHub Pages thi Render cloud server par data lavva mate CORS (Cross-Origin Resource Sharing) configure karyu chhe.<br/><br/>"
     "Database mate ame heavy SQL ni jagya e OpenPyXL library no use karyo chhe, je aavta badha bookings ne real-time ma 'car_service_orders.xlsx' sheet ma save kare chhe. Sathe j me Admin Dashboard pan banavyu chhe jethi garage manager badha orders ne live monitor ane status update kari shake."),
    
    ("4. Dhruvin (Testing & QA Specialist)",
     "Hello, hu Dhruvin chhu. Me aa system nu Quality Assurance, Testing ane Documentation karyu chhe.<br/><br/>"
     "Me badha API endpoints, form validation ane cross-browser compatibility check karya chhe.<br/><br/>"
     "• <b>Advantages:</b> Aa system zero-cost cloud infrastructure (GitHub Pages + Render) par chale chhe ane fast direct-card booking aape chhe.<br/>"
     "• <b>Limitations:</b> Excel file hoy aathi hu hajaro concurrent requests ma SQL jevlu scale nathi thai shakto.<br/>"
     "• <b>Future Scope:</b> Aagal jata ame isme Razorpay payment gateway, automated WhatsApp notification alerts ane mechanics mate task tracking portal add karvana chhiye.<br/><br/>"
     "Thank you!")
]

for name, script in script_data:
    p_name = Paragraph(name, name_style)
    p_script = Paragraph(script, body_style)
    
    t = Table([[p_name], [p_script]], colWidths=[530])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAFAFA")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E0E0E0")),
        ('LINELEFT', (0,0), (0,-1), 4, colors.HexColor("#FF5500")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 14))

doc.build(story)
print("PDF 'Car_Service_Management_Speaking_Script.pdf' generated successfully!")