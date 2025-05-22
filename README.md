# OdontoPrev - Sistema de Gestão Odontológica com MongoDB

## Integrantes

- **Caio Eduardo Martins** - RM554025  
- **Julia Mariano Barsotti** - RM552713  
- **Leonardo Gaspar Saheb** - RM553383  

## Objetivo do Projeto

Este projeto tem como objetivo migrar e modernizar o sistema de gestão odontológica da **OdontoPrev**, utilizando o banco de dados NoSQL **MongoDB** para obter maior desempenho, flexibilidade e escalabilidade.  
A aplicação foi desenvolvida em **Python**, utilizando o framework **Streamlit**, proporcionando uma interface intuitiva para operações **CRUD**, consultas e gerenciamento de dados clínicos.

---

## Tecnologias Utilizadas

- **Python**  
- **Streamlit**  
- **MongoDB**  
- **PyMongo**  

---

## Requisitos

- Python 3.9 ou superior  
- MongoDB (instalado localmente ou via MongoDB Atlas)

---

## Como Clonar e Executar o Projeto

### 1. Clone o repositório

`git clone https://github.com/Leonardo-Gaspar/OdontoPrevProject.git`

`cd OdontoPrevProject`

2. Crie um ambiente virtual (opcional, mas recomendado)

python -m venv venv

source venv/bin/activate # Linux/macOS

venv\Scripts\activate     # Windows

4. Instale as dependências
`pip install -r requirements.txt`

5. Inicie o MongoDB
Certifique-se de que o MongoDB está em execução localmente ou configure uma conexão com o MongoDB Atlas.

6. Execute a aplicação
`streamlit run app.py`

7. Acesse no navegador
O terminal exibirá um link como este:
`Local URL: http://localhost:8501`

Abra o navegador e acesse esse endereço para utilizar a interface web
