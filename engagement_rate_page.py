import json
import streamlit as st
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level

async def fetchUser(username):
    api = API()
    user_info = await api.user_by_login(username)
    return json.loads(user_info.json())

async def countRetweets(tweet_id):
    total_retweets = 0

    api = API()
    async for rep in api.user_tweets('1187636674269827073', limit=50):
        data = json.loads(rep.json())
        retweet_count = data.get('retweetCount', 0)
        total_retweets += retweet_count

    return total_retweets

async def countReplies(tweet_id):
    total_replies = 0
    api = API()
    async for rep in api.user_tweets('1187636674269827073', limit=50):
        data = json.loads(rep.json())
        reply_count = data.get('replyCount', 0)
        total_replies += reply_count

    return total_replies

def erPage():
    st.title("Engagement Rate Page")
    st.write("Masukkan username akun :")

    u_input = st.text_input("Username")
    if st.button("Search"):
        if u_input:
            try:
                user = asyncio.run(fetchUser(u_input))
                total_retweets = asyncio.run(countRetweets(user['id']))
                total_replies = asyncio.run(countReplies(user['id']))
                engagement_rate = round((total_retweets + total_replies) / user['followersCount'],4) * 100
                image_url = user['profileImageUrl']
                html_code = f"""
                    <div style="text-align: center;">
                        <p style="font-size: 20px; margin: 0;">Engagement Rate</p>
                        <p style="font-size: 40px; margin: 0;">{engagement_rate} %</p>
                        <img src="{image_url}" alt="Rounded Image" 
                            style="border-radius: 50%; width: 150px; height: 150px;">
                        <p style="font-size: 20px; margin: 0;">{user['followersCount']} Followers</p>
                        <p style="font-size: 20px; margin: 0;">Rata-rata interaksi Per Postingan</p>
                        <p style="font-size: 20px; margin: 0;">{user['favouritesCount']} likes</p>
                    </div>
                    """
                st.markdown(html_code, unsafe_allow_html=True)
                # st.write("Engagement Rate")
                # st.title("50%")      
                # followersCount = user['followersCount']
                # likes = user['favoritesCount']
                # retweets = user['retweetsCount']
   
                # st.write(user)
            except Exception as e:
                st.error(f"Error: {e}. Please try again later.")
        else:
            st.error("Username tidak boleh kosong.")