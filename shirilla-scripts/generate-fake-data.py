import csv
import os
from faker import Faker

# Try to import weasyprint, but don't crash if it's missing system libs
try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except (ImportError, OSError):
    HAS_WEASYPRINT = False

fake = Faker()

def generate_data():
    print("--- Starting Fake Data Generation ---")

    # 1. AWS Credentials
    aws_id, aws_key = "AKIAIOSFODNN7EXAMPLE", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    with open('setup_aws.sh', 'w') as f:
        f.write(f"#!/bin/bash\nexport AWS_ACCESS_KEY_ID='{aws_id}'\nexport AWS_SECRET_ACCESS_KEY='{aws_key}'\n")
    
    with open('aws_config_mock.py', 'w') as f:
        f.write(f"AWS_ACCESS_KEY = '{aws_id}'\nAWS_SECRET_KEY = '{aws_key}'\n")

    # 2. Employee & Customer Data
    employees = [{'name': fake.name(), 'dob': fake.date_of_birth(minimum_age=22).strftime('%Y-%m-%d'), 'ssn': fake.ssn()} for _ in range(15)]
    customers = [{'name': fake.name(), 'cc': fake.credit_card_number(), 'provider': fake.credit_card_provider()} for _ in range(15)]

    for filename, data, fields in [('employees.csv', employees, ['name', 'dob', 'ssn']), ('customers.csv', customers, ['name', 'cc', 'provider'])]:
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
    
    # 3. Report Generation
    emp_rows = "".join([f"<tr><td>{e['name']}</td><td>{e['dob']}</td><td>{e['ssn']}</td></tr>" for e in employees])
    cust_rows = "".join([f"<tr><td>{c['name']}</td><td>{c['cc']}</td><td>{c['provider']}</td></tr>" for c in customers])

    html_content = f"""
    <html>
    <head><style>body{{font-family:sans-serif;}} table{{width:100%; border-collapse:collapse;}} th,td{{border:1px solid #ddd; padding:8px;}} th{{background:#f2f2f2;}}</style></head>
    <body>
        <h1>Mock Data Audit</h1>
        <h2>Employees</h2><table>{emp_rows}</table>
        <h2>Customers</h2><table>{cust_rows}</table>
    </body>
    </html>"""

    if HAS_WEASYPRINT:
        try:
            HTML(string=html_content).write_pdf('mock_data_report.pdf')
            print("Successfully created: mock_data_report.pdf")
        except Exception as e:
            print(f"PDF Error: {e}. Falling back to HTML.")
            with open('mock_data_report.html', 'w') as f: f.write(html_content)
    else:
        print("WeasyPrint dependencies not found. Created HTML report instead.")
        with open('mock_data_report.html', 'w') as f:
            f.write(html_content)

    print("--- Done ---")

if __name__ == "__main__":
    generate_data()