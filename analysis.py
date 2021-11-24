from urlextract import URLExtract
extract = URLExtract()
import emoji
import pandas as pd
from collections import Counter

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['new_user'] == selected_user]

    num_msgs = df.shape[0]

    words = []
    for message in df['messages']:
        words.extend(message.split())
        

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    
    return num_msgs,len(words),len(links)

def most_busy_users(df):
    x = df['new_user'].value_counts().head()
    df = df['new_user'].value_counts() .head()
    return x,df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['new_user'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['new_user'] == selected_user]

    df['only_date'] = df['date'].dt.date

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    
    return daily_timeline

def most_busy_day(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['new_user'] == selected_user]

    return df['day_name'].value_counts()

def most_busy_month(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['new_user'] == selected_user]

    return df['month'].value_counts()

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['new_user'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
