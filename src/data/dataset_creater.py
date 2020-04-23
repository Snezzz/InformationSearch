import requests
import numpy as np
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2
import os
from tqdm import tqdm
import codecs
import re
import multiprocessing
import os.path
import time
import pandas as pd
import parsing_api as pa
            
            
def load_data():
    columns = (['FileName', 'Title', 'Author', 'Date', 'Rating','BookmarksAmount',
                'Tags', 'ViewsAmount', 'CommentsAmount','Text'])
    data = []
    PATH_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/external"
    
    fds = sorted(os.listdir(PATH_FILE))
    i = 1
    for file in fds:
        print(i)
        array = []
        
        file_name = file.split(".")[0]
        file_data = open(PATH_FILE+'/{}'.format(file),"r",encoding='utf-8');

        document = BeautifulSoup(file_data.read(),"lxml")
        if(document.find("pre")!=None):
            document.find("pre").contents[0] = ''
            for el in document.findAll("pre"):
                el.contents[0] = ""
            for el in document.findAll("code"):
                el.contents[0] = ""

        array = ([file_name, pa.get_title(document), pa.get_author(document), pa.get_publication_date(document), pa.get_rating(document), 
                      pa.get_bookmarks_count(document),
                      pa.get_tags(document),
                      pa.get_views_amount(document), 
                      pa.get_comments_amount(document),
                      pa.get_text_data(document)
                     ])
        data.append(dict(zip(columns, array)))
        i+=1
    return data


def clear_data(data):
    data = re.sub(r'(http|https)\S+',
                  '', data)
    data = re.sub(r'(http|https)\S+',
                  '', data)
    data = re.sub(r'(([a-zA-Z]*\.)*[a-zA-Z]*(\.com|\.io|\.ru|\.ua|\.en|\.gov|\.org|\.uk|\.us|.\/edu|\.net)\S+)','',data)
    data = re.sub(r'(([a-zA-Z]*\.)*[a-zA-Z]*(\.com|\.io|\.ru|\.ua|\.en|\.gov|\.org|\.uk|\.us|.\/edu|\.net))','',data)
    data.replace("\n","")
    data.replace("\r","")
    data = re.sub(r',', '', data)
    data = re.sub(r'–|—|←|↑|→|↓|↔|↕|⇆|⇅', '', data)
    data = re.sub(r'\.', '', data)
    data = re.sub(r'\:', '', data)
    data = re.sub(r'\;', '', data)
    data = re.sub(r'\?', '', data)
    data = re.sub(r'\!', '', data)
    data = re.sub(r'\…', '', data)
    data = re.sub(r'[0-9]+', '', data)
    data = re.sub(r'\"|«|»|“|”', '', data)
    data = re.sub(r'\/|\\', '', data)
    data = re.sub(r'\(@[a-z]*\)', '', data)
    data = re.sub(r'\(|\)','',data)
    data = re.sub(r'Q|UPD','',data)
    data = re.sub(r'\s\n',' ',data)
    data = re.sub(r'[\s]{2,}',' ',data)
    data = re.sub(r'\n|\r',' ',data)
    data = data.lower()
    return data

def set_stop_words(stopWordsList, words):
    for word in words:
        stopWordsList.add(word)

def filter_data(data):
    filtered_data = []
    for w in data:
        if w not in stopWords:
            filtered_data.append(w)
    return filtered_data

def write_data(filtered_data,data,words,final_data):
    data['Text'] = words;
    PATH_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/processed/"    
   #print(len(filtered_data))
    if(len(filtered_data) > 2000):
        final_data.append(data)
        file = open(PATH_FILE + "\{}.txt".format(data['FileName']),"w",encoding='utf-8');
        file.write(filtered_data);
        file.close();
        
def create_final_collection(filtered_data):
    
    df = pd.DataFrame(filtered_data)
    df.to_csv("results.csv")

    PATH_FILE = 'filtered-data'
    for data in filtered_data:
        if(len(data) > 2000):
            file = open(PATH_FILE + "\habr{}.txt".format(data['Href']),"w",encoding='utf-8');
            file.write(str(data));
            file.close();

if __name__ == "__main__":
    dataSet = load_data()
    print("Загрузка данных завершена")
    final_data = []
    morph = pymorphy2.MorphAnalyzer()
    
    for document in dataSet:
        new_data = clear_data(document['Text'])
        results = [morph.parse(word)[0].normal_form for word in new_data.split(' ')] 
        results = [x for x in results if len(x)>1] 
       
        stopWords = set(stopwords.words('russian'))
        new_stop_words = ["это","лишь","наш","ваш","ещё","уже","как","чтобы","а","но","если","что","нибудь","ваш","когда",
                  "где","зачем","почему","иначе","поэтому","потому","разве","при","после"]
        set_stop_words(stopWords,new_stop_words) 
        filtered_data = filter_data(results)
        
        stopWords = set(stopwords.words('english'))
        filtered_data = filter_data(filtered_data)
        filtered_text = ' '.join(filtered_data)
        
        write_data(filtered_text,document,filtered_data,final_data)
    df = pd.DataFrame(final_data)
    df.head()
    df.to_csv(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/processed/results.csv")