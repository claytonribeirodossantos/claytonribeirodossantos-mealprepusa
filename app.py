# MealPrep USA - SaaS completo em Streamlit + Supabase (baseado na conversa com Clayton)

import streamlit as st
import pandas as pd
import datetime
from supabase import create_client, Client

# --- CONFIGURAÇÕES INICIAIS ---

SUPABASE_URL = "https://oqswhizghgaxxjfplqxf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9xc3doaXpnaGdheHhqZnBscXhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc2OTIwOTIsImV4cCI6MjA2MzI2ODA5Mn0.gfH1gKOtcsB6tFvO1Kzk2dHF37NOqBMG1sJaijECgeE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="MealPrep USA", layout="wide")
st.title("🍱 MealPrep USA - Sistema de Marmitaria")

menu = st.sidebar.radio("Menu", ["📋 Pedidos", "👤 Clientes", "🍽 Cardápio", "📦 Produção", "🚚 Entregas", "📊 Relatórios"])

# --- 1. CLIENTES ---
if menu == "👤 Clientes":
    st.header("Cadastro de Clientes")

    with st.form("form_cliente", clear_on_submit=True):
        nome = st.text_input("Nome completo*")
        telefone = st.text_input("Telefone*")
        endereco = st.text_input("Endereço*")
        observacoes = st.text_area("Observações")
        submitted = st.form_submit_button("Salvar Cliente")

        if submitted:
            if nome and telefone and endereco:
                supabase.table("clientes").insert({
                    "nome": nome,
                    "telefone": telefone,
                    "endereco": endereco,
                    "observacoes": observacoes
                }).execute()
                st.success("Cliente salvo com sucesso!")
            else:
                st.error("Por favor, preencha os campos obrigatórios.")

    st.subheader("Clientes Cadastrados")
    clientes_data = supabase.table("clientes").select("*").execute().data
    df_clientes = pd.DataFrame(clientes_data)
    if not df_clientes.empty:
        st.dataframe(df_clientes)
    else:
        st.info("Nenhum cliente cadastrado ainda.")

# --- 2. CARDÁPIO ---
elif menu == "🍽 Cardápio":
    st.header("Cadastro de Marmitas")

    with st.form("form_cardapio", clear_on_submit=True):
        sabor = st.text_input("Sabor da marmita*")
        descricao = st.text_area("Descrição")
        preco = st.number_input("Preço (USD)*", min_value=0.0, format="%.2f")
        ativo = st.checkbox("Disponível para pedidos", value=True)
        submitted = st.form_submit_button("Salvar Marmita")

        if submitted and sabor and preco:
            supabase.table("cardapio").insert({
                "sabor": sabor,
                "descricao": descricao,
                "preco": preco,
                "ativo": ativo
            }).execute()
            st.success("Marmita cadastrada com sucesso!")

    st.subheader("Cardápio Atual")
    cardapio_data = supabase.table("cardapio").select("*").execute().data
    df_cardapio = pd.DataFrame(cardapio_data)
    if not df_cardapio.empty:
        st.dataframe(df_cardapio)
    else:
        st.info("Nenhuma marmita cadastrada ainda.")

# --- 3. PEDIDOS ---
elif menu == "📋 Pedidos":
    st.header("Novo Pedido")
    clientes = supabase.table("clientes").select("id, nome").execute().data
    cardapio = supabase.table("cardapio").select("id, sabor, preco").eq("ativo", True).execute().data

    cliente_dict = {c['nome']: c['id'] for c in clientes}
    marmita_dict = {f"{m['sabor']} - ${m['preco']:.2f}": (m['id'], m['preco']) for m in cardapio}

    with st.form("form_pedido", clear_on_submit=True):
        cliente_nome = st.selectbox("Cliente*", list(cliente_dict.keys()))
        marmita_nome = st.selectbox("Marmita*", list(marmita_dict.keys()))
        quantidade = st.number_input("Quantidade*", min_value=1, step=1, value=1)
        data_entrega = st.date_input("Data de entrega*", min_value=datetime.date.today())
        observacoes = st.text_area("Observações")
        submit_pedido = st.form_submit_button("Confirmar Pedido")

        if submit_pedido:
            cliente_id = cliente_dict[cliente_nome]
            marmita_id, preco_unitario = marmita_dict[marmita_nome]
            supabase.table("pedidos").insert({
                "cliente_id": cliente_id,
                "marmita_id": marmita_id,
                "quantidade": quantidade,
                "data_entrega": data_entrega.isoformat(),
                "observacoes": observacoes,
                "entregue": False
            }).execute()
            st.success("Pedido registrado com sucesso!")

# Outras telas como Entregas, Produção, Relatórios continuarão depois com base na mesma estrutura.
