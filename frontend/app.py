import streamlit as st
from pages import usuarios, dentistas, clinicas, enderecos_clinica, atendimentos, contatos_usuario, enderecos_usuario, imagens_usuario, previsoes_usuario

st.title("Bem-vindo ao OdontoPrev CRUD!")

st.sidebar.title("OdontoPrev CRUD")
entidade = st.sidebar.selectbox(
    "Escolha a entidade",
    [
        "Usuários", "Dentistas", "Clínicas", "Endereços Clínica", "Atendimentos",
        "Contatos Usuário", "Endereços Usuário", "Imagens Usuário", "Previsões Usuário"
    ]
)

if entidade == "Usuários":
    usuarios.crud()
elif entidade == "Dentistas":
    dentistas.crud()
elif entidade == "Clínicas":
    clinicas.crud()
elif entidade == "Endereços Clínica":
    enderecos_clinica.crud()
elif entidade == "Atendimentos":
    atendimentos.crud()
elif entidade == "Contatos Usuário":
    contatos_usuario.crud()
elif entidade == "Endereços Usuário":
    enderecos_usuario.crud()
elif entidade == "Imagens Usuário":
    imagens_usuario.crud()
elif entidade == "Previsões Usuário":
    previsoes_usuario.crud()
else:
    st.info("Selecione uma entidade no menu à esquerda para começar.")
