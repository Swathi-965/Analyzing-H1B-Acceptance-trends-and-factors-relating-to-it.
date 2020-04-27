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
    data_scnt['data']='Data Scientists'
    data_anlst['data']='Data Analysts'
    data_eng['data']='Data Engineer'
    mach_learn['data']='Machine Learning'
    jobs = [data_scnt,data_anlst,data_eng,mach_learn]
    datajobs = pd.concat(jobs)
    return datajobs

def clean_states(cleaned):
    """
    Function to change the WORKSITE_STATE cplumn some values are abbrevation,
    some values are state names, we are replacing with abbrevations wiith state
    names
    """
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "AL"),"WORKSITE_STATE_1"] = "ALABAMA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "AK"),"WORKSITE_STATE_1"] = "ALASKA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "AZ"),"WORKSITE_STATE_1"] = "ARIZONA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "AR"),"WORKSITE_STATE_1"] = "ARKANSAS"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "CA"),"WORKSITE_STATE_1"] = "CALIFORNIA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "CO"),"WORKSITE_STATE_1"] = "COLORADO"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "DE"),"WORKSITE_STATE_1"] = "DELAWARE"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "FL"),"WORKSITE_STATE_1"] = "FLORIDA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "GA"),"WORKSITE_STATE_1"] = "GEORGIA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "HI"),"WORKSITE_STATE_1"] = "HAWAII"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "ID"),"WORKSITE_STATE_1"] = "IDAHO"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "IL"),"WORKSITE_STATE_1"] = "ILLINOIS"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "IN"),"WORKSITE_STATE_1"] = "INDIANA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "IA"),"WORKSITE_STATE_1"] = "IOWA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "KS"),"WORKSITE_STATE_1"] = "KANSAS"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "KY"),"WORKSITE_STATE_1"] = "KENTUCKY"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "LA"),"WORKSITE_STATE_1"] = "LOUISIANA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "ME"),"WORKSITE_STATE_1"] = "MAINE"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MD"),"WORKSITE_STATE_1"] = "MARYLAND"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MA"),"WORKSITE_STATE_1"] = "MASSACHUSETTS"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MI"),"WORKSITE_STATE_1"] = "MICHIGAN"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MN"),"WORKSITE_STATE_1"] = "MINNESOTA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MS"),"WORKSITE_STATE_1"] = "MISSISSIPPI"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MO"),"WORKSITE_STATE_1"] = "MISSOURI"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MT"),"WORKSITE_STATE_1"] = "MONTANA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "NE"),"WORKSITE_STATE_1"] = "NEBRASKA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "NV"),"WORKSITE_STATE_1"] = "NEVADA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "NH"),"WORKSITE_STATE_1"] = "NEW HAMPSHIRE"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "NJ"),"WORKSITE_STATE_1"] = "NEW JERSEY"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "NM"),"WORKSITE_STATE_1"] = "NEW MEXICO"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "NY"),"WORKSITE_STATE_1"] = "NEW YORK"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "NC"),"WORKSITE_STATE_1"] = "NORTH CAROLINA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "ND"),"WORKSITE_STATE_1"] = "NORTH DAKOTA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "OH"),"WORKSITE_STATE_1"] = "OHIO"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "OK"),"WORKSITE_STATE_1"] = "OKLAHOMA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "OR"),"WORKSITE_STATE_1"] = "OREGON"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "PA"),"WORKSITE_STATE_1"] = "PENNSYLVANIA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "RI"),"WORKSITE_STATE_1"] = "RHODE ISLAND"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "SC"),"WORKSITE_STATE_1"] = "SOUTH CAROLINA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "SD"),"WORKSITE_STATE_1"] = "SOUTH DAKOTA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "TN"),"WORKSITE_STATE_1"] = "TENNESSEE"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "TX"),"WORKSITE_STATE_1"] = "TEXAS"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "UT"),"WORKSITE_STATE_1"] = "UTAH"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "VT"),"WORKSITE_STATE_1"] = "VERMONT"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "VA"),"WORKSITE_STATE_1"] = "VIRGINIA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "WA"),"WORKSITE_STATE_1"] = "WASHINGTON"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "WV"),"WORKSITE_STATE_1"] = "WEST VIRGINIA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "WI"),"WORKSITE_STATE_1"] = "WISCONSIN"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "WY"),"WORKSITE_STATE_1"] = "WYOMING"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "PR"),"WORKSITE_STATE_1"] = "PUERTO RICO"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "VI"),"WORKSITE_STATE_1"] = "U.S. VIRGIN ISLANDS"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MP"),"WORKSITE_STATE_1"] = "NORTHERN MARIANA ISLANDS"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "GU"),"WORKSITE_STATE_1"] = "GUAM"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "MH"),"WORKSITE_STATE_1"] = "MARSHALL ISLANDS"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "PW"),"WORKSITE_STATE_1"] = "PALAU"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "DC"),"WORKSITE_STATE_1"] = "DISTRICT OF COLUMBIA"
    cleaned.loc[(cleaned.WORKSITE_STATE_1 == "CT"),"WORKSITE_STATE_1"] = "CONNECTICUT"
    return cleaned

def cat_to_num(cleaned):
    """
    Function to convert categorical values into numerical values to use for classifiers
    """
    cleaned.loc[(cleaned.H1B_DEPENDENT=="Y"),"H1B_DEPENDENT"] = 1
    cleaned.loc[(cleaned.H1B_DEPENDENT=="N"),"H1B_DEPENDENT"] = 0
    return cleaned

    
    
    
    
    



    






