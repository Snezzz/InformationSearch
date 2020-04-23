from bs4 import BeautifulSoup
import re

def get_title(doc):
    try:
        return doc.find('span',{'class', 'post__title-text'}).text
    except:
        return None
    
def get_author(doc):
    try:
        return doc.find('span',{'class', 'user-info__nickname'}).text
    except:
        return None

def get_tags(doc):
    try:
        tags = doc.find('dd',{'class', 'post__tags-list'}).findAll('li')
        tags_list = list()
        for tag in tags:
            tags_list.append(tag.text)
        return tags_list  
    except:
        return None
    
def get_rating(doc):
    try:
        rating = doc.find('span',{'class', 'voting-wjt__counter'}).text
        return rating
    except:
        return None

def get_bookmarks_count(doc):
    try:
        return doc.find('span',{'class', 'bookmark__counter'}).text
    except:
        return None

def get_publication_date(doc):
    try:
        return doc.find('span',{'class', 'post__time'})['data-time_published']
    except:
        return None
    
def get_views_amount(doc):
    try:
        return doc.find('span',{'class', 'post-stats__views-count'}).text
    except:
        return None
    
def get_comments_amount(doc):
    try:
        return doc.find('span',{'class', 'post-stats__comments-count'}).text;
    except:
        return None

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', raw_html)
    return text

def get_text_data(doc):
    try:
        text = str(doc.find('div',id = 'post-content-body'))
        return cleanhtml(text)
    except:
        return None