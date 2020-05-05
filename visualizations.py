
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
    
