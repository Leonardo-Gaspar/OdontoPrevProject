import streamlit as st
from pymongo import MongoClient

def crud():
    client = MongoClient("mongodb://localhost:27017")
    db = client["OdontoPrev"]
    col = db["t_clinica_odontoprev"]

    st.header("Clínicas")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar nova clínica"])

    with tab1:
        clinicas = list(col.find({}, {"_id": 0}))
        if clinicas:
            st.dataframe(clinicas)
        else:
            st.info("Nenhuma clínica cadastrada ainda.")

        clinica_ids = [c["clinica_id"] for c in clinicas]
        if clinica_ids:
            selected_id = st.selectbox("Selecione o ID da clínica para editar/deletar", clinica_ids, key="clinica_id")
            clinica = col.find_one({"clinica_id": selected_id})

            with st.expander("Editar clínica"):
                with st.form("edit_clinica_form"):
                    dentista_id_edit = st.text_input("ID do Dentista", clinica.get("dentista_id", ""))
                    nome_edit = st.text_input("Nome da Clínica", clinica.get("nome_clinica", ""))
                    telefone_edit = st.text_input("Telefone", clinica.get("telefone_clinica", ""))
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"clinica_id": selected_id},
                            {"$set": {
                                "dentista_id": dentista_id_edit,
                                "nome_clinica": nome_edit,
                                "telefone_clinica": telefone_edit
                            }}
                        )
                        st.success("Clínica atualizada!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar clínica", key="del_clinica"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar esta clínica?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"clinica_id": selected_id})
                        st.success("Clínica deletada!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key="cancela_delete"):
                        st.session_state.confirm_delete = False
                        st.info("Operação cancelada.")
                        st.rerun()
        else:
            st.info("Nenhuma clínica para editar ou deletar.")

    with tab2:
        with st.form("add_clinica_form"):
            clinica_id = st.text_input("ID da Clínica")
            dentista_id = st.text_input("ID do Dentista")
            nome_clinica = st.text_input("Nome da Clínica")
            telefone_clinica = st.text_input("Telefone da Clínica")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "clinica_id": clinica_id,
                    "dentista_id": dentista_id,
                    "nome_clinica": nome_clinica,
                    "telefone_clinica": telefone_clinica
                }
                col.insert_one(doc)
                st.success("Clínica adicionada!")
                st.rerun()
