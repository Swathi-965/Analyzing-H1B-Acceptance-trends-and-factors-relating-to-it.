def wage_feature_eng(wage):
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
