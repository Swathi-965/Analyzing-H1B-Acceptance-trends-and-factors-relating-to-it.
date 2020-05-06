# -*- coding: utf-8 -*-
import string
import nltk
import gensim.downloader as api
word_vectors_1 = api.load("glove-wiki-gigaword-100")
import pandas as pd
import numpy as np
from autocorrect import Speller
from sklearn.preprocessing import OneHotEncoder 
import pandas as pd
nltk.download('wordnet')
nltk.download('words')
lemmatizer = nltk.stem.WordNetLemmatizer()
words = set(nltk.corpus.words.words())
spell = Speller()
Encoding = OneHotEncoder(handle_unknown='ignore',sparse = True)

def clean_wages(w):
    """
    Function to remove '$' symbol and other delimiters from wages column which consistes of str and float type values
    if the column entry is string type then remove the symbols else return the column value as it is 
    """
    if isinstance(w, str):
        return(w.replace('$', '').replace(',', ''))
    return(w)

def remove_num(text):
    """
    Function to clean JOB_TITLE and SOC_TITLE by removing digits from the values
    """
    if not any(c.isdigit() for c in text):
        return text
    return ''

def drop_less_significant(cleaned):
    """
    Function to drop less records in EMPLOYER_NAME,SOC_TITLE and SOC_CODE
    if the catergory in any of the columns is less than 15 we are dropping it
    """
    cleaned=cleaned.groupby("SOC_CODE").filter(lambda x: len(x)>15)
    cleaned=cleaned.groupby("SOC_TITLE").filter(lambda x: len(x)>15)
    cleaned=cleaned.groupby("EMPLOYER_NAME").filter(lambda x: len(x)>15)
    cleaned=cleaned.groupby("WORKSITE_STATE").filter(lambda x: len(x)>15)
    return cleaned
    
def wage_feature_eng(wage):
    """
    Feature engineering by making the quantitative type data in WAGE column
    into categorical data
    """
    if wage <= 50000:
        return "VERY LOW"
    elif wage in range(50000,75000):
        return "LOW"
    elif wage in range(75000,100000):
        return "AVERAGE"
    elif wage in range(100000,150000):
        return "HIGH"
    elif wage >= 150000:
        return "VERY HIGH"

def clean_wageUnit(np,cleaned):
    """
    Wage data has different unit such as hourly pay , annual pay
    we are converting this to yearly data
    """
    cleaned['WAGES']=np.where(cleaned['WAGE_UNIT_OF_PAY']=='Month',cleaned['WAGES']*12,cleaned['WAGES'])
    cleaned['WAGES']=np.where(cleaned['WAGE_UNIT_OF_PAY']=='Hour',cleaned['WAGES']*2080,cleaned['WAGES']) # 2080=8 hours*5 days* 52 weeks
    cleaned['WAGES']=np.where(cleaned['WAGE_UNIT_OF_PAY']=='Bi-Weekly',cleaned['WAGES']*26,cleaned['WAGES'])
    cleaned['WAGES']=np.where(cleaned['WAGE_UNIT_OF_PAY']=='Week',cleaned['WAGES']*52,cleaned['WAGES'])
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
    """
    Find all data science domain jobs and concatenate the dataframe
    created for each job category
    returns concatenated dataframe
    """
    data_scnt['data']='Data Scientists'
    data_anlst['data']='Data Analysts'
    data_eng['data']='Data Engineer'
    mach_learn['data']='Machine Learning'
    jobs = [data_scnt,data_anlst,data_eng,mach_learn]
    datajobs = pd.concat(jobs)
    return datajobs

def clean_states(cleaned):
    """
    Function to change the WORKSITE_STATE_1 cplumn some values are abbrevation,
    some values are state names, we are replacing with abbrevations wiith state
    names
    """
    state={"AL":"ALABAMA","AK":"ALASKA","AZ":"ARIZONA","AR":"ARKANSAS","CA":"CALIFORNIA","CO":"COLORADO","DE":"DELAWARE",\
       "FL":"FLORIDA","GA":"GEORGIA","HI":"HAWAII","ID":"IDAHO","IL":"ILLINOIS","IN":"INDIANA","IA":"IOWA","KS":"KANSAS",\
       "KY":"KENTUCKY","LA":"LOUISIANA","ME":"MAINE","MD":"MARYLAND","MA":"MASSACHUSETTS","MI":"MICHIGAN","MN":"MINNESOTA",\
       "MS":"MISSISSIPPI","MO":"MISSOURI","MT":"MONTANA","NE":"NEBRASKA","NV":"NEVADA","NH":"NEW HAMPSHIRE","NJ":"NEW JERSEY",\
       "NM":"NEW MEXICO","NY":"NEW YORK","NC":"NORTH CAROLINA","ND":"NORTH DAKOTA","OH":"OHIO","OK":"OKLAHOMA","OR":"OREGON",\
       "PA":"PENNSYLVANIA","RI":"RHODE ISLAND","SC":"SOUTH CAROLINA","SD":"SOUTH DAKOTA","TN":"TENNESSEE","TX":"TEXAS",\
       "UT":"UTAH","VT":"VERMONT","VA":"VIRGINIA","WA":"WASHINGTON","WV":"WEST VIRGINIA","WI":"WISCONSIN","WY":"WYOMING",\
       "PR":"PUERTO RICO","VI":"U.S. VIRGIN ISLANDS","MP":"NORTHERN MARIANA ISLANDS","GU":"GUAM","MH":"MARSHALL ISLANDS",\
       "PW":"PALAU","DC":"DISTRICT OF COLUMBIA","CT":"CONNECTICUT"}
    cleaned.replace({"WORKSITE_STATE": state},inplace = True)
    return cleaned

def states_vis(cleaned):
    """
    Function to change the states data to abbrevation codes that can be used in
    USA map viasualization
    """
    state_abbrev = {'Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ','Arkansas': 'AR','California': 'CA',\
                'Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC','Florida': 'FL',\
                'Georgia': 'GA','Guam': 'GU','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA',\
                'Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA',\
                'Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE',\
                'Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC',\
                'North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA',\
                'Puerto Rico': 'PR','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN',\
                'Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA',\
                'West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}
    abbrev={}
    for k,v in state_abbrev.items():
      abbrev[k.upper()]=v
    cleaned['CODE']=cleaned['WORKSITE_STATE'].map(abbrev)
    return cleaned

def cat_to_num(cleaned):
    """
    Function to convert categorical values into numerical values to use for classifiers
    """
    cleaned.loc[(cleaned.H1B_DEPENDENT=="Y"),"H1B_DEPENDENT"] = 1
    cleaned.loc[(cleaned.H1B_DEPENDENT=="N"),"H1B_DEPENDENT"] = 0
    cleaned.loc[(cleaned.CASE_STATUS == "CERTIFIED"),"CASE_STATUS"] = 1
    cleaned.loc[(cleaned.CASE_STATUS == "DENIED"),"CASE_STATUS"] = 0
    cleaned.loc[(cleaned.FULL_TIME_POSITION == 'Y'),"FULL_TIME_POSITION"] = 1
    cleaned.loc[(cleaned.FULL_TIME_POSITION == 'N'),"FULL_TIME_POSITION"] = 0
    return cleaned

def remove_punctuation(value):
    """
    Function to remove punctuations
    """
    result = ""
    for c in value:
        if str(c) not in string.punctuation:
            result += c
        else:
            result +=" "
    return result


def grouping(position):
    """
    Function to convert categorical columns(SOC_TITLE) to word_vectors 
    """
    z = np.zeros(100)
    x = position.split()
    count = 0
    for i in x:
        if i in word_vectors_1:
            z += word_vectors_1[i]
            count+=1
    if count>0:
        return z/count
    else:
        return z



def lemmatize_text(text):
    """
    Function to lemmatize, converting plural to single. 
    """
    return lemmatizer.lemmatize(text)

def spelling_checker(text):
    """
    Function to correct spelling mistakes.
    """
    return spell(text)

def text_clean(cleaned):
    """
    Function to  call lemmatizer and spell check
    """
    cleaned['JOB_TITLE']=cleaned.JOB_TITLE.apply(lambda txt: " ".join([remove_num(i) for i in txt.lower().split()]))
    cleaned['JOB_TITLE']=cleaned['JOB_TITLE'].str.replace(',', '')
    cleaned['SOC_TITLE']=cleaned.SOC_TITLE.apply(lambda txt: " ".join([remove_num(i) for i in txt.lower().split()]))
    cleaned['SOC_TITLE']=cleaned['SOC_TITLE'].str.replace(',', '')
    cleaned['SOC_TITLE']=cleaned.SOC_TITLE.apply(lambda txt: " ".join([lemmatize_text(i) for i in txt.lower().split()]))
    cleaned['SOC_TITLE']=cleaned.SOC_TITLE.apply(lambda txt: " ".join([spelling_checker(i) for i in txt.lower().split()]))
    return cleaned  


def fun_preprocessing(cleaned):
    """
    Cleaning and fitting the dataframe in X and Y train to use in the ML functions
    """
    Dataset = cleaned[["CASE_STATUS", "FULL_TIME_POSITION","SOC_TITLE", "WORKSITE_STATE", "WAGES", "H1B_DEPENDENT"]]
    Dataset.reset_index(drop = True,inplace = True)
    df = pd.DataFrame(columns = ["job_position"])
    Dataset["SOC_TITLE"] = Dataset["SOC_TITLE"].apply(lambda x : remove_punctuation(x))
    df = pd.DataFrame(columns = ["job_position"])
    df["job_position"] = Dataset["SOC_TITLE"].apply(lambda x : grouping(x))
    Dataset.drop(columns = ["SOC_TITLE"],axis=1,inplace=True)
    Dataset.reset_index(drop = True, inplace = True)
    Encoding_df = pd.DataFrame(Encoding.fit_transform(Dataset[["WORKSITE_STATE"]]).toarray())
    Dataset = Dataset.join(Encoding_df)
    Dataset.drop(columns = ['WORKSITE_STATE'],axis=1,inplace=True)
    word_vectors = df[["job_position"]].values
    temp = np.vstack(word_vectors.tolist())
    Y = Dataset["CASE_STATUS"].astype(float)
    Dataset.drop(columns = ["CASE_STATUS"],inplace = True)
    other_features = Dataset.iloc[:].values
    all_features = np.hstack([temp, other_features])
    X = all_features
    return X, Y


def get_df_wage(cleaned):
    """
    Function to form data_frame for wage classification.
    """
    order_date = '01-01-2018'
    cleaned['CASE_SUBMITTED']=pd.to_datetime(cleaned['CASE_SUBMITTED'])
    mask1 = (cleaned['CASE_SUBMITTED'] < order_date)
    cleaned_before = cleaned.loc[mask1]
    Dataset_wage=cleaned_before[["EMPLOYER_NAME","FULL_TIME_POSITION","SOC_TITLE", "WORKSITE_STATE", "WC_NUM","CASE_STATUS"]]
    Dataset_wage.reset_index(drop = True,inplace = True)
    Top_EMPLOYER = Dataset_wage["EMPLOYER_NAME"].value_counts().head(70)
    
    def emp_function(emp):
        """
        Function to  clean and take top employers
        """
        if emp in Top_EMPLOYER:
            return emp
        else:
            return "others"

    Dataset_wage["TOP_EMPLOYER"] = Dataset_wage["EMPLOYER_NAME"].apply(emp_function)
    Dataset_wage.drop(columns=["EMPLOYER_NAME"],axis = 1,inplace=True)
    Dataset_wage["SOC_TITLE"] = Dataset_wage["SOC_TITLE"].apply(lambda x : remove_punctuation(x))
    df_wage = pd.DataFrame(columns = ["soc_title"])
    Dataset_wage["SOC_TITLE"] = Dataset_wage["SOC_TITLE"].apply(lambda x : grouping(x))# converting job titles to numeric values using word_vectors.
    df_wage["soc_title"] = Dataset_wage["SOC_TITLE"]
    Dataset_wage.drop(columns=["SOC_TITLE"],axis=1,inplace=True)
    Dataset_wage.reset_index(drop = True, inplace = True)   
    Encoding = OneHotEncoder(handle_unknown='ignore',sparse = True)
    Encoding_wage = pd.DataFrame(Encoding.fit_transform(Dataset_wage[["WORKSITE_STATE","TOP_EMPLOYER"]]).toarray())
    Dataset_wage = Dataset_wage.join(Encoding_wage)
    Dataset_wage.drop(columns=["WORKSITE_STATE","TOP_EMPLOYER"],axis=1,inplace=True)
    return Dataset_wage,df_wage

def get_XY_wage(Dataset_wage,df_wage):
    """
    Spilt the dataframe in X and Y train for Wage prediction
    """
    Y = Dataset_wage["WC_NUM"].astype(float)
    wv_wage = df_wage[["soc_title"]].values
    temp_var = np.vstack(wv_wage.tolist())
    Dataset_wage.drop(columns = ["WC_NUM"],inplace = True)
    other_features = Dataset_wage.iloc[:].values
    sum_features = np.hstack([temp_var, other_features])
    X = sum_features
    return X,Y

def map_wage(cleaned):
    """
    Mapping wages to the 4 categories and creating label for wages
    """
    #mapping wages to 4 categories
    cleaned['WAGE_CATEGORY'] =pd.cut(cleaned.WAGES,bins=[0,50000,100000,140000,200000],
                                 labels=['LOW','AVERAGE','HIGH',"VERY HIGH"])
    df_temp = pd.DataFrame(columns = ["WC_NUM"])
    cleaned['WC_NUM'] = pd.cut(cleaned.WAGES,bins=[0,50000,100000,140000,200000],labels=[0,1,2,3])
    df_temp["WC_NUM"]=pd.cut(cleaned.WAGES,bins=[0,50000,100000,140000,200000],labels=[0,1,2,3])
    return cleaned,df_temp

    






