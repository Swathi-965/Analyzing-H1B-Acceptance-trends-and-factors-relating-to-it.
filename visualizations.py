
def top_employer(plt,sns, cleaned):
    """
    Function to create the visualization for top q0 employers who sponsor the
    most number of Visa applications
    """
    Top_Employer=cleaned['EMPLOYER_NAME'].value_counts()[:10]
    plt.figure(figsize=[8,8])
    ax=sns.barplot(y=Top_Employer.index,x=Top_Employer.values,palette=sns.color_palette('viridis',10))
    ax.tick_params(labelsize=12)
    for i, v in enumerate(Top_Employer.values):
        ax.text(.5, i, v,fontsize=15,color='white',weight='bold')
    plt.title('Top 10 Companies sponsoring H1B Visa in 2015-2019', fontsize=20)
    plt.xlabel("Number of applications filed by the companies",fontsize=15)
    return plt

def USA_map(go,tls,df):
    """
    Fucntion to create an interactive USA map visualization that break down
    the number of jobs for each state
    """

    fig = go.Figure(data=go.Choropleth(locations=df['CODE'],
                                       z = df['counts'].astype(float),
                                       locationmode = 'USA-states',
                                       colorscale = 'Reds',
                                       colorbar_title = "No of jobs"))

    fig.update_layout(title_text = 'Jobs Distribution around the US',title_x=0.5,geo_scope='usa')
    return fig

def salary(plt,sns, data_scnt,data_anlst,data_eng,mach_learn):
    """
    Function create two visualizationf for salary distribution
    and jobs available in the data science domain 
    """
    bplot1=plt.boxplot([data_scnt[data_scnt['WAGES']<200000].WAGES,
                        data_anlst[data_anlst['WAGES']<200000].WAGES,
                        data_eng[data_eng['WAGES']<200000].WAGES,
                        mach_learn[mach_learn['WAGES']<200000].WAGES],
                       patch_artist="True")
    ax.set_xticklabels(['Data Scientists','Data Analysts','Data Engineer','Machine Learning'],fontsize=15)
    ax.set_title('Salary Distribution for jobs in Data Science field in 2019', fontsize=15)
    ax.tick_params(labelsize=10)
    colors = ['blue','orange', 'green', 'red']
    for patch, color in zip(bplot1['boxes'], colors):
      patch.set_facecolor(color)
    datajobs=cw.data_concat(pd,data_scnt,data_anlst,data_eng,mach_learn)
    ax2=sns.countplot(x="data", data=datajobs)

    ax2.set_title('Number of petitions for each jobs in Data Science field in 2019', fontsize=12)
    return plt

def plot_precision_recall (plt, y_test, probs,precision_recall_curve):
    """
    Function to plot the precision recall graph 
    """
    pos_probs = probs[:, 1] if probs.ndim > 1 else probs
    plt.figure(figsize=(12,8))
    # calculate model precision-recall curve
    precision, recall, _ = precision_recall_curve(y_test, pos_probs)
    print('Precision and Recall: ', precision, recall)
    # plot the model precision-recall curve
    plt.plot(recall, precision, marker='.', label='Logistic')
    # axis labels
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()
    plt.title('Precision vs Recall curve', loc='center')

    return plt

def plot_buy_american_order(plt, original, pd):
    """
    Function that plots the visualization providing insight on
    the effects of a goverement policy on the H1B applications
    """
    order_date = '18-04-2017'
    srt='01-01-2015'

    original['CASE_SUBMITTED']=pd.to_datetime(original['CASE_SUBMITTED'])
    mask = (original['CASE_SUBMITTED'] < order_date )& (original['CASE_SUBMITTED'] >= srt)
    mask1 = (original['CASE_SUBMITTED'] >= order_date)
    cleaned_before = original.loc[mask]
    cleaned_after = original.loc[mask1]
    cleaned_before = cleaned_before.sample(n=10000, replace=False, random_state=1)
    cleaned_after = cleaned_after.sample(n=10000, replace=False, random_state=1)
    policy_dataframe = pd.concat([cleaned_before,cleaned_after]).reset_index(drop=True)
    policy_dataframe = policy_dataframe[['CASE_STATUS','CASE_SUBMITTED','CASE_NUMBER']]
    policy_dataframe = policy_dataframe.replace({'CERTIFIED-WITHDRAWN': 'CERTIFIED'})
    policy_dataframe['CASE_SUBMITTED'] = policy_dataframe['CASE_SUBMITTED'].dt.year

    policy_dataframe.drop(labels=policy_dataframe.loc[policy_dataframe['CASE_STATUS'] == 'WITHDRAWN'].index, inplace = True)
    policy_dataframe.drop(labels=policy_dataframe.loc[policy_dataframe['CASE_STATUS'] == 'DENIED'].index, inplace = True)

    plt.rcParams["figure.figsize"] = (8,4)
    line_certified = pd.crosstab(policy_dataframe.CASE_SUBMITTED,policy_dataframe.CASE_STATUS).plot()#title='H1B Visas Certified by year'
    plt.title('H1B Visas Certified by year', fontsize=22)
    plt.legend(title='# Visas')
    plt.axvline(x= 2017.5, color = 'r')
    plt.xlabel("Year")
    plt.annotate(
            'Hire American Executive Order',
            fontsize=14,
            color='r',
            xy=(2017.5, 4150), #400
            #arrowprops=dict(arrowstyle='->'),
            arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2'),
            xytext=(2015.5, 4150)) #405

    #deleting the temporary dataframe created to avoid ram consumption.
    del cleaned_before
    del cleaned_after
    del original
    del policy_dataframe

    return plt
