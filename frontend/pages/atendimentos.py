import streamlit as st
from pymongo import MongoClient

def crud():
    client = MongoClient("mongodb://localhost:27017")
    db = client["OdontoPrev"]
    col = db["t_atendimento_usuario_odontoprev"]

    st.header("Atendimentos")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar novo atendimento"])

    with tab1:
        atendimentos = list(col.find({}, {"_id": 0}))
        if atendimentos:
            st.dataframe(atendimentos)
        else:
            st.info("Nenhum atendimento cadastrado ainda.")

        atendimento_ids = [a["atendimento_id"] for a in atendimentos]
        if atendimento_ids:
            selected_id = st.selectbox("Selecione o ID do atendimento para editar/deletar", atendimento_ids, key="atendimento_id")
            atendimento = col.find_one({"atendimento_id": selected_id})

            with st.expander("Editar atendimento"):
                with st.form("edit_atendimento_form"):
                    usuario_id_edit = st.text_input("ID do Usuário", atendimento.get("usuario_id", ""))
                    dentista_id_edit = st.text_input("ID do Dentista", atendimento.get("dentista_id", ""))
                    clinica_id_edit = st.text_input("ID da Clínica", atendimento.get("clinica_id", ""))
                    data_atendimento_edit = st.text_input("Data do Atendimento (YYYY-MM-DD)", atendimento.get("data_atendimento", ""))
                    descricao_edit = st.text_input("Procedimento", atendimento.get("descricao_procedimento", ""))
                    custo_edit = st.number_input("Custo", value=float(atendimento.get("custo", 0)), step=0.01)
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"atendimento_id": selected_id},
                            {"$set": {
                                "usuario_id": usuario_id_edit,
                                "dentista_id": dentista_id_edit,
                                "clinica_id": clinica_id_edit,
                                "data_atendimento": data_atendimento_edit,
                                "descricao_procedimento": descricao_edit,
                                "custo": custo_edit
                            }}
                        )
                        st.success("Atendimento atualizado!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar atendimento", key="del_atendimento"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar este atendimento?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"atendimento_id": selected_id})
                        st.success("Atendimento deletado!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key="cancela_delete"):
                        st.session_state.confirm_delete = False
                        st.info("Operação cancelada.")
                        st.rerun()
        else:
            st.info("Nenhum atendimento para editar ou deletar.")

    with tab2:
        with st.form("add_atendimento_form"):
            atendimento_id = st.text_input("ID do Atendimento")
            usuario_id = st.text_input("ID do Usuário")
            dentista_id = st.text_input("ID do Dentista")
            clinica_id = st.text_input("ID da Clínica")
            data_atendimento = st.text_input("Data do Atendimento (YYYY-MM-DD)")
            descricao_procedimento = st.text_input("Procedimento")
            custo = st.number_input("Custo", min_value=0.0, step=0.01)
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "atendimento_id": atendimento_id,
                    "usuario_id": usuario_id,
                    "dentista_id": dentista_id,
                    "clinica_id": clinica_id,
                    "data_atendimento": data_atendimento,
                    "descricao_procedimento": descricao_procedimento,
                    "custo": custo
                }
                col.insert_one(doc)
                st.success("Atendimento adicionado!")
                st.rerun()
