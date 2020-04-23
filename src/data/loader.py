import multiprocessing
import requests
import numpy as np
import os.path
import time
from bs4 import BeautifulSoup

def download_document(post_id):
    PATH_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/external"
    
    req = ''
    while req == '':
        try:
            req = requests.get('https://habrahabr.ru/post/' +str(post_id) + '/')
        except:
            print(post_id)
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(2)
            print("Was a nice sleep, now let me continue...")
            continue;

    soup = BeautifulSoup(req.text, 'lxml') 
    doc = {}
    data = soup.find('div',{'class':'post__text'}) 
    if not soup.find("span", {"class": "post__title-text"}):
        return None;
    else:
        article = soup.find('article',{'class':'post_full'})
        metadata = soup.find('ul',{'class':'post-stats post-stats_post js-user_'})
        file_path = PATH_FILE + "\habr{}.html".format(post_id);
        if(os.path.exists(file_path)):
            return None;
        file = open(file_path,"w",encoding='utf-8');
        file.write(str(article));
        file.write(str(metadata));
        file.close();

if __name__ == '__main__':
    num_processor = 7
    with multiprocessing.Pool(num_processor) as p:
        docs = p.map(download_document, np.arange(200000))
