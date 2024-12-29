
def filter_data(search_query,df,column_name):
    return df[df[column_name].str.contains(search_query, case=False)]