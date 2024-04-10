# Instale o Streamlit: pip install streamlit
#Importando as bibliotecas que serão utilizadas
import streamlit as st
import datetime as dt
import pandas as pd
#Retirando avisos chatos
import warnings
warnings.filterwarnings("ignore") 


def isnumber(value):
    try:
         float(value)
    except ValueError:
         return False
    return True


#Título da Página
col1, col2, col3 = st.columns(3)
col2.image('Logo.png', width=100, use_column_width="always" )

col1,= st.columns(1)
col1.markdown("<h1 style='text-align: center; color: 	#C9D200;'>Mesa de Precificação</h1>", unsafe_allow_html=True)
col1.markdown("<h1></h1>", unsafe_allow_html=True)

#Taxas
with st.container(border=True):
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)

#Carregando dados
df_despesas = pd.read_excel("Base.xlsx",sheet_name='Despesas')
df_cred = pd.read_excel("Base.xlsx",sheet_name='Crédito')
df_CDI = pd.read_excel("Base.xlsx",sheet_name='CDI')

custo_cred_med = (-1*df_despesas["Despesa ADM"].sum() / df_despesas["Saldo Devedor (PA)"].sum())
custo_cred_med = round(custo_cred_med*100,2)

inad_med = (df_cred["Provisão"].sum() / df_cred["Saldo Devedor"].sum()) * 100
inad_med = round(((1+inad_med/100)**(1/12)-1)*100,2)

with st.expander("Parâmetros"):
    
    col1, col2, col3 = st.columns([1.5,4,6])

    df_cred.sort_values(by="Número PA", ascending=True)

    PA = col1.selectbox("PA", df_cred["Número PA"].unique())

    df_cred = df_cred[df_cred["Número PA"] == PA]
    df_despesas = df_despesas[df_despesas["Número PA"] == PA]

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    pessoa = m_col1.selectbox("Tipo de Pessoa", df_cred["Tipo Pessoa"].unique())
    df_cred = df_cred[df_cred["Tipo Pessoa"] == pessoa]  

    risco = m_col2.selectbox("Risco", df_cred["Risco BACEN"].unique())
    df_cred = df_cred[df_cred["Risco BACEN"] == risco]  

    Carteira = col2.selectbox("Carteira", df_cred["Carteira"].unique())

    df_cred = df_cred[df_cred["Carteira"] == Carteira]

    Linha = col3.selectbox("Linha", df_cred["Linha Simplificada"].unique())

    df_cred = df_cred[df_cred["Linha Simplificada"] == Linha]
    
    tx_final = 0.00
    cdi = df_CDI["CDI"].max() * 100

    custo_cred = (-1*df_despesas["Despesa ADM"].sum()/ df_despesas["Saldo Devedor (PA)"].sum())
    custo_cred = ((1+ custo_cred)**(12)-1)*100

    tx_inad = (df_cred["Provisão"].sum() / df_cred["Saldo Devedor"].sum()) * 100

    tx_final = tx_final + custo_cred

    #Natureza da Taxa
    taxa_op = m_col3.selectbox(
        'Natureza da taxa?',
        ('Pré-fixada', 'Pós-fixada'))

    if taxa_op == "Pré-fixada":
        tx_final = tx_final
        tx_op = 0.00
    elif taxa_op == "Pós-fixada":
        tx_final = tx_final + cdi
        tx_op = cdi
        
    #INAD
    inad_op = m_col4.selectbox(
        'Considerar o INAD?',
        ('Sim', 'Não'))

    if inad_op == "Não":
        tx_final = tx_final
        tx_inad = 0.00
        
    elif inad_op == "Sim":
        
        tx_final = tx_final + tx_inad

with st.expander("Spread (%)"):
    col1, col2, col3 = st.columns([2,1,1])
     
    #Spread
    spread_op = col1.text_input("Spread em termos do CDI (%)",
            "0",
            key="spread_op",
        )
    
    spread = 0
    if isnumber(spread_op) == True and spread_op !=0:
        spread = float(spread_op)
        spread_op = cdi * float(spread_op)/100
        tx_final = tx_final + spread_op
    else:
        tx_final = tx_final
        spread_op = 0.00

    cdi_am = round(((1+(cdi/100))**(1/12)-1)*100,2)
    col2.metric("CDI (a.m)" , f"{cdi_am}%")
    col3.metric("Spread em CDI (a.m)" , f"{round((spread/100)*cdi_am,2)}%")

with st.expander("Redutores (%)"):
    col1, col2 = st.columns(2)
    
    #RedutorCC
    redutorCC_op = col1.text_input("Redutor do Custo de Crédito (%)",
            "0",
            key="redutorCC_op",
        )

    if isnumber(redutorCC_op) == True and redutorCC_op !=0:
        custo_cred = custo_cred - (custo_cred * (float(redutorCC_op)/100))
        tx_final = tx_inad + tx_op + custo_cred + spread_op
    else:
        tx_final = tx_final
        
    #RedutorTB  
    redutorTB_op = col2.text_input("Rebate da Taxa de Balcão (%)",
            "0",
            key="redutorTB_op",
        )

    if isnumber(redutorTB_op) == True and redutorTB_op !=0:
        tx_final = tx_final - (tx_final * (float(redutorTB_op)/100))
    else:
        tx_final = tx_final
        
    custo_cred_am = round(((1+custo_cred/100)**(1/12)-1)*100,2)
    tx_inad_am = round(((1+tx_inad/100)**(1/12)-1)*100,2)
    tx_final_am = round((((1 + tx_final/100)**(1/12)-1)*100),2)
    tx_final_aa = round(tx_final, 2)
    cdi_am = round(((1+cdi/100)**(1/12)-1)*100,2)
    cdi_aa = cdi
        

#Taxas    

p_col1.metric("Custo do Crédito (a.m)" , f"{custo_cred_am}%", f"{round(custo_cred_med - custo_cred_am,2)}%" )
p_col2.metric("Inadimplência (a.m)" , f"{tx_inad_am}%", f"{round(inad_med - tx_inad_am,2)}%")
p_col3.metric("Taxa Base (a.m) " , f"{tx_final_am }%", f"{round(tx_final_am - cdi_am,2)} p.p CDI (a.m)")
p_col4.metric("Taxa Base (a.a)" , f"{tx_final_aa }%", f"{round(tx_final_aa - cdi_aa,2)} p.p CDI (a.a)")

col1, col2, col3 = st.columns([1,4,1])
col2.write("Desenvolvido pela equipe de BI no departamento de Controladoria!")
col1, col2 = st.columns([2,3])
col2.image('Selo.png', width=110)