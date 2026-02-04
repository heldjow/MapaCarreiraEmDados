# 📊 Mapa Carreira em Dados

Projeto criado para responder à pergunta:

> **Quais informações são relevantes para quem deseja iniciar ou migrar para a área de Dados?**

A partir de uma base pública sobre salários e perfis profissionais da área, este projeto percorre **todo o ciclo de um projeto real de dados**:

**Extração → Limpeza → Transformação → Análise → Visualização → Deploy**

A entrega final é um **dashboard interativo em Streamlit**, publicado na nuvem.

🔗 **Acesse a aplicação online:** *(coloque aqui o link do seu deploy)*

---

## 🎯 Objetivo do Projeto

Demonstrar, na prática, como um projeto de dados é construído desde os dados brutos até a geração de valor em forma de dashboard analítico.

Este projeto também serve como base para evoluções arquiteturais mais avançadas, como SQL, Data Warehouse e Modelagem Dimensional.

---

## 🧱 Arquitetura do Projeto — v1.0 (Atual)

Nesta primeira versão, a arquitetura utiliza um pipeline direto com Pandas:

```
Dados brutos → Pandas (ETL) → CSV tratado → Streamlit → Dashboard
```

Essa abordagem é simples, funcional e muito comum em projetos iniciais de análise de dados.

---

## 🚀 Evolução Planejada — v2.0

A próxima etapa do projeto consiste em evoluir essa arquitetura para um modelo mais profissional utilizando:

- Banco de dados SQL para persistência
- Separação entre ingestão, transformação e consumo
- Modelagem Dimensional (Star Schema)
- Consultas analíticas diretamente do banco no Streamlit

O objetivo é demonstrar **por que a abordagem com Pandas funciona**, mas **por que uma arquitetura com banco de dados é mais escalável e organizada**.

---

## ✨ Funcionalidades

- Limpeza e padronização de dados com Pandas
- Tratamento de variáveis categóricas e quantitativas
- Tradução e organização das informações da base
- Análise exploratória dos dados
- Dashboards interativos com filtros dinâmicos
- Deploy em nuvem com Streamlit Cloud

---

## 🗂️ Estrutura do Repositório

```
.
├── app.py
├── df_limpo.csv
├── etl_colab.ipynb
├── requirements.txt
├── img/
└── README.md
```

---

## ✅ Pré-requisitos

Para executar o projeto localmente é necessário ter instalado:

- Python 3.10+
- Git

Opcional:
- VSCode ou outro editor de código

---

## 🛠️ Como executar localmente

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/heldjow/ImersaoDadosAlura
cd ImersaoDadosAlura
```

### 2️⃣ Crie o ambiente virtual

Linux / Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Execute a aplicação

```bash
streamlit run app.py
```

---

## 🌐 Deploy da Aplicação

O deploy pode ser feito gratuitamente utilizando o **Streamlit Cloud**:

1. Acesse: https://streamlit.io/cloud
2. Conecte sua conta do GitHub
3. Selecione este repositório
4. Informe o arquivo `app.py` como ponto de entrada

---

## 🧠 O que este projeto demonstra

Este projeto evidencia conhecimentos em:

- Processo completo de ETL com Pandas
- Análise exploratória de dados
- Construção de dashboards analíticos
- Deploy de aplicações de dados
- Organização de projeto e versionamento
- Base para evolução para arquitetura SQL + Data Warehouse

---

## 🔖 Versionamento do Projeto

- **v1.0** — Pipeline direto com Pandas e CSV tratado
- **v2.0 (em desenvolvimento)** — Persistência em SQL + Modelagem Dimensional

---

## 📌 Observação

Todo o processo de tratamento dos dados pode ser visualizado no notebook disponível no repositório (`etl_colab.ipynb`).

