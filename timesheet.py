import pandas as pd
import streamlit as st
from io import BytesIO
import os

# Define the function to create a new timesheet
def new_timesheet():
    st.header("Create New Timesheet")
    project_name = st.text_input("Project Name")
    hours_worked = st.number_input("Hours Worked")
    task_description = st.text_area("Task Description")
    date = st.date_input("Date", pd.to_datetime("today"))

    if st.button("Submit"):
        data = {"Project Name": project_name,
                "Hours Worked": hours_worked,
                "Task Description": task_description,
                "Date": date}
        df = pd.DataFrame(data, index=[0])
        df.to_csv("timesheet.csv", mode="a", header=not os.path.isfile("timesheet.csv"), index=False)
        st.success("Timesheet created successfully!")

# Define the function to view the existing timesheets
def view_timesheets():
    st.header("View Timesheets")
    df = pd.read_csv("timesheet.csv")
    st.dataframe(df)

    # Add an option to download the timesheet as an Excel file
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    output.seek(0)
    st.download_button('Download Timesheet (Excel)', data=output.read(), file_name='timesheet.xlsx')

# Define the Streamlit app
def main():
    st.set_page_config(page_title="Timesheet App")
    st.title("Timesheet App")
    menu = ["Create New Timesheet", "View Timesheets"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Create New Timesheet":
        new_timesheet()
    elif choice == "View Timesheets":
        view_timesheets()

if __name__ == "__main__":
    main()
