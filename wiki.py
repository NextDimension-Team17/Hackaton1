import re

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import requests
from bs4 import BeautifulSoup
from networkx.drawing.nx_agraph import graphviz_layout


def test_load(start, end):
    count = 0
    file = open('./data/dataset.csv', 'a')
    hrefs = {None: {'title': None, 'urls': [start]}}
    
    while count < 10:
        count += 1
        new_hrefs = {}
        
        for parent_url, parent in hrefs.items():
            new_hrefs = {}
            
            for index, url in enumerate(parent['urls']):
                print('LOAD: DEEP - {} | ITER {} of {} of {}'.format(count, index, len(parent['urls']), len(hrefs)))
                r = requests.get(url, stream=True)
                print('**** CODE', r.status_code)
                
                soup = BeautifulSoup(r.content, 'html.parser')
                content = soup.findChild("div", {'id': 'content'})
                title = content.find('h1').text
                print('**** {}'.format(title))
                
                file.write('{},{},{},{} \n'.format(parent['title'], title, parent_url, url))
                
                new_hrefs[url] = {'title': title, 'urls': []}
                for tag in content.find_all():
                    if tag.text == 'Литература' or tag.text == 'Примечания':
                        break
                    
                    if (
                        tag.name != 'a'
                        or 'href' not in tag.attrs
                        or not tag.attrs['href'].startswith('/wiki/')
                        or re.search('.[png|jpg]', tag.attrs['href'])
                        or ('title' in tag.attrs and re.search(':', tag.attrs['title']))
                        or re.search('[0-3][0-9]{3}', tag.text)
                        or tag.text == 'англ.'
                    ):
                        continue
                    
                    new_hrefs[url]['urls'].append('https://ru.wikipedia.org{}'.format(tag.attrs['href']))
        
        hrefs = new_hrefs
    file.close()


def text_to_csv():
    columns = ['parent_title', 'title', 'parent_url', 'url']
    df = pd.DataFrame(data=[], columns=columns)
    for line in open('./data/dataset.csv', 'r').readlines():
        line = [i.strip() for i in line.split(',')]
        if len(line) > 4:
            continue
        s = pd.Series(line, index=columns)
        df = df.append(s, ignore_index=True)
    
    df.to_csv('./data/wiki_2.csv', index=False)


def clean_dataset():
    df = pd.read_csv('./data/wiki_3.csv')
    
    # print(len(df))
    # df.drop_duplicates(subset=['title'], inplace=True)
    # print(len(df))
    #
    # df.to_csv('./data/wiki_3.csv', index=False)
    
    G = nx.from_pandas_edgelist(df, 'parent_title', 'title')
    print(nx.is_tree(G))
    
    pos = graphviz_layout(G, prog="twopi", args="")
    nx.draw(G, pos, with_labels=True, node_size=0.05, font_size=0.001, width=0.01, edge_color='#AAAAAA')
    plt.savefig('./data/wiki_tree_1.png', dpi=3000)
    
    # nx.draw(G, with_labels=True, node_size=0.1, font_size=0.001, width=0.01, edge_color='#AAAAAA')
    # plt.savefig('./data/wiki_graph_1.png', dpi=3000)
    
    plt.show()
