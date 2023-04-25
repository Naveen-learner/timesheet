from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import streamlit as st
from io import BytesIO
from reportlab.lib.units import inch
#import datetime
from datetime import datetime
from streamlit.components.v1 import components as stc


# ...
company_logo = 'cloudpro_logo.png'
company_name = 'CloudPro IT Solutions'
def generate_report(employee_name, report_dates, due_date, job_title, frequency, project_name, client_name, tasks, task_details, signature):
    
    # Create a canvas object to generate the PDF
    report = canvas.Canvas("weekly_timesheet.pdf", pagesize=letter)
    
    # Set the position and size of the image
    x, y = 50, 750
    width, height = 1*inch, 1*inch

    # Draw the image
    report.drawImage(company_logo, x, y, width, height)
    
    # Set the position of the company name
    report.setFont("Helvetica-Bold", 20)
    report.drawCentredString(300, 750, company_name)
    
    # Set the position and content of Section 1 - Report Details
    report.setFont("Helvetica-Bold", 14)
    report.drawString(50, 700, "Report Details")
    report.setFont("Helvetica", 12)
    report.drawString(50, 675, f"Employee Name: {employee_name}")
    report.drawString(50, 650, f"Report Dates: {report_dates[0].strftime('%m/%d/%Y')} - {report_dates[1].strftime('%m/%d/%Y')}")
    report.drawString(50, 625, f"Due Date: {due_date.strftime('%m/%d/%Y')}")
    report.drawString(50, 600, f"Job Title: {job_title}")
    report.drawString(50, 575, f"Frequency: {frequency}")
    
    # Set the position and content of Section 2 - Project Name / Client Name
    report.setFont("Helvetica-Bold", 14)
    report.drawString(50, 525, "Project Name / Client Name")
    report.setFont("Helvetica", 12)
    report.drawString(50, 500, f"Project Name: {project_name}")
    report.drawString(50, 475, f"Client Name: {client_name}")
    
    # Set the position and content of Section 3 - Accomplished this week (Tasks)
    report.setFont("Helvetica-Bold", 14)
    report.drawString(50, 425, "Accomplished this week (Tasks)")
    report.setFont("Helvetica", 12)
    y = 400
    for task in tasks:
        report.drawString(50, y, task)
        y -= 25
    
    # Set the position and content of Section 4 - Accomplished Tasks Details
    report.setFont("Helvetica-Bold", 14)
    report.drawString(50, 350, "Accomplished Tasks Details")
    report.setFont("Helvetica", 12)
    y = 325
    for task in task_details:
        report.drawString(50, y, task)
        y -= 25
    
    # Add signature and timestamp below signature
    signature_img = Image.open(signature)
    report.drawInlineImage(signature_img, 50, 150, width=120, height=50)
    report.setFont("Helvetica", 12)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report.drawString(50, 125, f"{current_time}")
    
    # Save and close the PDF
    report.save()
    
# ...

def main():
    # ...
    st.title("Weekly Timesheet Report")

    # Get employee details
    employee_name = st.text_input("Employee Name")
    # Get the start and end dates for the report
    report_dates = st.date_input("Report Dates", value=(datetime.now().date(), datetime.now().date()))
    start_date, end_date = report_dates

    # Get the due date for the report
    due_date = st.date_input("Due Date", value=datetime.now().date())
    job_title = st.text_input("Job Title")
    frequency = st.text_input("Frequency")

    # Get project and client details
    project_name = st.text_input("Project Name")
    client_name = st.text_input("Client Name")

    # Get tasks
    tasks = st.text_area("Accomplished this week (Tasks)", height=150)
    # Get task details
    task_details = st.text_area("Accomplished tasks details", height=150)

    # Get signature
    signature = st.file_uploader("Upload Signature", type=['jpg', 'jpeg', 'png'])

    # Get date
    #date = st.text_input("Date")
    
    # Generate the report when the "Generate Report" button is clicked
    if st.button("Generate Report"):
        if signature is None:
            st.error("Please upload your signature!")
        else:
            signature_bytes = signature.read()
            signature_path = "signature.png"
            with open(signature_path, "wb") as f:
                f.write(signature_bytes)
            generate_report(employee_name, report_dates, due_date, job_title, frequency, project_name, client_name, tasks.split('\n'), task_details.split('\n'),signature_path)
            # Generate the report
            #generate_report(employee_name, report_dates, due_date, job_title, frequency, project_name, client_name, tasks.split('\n'), "signature.png", date)

            # Download the generated report
            with open("weekly_timesheet.pdf", "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="Download Timesheet",
                data=pdf_bytes,
                file_name="weekly_timesheet.pdf",
                mime="application/pdf",
            )

if __name__ == "__main__":
    main()
