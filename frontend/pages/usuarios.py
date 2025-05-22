import streamlit as st
from pymongo import MongoClient
from datetime import datetime, date

def format_date_str(date_str):
    if not date_str:
        return ""
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", ""))
            return dt.strftime("%d/%m/%Y %H:%M")
        else:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
    except Exception:
        return date_str

def to_iso_date(date_obj):
    if isinstance(date_obj, date):
        return date_obj.strftime("%Y-%m-%d")
    return date_obj

def crud():
    client = MongoClient("mongodb://localhost:27017")
    db = client["OdontoPrev"]
    col = db["t_usuario_odontoprev"]

    st.header("Usuários")

    tab1, tab2 = st.tabs(["Visualizar dados", "Adicionar novo usuário"])

    with tab1:
        usuarios = list(col.find({}, {"_id": 0}))
        for u in usuarios:
            u["data_nascimento"] = format_date_str(u.get("data_nascimento", ""))
            u["data_cadastro"] = format_date_str(u.get("data_cadastro", ""))
        if usuarios:
            st.dataframe(usuarios)
        else:
            st.info("Nenhum usuário cadastrado ainda.")

        usuario_ids = [u["usuario_id"] for u in usuarios]
        if usuario_ids:
            selected_id = st.selectbox("Selecione o ID do usuário para editar/deletar", usuario_ids, key="usuario_id")
            user = col.find_one({"usuario_id": selected_id})

            with st.expander("Editar usuário"):
                with st.form("edit_user_form"):
                    cpf_edit = st.text_input("CPF", user.get("cpf", ""))
                    nome_edit = st.text_input("Nome", user.get("nome", ""))
                    sobrenome_edit = st.text_input("Sobrenome", user.get("sobrenome", ""))
                    dn = user.get("data_nascimento", "")
                    if dn and "/" in dn:
                        try:
                            data_nasc_edit = datetime.strptime(dn, "%d/%m/%Y").date()
                        except Exception:
                            data_nasc_edit = date.today()
                    elif dn:
                        try:
                            data_nasc_edit = datetime.strptime(dn[:10], "%Y-%m-%d").date()
                        except Exception:
                            data_nasc_edit = date.today()
                    else:
                        data_nasc_edit = date.today()
                    data_nascimento_edit = st.date_input("Data de Nascimento", data_nasc_edit)
                    genero_edit = st.selectbox("Gênero", ["M", "F", "Outro"], index=["M", "F", "Outro"].index(user.get("genero", "M")))
                    dc = user.get("data_cadastro", "")
                    if dc and "/" in dc:
                        try:
                            data_cad_edit = datetime.strptime(dc.split(" ")[0], "%d/%m/%Y").date()
                        except Exception:
                            data_cad_edit = date.today()
                    elif dc:
                        try:
                            data_cad_edit = datetime.strptime(dc[:10], "%Y-%m-%d").date()
                        except Exception:
                            data_cad_edit = date.today()
                    else:
                        data_cad_edit = date.today()
                    data_cadastro_edit = st.date_input("Data de Cadastro", data_cad_edit)
                    if st.form_submit_button("Atualizar"):
                        col.update_one(
                            {"usuario_id": selected_id},
                            {"$set": {
                                "cpf": cpf_edit,
                                "nome": nome_edit,
                                "sobrenome": sobrenome_edit,
                                "data_nascimento": to_iso_date(data_nascimento_edit),
                                "genero": genero_edit,
                                "data_cadastro": to_iso_date(data_cadastro_edit)
                            }}
                        )
                        st.success("Usuário atualizado!")
                        st.rerun()

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            if st.button("Deletar usuário", key="del_usuario"):
                st.session_state.confirm_delete = True
            if st.session_state.confirm_delete:
                st.warning("Tem certeza que deseja deletar este usuário?")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Sim, deletar", key="confirma_delete"):
                        col.delete_one({"usuario_id": selected_id})
                        st.success("Usuário deletado!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key="cancela_delete"):
                        st.session_state.confirm_delete = False
                        st.info("Operação cancelada.")
                        st.rerun()
        else:
            st.info("Nenhum usuário para editar ou deletar.")

    with tab2:
        with st.form("add_user_form"):
            usuario_id = st.text_input("ID do Usuário")
            cpf = st.text_input("CPF")
            nome = st.text_input("Nome")
            sobrenome = st.text_input("Sobrenome")
            data_nascimento = st.date_input("Data de Nascimento")
            genero = st.selectbox("Gênero", ["M", "F", "Outro"])
            data_cadastro = st.date_input("Data de Cadastro", value=date.today())
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                doc = {
                    "usuario_id": usuario_id,
                    "cpf": cpf,
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "data_nascimento": to_iso_date(data_nascimento),
                    "genero": genero,
                    "data_cadastro": to_iso_date(data_cadastro)
                }
                col.insert_one(doc)
                st.success("Usuário adicionado!")
                st.rerun()
