import streamlit as st
from pymongo import MongoClient

def crud():
    client = MongoClient("mongodb://localhost:27017")
    db = client["OdontoPrev"]
    col = db["t_endereco_usuario_odontoprev"]

    st.header("Endereços de Usuário")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar novo endereço"])

    with tab1:
        enderecos = list(col.find({}, {"_id": 0}))
        if enderecos:
            st.dataframe(enderecos)
        else:
            st.info("Nenhum endereço cadastrado ainda.")

        endereco_ids = [e["endereco_usuario_id"] for e in enderecos]
        if endereco_ids:
            selected_id = st.selectbox("Selecione o ID do endereço para editar/deletar", endereco_ids, key="endereco_usuario_id")
            endereco = col.find_one({"endereco_usuario_id": selected_id})

            with st.expander("Editar endereço"):
                with st.form("edit_endereco_form"):
                    usuario_id_edit = st.text_input("ID do Usuário", endereco.get("usuario_id", ""))
                    cep_edit = st.text_input("CEP", endereco.get("cep_usuario", ""))
                    cidade_edit = st.text_input("Cidade", endereco.get("cidade_usuario", ""))
                    estado_edit = st.text_input("Estado", endereco.get("estado_usuario", ""))
                    logradouro_edit = st.text_input("Logradouro", endereco.get("logradouro_usuario", ""))
                    bairro_edit = st.text_input("Bairro", endereco.get("bairro_usuario", ""))
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"endereco_usuario_id": selected_id},
                            {"$set": {
                                "usuario_id": usuario_id_edit,
                                "cep_usuario": cep_edit,
                                "cidade_usuario": cidade_edit,
                                "estado_usuario": estado_edit,
                                "logradouro_usuario": logradouro_edit,
                                "bairro_usuario": bairro_edit
                            }}
                        )
                        st.success("Endereço atualizado!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar endereço", key="del_endereco"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar este endereço?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"endereco_usuario_id": selected_id})
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
        with st.form("add_endereco_form"):
            endereco_usuario_id = st.text_input("ID do Endereço")
            usuario_id = st.text_input("ID do Usuário")
            cep_usuario = st.text_input("CEP")
            cidade_usuario = st.text_input("Cidade")
            estado_usuario = st.text_input("Estado")
            logradouro_usuario = st.text_input("Logradouro")
            bairro_usuario = st.text_input("Bairro")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "endereco_usuario_id": endereco_usuario_id,
                    "usuario_id": usuario_id,
                    "cep_usuario": cep_usuario,
                    "cidade_usuario": cidade_usuario,
                    "estado_usuario": estado_usuario,
                    "logradouro_usuario": logradouro_usuario,
                    "bairro_usuario": bairro_usuario
                }
                col.insert_one(doc)
                st.success("Endereço adicionado!")
                st.rerun()
