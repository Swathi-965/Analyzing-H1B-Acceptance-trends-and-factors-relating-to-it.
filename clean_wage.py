# -*- coding: utf-8 -*-
def clean_wages(w):
    """
    Function to remove '$' symbol and other delimiters from wages column which consistes of str and float type values
    if the column entry is string type then remove the symbols else return the column value as it is 
    """
    if isinstance(w, str):
        return(w.replace('$', '').replace(',', ''))
    return(w)

def wage_feature_eng(wage):
    """
    Feature engineering by making the quantitative type data in WAGE column
    into categorical data
    """
    if wage <=50000:
        return "VERY LOW"
    elif wage in range(50000,75000):
        return "LOW"
    elif wage in range(75000,100000):
        return "AVERAGE"
    elif wage in range(100000,150000):
        return "HIGH"
    elif wage >=150000:
        return "VERY HIGH"

def clean_wageUnit(np,cleaned):
    """
    Wage data has different unit such as hourly pay , annual pay
    we are converting this to yearly data
    """
    cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY'] == 'Month',cleaned['WAGES'] * 12,cleaned['WAGES'])
    cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY'] == 'Hour',cleaned['WAGES'] * 2080,cleaned['WAGES']) # 2080=8 hours*5 days* 52 weeks
    cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY'] == 'Bi-Weekly',cleaned['WAGES'] *26,cleaned['WAGES'])
    cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY'] == 'Week',cleaned['WAGES'] * 52,cleaned['WAGES'])
    return cleaned


def data_jobs(cleaned):
    """
    Function takes a dataframe as input and returns 4 data
    frames for each job category
    """
    data_scnt=cleaned[cleaned['JOB_TITLE'].str.contains('data scientist')]
    data_anlst=cleaned[cleaned['JOB_TITLE'].str.contains('data analyst')]
    data_eng=cleaned[cleaned['JOB_TITLE'].str.contains('data eng')]
    mach_learn=cleaned[cleaned['JOB_TITLE'].str.contains('machine learning')]
    return data_scnt,data_anlst,data_eng,mach_learn

def data_concat(pd,data_scnt,data_anlst,data_eng,mach_learn):
    data_scnt['data']='Data Scientists'
    data_anlst['data']='Data Analysts'
    data_eng['data']='Data Engineer'
    mach_learn['data']='Machine Learning'
    jobs = [data_scnt,data_anlst,data_eng,mach_learn]
    datajobs = pd.concat(jobs)
    return datajobs

    






