import streamlit as st
from contextlib import contextmanager
import sqlite3
import pandas as pd

@st.cache_resource
def get_init_connection():
    return sqlite3.connect('my_database.db',check_same_thread=False)

@contextmanager
def get_conn():
    conn = get_init_connection()
    try:
        yield conn
    finally:
        conn.commit()

def init_db():
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            create table if not exists employees(
                id integer primary key autoincrement,
                employee_id text not null,
                name text not null,
                gender text,
                date_of_joining date,
                salary real,
                position text
            )
            ''')
            cursor.execute('create index if not exists idx_employee_id on employees(employee_id)')
            cursor.execute('create index if not exists idx_employee_name on employees(name)')
            conn.commit()
        except Exception as e:
            st.error('Cannot create table')
            st.error(e)

def insert_data(table_name,column_names,values):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            placeholders = ','.join(['?' for _ in column_names])
            query = f"insert into {table_name} ({','.join(column_names)}) values ({placeholders})"
            cursor.execute(query,values)
            conn.commit()
            st.success('Data Inserted Successfully')
        except Exception as e:
            st.error('Error while inserting data')
            st.error(e)

def update_data(table_name,column_names,values,condition,condition_values):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            set_clause = ','.join([f'{col}=?' for col in column_names])
            query = f'update {table_name} set {set_clause} where {condition}'
            cursor.execute(query,values+condition_values)
            conn.commit()
            st.success('Record Updated Successfully')
        except Exception as e:
            st.error('Error in updating data')
            st.error(e)

def delete_data(table_name,condition,condition_values):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            query = f'delete from {table_name} where {condition}'
            cursor.execute(query,condition_values)
            conn.commit()
            st.success('Employee deleted successfully')
        except Exception as e:
            st.error('Error while deleting employee')
            st.error(e)

def bulk_insert(df,table_name):
    with get_conn() as conn:
        try:
            df.to_sql(table_name,conn,if_exists='append',index=False)
            st.success(f'Successfully inserted {len(df)} rows into db')
        except Exception as e:
            st.error(f'Error in bulk insert into {table_name} table')
            st.error(e)

def bulk_delete(df,table_name,column_name):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            emp_ids = df[column_name].tolist()
            chunk_size = 999
            for i in range(0,len(emp_ids),chunk_size):
                chunk = emp_ids[i:i+chunk_size]
                placeholders = ','.join(['?']*len(chunk))
                query = f"delete from {table_name} where {column_name} in ({placeholders})"
                cursor.execute(query,chunk)
            conn.commit()
            st.success(f'Deleted {len(df)} rows from db')
        except Exception as e:
            st.error(f'Error in bulk delete from {table_name} table')
            st.error(e)

def delete_all_data(table_name):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f'delete from {table_name}')
            conn.commit()
            st.success(f'All data from {table_name} table has been deleted')
        except Exception as e:
            st.error(f'Couldn\'t delete all data from {table_name} table')
            st.error(e)

def fetch_data():
    with get_conn() as conn:
        try:
            df = pd.DataFrame(columns=['employee_id','name','gender','date_of_joining','salary','position'])
            df = pd.read_sql_query('select * from employees',conn)
        except Exception as e:
            st.error('Error in retrieving data')
            st.error(e)
        finally:
            return df