import random
from datetime import datetime
import datetime

import matplotlib.pyplot as plt
import numpy as np

import excel

values = excel.get_values()

date_list = []
nums_list = []

def get_year(t_date):
    temp = ""
    n = 11
    for i in range(len(t_date) - n):
        temp = temp + t_date[i]
    year = ""
    for i in range(4,0,-1):
        year += temp[-i]
    return(year)

date_format = "%B %-d, %Y at %I:%M%p"
new_date = "06/May/2021 09:16:21"
ndate_format = "%d/%B/%Y %H:%M:%S"

def change_dformat(new_date):
    ndate_format = "%d/%B/%Y %H:%M:%S"
    date = datetime.datetime.strptime(new_date, ndate_format)
    return(date.strftime("%B %d, %Y at %I:%M%p"))

print(get_ogdate(new_date))