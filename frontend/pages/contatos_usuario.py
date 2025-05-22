import streamlit as st
from pymongo import MongoClient

def crud():
    client = MongoClient("mongodb://localhost:27017")
    db = client["OdontoPrev"]
    col = db["t_contato_usuario_odontoprev"]

    st.header("Contatos de Usuário")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar novo contato"])

    with tab1:
        contatos = list(col.find({}, {"_id": 0}))
        if contatos:
            st.dataframe(contatos)
        else:
            st.info("Nenhum contato cadastrado ainda.")

        contato_ids = [c["contato_usuario_id"] for c in contatos]
        if contato_ids:
            selected_id = st.selectbox("Selecione o ID do contato para editar/deletar", contato_ids, key="contato_usuario_id")
            contato = col.find_one({"contato_usuario_id": selected_id})

            with st.expander("Editar contato"):
                with st.form("edit_contato_form"):
                    usuario_id_edit = st.text_input("ID do Usuário", contato.get("usuario_id", ""))
                    email_edit = st.text_input("Email", contato.get("email_usuario", ""))
                    telefone_edit = st.text_input("Telefone", contato.get("telefone_usuario", ""))
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"contato_usuario_id": selected_id},
                            {"$set": {
                                "usuario_id": usuario_id_edit,
                                "email_usuario": email_edit,
                                "telefone_usuario": telefone_edit
                            }}
                        )
                        st.success("Contato atualizado!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar contato", key="del_contato"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar este contato?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"contato_usuario_id": selected_id})
                        st.success("Contato deletado!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key="cancela_delete"):
                        st.session_state.confirm_delete = False
                        st.info("Operação cancelada.")
                        st.rerun()
        else:
            st.info("Nenhum contato para editar ou deletar.")

    with tab2:
        with st.form("add_contato_form"):
            contato_usuario_id = st.text_input("ID do Contato")
            usuario_id = st.text_input("ID do Usuário")
            email_usuario = st.text_input("Email")
            telefone_usuario = st.text_input("Telefone")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "contato_usuario_id": contato_usuario_id,
                    "usuario_id": usuario_id,
                    "email_usuario": email_usuario,
                    "telefone_usuario": telefone_usuario
                }
                col.insert_one(doc)
                st.success("Contato adicionado!")
                st.rerun()
