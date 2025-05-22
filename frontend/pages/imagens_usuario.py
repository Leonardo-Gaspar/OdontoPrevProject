import streamlit as st
from pymongo import MongoClient
from datetime import datetime, date

def to_iso_date(date_obj):
    if isinstance(date_obj, date):
        return date_obj.strftime("%Y-%m-%d")
    return date_obj

def parse_iso_date(date_str):
    if not date_str:
        return date.today()
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").date()
    except Exception:
        pass
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").date()
    except Exception:
        pass
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        pass
    return date.today()

def crud():
    client = MongoClient("mongodb://localhost:27017")
    db = client["OdontoPrev"]
    col = db["t_imagem_usuario_odontoprev"]

    st.header("Imagens de Usuário")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar nova imagem"])

    with tab1:
        imagens = list(col.find({}, {"_id": 0}))
        if imagens:
            st.dataframe(imagens)
        else:
            st.info("Nenhuma imagem cadastrada ainda.")

        imagem_ids = [i["imagem_usuario_id"] for i in imagens]
        if imagem_ids:
            selected_id = st.selectbox("Selecione o ID da imagem para editar/deletar", imagem_ids, key="imagem_usuario_id")
            imagem = col.find_one({"imagem_usuario_id": selected_id})

            with st.expander("Editar imagem"):
                with st.form("edit_imagem_form"):
                    usuario_id_edit = st.text_input("ID do Usuário", imagem.get("usuario_id", ""))
                    imagem_url_edit = st.text_input("URL da Imagem", imagem.get("imagem_url", ""))
                    data_envio_edit = st.date_input(
                        "Data de Envio",
                        value=parse_iso_date(imagem.get("data_envio", "2025-01-01"))
                    )
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"imagem_usuario_id": selected_id},
                            {"$set": {
                                "usuario_id": usuario_id_edit,
                                "imagem_url": imagem_url_edit,
                                "data_envio": to_iso_date(data_envio_edit)
                            }}
                        )
                        st.success("Imagem atualizada!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar imagem", key="del_imagem"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar esta imagem?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"imagem_usuario_id": selected_id})
                        st.success("Imagem deletada!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key="cancela_delete"):
                        st.session_state.confirm_delete = False
                        st.info("Operação cancelada.")
                        st.rerun()
        else:
            st.info("Nenhuma imagem para editar ou deletar.")

    with tab2:
        with st.form("add_imagem_form"):
            imagem_usuario_id = st.text_input("ID da Imagem")
            usuario_id = st.text_input("ID do Usuário")
            imagem_url = st.text_input("URL da Imagem")
            data_envio = st.date_input("Data de Envio", value=date.today())
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "imagem_usuario_id": imagem_usuario_id,
                    "usuario_id": usuario_id,
                    "imagem_url": imagem_url,
                    "data_envio": to_iso_date(data_envio)
                }
                col.insert_one(doc)
                st.success("Imagem adicionada!")
                st.rerun()
