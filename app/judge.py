import pandas as pd
import os

def read(io):
    file = pd.read_excel(io)

    return file

def classfiy():
    file_urls = {'src':os.path.dirname(os.path.abspath(__file__)) + '/static/uploads'}
    k = {}

    for file in os.listdir(file_urls['src']):
        base_file,ext = os.path.splitext(file)
        if ext == '.xls': 
            df = read(file_urls['src'] + '/' + file)           
            if df.columns[0] == '用户编号':
                k['cldh'] = df
            elif df.columns[0] == '日期':
                k['tqxs'] = df
            elif df.columns[0] =='所属台区':
                k['sstq'] = df
            elif df.columns[7] == '三相电流平均值':
                k['sxdl'] = df
            elif df.columns[7] == '三相电压平均值':
                k['sxdy'] = df

        elif ext =='.xlsx':
            df = read(file_urls['src'] + '/' + file)
            if df.columns[0] == '用户编号':
                k['yxzl'] = df
            elif df.columns[0] == '用户名称':
                k['tqdl'] = df

    return k
