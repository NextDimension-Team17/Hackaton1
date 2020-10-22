import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import requests
from bs4 import BeautifulSoup
from networkx.drawing.nx_agraph import graphviz_layout


def test_load(start, end):
    count = 0
    hrefs = {None: [start]}
    file = open('./data/dataset.txt', 'a')
    
    while count < 10:
        count += 1
        new_hrefs = {}
        
        for key, urls in hrefs.items():
            new_hrefs = {}
            
            for url in urls:
                new_hrefs[url] = []
                
                print('LOAD URL', count, url)
                r = requests.get(url, stream=True)
                print('**** CODE', r.status_code)
                
                soup = BeautifulSoup(r.content, 'html.parser')
                content = soup.findChild("div", {'id': 'content'})
                title = content.find('h1').text
                print('**** {}'.format(title))
                
                file.write('{} *** {} *** {} \n'.format(title, key, url))
                
                for tag in content.find_all():
                    if tag.text == 'Литература' or tag.text == 'Примечания':
                        break
                    
                    if (
                        tag.name != 'a'
                        or 'href' not in tag.attrs
                        or not tag.attrs['href'].startswith('/wiki/')
                        or ('title' in tag.attrs and tag.attrs['title'].startswith('Википедия:'))
                        or tag.text == 'англ.'
                    ):
                        continue
                    
                    new_hrefs[url].append('https://ru.wikipedia.org{}'.format(tag.attrs['href']))
        hrefs = new_hrefs
    print(file)
    file.close()


def text_to_csv():
    columns = ['title', 'parent', 'url']
    df = pd.DataFrame(data=[], columns=columns)
    for line in open('./data/dataset.txt', 'r').readlines():
        s = pd.Series([i.strip() for i in line.split('***')], index=columns)
        df = df.append(s, ignore_index=True)
    
    df.to_csv('./data/wiki.csv', index=False)


def add_parent_title():
    df = pd.read_csv('./data/wiki.csv')
    res = [None]
    prev_url = None
    
    for index, url in enumerate(df['parent']):
        print(index)
        if url == 'None':
            continue
        
        if prev_url == url:
            res.append(res[-1])
        else:
            r = requests.get(url, stream=True)
            soup = BeautifulSoup(r.content, 'html.parser')
            content = soup.findChild("div", {'id': 'content'})
            title = content.find('h1').text
            res.append(title)
            prev_url = url
            print(title)
    
    df['parent_title'] = res
    df.to_csv('./data/wiki.csv', index=False)


def print_graph():
    df = pd.read_csv('./data/wiki.csv')
    df.loc[(df['title'] == 'Арифметика'), 'title'] = 'Арифметика !!!!!!!!!!!!!!!!!'
    df.loc[(df['parent_title'] == 'Арифметика'), 'parent_title'] = 'Арифметика !!!!!!!!!!!!!!!!!'
    
    G = nx.from_pandas_edgelist(df, 'parent_title', 'title')
    
    print(nx.is_arborescence(G))
    
    nx.draw(G, with_labels=True, node_size=0.5, font_size=0.1, width=0.05, edge_color='#AAAAAA')
    # plt.figure(3, figsize=(100, 100))
    plt.savefig('./data/filename.png', dpi=1200)
    plt.show(dpi=1200)


def clean_dataset():
    df = pd.read_csv('./data/wiki.csv')
    
    print(len(df))
    df = df.drop_duplicates(subset=['title'])
    
    num_rows = df.loc[(df['title'].str.match(r'[0-3][0-9]{3}')) | df['parent_title'].str.match(r'[0-3][0-9]{3}')
                      | (df['title'].str.match('Файл:')) | (df['parent_title'].str.match('Файл:'))]
    df = df.drop(num_rows.index)
    print(len(df))

    df.to_csv('./data/wiki.csv', index=False)
    
    G = nx.from_pandas_edgelist(df, 'parent_title', 'title')
    
    pos = graphviz_layout(G, prog="twopi", args="")
    # plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, node_size=0.1, font_size=0.001, width=0.01, edge_color='#AAAAAA')
    plt.savefig('./data/wiki_tree.png', dpi=2000)
    plt.show()
