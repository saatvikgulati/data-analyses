import pandas as pd
import streamlit as st
import sqlite3
import matplotlib.pyplot as plt

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
        cursor.execute('create index if not exists idx_employee_id on employees(employee_id)')
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

def bulk_insert(df):
    conn = sqlite3.connect('my_database.db')
    try:
        df.columns = ['employee_id','name','gender','date_of_joining','salary','position']
        df.to_sql('employees',conn,if_exists='append',index=False)
        st.success(f'Successfully inserted {len(df)} rows into db')
    except Exception as e:
        st.error('Error in bulk inserting')
        st.error(e)
    finally:
        conn.close()

def bulk_delete(df):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        df.columns = ['employee_id', 'name', 'gender', 'date_of_joining', 'salary', 'position']
        emp_ids = df["employee_id"].tolist()
        chunk_size = 999
        for i in range(0,len(emp_ids),chunk_size):
            chunk = emp_ids[i:i+chunk_size]
            placeholders = ','.join(['?']*len(chunk))
            query = f"delete from employees where employee_id in ({placeholders})"
            cursor.execute(query,chunk)
        conn.commit()
        st.success(f'Deleted {len(df)} rows from db')
    except Exception as e:
        st.error('Error in bulk delete')
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

def pie_chart(df):
    st.subheader('Gender Distribution')
    gender_counts = df['gender'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(gender_counts, labels=gender_counts.index, startangle=90)
    ax.axis('equal')
    ax.set_title('Gender Distribution')
    st.pyplot(fig)
    st.subheader('Position Distribution')
    position_counts = df['position'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(position_counts, labels=position_counts.index, startangle=90)
    ax.axis('equal')
    ax.set_title('Position Distribution')
    st.pyplot(fig)

def bar_chart(df):
    st.subheader('Gender Distribution')
    gender_counts = df['gender'].value_counts()
    fig,ax = plt.subplots()
    ax.bar(gender_counts.index,gender_counts,color='skyblue')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Count')
    ax.set_title('Gender Distribution')
    st.pyplot(fig)
    st.subheader('Position Distribution')
    position_counts = df['position'].value_counts()
    fig,ax = plt.subplots()
    ax.bar(position_counts.index,position_counts,color='lightgreen')
    ax.set_xlabel('Position')
    ax.set_ylabel('Count')
    ax.set_title('Position Distribution')
    st.pyplot(fig)

def main():
    st.title('Employee Data Management App')

    tab1,tab2,tab3,tab4,tab5 = st.tabs(['Add Data','Manage/View/Update/Delete Data','Flood Database','Bulk Delete','Summary'])

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

            delete = st.button('Delete Employee')
            if delete:
                delete_data(selected_employee_id)
                st.experimental_rerun()
        else:
            st.info('No records found in db')
    with tab3:
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
                bulk_insert(df)
                st.experimental_rerun()

    with tab4:
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
                bulk_delete(df)
                st.experimental_rerun()
    with tab5:
        st.subheader('Summary')
        data = fetch_data()
        if not data.empty:
            chart = st.radio('Chart',['Pie Chart','Bar Chart'],index=0)
            if chart == 'Pie Chart':
                pie_chart(data)
            elif chart == 'Bar Chart':
                bar_chart(data)
        else:
            st.info('No data to display')



if __name__ == "__main__":
    init_db()
    main()