import streamlit as st
import plotly.express as px

def pie_chart(df):
    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader('Gender Distribution')
        gender_counts = df['gender'].value_counts().reset_index()
        gender_counts.columns = ['gender','count']
        fig = px.pie(gender_counts, names='gender', values='count',title='Gender Distribution')
        st.plotly_chart(fig)
    with col2:
        st.subheader('Position Distribution')
        position_counts = df['position'].value_counts().reset_index()
        position_counts.columns = ['position','count']
        fig = px.pie(position_counts, names='position',values='count',title='Position Distribution')
        st.plotly_chart(fig)
    with col3:
        st.subheader('Salary Range Distribution')
        salary_range_counts = df['salary_distribution'].value_counts().reset_index()
        salary_range_counts.columns = ['salary_distribution','count']
        fig = px.pie(salary_range_counts,names='salary_distribution',values='count',title='Salary Range')
        st.plotly_chart(fig)

def bar_chart(df):
    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader('Gender Distribution')
        gender_counts = df['gender'].value_counts().reset_index()
        gender_counts.columns = ['gender','count']
        fig = px.bar(gender_counts,x='gender',y='count',color='gender',title='Gender Distribution',labels={'gender':'Gender','count':'Count'})
        st.plotly_chart(fig)
    with col2:
        st.subheader('Position Distribution')
        position_counts = df['position'].value_counts().reset_index()
        position_counts.columns = ['position','count']
        fig = px.bar(position_counts,x='position',y='count',color='position',title='Position Distribution',labels={'position':'Position','count':'Count'})
        st.plotly_chart(fig)
    with col3:
        st.subheader('Salary Range Distribution')
        salary_range_counts = df['salary_distribution'].value_counts().reset_index()
        salary_range_counts.columns = ['salary_distribution', 'count']
        fig = px.bar(salary_range_counts, x='salary_distribution',y='count',color='salary_distribution',title='Salary Range',labels={'salary_distribution':'Salary Range','count':'Count'})
        st.plotly_chart(fig)