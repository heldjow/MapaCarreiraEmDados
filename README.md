
# Imersão de dados alura

Projeto construído durante a imersão em dados com python pela Alura. Nesse projeto pude recapitular e aprender a realizar um projeto de análise de dados. Desde a filtragem e tratamento dos dados até a realização de gráficos e dashboards interativos no streamlit.

## 📖 Sumário

1. [✨ Funcionalidades ](#-features)
2. [🛠️ Instalação local](#-local-installation)
3. [⚡ Como rodar na sua máquina](#-usage)


## **✨ Funcionalidades**

- **🐼 Exploração dos dados com a biblioteca pandas**: importação dos dados, estatisticas das variaveis quantitativas e qualitativas, tradução dos termos e destrinchamento das siglas.
- **🧹 Tratamento e limpeza dos dados**: conversão de variaveis, limpeza de dados nulos.
- **🔍 Dashboards interativos**: análise exploratória, insights e apresentação interativa das informações.

## **🛠️ Instalação local**

1. Toda exploração, tratamento e limpeza dos dados foi feita no google collab, pois é de fácil acesso e não gasta processamento nem memória da minha máquina, além de grande parte das bibliotecas virem instaladas por default. [Google Collab](https://colab.research.google.com/drive/1hRJZqk24GtUbjsYjKeIPOXWUdySHEOt5?usp=sharing).
2. Dashboards interativos feitos no streamlit, mais informações na próxima sessão.

## **⚡ Como rodar na sua máquina**

1. Crie o ambiente virtual

python3 -m venv venv

2. Ative o ambiente virtual em Windonws

.venv\Scripts\Activate

Em Linux/MacOS

source .venv/bin/activate

3. Criar um arquivo chamado requirements.txt

pandas==2.2.3
streamlit==1.44.1
plotly==5.24.1

4. Instale as bibliotecas nescessárias

pip -install -r requirements

5. Rode o código no ambiente virtual

streamlit run app.py

6. Realize o deploy na nuvem 

Acesse o site do streamlit e associe a sua conta do github em deploy Free (Login with in github)

Create app (deploy a public app from github)

OBS: Nescessário ter Python e um editor de código na sua máquina.
