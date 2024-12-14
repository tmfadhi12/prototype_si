import json
import streamlit as st
import os
import pandas as pd
TOPIC_DIR = "topics"
from sentimentSection import sentimentSection

def topicDetailPage():
    # Retrieve the selected topic from session state
        selected_topic = st.session_state.selected_topic
        
        if selected_topic:
            st.title(f"Detail for Topic: {selected_topic}")

            topic_folder_path = os.path.join(TOPIC_DIR, selected_topic)
            topic_files = os.listdir(topic_folder_path)
            final_json_path = os.path.join(topic_folder_path, 'tweets_final.json')
            st_path = os.path.join(topic_folder_path, 'selected_template.txt')
            
            with open(st_path, 'r') as file:
                selected_template = file.read().strip()
            st.subheader(f"Template: {selected_template}")
            
            st.subheader("Potential Impression")

            if 'tweets_final.json' in topic_files:
                try:
                    with open(final_json_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    df = pd.DataFrame(data)
                    df['Date'] = pd.to_datetime(df['date'])  
                    df['userFollowersCount'] = df['user'].apply(lambda x: x['followersCount'])
                    df['Day'] = df['Date'].dt.day  
                    result = df.groupby('Day')['userFollowersCount'].sum().reset_index()
                    result.columns = ['Day', 'Y']

                    st.write("Aggregated Potential Impression by Day")
                    st.line_chart(result.set_index('Day'))

                except Exception as e:
                    st.error(f"Error reading `tweets_final.json`: {e}")
            else:
                st.write("`tweets_final.json` not found in the selected topic folder.")
           
            st.subheader("Sentiment")    
            sentimentSection()
            
            # if topic_files:
            #     st.write("Files in this topic:")
            #     for file in topic_files:
            #         st.write(f"- {file}")
            # else:
            #     st.write("No files found in this topic.")
            
            if st.button("Back to Topic List"):  
                del st.session_state.selected_topic  
                st.rerun()
        else:
            st.write("No topic selected.")