import streamlit as st
import pandas as pd
import display
import utility
import helper

if 'confirm_delete_all' not in st.session_state:
    st.session_state.confirm_delete_all = False

st.set_page_config(layout='wide')

def main():
    st.title('Employee Data Management App')
    employee_columns = ['employee_id', 'name', 'gender', 'date_of_joining', 'salary', 'position']
    employee_columns_update_delete = ['name', 'gender', 'date_of_joining', 'salary', 'position']
    condition = 'employee_id=?'
    table_name = 'employees'
    with st.sidebar:
        page = st.radio('Main Menu',['Add Data','Manage Data','Flood Database','Bulk Delete','Summary'])

    if page == 'Add Data':
        st.subheader('Add New Employee')

        with st.form('data_entry_form'):
            employee_id = st.text_input('Employee ID')
            name = st.text_input('Name')
            gender = st.selectbox('Gender',['Male','Female','Others'])
            doj = st.date_input('Date of Joining')
            salary = st.number_input('Salary',min_value=0.0,step=1.0)
            position = st.text_input('Position')

            submit = st.form_submit_button('Submit')
            if submit:
                if employee_id and name:
                    employee_data = (employee_id, name, gender, doj, salary, position)
                    utility.insert_data(table_name,employee_columns,employee_data)
                else:
                    st.warning('Please fill in required fields')

    elif page == 'Manage Data':
        st.subheader("Manage Employees")
        data = utility.fetch_data()

        if not data.empty:
            st.dataframe(data)
            csv = data.to_csv(index=False)
            st.download_button('Export to Excel', csv, 'employee.csv', mime='text/csv')

            # Select a user to edit
            search_query = st.text_input("Search for Employee Name to Edit")
            if search_query:
                filtered_data = helper.filter_data(search_query=search_query,df=data,column_name='name')

                # Limiting options for employee_id in the selectbox
                if not filtered_data.empty:
                    selected_employee_id = st.selectbox("Select an Employee ID to Edit",
                                                        filtered_data['employee_id'].tolist())
                    selected_employee = filtered_data[filtered_data['employee_id'] == selected_employee_id]

                    # Edit Employee
                    st.subheader("Edit Employee")
                    with st.form("edit_form"):
                        new_name = st.text_input("Name", selected_employee['name'].values[0])
                        new_gender = st.selectbox("Gender", ["Male", "Female", "Other"],
                                                  index=["Male", "Female", "Other"].index(
                                                      selected_employee['gender'].values[0]))
                        new_date_of_joining = st.date_input("Date of Joining",
                                                            pd.to_datetime(selected_employee['date_of_joining'].values[0]))
                        new_salary = st.number_input("Salary", min_value=0.0, step=0.1,
                                                     value=float(selected_employee['salary'].values[0]))
                        new_position = st.text_input("Position", selected_employee['position'].values[0])
                        update = st.form_submit_button("Submit")

                        if update:
                            values = (new_name,new_gender,new_date_of_joining,new_salary,new_position)
                            condition_values = (selected_employee['employee_id'].values[0],)
                            utility.update_data(table_name,employee_columns_update_delete,values,condition,condition_values)
                            st.success("Employee updated successfully!")
                            st.rerun()

            # Multiple Delete Employees
            st.subheader("Delete Employees")
            search_query = st.text_input("Search for Employee Name")

            # Filter data based on search query
            if search_query:
                filtered_data = helper.filter_data(search_query,data,'name')
                if not filtered_data.empty:
                    # Show filtered employee IDs in the multiselect
                    selected_employees_to_delete = st.multiselect(
                        "Select Employee IDs to Delete",
                        filtered_data['employee_id'].tolist()
                    )

                    if st.button("Delete Selected Employees"):
                        if selected_employees_to_delete:
                            for emp_id in selected_employees_to_delete:
                                condition_values = (emp_id,)
                                utility.delete_data(table_name,condition, condition_values)
                            st.success(f"Successfully deleted {len(selected_employees_to_delete)} employees.")
                            st.rerun()
                        else:
                            st.warning("No employees selected for deletion.")

            # Delete All Employees
            st.subheader("Delete All Employees")
            #st.session_state.confirm_delete_all = False
            if not st.session_state.confirm_delete_all:
                if st.button("Delete All Employees"):
                    st.session_state.confirm_delete_all = True
                    st.rerun()
            else:
                st.warning("⚠️ Are you sure you want to delete all employees? This action cannot be undone.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Confirm Delete All"):
                        utility.delete_all_data(table_name)
                        st.session_state.confirm_delete_all = False
                        st.success("All employees have been successfully deleted.")
                        st.rerun()
                with col2:
                    if st.button("Cancel"):
                        st.session_state.confirm_delete_all = False
                        st.info("Delete all action was canceled.")
                        st.rerun()

        else:
            st.info("No employees found in the database.")
    elif page == 'Flood Database':
        st.subheader('Flood Database')
        uploaded_file = st.file_uploader('Upload CSV or Excel',type = ['csv','xlsx'],key='flood_uploader')

        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            st.write('Uploaded Data: ')
            st.dataframe(df)
            flood_database = st.button('Flood Database')
            if flood_database:
                df.columns = employee_columns
                utility.bulk_insert(df,table_name)
                st.rerun()

    elif page == 'Bulk Delete':
        st.subheader('Bulk Delete ')
        delete_from_file = st.file_uploader('Upload CSV or Excel',type=['csv','xlsx'],key='delete_uploader')
        if delete_from_file:
            if delete_from_file.name.endswith('.csv'):
                df = pd.read_csv(delete_from_file)
            elif delete_from_file.name.endswith('.xlsx'):
                df = pd.read_excel(delete_from_file)

            st.write('Uploaded Data:')
            st.dataframe(df)
            many_delete = st.button('Bulk Delete')
            if many_delete:
                df.columns = employee_columns
                utility.bulk_delete(df,table_name,'employee_id')
                st.rerun()
    elif page == 'Summary':
        st.subheader('Summary')
        data = utility.fetch_data()
        if not data.empty:
            bins = [0, 30000, 50000, float('inf')]
            labels = ['<30k','30k-50k','>500k']
            data['gender'] = data['gender'].fillna('Not Disclosed')
            data['salary'] = data['salary'].fillna(0)
            data['position'] = data['position'].fillna('Not Disclosed')
            data['salary_distribution'] = pd.cut(data['salary'],bins=bins,labels=labels,right=True)
            data['salary_distribution'] = data['salary_distribution']
            chart = st.radio('Chart',['Pie Chart','Bar Chart'],index=0)
            if chart == 'Pie Chart':
                display.pie_chart(data)
            elif chart == 'Bar Chart':
                display.bar_chart(data)
        else:
            st.info('No data to display')



if __name__ == "__main__":
    utility.init_db()
    main()