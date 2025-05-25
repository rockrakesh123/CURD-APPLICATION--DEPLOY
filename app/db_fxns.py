import psycopg2
from psycopg2 import sql

from dotenv import load_dotenv, dotenv_values
import os
# Load environment variables from .env
load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS blogtable (
            author TEXT,
            title TEXT,
            article TEXT,
            postdate DATE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_data(author, title, article, postdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO blogtable (author, title, article, postdate) VALUES (%s, %s, %s, %s)', 
                (author, title, article, postdate))
    conn.commit()
    cur.close()
    conn.close()

def view_all_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blogtable')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def view_all_titles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT title FROM blogtable')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_single_blog(title):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blogtable WHERE title = %s', (title,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_blog_by_title(title):
    return get_single_blog(title)

def get_blog_by_author(author):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blogtable WHERE author = %s', (author,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_blog_by_msg(article):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blogtable WHERE article ILIKE %s", (f"%{article}%",))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def edit_blog_author(author, new_author):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE blogtable SET author = %s WHERE author = %s', (new_author, author))
    conn.commit()
    cur.close()
    conn.close()

def edit_blog_title(title, new_title):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE blogtable SET title = %s WHERE title = %s', (new_title, title))
    conn.commit()
    cur.close()
    conn.close()

def edit_blog_article(article, new_article):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE blogtable SET article = %s WHERE article = %s', (new_article, article))
    conn.commit()
    cur.close()
    conn.close()

def delete_data(title):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM blogtable WHERE title = %s', (title,))
    conn.commit()
    cur.close()
    conn.close()