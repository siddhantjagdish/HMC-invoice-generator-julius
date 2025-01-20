# app.py
from flask import Flask, render_template, request, send_file
from pdf_generator import generate_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('invoice_form.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    # Initialize data structure
    data = {
        'client': {
            'name': request.form.get('client_name', ''),
            'email': request.form.get('client_email', ''),
            'phone': request.form.get('client_phone', ''),
            'payment_mode': request.form.get('payment_mode', '')
        },
        'equipment': {
            'lenses': [],
            'cameras': [],
            'drones': []
        },
        'services': [],
        'transport': []
    }
    
    # Process all equipment types with correct mapping
    equipment_mapping = {
        'lens': 'lenses',
        'camera': 'cameras',
        'drone': 'drones'
    }
    
    # Process all equipment types
    for eq_type, plural_type in equipment_mapping.items():
        names = request.form.getlist(f'{eq_type}_name[]')
        prices = request.form.getlist(f'{eq_type}_price[]')
        quantities = request.form.getlist(f'{eq_type}_quantity[]')
        
        for name, price, qty in zip(names, prices, quantities):
            if name and price and qty and float(qty) > 0:
                data['equipment'][plural_type].append({
                    'name': name,
                    'price': float(price),
                    'quantity': int(qty),
                    'total': float(price) * int(qty)
                })
    
    # Process services
    service_names = request.form.getlist('service_name[]')
    service_prices = request.form.getlist('service_price[]')
    service_quantities = request.form.getlist('service_quantity[]')
    
    for name, price, qty in zip(service_names, service_prices, service_quantities):
        if name and price and qty and float(qty) > 0:
            data['services'].append({
                'name': name,
                'price': float(price),
                'quantity': int(qty),
                'total': float(price) * int(qty)
            })
    
    # Process transport
    transport_names = request.form.getlist('transport_name[]')
    transport_expenses = request.form.getlist('transport_expense[]')
    
    for name, expense in zip(transport_names, transport_expenses):
        if name and expense and float(expense) > 0:
            data['transport'].append({
                'name': name,
                'expense': float(expense)
            })
    
    # Generate PDF
    pdf_path = generate_pdf(data)
    
    return send_file(pdf_path, as_attachment=True, download_name='invoice.pdf')

if __name__ == '__main__':
    app.run(debug=True)