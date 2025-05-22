import streamlit as st
from pymongo import MongoClient

def crud():
    client = MongoClient("mongodb://localhost:27017")
    db = client["OdontoPrev"]
    col = db["t_dentista_odontoprev"]

    st.header("Dentistas")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar novo dentista"])

    with tab1:
        dentistas = list(col.find({}, {"_id": 0}))
        if dentistas:
            st.dataframe(dentistas)
        else:
            st.info("Nenhum dentista cadastrado ainda.")

        dentista_ids = [d["dentista_id"] for d in dentistas]
        if dentista_ids:
            selected_id = st.selectbox("Selecione o ID do dentista para editar/deletar", dentista_ids, key="dentista_id")
            dentista = col.find_one({"dentista_id": selected_id})

            with st.expander("Editar dentista"):
                with st.form("edit_dentista_form"):
                    usuario_id_edit = st.text_input("ID do Usuário", dentista.get("usuario_id", ""))
                    nome_edit = st.text_input("Nome", dentista.get("nome_dentista", ""))
                    especialidade_edit = st.text_input("Especialidade", dentista.get("especialidade", ""))
                    telefone_edit = st.text_input("Telefone", dentista.get("telefone_dentista", ""))
                    email_edit = st.text_input("Email", dentista.get("email_dentista", ""))
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"dentista_id": selected_id},
                            {"$set": {
                                "usuario_id": usuario_id_edit,
                                "nome_dentista": nome_edit,
                                "especialidade": especialidade_edit,
                                "telefone_dentista": telefone_edit,
                                "email_dentista": email_edit
                            }}
                        )
                        st.success("Dentista atualizado!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar dentista", key="del_dentista"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar este dentista?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"dentista_id": selected_id})
                        st.success("Dentista deletado!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key="cancela_delete"):
                        st.session_state.confirm_delete = False
                        st.info("Operação cancelada.")
                        st.rerun()
        else:
            st.info("Nenhum dentista para editar ou deletar.")

    with tab2:
        with st.form("add_dentista_form"):
            dentista_id = st.text_input("ID do Dentista")
            usuario_id = st.text_input("ID do Usuário")
            nome_dentista = st.text_input("Nome")
            especialidade = st.text_input("Especialidade")
            telefone_dentista = st.text_input("Telefone")
            email_dentista = st.text_input("Email")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "dentista_id": dentista_id,
                    "usuario_id": usuario_id,
                    "nome_dentista": nome_dentista,
                    "especialidade": especialidade,
                    "telefone_dentista": telefone_dentista,
                    "email_dentista": email_dentista
                }
                col.insert_one(doc)
                st.success("Dentista adicionado!")
                st.rerun()
