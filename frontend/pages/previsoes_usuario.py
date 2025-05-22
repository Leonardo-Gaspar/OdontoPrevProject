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
    col = db["t_previsao_usuario_odontoprev"]

    st.header("Previsões de Usuário")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar nova previsão"])

    with tab1:
        previsoes = list(col.find({}, {"_id": 0}))
        if previsoes:
            st.dataframe(previsoes)
        else:
            st.info("Nenhuma previsão cadastrada ainda.")

        previsao_ids = [p["previsao_usuario_id"] for p in previsoes]
        if previsao_ids:
            selected_id = st.selectbox("Selecione o ID da previsão para editar/deletar", previsao_ids, key="previsao_usuario_id")
            previsao = col.find_one({"previsao_usuario_id": selected_id})

            with st.expander("Editar previsão"):
                with st.form("edit_previsao_form"):
                    imagem_usuario_id_edit = st.text_input("ID da Imagem", previsao.get("imagem_usuario_id", ""))
                    usuario_id_edit = st.text_input("ID do Usuário", previsao.get("usuario_id", ""))
                    previsao_texto_edit = st.text_input("Previsão", previsao.get("previsao_texto", ""))
                    probabilidade_edit = st.number_input("Probabilidade", value=float(previsao.get("probabilidade", 0)), step=0.01)
                    recomendacao_edit = st.text_input("Recomendação", previsao.get("recomendacao", ""))
                    data_previsao_edit = st.date_input(
                        "Data da Previsão",
                        value=parse_iso_date(previsao.get("data_previsao", "2025-01-01"))
                    )
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"previsao_usuario_id": selected_id},
                            {"$set": {
                                "imagem_usuario_id": imagem_usuario_id_edit,
                                "usuario_id": usuario_id_edit,
                                "previsao_texto": previsao_texto_edit,
                                "probabilidade": probabilidade_edit,
                                "recomendacao": recomendacao_edit,
                                "data_previsao": to_iso_date(data_previsao_edit)
                            }}
                        )
                        st.success("Previsão atualizada!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar previsão", key="del_previsao"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar esta previsão?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"previsao_usuario_id": selected_id})
                        st.success("Previsão deletada!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key="cancela_delete"):
                        st.session_state.confirm_delete = False
                        st.info("Operação cancelada.")
                        st.rerun()
        else:
            st.info("Nenhuma previsão para editar ou deletar.")

    with tab2:
        with st.form("add_previsao_form"):
            previsao_usuario_id = st.text_input("ID da Previsão")
            imagem_usuario_id = st.text_input("ID da Imagem")
            usuario_id = st.text_input("ID do Usuário")
            previsao_texto = st.text_input("Previsão")
            probabilidade = st.number_input("Probabilidade", min_value=0.0, max_value=1.0, step=0.01)
            recomendacao = st.text_input("Recomendação")
            data_previsao = st.date_input("Data da Previsão", value=date.today())
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "previsao_usuario_id": previsao_usuario_id,
                    "imagem_usuario_id": imagem_usuario_id,
                    "usuario_id": usuario_id,
                    "previsao_texto": previsao_texto,
                    "probabilidade": probabilidade,
                    "recomendacao": recomendacao,
                    "data_previsao": to_iso_date(data_previsao)
                }
                col.insert_one(doc)
                st.success("Previsão adicionada!")
                st.rerun()
