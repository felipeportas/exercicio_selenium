#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Desafio: 
# 
# Automação de atualização de preços a partir dos valores de cotação.

# In[26]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#abrir o navegador
navegador = webdriver.Chrome()
navegador.get("https://www.google.com.br/")

#localizar o campo de busca na página (vale para qualquer elemento do site - inspecionar e copiar o xpath)
#Cotação dolar

navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dolar")

navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

#Obter/extrair as informações da página
cotacao_dolar = navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print("Cotação dolar hoje:", cotacao_dolar)

#Cotação euro
navegador.get("https://www.google.com.br/")
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")

navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_euro = navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print("Cotação euro hoje:", cotacao_euro)

#Cotação ouro
navegador.get("https://www.melhorcambio.com/ouro-hoje")

cotacao_ouro = navegador.find_element_by_xpath('//*[@id="comercial"]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(",", ".")
print("cotação ouro hoje:", cotacao_ouro)

#Fechando o navegador
navegador.quit()


# ### tualizar a base de preços com as novas cotações

# - Importando a base de dados

# In[27]:


#Importar a lista de produtos

import pandas as pd

tabela = pd.read_excel("Produtos.xlsx")
display(tabela)


# - Atualizar a cotação
# - Atualizando o preço Base Reais (preço base original * cotação)
# - Atualizar o Preço Final (preço base reais * margem)

# In[28]:


#atualizar a cotação
#localização da cotação dolar - linhas onde a coluna Moeda é Dólar e coluna Cotação

tabela.loc[tabela["Moeda"] == "Dólar" ,"Cotação"] = float(cotacao_dolar)

#o mesmo para as outras cotações
tabela.loc[tabela["Moeda"] == "Euro" ,"Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro" ,"Cotação"] = float(cotacao_ouro)

#atualizar preço base reais

tabela["Preço Base Reais"] = tabela["Preço Base Original"] * tabela["Cotação"]

#atualziar preço final

tabela["Preço Final"] = tabela["Preço Base Reais"] * tabela["Margem"]

display(tabela)


# ### Exportar a nova base de preços atualizada

# In[29]:


tabela.to_excel("Produtos Novos.xlsx", index=False)

