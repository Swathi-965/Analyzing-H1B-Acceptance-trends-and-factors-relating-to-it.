def drop_less_significant(cleaned):
        cleaned = cleaned.groupby("SOC_CODE").filter(lambda x: len(x) > 15)
        cleaned = cleaned.groupby("SOC_TITLE").filter(lambda x: len(x) > 15)
        cleaned = cleaned.groupby("EMPLOYER_NAME").filter(lambda x: len(x) > 15)
        return cleaned

def clean_wageUnit(np,cleaned):
        cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY_1'] == 'Month',cleaned['WAGES'] * 12,cleaned['WAGES'])
        cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY_1'] == 'Hour',cleaned['WAGES'] * 2080,cleaned['WAGES']) # 2080=8 hours*5 days* 52 weeks
        cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY_1'] == 'Bi-Weekly',cleaned['WAGES'] *26,cleaned['WAGES'])
        cleaned['WAGES'] = np.where(cleaned['WAGE_UNIT_OF_PAY_1'] == 'Week',cleaned['WAGES'] * 52,cleaned['WAGES'])
        return cleaned