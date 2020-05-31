# -*- coding: utf-8 -*-
"""
Created on Fri May 29 23:24:16 2020

@author: diego
"""
#import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
import os
import pandas as pd
from tqdm import tqdm
import uuid
#import requests

#%% 
options = Options()
options.add_argument('--headless')
options.add_argument("--incognito")

#driver = webdriver.Chrome(executable_path="chromedriver")  # Optional argument, if not specified will search path.


#%% 
archive_name = "g1_news.csv"

try:
    News_Pandas = pd.read_csv( archive_name, index_col = False)
    print("Cargando archivo: {archivo}".format(archivo = archive_name))
except:
    new_news = {'ID':[], 'regioes':[],'cidade':[], 'hyperlink':[], 'title':[], 'subtitle':[], 'date':[]}
    News_Pandas = pd.DataFrame(new_news)
    print("Nuevo Archivo")

#%% 

links = ["https://g1.globo.com/pe/petrolina-regiao/",
        "https://g1.globo.com/pe/pernambuco/",
        "https://g1.globo.com/pe/caruaru-regiao/",
        "https://g1.globo.com/df/distrito-federal/",
        "https://g1.globo.com/go/goias/",
        "https://g1.globo.com/mt/mato-grosso/",
        "https://g1.globo.com/al/alagoas/",
        "https://g1.globo.com/ms/mato-grosso-do-sul/",
        "https://g1.globo.com/ba/bahia/",
        "https://g1.globo.com/ce/ceara/",
        "https://g1.globo.com/ma/maranhao/",
        "https://g1.globo.com/pb/paraiba/",
        "https://g1.globo.com/pi/piaui/",
        "https://g1.globo.com/rn/rio-grande-do-norte/",
        "https://g1.globo.com/se/sergipe/",
        "https://g1.globo.com/ac/acre/",
        "https://g1.globo.com/pa/para/",
        "https://g1.globo.com/am/amazonas/",
        "https://g1.globo.com/ap/amapa/",
        "https://g1.globo.com/ro/rondonia/",
        "https://g1.globo.com/to/tocantins/",
        "https://g1.globo.com/es/espirito-santo/",
        "https://g1.globo.com/mg/minas-gerais/",
        "https://g1.globo.com/mg/centro-oeste/",
        "https://g1.globo.com/mg/grande-minas/",
        "https://g1.globo.com/mg/sul-de-minas/",
        "https://g1.globo.com/mg/triangulo-mineiro/",
        "https://g1.globo.com/mg/vales-mg/",
        "https://g1.globo.com/mg/zona-da-mata/",
        "https://g1.globo.com/rj/rio-de-janeiro/",
        "https://g1.globo.com/rj/norte-fluminense/",
        "https://g1.globo.com/rj/regiao-dos-lagos/",
        "https://g1.globo.com/rj/regiao-serrana/",
        "https://g1.globo.com/rj/sul-do-rio-costa-verde/",
        "https://g1.globo.com/sp/sao-carlos-regiao/",
        "https://g1.globo.com/sp/sorocaba-jundiai/",
        "https://g1.globo.com/sp/vale-do-paraiba-regiao/",
        "https://g1.globo.com/sp/sao-paulo/",
        "https://g1.globo.com/sp/bauru-marilia/",
        "https://g1.globo.com/sp/campinas-regiao/",
        "https://g1.globo.com/sp/itapetininga-regiao/",
        "https://g1.globo.com/sp/mogi-das-cruzes-suzano/",
        "https://g1.globo.com/sp/piracicaba-regiao/",
        "https://g1.globo.com/sp/presidente-prudente-regiao/",
        "https://g1.globo.com/sp/ribeirao-preto-franca/",
        "https://g1.globo.com/sp/sao-jose-do-rio-preto-aracatuba/",
        "https://g1.globo.com/sp/santos-regiao/"]

wd = webdriver.Firefox(executable_path=os.path.join(os.getcwd(),"websdrivers",'geckodriver'),options=options)
wd.set_page_load_timeout(15)

Name_archive = "g1_news.csv"
extend_link = "/index/feed/pagina-{page}.ghtml".format(page="2")
Datos_iniciales = News_Pandas.shape[0]
page_web = 350
limit_repeat_news = 10000000000

total_j = 0

for i, link in enumerate(links):
    print("Estamos en el link número {i} de {total}".format(i=i+1, total=len(links)))
    print("Estamos en el link: {link}".format(link = link))
    Regioes = link.split("/")[3]
    Cidade = link.split("/")[4]
    Repeat_count = 0
    
    
    for j in tqdm(range(130,page_web)):
        if j == 0:
            total_link = link
        else:
            total_link = link + "index/feed/pagina-{page}.ghtml".format(page=str(j))
        
        while True:
            try:
                wd.get(total_link ) 
                wd.implicitly_wait(150)
                break
            except:
                wd = webdriver.Firefox(executable_path=os.path.join(os.getcwd(),"websdrivers",'geckodriver'),options=options)
                wd.set_page_load_timeout(15)
                
        
        if total_j%30==0:
            while True:
                try:
                    wd.close()
                    wd = webdriver.Firefox(executable_path=os.path.join(os.getcwd(),"websdrivers",'geckodriver'),options=options)
                    wd.set_page_load_timeout(15)
                    wd.get( total_link ) 
                    wd.implicitly_wait(150)
                    break
                except:
                    pass
        total_j = total_j + 1
            
#       print(wd.current_url)
        soup = BeautifulSoup(wd.page_source, 'html.parser')
        soup = soup.find_all("div",attrs={"class":"bastian-feed-item","data-type":["materia", "post-playlist"] })
#        print(len(soup))
        for k in range(len(soup)):
            new_news = {}#'ID':[], 'regioes':[],'cidade':[], 'hyperlink':[], 'title':[], 'subtitle':[], 'date':[]} 
            try:
              hyperlink = soup[k].find("div").find("div").find("a")["href"]
              title = soup[k].find("div").find("div").find("a").text.replace("  "," ").replace("\n"," ")
              subtitle = soup[k].find("div").find_all("div")[5].text.replace("  "," ").replace("\n"," ")
              date = soup[k].find("div").find_all("div")[-1].find("span").text
            except:
              continue
          
            new_news['ID'] = (str(uuid.uuid4()))
            new_news['regioes'] = (Regioes)
            new_news['cidade'] = (Cidade)
            new_news['hyperlink'] = (hyperlink)
            new_news['title'] = (title)
            new_news['subtitle'] = (subtitle)
            new_news['date'] = (date)
            
            if title in News_Pandas.title.where(News_Pandas['cidade'] == Cidade).values:
                Repeat_count = Repeat_count + 1    
            else:
                News_Pandas = News_Pandas.append(new_news, ignore_index=True)
            
        if Repeat_count > limit_repeat_news:
            print("Ya se encuentran {numero} noticias repetidas en el dataframe, seguiremos al siguiente link".format(numero = str(limit_repeat_news)))
            print("Hasta la pagina {j}".format( j = str(j) ))
            break
        News_Pandas.to_csv(archive_name,index=False,encoding="utf-8-sig")
            
    News_Pandas.to_csv(archive_name,index=False,encoding="utf-8-sig")
    
    if i==3:
        break
         
Datos_finales = News_Pandas.shape[0]
Nuevos_datos = Datos_finales - Datos_iniciales
print("Hemos tomado {Nuevos_datos} datos nuevos".format(Nuevos_datos = Nuevos_datos))
News_Pandas.to_csv(archive_name,index=False,encoding="utf-8-sig")

