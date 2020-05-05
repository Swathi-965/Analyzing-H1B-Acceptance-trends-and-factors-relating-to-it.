### **The Parselmouths**

Repository for CS 418  Group Project.

- Project : Analyzing H1B Acceptance trends and factors relating to it.


H1B visa is a nonimmigrant visa issued to graduate level applicants allowing them to work in the United States. The employer sponsors the H1B visa for workers with theoretical or technical expertise in specialized fields such as in IT, finance, accounting etc. An interesting fact about immigrant workers is that about 52 percent of new Silicon valley companies were founded by such workers during 1995 and 2005. 

Some famous CEOs like Indira Nooyi (Pepsico), Elon Musk (Tesla), Sundar Pichai (Google),Satya Nadella (Microsoft) once arrived to the US on a H1B visa.

**Motivation**: Our team consists of five international graduate students, in the future we will be applying for H1B visa. The visa application process seems very long, complicated and uncertain. So we decided to understand this process and use Machine learning algorithms to predict the acceptance rate and trends of H1B visa petitions. 

#### Data Set:

The data used in the project has been collected from [the Office of Foreign Labor Certification (OFLC).](https://www.foreignlaborcert.doleta.gov/performancedata.cfm)The Data provides insight into each petition with information such as the Job title, Wage, Employer, Worksite location etc. To download the data follow the steps below:

1. Click on the above link to open the OFLC webpage. 
2. Click on the Disclosure data tab.
3. Scroll down to find the LCA/H1B data. 

#### Files in the repository:

- cleaning.py - a collection of methods used to clean the data and used for feature engineering. 

- baseline.py- A python file used to calculate the baseline prediction.

- read_files.py - A python program to read csv files for years 2015, 2016, 2017, 2018 and 2019 in an efficient way to avoid the RAM from crashing.

- visualizations.py- Code for the visualizations shown in the notebook.

- mid_progress_report.ipnyb: Progress report submitted in April. 

- H1b_perm.ipnyb: Perm data set used to create visualization for Education.png

- Education.png: Visualizations shows education levels. 

- read_me_python_files.pdf: Instructions to load python files to google colab. 

  