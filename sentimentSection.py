import json
import os
import pandas as pd
from transformers import pipeline
import streamlit as st

TOPIC_DIR = "topics"

def sentimentSection():
    selected_topic = st.session_state.selected_topic
    pretrained_name = "w11wo/indonesian-roberta-base-sentiment-classifier"

    nlp = pipeline(
        "sentiment-analysis",
        model=pretrained_name,
        tokenizer=pretrained_name,
        framework="pt"
    )

    topic_folder_path = os.path.join(TOPIC_DIR, selected_topic)
    final_json_path = os.path.join(topic_folder_path, 'tweets_final.json')

    with open(final_json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['date']).dt.date  # Remove day details and keep only the date
    df['userFollowersCount'] = df['user'].apply(lambda x: x['followersCount'])
    texts = df['rawContent'].tolist()

    # Perform sentiment analysis
    results = nlp(texts, batch_size=16)
    df['Sentiment'] = [result["label"] for result in results]

    # Aggregate sentiment counts by date
    sentiment_by_date = df.groupby(['Date', 'Sentiment']).size().reset_index(name='Count')
    sentiment_pivot = sentiment_by_date.pivot(index='Date', columns='Sentiment', values='Count').fillna(0)

    # Ensure all sentiment columns exist
    for sentiment in ['positive', 'neutral', 'negative']:
        if sentiment not in sentiment_pivot.columns:
            sentiment_pivot[sentiment] = 0

    # Display sentiment counts as text
    total_positive = sentiment_pivot['positive'].sum()
    total_neutral = sentiment_pivot['neutral'].sum()
    total_negative = sentiment_pivot['negative'].sum()

    st.write(f"Total Sentimen Positif: {total_positive}")
    st.write(f"Total Sentimen Netral: {total_neutral}")
    st.write(f"Total Sentimen Negatif: {total_negative}")

    # Plot separate charts for each sentiment
    st.write("### Positive Sentiment Trend")
    st.line_chart(sentiment_pivot[['positive']])

    st.write("### Neutral Sentiment Trend")
    st.line_chart(sentiment_pivot[['neutral']])

    st.write("### Negative Sentiment Trend")
    st.line_chart(sentiment_pivot[['negative']])

