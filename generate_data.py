import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime,timedelta
import time

fake = Faker()
def generate_data(num,f_name):

    # st = time.perf_counter()
    # empids = [i for i in range(1,num_employees+1)]
    #
    # employee_names =[random.choice(names) for _ in range(num_employees)]
    # gender = [random.choice(['Male','Female']) for _ in range(num_employees)]
    # doj = [(datetime.now() - timedelta(days=np.random.randint(60,3650))).strftime('%Y-%m-%d') for _ in range(num_employees)]
    # salaries =[np.random.randint(35000,250000) for _ in range(num_employees)]
    #
    # employeepositions = [random.choice(positions) for _ in range(num_employees)]
    # end = time.perf_counter()
    # print("Original code execution time:",end-st)

    # optimzied code
    st = time.perf_counter()
    temp_dict= {}
    gender = ['Male','Female']
    positions = ["Software Engineer", "Manager", "Analyst", "Designer", "HR Specialist"]
    for i in range(0,num):
        temp_dict['id'] = random.randint(1,100)
        temp_dict['name'] = fake.name()
        temp_dict['gender'] = random.choice(gender)
        temp_dict['doj'] = fake.date_between()
        temp_dict['salaries'] = random.randint(35000,250000)
        temp_dict['positions'] = random.choice(positions)
    # employee_names = np.random.choice(d['names'],num)
    # gender = np.random.choice(d['gender'],num)
    # doj = (datetime.now() - pd.to_timedelta(np.random.randint(60, 3650, num), unit='D')).strftime('%Y-%m-%d')
    # salaries = np.random.randint(35000,250000,num)
    # employeepositions = np.random.choice(d['positions'],num)
    end = time.perf_counter()
    print("Optimized code execution time:",end-st)


    df = pd.DataFrame(temp_dict,index=[temp_dict['id']])
    # st = time.perf_counter()
    # df.to_parquet('employees.parquet',index=False,engine = 'pyarrow',compression = 'snappy')
    # end = time.perf_counter()
    # print("Time for saving to disk:",end-st)

    st = time.perf_counter()
    df.to_csv(f'data/{f_name}',index=False)
    end = time.perf_counter()
    print("Optimized saving time:",end-st)

num = 1000000
# d={'names' : ['Raj','Sam','Shyam','Saatvik','Harshal','Krish','Rajesh'],
# 'positions' : ["Software Engineer", "Manager", "Analyst", "Designer", "HR Specialist"],
# 'gender': ['Male','Female']
# }

generate_data(num,'employees.csv')