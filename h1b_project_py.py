#!/usr/bin/env python
# coding: utf-8

# # Analysing H1B Acceptance Trends 

# H1B visa is a nonimmigrant visa issued to gradute level workers which allows them to work in the United States. The employer sponsors the H1B visa for workers with theoretical or technical expertise in specialized fields such as in IT, finance, accounting etc. An interesting fact about immigrant workers is that about 52 percent of new Silicon valley companies were founded by such workers during 1995 and 2005. Some famous CEOs like Indira Nooyi (Pepsico), Elon Musk (Tesla), Sundar Pichai (Google),Satya Nadella (Microsoft) once arrived to the US on a H1B visa.

# **Motivation**: Our team consists of five international gradute students, in the future we will be applying for H1B visa. The visa application process seems very long, complicated and uncertain. So we decided to understand this process and use Machine learning algorithms to predict the acceptance rate and trends of H1B visa. 

# ## Data 
# The data used in the project has been collected from <a href="https://www.foreignlaborcert.doleta.gov/performancedata.cfm">the Office of Foreign Labor Certification (OFLC).</a> 

# In[ ]:


from google.colab import drive
drive.mount('/content/gdrive')


# In[2]:


get_ipython().system('pip install autocorrect')
import pandas as pd
import numpy as np
import warnings
import nltk
#from textblob import TextBlob
from autocorrect import Speller 
nltk.download('wordnet')


# ## Exploratory Data Analysis

# Before we begin working on our data we need to understand the traits of our data which we accomplish using EDA. We see that we have about 260 columns , not all 260 columns have essential information that contributes to our analysis. Hence we pick out the columns such as case status( Accepted/ Denied) ,Employer, Job title etc. 

# In[3]:


#Read the csv file and stored in file
file=pd.read_csv('H-1B_Disclosure_Data_FY2019.csv')


# In[4]:


file.shape


# In[26]:


cleaned=file[['CASE_NUMBER','CASE_STATUS','CASE_SUBMITTED','DECISION_DATE','VISA_CLASS','FULL_TIME_POSITION','JOB_TITLE','SOC_CODE','SOC_TITLE',              'EMPLOYER_NAME','WAGE_RATE_OF_PAY_FROM_1','WAGE_UNIT_OF_PAY_1','NAICS_CODE','WORKSITE_CITY_1','WORKSITE_STATE_1']]
cleaned.head()


# In[27]:


cleaned.shape


# In[28]:


cleaned['VISA_CLASS'].value_counts()


# In[30]:


# Visa class has many categories which are not of use , we require only H1B visa type , hence we drop all records with other visa types
cleaned.drop(labels=cleaned.loc[cleaned['VISA_CLASS']!='H-1B'].index , inplace=True)


# In[31]:


cleaned['FULL_TIME_POSITION'].value_counts()


# In[32]:


cleaned['CASE_STATUS'].value_counts()


# In[33]:


#As we want to only need accepted and denied cases we are dropping withdrawn from the data frame. 
#Case status of class certified-withdraw were certified earlier and later withdraw which can be considered a
cleaned.replace({"CASE_STATUS":"CERTIFIED-WITHDRAWN"},"CERTIFIED",inplace=True)
cleaned.drop(labels=cleaned.loc[cleaned['CASE_STATUS']=='WITHDRAWN'].index , inplace=True)
cleaned.head()


# In[34]:


cleaned.info()


# In[35]:


#the column wages has a mix of both string and float value types and some record have the symbol '$' which we want to remove
cleaned['WAGE_RATE_OF_PAY_FROM_1'].apply(type).value_counts()


# In[36]:


cleaned['WORKSITE_STATE_1'].apply(type).value_counts()


# In[37]:


def clean_wages(w):
    """ Function to remove '$' symbol and other delimiters from wages column which consistes of str and float type values
    if the column entry is string type then remove the symbols else return the column value as it is 
    """
    if isinstance(w, str):
        return(w.replace('$', '').replace(',', ''))
    return(w)


# In[38]:


cleaned['WAGES']=cleaned['WAGE_RATE_OF_PAY_FROM_1'].apply(clean_wages).astype('float')
cleaned.info()


# In[39]:


# the wage information that we have available has different unit of pay
cleaned['WAGE_UNIT_OF_PAY_1'].value_counts()


# In[40]:


x=cleaned.loc[cleaned['WAGE_UNIT_OF_PAY_1']=="Month"]
x.head(2)


# In[41]:


# we convert the different units of pay to the type 'Year'
cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY_1'] == 'Month',cleaned['WAGES'] * 12,cleaned['WAGES'])
cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY_1'] == 'Hour',cleaned['WAGES'] * 2080,cleaned['WAGES']) # 2080=8 hours*5 days* 52 weeks
cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY_1'] == 'Bi-Weekly',cleaned['WAGES'] *26,cleaned['WAGES'])
cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY_1'] == 'Week',cleaned['WAGES'] * 52,cleaned['WAGES'])


# In[42]:


#As we have got the information of Wages and made transformation we can drop the initial two records
cleaned.drop(columns=['WAGE_RATE_OF_PAY_FROM_1','WAGE_UNIT_OF_PAY_1'],axis=1,inplace=True)


# In[43]:


cleaned.info()


# In[44]:


"""
We should remove record that have null objects, from the above cell we see
that all columns don't have same number of non-null records
which means we have to remove the records that have the null values.
we see that there are about 17 records that have null values
""" 
null_rows = cleaned.isnull().any(axis=1)
print(cleaned[null_rows].shape)
print(cleaned.shape)


# In[45]:


cleaned.dropna(inplace=True)
print(cleaned.shape)


# In[46]:


cleaned['JOB_TITLE'].value_counts()


# In[47]:


#we see that the job title has integers(words with integers also) 
#removing comma also
def remove_num(text):
  if not any(c.isdigit() for c in text):
    return text
  return ''
cleaned['JOB_TITLE']=cleaned.JOB_TITLE.apply(lambda txt: " ".join([remove_num(i) for i in txt.lower().split()]))
cleaned['JOB_TITLE']=cleaned['JOB_TITLE'].str.replace(',', '')
cleaned['SOC_TITLE']=cleaned.SOC_TITLE.apply(lambda txt: " ".join([remove_num(i) for i in txt.lower().split()]))
cleaned['SOC_TITLE']=cleaned['SOC_TITLE'].str.replace(',', '')

cleaned.head()
cleaned['JOB_TITLE'].value_counts()


# In[48]:


#code to clean and group the JOB_TITLE COLUMN
# lemmatization and spell check function
nltk.download('words')
lemmatizer = nltk.stem.WordNetLemmatizer()
words = set(nltk.corpus.words.words())
spell = Speller()


def lemmatize_text(text):
  return lemmatizer.lemmatize(text)

def spelling_checker(text):
  return spell(text)
 
print(spelling_checker("computr sciece progam check"))


# In[49]:


#this part takes more time because spell_checker 
cleaned['JOB_TITLE']=cleaned.JOB_TITLE.apply(lambda txt: " ".join([lemmatize_text(i) for i in txt.lower().split()]))
print(' after lemmatization')
print(cleaned['JOB_TITLE'].value_counts() )
cleaned['JOB_TITLE']=cleaned.JOB_TITLE.apply(lambda txt: " ".join([spelling_checker(i) for i in txt.lower().split()]))
print('after spell correction')
#cleaned['JOB_TITLE']=cleaned.JOB_TITLE.apply(lambda txt: " ".join([remove_text(i) for i in txt.lower().split()]))
cleaned['JOB_TITLE'].value_counts() 


# In[50]:


#clean SOC TITLE
cleaned['SOC_TITLE']=cleaned.SOC_TITLE.apply(lambda txt: " ".join([lemmatize_text(i) for i in txt.lower().split()]))
cleaned['SOC_TITLE']=cleaned.SOC_TITLE.apply(lambda txt: " ".join([spelling_checker(i) for i in txt.lower().split()]))
cleaned['SOC_TITLE'].value_counts() 


# In[51]:


#we see that the job title has integers in the record which we can remove
cleaned['JOB_TITLE']=cleaned['JOB_TITLE'].str.replace('[0-9(){}[].]', '')
cleaned.head()


# In[52]:


cleaned['SOC_TITLE'].value_counts()


# In[53]:


Top_Employer=cleaned['EMPLOYER_NAME'].value_counts()[:10]
Top_Employer


# In[54]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns


# In[55]:


plt.figure(figsize=[10,10])
ax=sns.barplot(y=Top_Employer.index,x=Top_Employer.values,palette=sns.color_palette('viridis',10))
ax.tick_params(labelsize=12)
for i, v in enumerate(Top_Employer.values): 
    ax.text(.5, i, v,fontsize=15,color='white',weight='bold')
plt.title('Top 10 Companies sponsoring H1B Visa in 2019', fontsize=20)
plt.show()


# In[56]:


grouped_wages=cleaned.groupby('JOB_TITLE', as_index=False).agg({'WAGES':'mean'})
op=grouped_wages.sort_values(by=['WAGES'],ascending=False)
#X=op.loc[op['JOB_TITLE']=='software engineer']
display(op)
display(X)


# In[196]:


cleaned.head()


# In[221]:


data2 = cleaned.drop(columns=['CASE_NUMBER','CASE_SUBMITTED','DECISION_DATE','VISA_CLASS','FULL_TIME_POSITION',
                             'SOC_CODE','SOC_TITLE','NAICS_CODE','WAGES','WORKSITE_CITY_1','WORKSITE_STATE_1',])

data2.CASE_STATUS[data2['CASE_STATUS']== 'CERTIFIED'] =1
data2.CASE_STATUS[data2['CASE_STATUS']== 'DENIED'] = 0


fact_JobTitle = pd.factorize(data2['JOB_TITLE'])[0]
fact_EmployeeName = pd.factorize(data2['EMPLOYER_NAME'])[0]

data2['JOB_TITLE'] = fact_JobTitle
data2['EMPLOYER_NAME'] = fact_EmployeeName

data = data2
data


# In[84]:


# Predicting using Randon Forest
#    Seeting up data
data = cleaned.drop(columns=['CASE_NUMBER','CASE_SUBMITTED','DECISION_DATE','VISA_CLASS','FULL_TIME_POSITION',
                             'JOB_TITLE','SOC_CODE','SOC_TITLE','EMPLOYER_NAME','WORKSITE_CITY_1','WORKSITE_STATE_1',])
data.CASE_STATUS[data['CASE_STATUS']== 'CERTIFIED'] =1
data.CASE_STATUS[data['CASE_STATUS']== 'DENIED'] = 0
data


# In[216]:


Y = data['CASE_STATUS'].values
Y = Y.astype('int')
Y

X = data.drop(labels=['CASE_STATUS'], axis=1)
X


# In[ ]:





# In[217]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=20)


# In[218]:


from sklearn.ensemble import RandomForestClassifier

#model_clf = RandomForestClassifier(n_estimators=10, random_state=30)
model_clf = RandomForestClassifier(n_jobs=2,random_state=0)

model_clf.fit(X_train,y_train)


# In[219]:


prediction_test = model_clf.predict(X_test)
prediction_test


# In[220]:


#compare with original value, Y_test
from sklearn import metrics

print("Accuracy = ", metrics.accuracy_score(y_test, prediction_test))


# In[201]:


status_label = np.array(['Denied','Approved'])

new_pred_number = model_clf.predict([[5416.0,108900.0],[423840.0,99840.0],[423840.0,99842.0]])
new_pred_label= status_label[ new_pred_number ]
new_pred_label


# In[222]:


status_label = np.array(['Denied','Approved'])

new_pred_number = model_clf.predict([[17668,11328],[17668,11328]])
new_pred_label= status_label[ new_pred_number ]
new_pred_label

