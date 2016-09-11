#-*-coding:utf-8-*-

import pandas as pd
import os

all_stock=[]

def get_all_stock(path):
    for dirpath, dirnames, filenames in os.walk(path):
        if filenames :
            for f in  filenames:
                all_stock.append(f)

    return all_stock
