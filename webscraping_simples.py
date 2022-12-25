'''Objetivo principal e fazer um webscraping utilizando Python para obter dados do salário mínimo'''
# Importando bibliotecas
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
# acessando a url para coleta dos dados
req = requests.get(
    'http://www.fetapergs.org.br/index.php/2015-07-27-16-46-22/tabelas-salario-minimo')
if req.status_code == 200:
    print('requisição bem sucedida!')
    content = req.content

soup = BeautifulSoup(content, 'html.parser')
# preparando os dados para serem gravados em csv
data = []
list_header = []
header = soup.find_all("table")[0].find("tr")

for itens in header:
    try:
        list_header.append(itens.get_text())
    except:
        continue
dados_html = soup.find_all("table")[0].find_all("tr")[1:]

for elementos in dados_html:
    sub_data = []
    for sub_element in elementos:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    data.append(sub_data)
dataFrame = pd.DataFrame(data=data, columns=list_header)

dataFrame.to_csv('SalarioMinimo.csv')
# lendo o arquivo gravado em csv
df2 = pd.read_csv(
    r'\Users\rosan\Desktop\engenharia de dados\StagingArea\SalarioMinimo.csv', encoding='utf-8')
# formatando os dados para interpretação
# print(df2.columns)
df2 = df2.rename(columns={'\n\nAno\n': 'Ano'})
df2 = df2.rename(columns={'\n\nSalário Mínimo\n': 'Salario_Minimo'})
df2 = df2.rename(columns={'\n\nVigência\n': 'Vigencia'})
df2 = df2.rename(
    columns={'\nReajuste Salário\nMínimo\n': 'Reajuste_SM'})
df2 = df2.rename(
    columns={'\nTeto Máximo de Contribuição\n': 'Teto_Max_Contribuição'})
df2.drop(['Unnamed: 0', '\n', '\n.1', '\n.6', '\n.5', '\n.4',
         '\n.3', '\n.2'], axis=1, inplace=True)

df2 = (df2[['Ano', 'Salario_Minimo', 'Reajuste_SM']])
# alterando os dados de string para float
df2 = df2.dropna()
df2['Reajuste_SM'] = df2['Reajuste_SM'].str.replace('%', '')
df2['Reajuste_SM'] = df2['Reajuste_SM'].str.replace(',', '.').astype(float)
df2 = (df2[:12])
print(df2)
menor_reajuste = df2['Reajuste_SM'].min()
maior_reajuste = df2['Reajuste_SM'].max()
print(
    f"O menor reajuste foi de  {menor_reajuste} % e o maior foi {maior_reajuste} %   nos ultimos 12 anos")
