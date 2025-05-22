import streamlit as st
from pymongo import MongoClient

def crud():
    client = MongoClient("mongodb://localhost:27017")
    db = client["OdontoPrev"]
    col = db["t_endereco_clinica_odontoprev"]

    st.header("Endereços de Clínica")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar novo endereço"])

    with tab1:
        enderecos = list(col.find({}, {"_id": 0}))
        if enderecos:
            st.dataframe(enderecos)
        else:
            st.info("Nenhum endereço cadastrado ainda.")

        endereco_ids = [e["endereco_clinica_id"] for e in enderecos]
        if endereco_ids:
            selected_id = st.selectbox("Selecione o ID do endereço para editar/deletar", endereco_ids, key="endereco_clinica_id")
            endereco = col.find_one({"endereco_clinica_id": selected_id})

            with st.expander("Editar endereço"):
                with st.form("edit_endereco_clinica_form"):
                    clinica_id_edit = st.text_input("ID da Clínica", endereco.get("clinica_id", ""))
                    cep_edit = st.text_input("CEP", endereco.get("cep_clinica", ""))
                    cidade_edit = st.text_input("Cidade", endereco.get("cidade_clinica", ""))
                    estado_edit = st.text_input("Estado", endereco.get("estado_clinica", ""))
                    logradouro_edit = st.text_input("Logradouro", endereco.get("logradouro_clinica", ""))
                    bairro_edit = st.text_input("Bairro", endereco.get("bairro_clinica", ""))
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"endereco_clinica_id": selected_id},
                            {"$set": {
                                "clinica_id": clinica_id_edit,
                                "cep_clinica": cep_edit,
                                "cidade_clinica": cidade_edit,
                                "estado_clinica": estado_edit,
                                "logradouro_clinica": logradouro_edit,
                                "bairro_clinica": bairro_edit
                            }}
                        )
                        st.success("Endereço atualizado!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar endereço", key="del_endereco_clinica"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar este endereço?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"endereco_clinica_id": selected_id})
                        st.success("Endereço deletado!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key="cancela_delete"):
                        st.session_state.confirm_delete = False
                        st.info("Operação cancelada.")
                        st.rerun()
        else:
            st.info("Nenhum endereço para editar ou deletar.")

    with tab2:
        with st.form("add_endereco_clinica_form"):
            endereco_clinica_id = st.text_input("ID do Endereço")
            clinica_id = st.text_input("ID da Clínica")
            cep_clinica = st.text_input("CEP")
            cidade_clinica = st.text_input("Cidade")
            estado_clinica = st.text_input("Estado")
            logradouro_clinica = st.text_input("Logradouro")
            bairro_clinica = st.text_input("Bairro")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "endereco_clinica_id": endereco_clinica_id,
                    "clinica_id": clinica_id,
                    "cep_clinica": cep_clinica,
                    "cidade_clinica": cidade_clinica,
                    "estado_clinica": estado_clinica,
                    "logradouro_clinica": logradouro_clinica,
                    "bairro_clinica": bairro_clinica
                }
                col.insert_one(doc)
                st.success("Endereço adicionado!")
                st.rerun()
