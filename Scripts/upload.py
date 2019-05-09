from bs4 import BeautifulSoup
import pandas as pd
from calendar import monthrange
import pysolr

def read_file(path):
    file_doc = open(path,'r', encoding="windows-1252", errors='ignore')
    text = file_doc.read()
    file_doc.close()
    return text


def get_all_tags(file_docs, except_tegs=None):
    soup = BeautifulSoup(file_docs, 'html.parser')
    all_tags_set = set([tag.name for tag in soup.find_all()])
    all_tags = list(all_tags_set)
    if except_tegs:
        for teg in except_tegs: 
            all_tags.remove(teg)
    return all_tags


def transform_df(file_docs, all_tags):
    soup = BeautifulSoup(file_docs, 'html.parser')
    dict_teste = {}
    for tag in all_tags:
        dict_teste[tag] = [doc.text for doc in soup.find_all(tag)]
    return pd.DataFrame(dict_teste)


def connect_solr(host, collection, port=8983):
    path = 'http://{}:{}/solr/{}'.format(host, port, collection)
    return pysolr.Solr(path)


def dict_docs(docs_dataframe):
    all_docs = []
    for index in range(0, len(docs_dataframe)):
        doc = docs_dataframe.ix[index]
        all_docs.append(doc)
    return all_docs

def add_solr(solr_client, all_docs_list):
    solr_client.add(all_docs_list)
    solr_client.commit()


# Carrega os dados.

solr_client = connect_solr('localhost', 'noticias')
#pegando do ano de 94 e 95
years = [94, 95]
for year in years:
    print("INSERINDO ANO {}".format(year))
    for month in range(1, 13):
        print("INSERINDO MES {}".format(month))
        year_complete = year + 1900 
        days = monthrange(year_complete, month)[1]
        
        list_docs = []
        for day in range(1, days+1):
            # print("INSERINDO DIA {}".format(day))
            
            #pega o caminho do arquivo
            path = "colecao_teste/FSP.{:02d}{:02d}{:02d}.sgml".format(year,month, day)
                        
            #lendo o documento
            file_text = read_file(path)
            all_tags = get_all_tags(file_text, except_tegs=['doc','docno'])
            docs_dataframe = transform_df(file_text, all_tags)
            docs_dataframe = docs_dataframe.rename(columns={'docid':'id'})
            
            list_docs +=  dict_docs(docs_dataframe)
        #conectando e adicionando ao solr
        add_solr(solr_client, list_docs)