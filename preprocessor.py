import re
import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s'
    date = re.findall(pattern,data)[1:]
    messages = re.split(pattern,data)[2:]

    clean_am = []
    for i in messages:
        i = i.replace('am','')
        clean_am.append(i)

    clean_pm = []
    for i in clean_am:
        i = i.replace('pm','')
        clean_pm.append(i)

    


    df = pd.DataFrame({'messages':clean_pm , 'date':date})
    df['date']  = pd.to_datetime(df['date'])

    users = []
    messages = []
    for message in df['messages']:
        entry = re.split('-([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['messgaes'] = messages
    df['users'] = users

    df['year'] = df['date'].dt.year

    df['month'] = df['date'].dt.month_name()

    df['month_num'] = df['date'].dt.month

    df['day'] = df['date'].dt.day

    df['hour'] = df['date'].dt.hour

    df['minutes'] = df['date'].dt.minute

    df['day_name']= df['date'].dt.day_name()


    new_user = []
    for i in df['users']:
        i = i.replace(' ','')
        new_user.append(i)
    
    df['new_user'] = new_user


    return df



