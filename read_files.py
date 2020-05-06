import pandas as pd

def read_csv(pd,link2015,link2016,link2017,link2018,link2019):
    """
    Our Project works on data from 2015 to 2019
    The data is taken from OFLC (link in the notebook)
    Each year the column names vary this has been fixed in the code below
    the dataframe for all years are concatenated to create one dataframe
    and the intermediate dataframes are deleted to avoid the RAM from crashing
    """
    
    file2015=pd.read_csv(link2015,encoding='latin-1', low_memory=False)
    file2015.rename(columns = {'H-1B_DEPENDENT':'H1B_DEPENDENT','SOC_NAME':'SOC_TITLE','WAGE_RATE_OF_PAY':'WAGE_RATE_OF_PAY_FROM'}, inplace = True)
                         
    df2015 = file2015[['CASE_NUMBER', 'CASE_STATUS', 'CASE_SUBMITTED', 'DECISION_DATE',
                       'VISA_CLASS','FULL_TIME_POSITION','JOB_TITLE', 'SOC_CODE', 'SOC_TITLE',
                       'EMPLOYER_NAME','WAGE_RATE_OF_PAY_FROM','WAGE_UNIT_OF_PAY','WORKSITE_CITY',
                       'WORKSITE_STATE','H1B_DEPENDENT']]
    df2015['WAGE_RATE_OF_PAY_FROM'] = df2015['WAGE_RATE_OF_PAY_FROM'].str.split('-').str[0]

    del file2015

    file2016=pd.read_csv(link2016,encoding='latin-1', low_memory=False)
    
    file2016.rename(columns = {'H-1B_DEPENDENT':'H1B_DEPENDENT','SOC_NAME':'SOC_TITLE'}, inplace = True)
    df2016=file2016[['CASE_NUMBER', 'CASE_STATUS', 'CASE_SUBMITTED', 'DECISION_DATE',
                     'VISA_CLASS','FULL_TIME_POSITION','JOB_TITLE', 'SOC_CODE', 'SOC_TITLE',
                     'EMPLOYER_NAME','WAGE_RATE_OF_PAY_FROM','WAGE_UNIT_OF_PAY','WORKSITE_CITY',
                     'WORKSITE_STATE','H1B_DEPENDENT']]

    del file2016

    file2017=pd.read_csv(link2017,encoding='latin-1', low_memory=False)
    
    file2017=pd.read_csv('/content/gdrive/My Drive/H1B_project/H-1B_Disclosure_Data_FY17.csv',encoding='latin-1', low_memory=False)
    file2017.rename(columns = {'SOC_NAME':'SOC_TITLE'}, inplace = True)
    df2017=file2017[['CASE_NUMBER', 'CASE_STATUS', 'CASE_SUBMITTED', 'DECISION_DATE',
                     'VISA_CLASS','FULL_TIME_POSITION','JOB_TITLE', 'SOC_CODE',
                     'SOC_TITLE','EMPLOYER_NAME','WAGE_RATE_OF_PAY_FROM',
                     'WAGE_UNIT_OF_PAY','WORKSITE_CITY','WORKSITE_STATE','H1B_DEPENDENT']]
    del file2017

    file2018=pd.read_csv(link2018,encoding='latin-1', low_memory=False)
    
    file2018=pd.read_csv('/content/gdrive/My Drive/H1B_project/H-1B_Disclosure_Data_FY2018_EOY.csv',encoding='latin-1', low_memory=False)
    file2018.rename(columns = {'SOC_NAME':'SOC_TITLE'}, inplace = True)
    df2018=file2018[['CASE_NUMBER', 'CASE_STATUS', 'CASE_SUBMITTED', 'DECISION_DATE',
                     'VISA_CLASS','FULL_TIME_POSITION','JOB_TITLE', 'SOC_CODE', 'SOC_TITLE',
                     'EMPLOYER_NAME','WAGE_RATE_OF_PAY_FROM','WAGE_UNIT_OF_PAY',
                     'WORKSITE_CITY','WORKSITE_STATE','H1B_DEPENDENT']]

    del file2018

    file2019=pd.read_csv(link2019,encoding='latin-1', low_memory=False)
    
    file2019=pd.read_csv('/content/gdrive/My Drive/H1B_project/H-1B_Disclosure_Data_FY2019.csv',encoding='latin-1', low_memory=False)
    file2019.rename(columns = {'H-1B_DEPENDENT':'H1B_DEPENDENT','WAGE_RATE_OF_PAY_FROM_1':'WAGE_RATE_OF_PAY_FROM',
                               'WAGE_UNIT_OF_PAY_1':'WAGE_UNIT_OF_PAY','WORKSITE_CITY_1':'WORKSITE_CITY',
                               'WORKSITE_STATE_1':'WORKSITE_STATE'}, inplace = True)
    df2019=file2019[['CASE_NUMBER', 'CASE_STATUS', 'CASE_SUBMITTED', 'DECISION_DATE',
                     'VISA_CLASS','FULL_TIME_POSITION','JOB_TITLE', 'SOC_CODE', 'SOC_TITLE',
                     'EMPLOYER_NAME','WAGE_RATE_OF_PAY_FROM','WAGE_UNIT_OF_PAY',
                     'WORKSITE_CITY','WORKSITE_STATE','H1B_DEPENDENT']]

    del file2019
    
    cleaned=pd.concat([df2015,df2016,df2017,df2018,df2019])
    # To avoid using the RAM completely
    del df2019
    del df2018
    del df2017
    del df2016
    del df2015
    
    return cleaned
    
