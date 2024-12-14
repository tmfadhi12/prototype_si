import streamlit as st
import os
from tweets import searchTweets
import asyncio
from topic_detail_page import topicDetailPage
import shutil
from engagement_rate_page import erPage

TOPIC_DIR = "topics"

if not os.path.exists(TOPIC_DIR):
    os.makedirs(TOPIC_DIR)

def home_page():
    def listening_page():
        st.title("Listening Page")

        button_tambah = st.button("Tambah Topik")

        if button_tambah:
            st.session_state.tambah_topik = ("Tambah Topik")
            st.rerun()
        
        st.write("List Topik:")
        topic_folders = os.listdir(TOPIC_DIR)

        if topic_folders:
            for folder in topic_folders:
                if os.path.isdir(os.path.join(TOPIC_DIR, folder)): 
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        if st.button(folder):
                            st.session_state.selected_topic = folder
                            st.rerun()
                    
                    with col2:
                        delete_button = st.button("Delete", key=f"delete_{folder}", type="primary")
                        if delete_button:
                            # Delete the folder
                            folder_path = os.path.join(TOPIC_DIR, folder)
                            try:
                                shutil.rmtree(folder_path)
                                st.rerun()
                                st.success(f"Topik '{folder}' berhasil dihapus!")
                            except Exception as e:
                                st.error(f"Gagal menghapus topik '{folder}': {e}")
        else:
            st.write("Belum ada topik yang dibuat.")
    
    def tambah_page():
        st.title("Tambah Topik")

        st.write("Pilih template")

        if st.button("Politikus"):
            st.session_state.selected_template = "Politikus"
            del st.session_state.tambah_topik
            st.rerun()

        if st.button("Partai Politik"):
           st.session_state.selected_template = "Partai Politik"
           del st.session_state.tambah_topik
           st.rerun()

        if st.button("Isu"):
            st.session_state.selected_template = "Isu"
            del st.session_state.tambah_topik
            st.rerun()

        # st.write("atau")
        # topic_name = st.text_input("Masukkan nama topik")
        
        if st.button("Back to Topic List", type="primary"):  
            del st.session_state.tambah_topik
            st.rerun()

    def form_page():
        selected_template = st.session_state.selected_template
        st.title("Tambah Topik")
        judul = st.text_input("Judul Topik")
        keyword = st.text_input("Keyword", value=selected_template) 

        button_tambah = st.button("Simpan Topik")

        if button_tambah:
            if judul:
                topic_folder_path = os.path.join(TOPIC_DIR, judul)
                sl_path = os.path.join(topic_folder_path, 'selected_template.txt')

                if not os.path.exists(topic_folder_path):
                    progress_bar = st.progress(0)

                    try:
                        os.makedirs(topic_folder_path)
                        progress_bar.progress(10)

                        with open(sl_path, 'w') as file:
                            file.write(selected_template)
                        progress_bar.progress(15)

                        st.write("Fetching tweets...")
                        asyncio.run(searchTweets(keyword, topic_folder_path))
                        progress_bar.progress(100)

                        st.success(f"Topik '{judul}' berhasil dibuat! Silahkan kembali ke halaman Listening.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        shutil.rmtree(topic_folder_path)
                    finally:
                        progress_bar.empty() 

                    if st.button("Back to Listening Page", type="primary"):  
                        st.session_state.current_page = "listening"
                        st.rerun()
                else:
                    st.error(f"Topik '{judul}' sudah ada.")


        if st.button("Back to Template List", type="primary"):  
            del st.session_state.selected_template
            st.session_state.tambah_topik = ("Tambah Topik")
            st.rerun()
    
    def topic_detail_page():
        topicDetailPage()

    def er_page():
        erPage()

    def popular_issue_page():
        st.title("Contact Page")
        st.write("This is the Contact page. Reach out to us at contact@example.com.")

    page = st.sidebar.radio("Select a page", ["Listening", "Engagement Rate"])

    if page == "Listening":
        if 'selected_topic' in st.session_state:
            topic_detail_page()
        elif 'tambah_topik' in st.session_state:
            tambah_page()
        elif 'selected_template' in st.session_state:
            form_page()
        else:
            listening_page()
    elif page == "Engagement Rate":
        er_page()
