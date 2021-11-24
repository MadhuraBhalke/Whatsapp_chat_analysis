import streamlit as st 
import preprocessor
import matplotlib.pyplot as plt

import analysis

st.sidebar.title('WhatsApp Chat Analyzer !')

data_file = st.sidebar.file_uploader("Choose a File")
		
if data_file is not None:
     byte_data = data_file.getvalue()
     data = byte_data.decode('utf-8')
     df = preprocessor.preprocess(data)

     user_list =df['new_user'].unique().tolist()
     user_list.sort()
     user_list.insert(0,'Overall')
     user_list.insert(1,'group notification')
     selected_user = st.sidebar.selectbox('Show Analysis With : ',user_list)

     if st.sidebar.button('Show Analysis'):
          num_msgs, words, num_links = analysis.fetch_stats(selected_user,df)

          col1, col2, col3, col4 = st.columns(4)

          with col1:
               st.header("Total Messages")
               st.title(num_msgs)
          with col2:
               st.header("Total Words")
               st.title(words)
          with col3:
               st.header("Links Shared")
               st.title(num_links)

          if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = analysis.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
               ax.bar(x.index, x.values,color='red')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


          st.title("Monthly Timeline")
          timeline = analysis.monthly_timeline(selected_user,df)
          fig,ax = plt.subplots()
          ax.plot(timeline['time'], timeline['messages'],color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)
          

          st.title("Daily Timeline")
          daily_timeline = analysis.daily_timeline(selected_user, df)
          fig,ax = plt.subplots()
          ax.plot(daily_timeline['only_date'], daily_timeline['messages'],color='blue')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          col1, col2  = st.columns(2)

          with col1 :
               st.header("Most busy day")
               busy_day = analysis.most_busy_day(selected_user,df)
               fig, ax = plt.subplots()
               ax.bar(busy_day.index, busy_day.values,color='orange')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

          with col2:
               st.header("Most busy month")
               busy_month = analysis.most_busy_month(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values,color='orange')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

          emoji_df = analysis.emoji_helper(selected_user,df)
          st.title("Emoji Analysis")

          col1,col2 = st.columns(2)

          with col1:
               st.dataframe(emoji_df)
          with col2:
               fig,ax = plt.subplots()
               ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
               st.pyplot(fig)
