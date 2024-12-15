import pandas as pd
import streamlit as st
import sqlite3

def init_db():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        create table if not exists employees(
            id integer primary key autoincrement,
            employee_id text not null,
            name text not null,
            gender text,
            date_of_joining text,
            salary real,
            position text
        )
        ''')
        conn.commit()
    except Exception as e:
        st.error('Cannot create table')
        st.error(e)
    finally:
        conn.close()

def insert_data(employee_id,name,gender,date_of_joining,salary,position):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        insert into employees (employee_id,name,gender,date_of_joining,salary,position) values (?,?,?,?,?,?)
        ''',(employee_id,name,gender,date_of_joining,salary,position))
        conn.commit()
        st.success('Data Inserted Successfully')
    except Exception as e:
        st.error('Error while inserting data')
        st.error(e)
    finally:
        conn.close()

def update_data(employee_id,name,gender,date_of_joining,salary,position):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        update employees set name = ?, gender=?,date_of_joining=?,salary=?,position=? where employee_id=?
        ''',(name,gender,date_of_joining,salary,position,employee_id))
        conn.commit()
        st.success('Record Updated Successfully')
    except Exception as e:
        st.error('Error in updating data')
        st.error(e)
    finally:
        conn.close()

def delete_data(employee_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        delete from employees where employee_id=?
        ''',(employee_id,))
        conn.commit()
        st.success('Employee deleted successfully')
    except Exception as e:
        st.error('Error while deleting employee')
        st.error(e)
    finally:
        conn.close()

def fetch_data():
    conn = sqlite3.connect('my_database.db')
    try:
        df = pd.DataFrame(columns=['employee_id','name','gender','date_of_joining','salary','position'])
        df = pd.read_sql_query('select * from employees',conn)
    except Exception as e:
        st.error('Error in retrieving data')
    finally:
        conn.close()
        return df

def main():
    st.title('Employee Data Management App')

    tab1,tab2,tab3 = st.tabs(['Add Data','Manage/View/Update/Delete Data','Flood Database'])

    with tab1:
        st.subheader('Add New Employee')

        with st.form('data_entry_form'):
            employee_id = st.text_input('Employee ID')
            name = st.text_input('Name')
            gender = st.selectbox('Gender',['Female','Male','Others'])
            doj = st.date_input('Date of Joining')
            salary = st.number_input('Salary',min_value=0.0,step=1.0)
            position = st.text_input('Position')

            submit = st.form_submit_button('Submit')

            if submit:
                if employee_id and name:
                    insert_data(employee_id,name,gender,doj,salary,position)
                else:
                    st.warning('Please fill in required fields')

    with tab2:
        st.subheader('Manage Data')

        data = fetch_data()
        if not data.empty:
            st.dataframe(data)
            selected_employee_id = st.selectbox('Select an Employee ID to edit/delete',data['employee_id'])
            selected_employee = data[data['employee_id']==selected_employee_id]

            # edit/delete employee
            st.subheader('Edit/Delete Employee')
            with st.form('edit_delete_employee'):
                new_name = st.text_input('Name',selected_employee['name'].values[0])
                new_gender = st.selectbox('Gender', ['Male', 'Female', 'Others'],index=['Male','Female','Others'].index(selected_employee['gender'].values[0]))
                new_doj = st.date_input('Date of Joining',pd.to_datetime(selected_employee['date_of_joining'].values[0]))
                new_salary = st.number_input('Salary',value=float(selected_employee['salary'].values[0]),min_value=0.0,step=1.0)
                new_position = st.text_input('Position', selected_employee['position'].values[0])

                update = st.form_submit_button('Update')
                if update:
                    update_data(selected_employee_id,new_name,new_gender,new_doj,new_salary,new_position)
                    st.experimental_rerun()
                delete = st.form_submit_button('Delete Employee')
                if delete:
                    st.warning('Are you sure you want to delete the employee? This act cannot be undone')
                    confirm_delete = st.radio('Are you sure?',['No','Yes'])
                    if confirm_delete=='Yes':
                        delete_data(selected_employee_id)
                        st.experimental_rerun()

if __name__ == "__main__":
    init_db()
    main()