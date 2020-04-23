# -*- coding: utf-8 -*-
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
    cleaned = cleaned.groupby("SOC_CODE").filter(lambda x: len(x) > 15)
    cleaned = cleaned.groupby("SOC_TITLE").filter(lambda x: len(x) > 15)
    cleaned = cleaned.groupby("EMPLOYER_NAME").filter(lambda x: len(x) > 15)
    cleaned = cleaned.groupby("WORKSITE_STATE").filter(lambda x: len(x) > 15)
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
    if wage <=50000:
    if wage <= 50000:
        return "VERY LOW"
    elif wage in range(50000,75000):
        return "LOW"
    elif wage in range(75000,100000):
        return "AVERAGE"
    elif wage in range(100000,150000):
        return "HIGH"
    elif wage >=150000:
    elif wage >= 150000:
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
    data_scnt['data']='Data Scientists'
    data_anlst['data']='Data Analysts'
    data_eng['data']='Data Engineer'
    mach_learn['data']='Machine Learning'
    jobs = [data_scnt,data_anlst,data_eng,mach_learn]
    datajobs = pd.concat(jobs)
    return datajobs

def clean_states(cleaned):
    cleaned.loc[(cleaned.WORKSITE_STATE == "AL"),"WORKSITE_STATE"] = "ALABAMA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "AK"),"WORKSITE_STATE"] = "ALASKA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "AZ"),"WORKSITE_STATE"] = "ARIZONA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "AR"),"WORKSITE_STATE"] = "ARKANSAS"
    cleaned.loc[(cleaned.WORKSITE_STATE == "CA"),"WORKSITE_STATE"] = "CALIFORNIA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "CO"),"WORKSITE_STATE"] = "COLORADO"
    cleaned.loc[(cleaned.WORKSITE_STATE == "DE"),"WORKSITE_STATE"] = "DELAWARE"
    cleaned.loc[(cleaned.WORKSITE_STATE == "FL"),"WORKSITE_STATE"] = "FLORIDA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "GA"),"WORKSITE_STATE"] = "GEORGIA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "HI"),"WORKSITE_STATE"] = "HAWAII"
    cleaned.loc[(cleaned.WORKSITE_STATE == "ID"),"WORKSITE_STATE"] = "IDAHO"
    cleaned.loc[(cleaned.WORKSITE_STATE == "IL"),"WORKSITE_STATE"] = "ILLINOIS"
    cleaned.loc[(cleaned.WORKSITE_STATE == "IN"),"WORKSITE_STATE"] = "INDIANA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "IA"),"WORKSITE_STATE"] = "IOWA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "KS"),"WORKSITE_STATE"] = "KANSAS"
    cleaned.loc[(cleaned.WORKSITE_STATE == "KY"),"WORKSITE_STATE"] = "KENTUCKY"
    cleaned.loc[(cleaned.WORKSITE_STATE == "LA"),"WORKSITE_STATE"] = "LOUISIANA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "ME"),"WORKSITE_STATE"] = "MAINE"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MD"),"WORKSITE_STATE"] = "MARYLAND"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MA"),"WORKSITE_STATE"] = "MASSACHUSETTS"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MI"),"WORKSITE_STATE"] = "MICHIGAN"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MN"),"WORKSITE_STATE"] = "MINNESOTA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MS"),"WORKSITE_STATE"] = "MISSISSIPPI"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MO"),"WORKSITE_STATE"] = "MISSOURI"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MT"),"WORKSITE_STATE"] = "MONTANA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "NE"),"WORKSITE_STATE"] = "NEBRASKA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "NV"),"WORKSITE_STATE"] = "NEVADA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "NH"),"WORKSITE_STATE"] = "NEW HAMPSHIRE"
    cleaned.loc[(cleaned.WORKSITE_STATE == "NJ"),"WORKSITE_STATE"] = "NEW JERSEY"
    cleaned.loc[(cleaned.WORKSITE_STATE == "NM"),"WORKSITE_STATE"] = "NEW MEXICO"
    cleaned.loc[(cleaned.WORKSITE_STATE == "NY"),"WORKSITE_STATE"] = "NEW YORK"
    cleaned.loc[(cleaned.WORKSITE_STATE == "NC"),"WORKSITE_STATE"] = "NORTH CAROLINA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "ND"),"WORKSITE_STATE"] = "NORTH DAKOTA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "OH"),"WORKSITE_STATE"] = "OHIO"
    cleaned.loc[(cleaned.WORKSITE_STATE == "OK"),"WORKSITE_STATE"] = "OKLAHOMA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "OR"),"WORKSITE_STATE"] = "OREGON"
    cleaned.loc[(cleaned.WORKSITE_STATE == "PA"),"WORKSITE_STATE"] = "PENNSYLVANIA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "RI"),"WORKSITE_STATE"] = "RHODE ISLAND"
    cleaned.loc[(cleaned.WORKSITE_STATE == "SC"),"WORKSITE_STATE"] = "SOUTH CAROLINA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "SD"),"WORKSITE_STATE"] = "SOUTH DAKOTA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "TN"),"WORKSITE_STATE"] = "TENNESSEE"
    cleaned.loc[(cleaned.WORKSITE_STATE == "TX"),"WORKSITE_STATE"] = "TEXAS"
    cleaned.loc[(cleaned.WORKSITE_STATE == "UT"),"WORKSITE_STATE"] = "UTAH"
    cleaned.loc[(cleaned.WORKSITE_STATE == "VT"),"WORKSITE_STATE"] = "VERMONT"
    cleaned.loc[(cleaned.WORKSITE_STATE == "VA"),"WORKSITE_STATE"] = "VIRGINIA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "WA"),"WORKSITE_STATE"] = "WASHINGTON"
    cleaned.loc[(cleaned.WORKSITE_STATE == "WV"),"WORKSITE_STATE"] = "WEST VIRGINIA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "WI"),"WORKSITE_STATE"] = "WISCONSIN"
    cleaned.loc[(cleaned.WORKSITE_STATE == "WY"),"WORKSITE_STATE"] = "WYOMING"
    cleaned.loc[(cleaned.WORKSITE_STATE == "PR"),"WORKSITE_STATE"] = "PUERTO RICO"
    cleaned.loc[(cleaned.WORKSITE_STATE == "VI"),"WORKSITE_STATE"] = "U.S. VIRGIN ISLANDS"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MP"),"WORKSITE_STATE"] = "NORTHERN MARIANA ISLANDS"
    cleaned.loc[(cleaned.WORKSITE_STATE == "GU"),"WORKSITE_STATE"] = "GUAM"
    cleaned.loc[(cleaned.WORKSITE_STATE == "MH"),"WORKSITE_STATE"] = "MARSHALL ISLANDS"
    cleaned.loc[(cleaned.WORKSITE_STATE == "PW"),"WORKSITE_STATE"] = "PALAU"
    cleaned.loc[(cleaned.WORKSITE_STATE == "DC"),"WORKSITE_STATE"] = "DISTRICT OF COLUMBIA"
    cleaned.loc[(cleaned.WORKSITE_STATE == "CT"),"WORKSITE_STATE"] = "CONNECTICUT"
    
    """
    Function to change the WORKSITE_STATE cplumn some values are abbrevation,
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

def cat_to_num(cleaned):
    """
    Function to convert categorical values into numerical values to use for classifiers
    """
    cleaned.loc[(cleaned.H1B_DEPENDENT=="Y"),"H1B_DEPENDENT"] = 1
    cleaned.loc[(cleaned.H1B_DEPENDENT=="N"),"H1B_DEPENDENT"] = 0
    return cleaned

    
    
    
    
    



    






