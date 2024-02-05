import streamlit as st
import datetime as dt
import Dados as dd
import Modelo as md
import warnings
warnings.filterwarnings("ignore") 

#Definindo Datas
data_inicio = "01/01/2004"
data_fim = dt.date.today().strftime("%d/%m/%Y")

#Baixando Dados via API
df_IPCA = dd.dataframe.extracao_bcb(13522, data_inicio, data_fim, "IPCA")
df_SELIC = dd.dataframe.extracao_bcb(432, data_inicio, data_fim, "SELIC")
df_CAMB = dd.dataframe.extracao_bcb(3697, data_inicio, data_fim, "CAMB")
df_DES = dd.dataframe.extracao_bcb(24369, data_inicio, data_fim, "DES")

#Unindo os Dataframes
df = dd.dataframe.unir_DFs( df_SELIC, "SELIC", df_IPCA, "IPCA", df_CAMB, "CAMB", df_DES, "DES")

#Título da Página
st.markdown("<h1 style='text-align: center; color: 	#B0E0E6;'>Panorama Macro</h1>", unsafe_allow_html=True)

opcao = st.selectbox(
    'Qual indicador deseja analisar?',
    ('SELIC (%)', 'IPCA (%)','Desemprego (%)','Câmbio (Real/Dólar)'))

if opcao == 'SELIC (%)':
   cl = "SELIC"
   cl2 = "IPCA"
   tipo = " %"
   dif = 4
   coint = 1
   tend = "li"
   pfrente = 24
   index = 0
   
elif opcao == 'IPCA (%)':
    cl = "IPCA"
    cl2 = "DES"
    tipo = " %"
    dif = 4
    coint = 1
    tend = "ci"
    pfrente = 24
    index = 1

elif opcao == 'Câmbio (Real/Dólar)':
    cl = "CAMB"
    cl2 = "SELIC"
    tipo = " R$"
    dif = 4
    coint = 1
    tend = "ci"
    pfrente = 24
    index = 2

elif opcao == 'Desemprego (%)':
    cl = "DES"
    cl2 = "IPCA"
    tipo = " %"
    dif = 4
    coint = 1
    tend = "ci"
    pfrente = 24
    index = 3
    

col1, col2, col3, col4 = st.columns(4)

ult_linha = dd.dataframe.ult_dado(cl, df).round(2)
var_linha = dd.dataframe.var_dado(cl, df)
var_perc = ((var_linha / ult_linha)*100).round(2)

col1.metric(opcao, str(ult_linha) + tipo, str(var_perc) +" %")
col2.metric("Média Histórica" , str(df[cl].mean().round(2)) + tipo)
col3.metric("Máxima Histórica", str(df[cl].max().round(2)) + tipo)
col4.metric("Mínima Histórica", str(df[cl].min().round(2)) + tipo)

st.header("Série Histórica")
st.line_chart(df, x='Ano-Mês', y=cl, color=	"#40E0D0")

st.header("Projeção 24 meses à frente")
df_proj = md.modelo.vecm(df, cl, dif, coint, tend, pfrente, index)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Projeção para 2024-12" , str(dd.dataframe.ult_mes_ano(df_proj, "Ano-Mês", "2024-12", cl)) + tipo, str(dd.dataframe.var_12M(cl, df_proj, "Ano-Mês", "2024-01", "2024-12"))+" %")
col2.metric("Projeção para 2025-12" , str(dd.dataframe.ult_mes_ano(df_proj, "Ano-Mês", "2025-12", cl)) + tipo, str(dd.dataframe.var_12M(cl, df_proj, "Ano-Mês", "2025-01", "2025-12"))+" %")
col3.metric("Máxima Projetada", str(df_proj[cl].max().round(2)) + tipo)
col4.metric("Mínima Projetada", str(df_proj[cl].min().round(2)) + tipo)


st.line_chart(df_proj, x='Ano-Mês', y=cl, color="#0099ff")

st.header("Relações Econômicas")
st.line_chart(df, x=cl2, y=cl, color="#00FA9A")
