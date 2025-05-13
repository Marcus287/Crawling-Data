import requests 
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect("quotes.db") #Where is this store and what database?
cursor = conn.cursor() # what is this

#Craw data
def crawl_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for article in soup.select('.card'):
        title_tag = article.select_one('.card-title')
        link_tag = article.select_one('a')

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = "https://realpython.com" +link_tag['href']
            articles.append((title,link))

    return articles

def save_to_db(data):
    conn = sqlite3.connect("articles.db")
    db_cursor = conn.cursor()

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS articles(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      url TEXT)
                      ''')
    
    db_cursor.executemany('INSERT INTO articles (title, url) VALUES (?,?)',data)
    conn.commit()
    conn.close()

#Query the database
def query_articles():
    conn = sqlite3.connect("articles.db")
    db_cursor = conn.cursor()

    db_cursor.execute('SELECT * FROM articles')
    rows = db_cursor.fetchall()

    for row in rows:
        print(f"[{row[0]}] {row[1]}\n{row[2]}\n")
    conn.close()

if __name__ == "__main__":
    url = "https://realpython.com/"
    articles = crawl_articles(url)
    save_to_db(articles)
    query_articles()

