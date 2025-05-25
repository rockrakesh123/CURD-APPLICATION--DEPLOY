
import streamlit as st
import psycopg2
import pandas as pd

# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
import os
# loading variables from .env file
load_dotenv() 

# Database connection parameters
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
c = conn.cursor()

def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS blogtable(
            author TEXT,
            title TEXT,
            article TEXT,
            postdate DATE
        )
    ''')
    conn.commit()

def add_data(author, title, article, postdate):
    c.execute('''
        INSERT INTO blogtable(author, title, article, postdate)
        VALUES (%s, %s, %s, %s)
    ''', (author, title, article, postdate))
    conn.commit()

def view_all_notes():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data

def view_all_titles():
    c.execute('SELECT DISTINCT title FROM blogtable')
    data = c.fetchall()
    return data

def get_blog_by_title(title):
    c.execute('SELECT * FROM blogtable WHERE title=%s', (title,))
    data = c.fetchall()
    return data

def get_blog_by_author(author):
    c.execute('SELECT * FROM blogtable WHERE author=%s', (author,))
    data = c.fetchall()
    return data

def delete_data(title):
    c.execute('DELETE FROM blogtable WHERE title=%s', (title,))
    conn.commit()

def readingTime(mytext):
    total_words = len(mytext.split(" "))
    estimatedTime = total_words / 200.0
    return estimatedTime

def main():
    """A Simple CRUD Blog App"""
    html_temp = """
        <div style="background-color:{};padding:10px;border-radius:10px">
        <h1 style="color:{};text-align:center;">St Blog </h1>
        </div>
    """
    st.markdown(html_temp.format('royalblue', 'white'), unsafe_allow_html=True)

    menu = ["Home", "View Post", "Add Post", "Search", "Manage Blog"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        result = view_all_notes()
        for i in result:
            short_article = str(i[2])[0:50]
            st.write(f"<div style='background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;'>"
                     f"<h4 style='color:white;text-align:center;'>{i[1]}</h4>"
                     f"<img src='https://www.w3schools.com/howto/img_avatar.png' alt='Avatar' style='vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;'>"
                     f"<h6>Author:{i[0]}</h6><br/><br/><p style='text-align:justify'>{short_article}</p></div>",
                     unsafe_allow_html=True)

    elif choice == "Add Post":
        st.subheader("Add Your Article")
        create_table()
        blog_title = st.text_input('Enter Notes Title')
        blog_author = st.text_input("Enter Author Name", max_chars=50)
        blog_article = st.text_area("Enter Your Message", height=200)
        blog_post_date = st.date_input("Post Date")
        if st.button("Add"):
            add_data(blog_author, blog_title, blog_article, blog_post_date)
            st.success(f"Post::'{blog_title}' Saved")

    elif choice == "Search":
        st.subheader("Search Articles")
        search_term = st.text_input("Enter Term")
        search_choice = st.radio("Field to Search", ("title", "author"))
        if st.button('Search'):
            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice == "author":
                article_result = get_blog_by_author(search_term)

            for i in article_result:
                st.text(f"Reading Time:{readingTime(str(i[2]))} minutes")
                st.write(f"<div style='background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;'>"
                         f"<h4 style='color:white;text-align:center;'>{i[1]}</h4>"
                         f"<img src='https://www.w3schools.com/howto/img_avatar.png' alt='Avatar' style='vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;'>"
                         f"<h6>Author:{i[0]}</h6><h6>Post Date: {i[3]}</h6></div>",
                         unsafe_allow_html=True)
                st.write(f"<div style='background-color:silver;padding:10px;border-radius:5px;margin:10px;'>"
                         f"<p style='text-align:justify;color:black;padding:10px'>{i[2]}</p></div>",
                         unsafe_allow_html=True)

    elif choice == "Manage Blog":
        st.subheader("Manage Blog")
        result = view_all_notes()
        clean_db = pd.DataFrame(result, columns=["Author", "Title", "Article", "Date"])
        st.dataframe(clean_db)
        unique_list = [i[0] for i in view_all_titles()]
        delete_by_title = st.selectbox("Select Title", unique_list)
        if st.button("Delete"):
            delete_data(delete_by_title)
            st.warning(f"Deleted: '{delete_by_title}'")

if __name__ == '__main__':
    main()
