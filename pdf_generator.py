# pdf_generator.py
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def generate_pdf(data):
    # Create PDF file with a unique name
    pdf_path = f'invoice_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Add header image with transparency
    header_path = "static/images/headeredge.png"
    c.drawImage(header_path, 0, 742, width=612, height=50, preserveAspectRatio=True, mask='auto')
    
    # Add invoice and client details
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(50, 700, f"Invoice #: INV-{datetime.now().strftime('%Y%m%d%H%M')}")
    
    # Client Details Box
    c.rect(50, 620, 500, 60)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, 660, "Bill To:")
    c.setFont("Helvetica", 11)
    c.drawString(60, 645, f"Name: {data['client']['name']}")
    c.drawString(60, 630, f"Phone: {data['client']['phone']}")
    c.drawString(300, 630, f"Payment Mode: {data['client']['payment_mode']}")
    
    y_position = draw_items_section(c, data)
    y_position = draw_totals_section(c, data, y_position)
    draw_footer(c)
    
    c.save()
    return pdf_path

def draw_items_section(c, data):
    y_position = 580
    
    # Add section headers with gray background
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.rect(50, y_position, 500, 20, fill=True)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y_position + 5, "Item")
    c.drawString(250, y_position + 5, "Rate")
    c.drawString(350, y_position + 5, "Qty")
    c.drawString(450, y_position + 5, "Amount")
    
    y_position -= 30
    
    # Equipment section
    if any(data['equipment'].values()):
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Equipment")
        y_position -= 20
        
        for category_name, category_items in data['equipment'].items():
            if category_items:
                c.setFont("Helvetica-Bold", 11)
                c.drawString(70, y_position, category_name.title())
                y_position -= 20
                
                c.setFont("Helvetica", 11)
                for item in category_items:
                    c.drawString(90, y_position, f"{item['name']}")
                    c.drawString(250, y_position, f"₹{item['price']}")
                    c.drawString(350, y_position, str(item['quantity']))
                    c.drawString(450, y_position, f"₹{item['total']}")
                    y_position -= 20
                y_position -= 10
    
    # Services section
    if data['services']:
        y_position -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Services")
        y_position -= 20
        
        c.setFont("Helvetica", 11)
        for service in data['services']:
            c.drawString(70, y_position, f"{service['name']}")
            c.drawString(250, y_position, f"₹{service['price']}")
            c.drawString(350, y_position, str(service['quantity']))
            c.drawString(450, y_position, f"₹{service['total']}")
            y_position -= 20
    
    # Transport section
    if data['transport']:
        y_position -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Transport")
        y_position -= 20
        
        c.setFont("Helvetica", 11)
        for transport in data['transport']:
            c.drawString(70, y_position, f"{transport['name']}")
            c.drawString(450, y_position, f"₹{transport['expense']}")
            y_position -= 20
    
    return y_position

def draw_totals_section(c, data, y_position):
    # Calculate totals
    equipment_total = sum(item['total'] for category in data['equipment'].values() for item in category)
    services_total = sum(service['total'] for service in data['services'])
    transport_total = sum(transport['expense'] for transport in data['transport'])
    grand_total = equipment_total + services_total + transport_total
    
    # Add totals section
    y_position -= 40
    c.line(50, y_position, 500, y_position)
    y_position -= 20
    
    c.setFont("Helvetica", 12)
    c.drawString(350, y_position, "Equipment Total:")
    c.drawString(450, y_position, f"₹{equipment_total}")
    y_position -= 20
    
    c.drawString(350, y_position, "Services Total:")
    c.drawString(450, y_position, f"₹{services_total}")
    y_position -= 20
    
    c.drawString(350, y_position, "Transport Total:")
    c.drawString(450, y_position, f"₹{transport_total}")
    y_position -= 30
    
    # Grand Total with bold font
    c.setFont("Helvetica-Bold", 14)
    c.drawString(350, y_position, "Grand Total:")
    c.drawString(450, y_position, f"₹{grand_total}")
    
    return y_position

def draw_footer(c):
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "Terms & Conditions:")
    c.drawString(50, 35, "1. Payment is due within 15 days")
    c.drawString(50, 20, "2. This is a computer generated invoice")