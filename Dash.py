import streamlit as st
import Dados as dd
import Modelo as md
import warnings
warnings.filterwarnings("ignore") 

data_inicio = "01/01/2004"
data_fim = "01/01/2024"


#Baixando Dados via API
df_IPCA = dd.dataframe.extracao_bcb(13522, data_inicio, data_fim)
df_IPCA.rename(columns={'valor': 'IPCA'}, inplace = True)

df_SELIC = dd.dataframe.extracao_bcb(432, data_inicio, data_fim)
df_SELIC.rename(columns={'valor': 'SELIC'}, inplace = True)

df_CAMB = dd.dataframe.extracao_bcb(3697, data_inicio, data_fim)
df_CAMB.rename(columns={'valor': 'CAMB'}, inplace = True)

#Unindo os Dataframes
df = dd.dataframe.unir_DFs( df_SELIC, df_IPCA, df_CAMB)


#Tratando Coluna duplicada
df.drop(columns=['IPCA_x'], inplace= True)
df.rename(columns={'IPCA_y' : 'IPCA'}, inplace= True)
df['Ano-Mês'] = df.index

st.markdown("<h1 style='text-align: center; color: 	#B0E0E6;'>Panorama Macro</h1>", unsafe_allow_html=True)

opcao = st.selectbox(
    'Qual indicador deseja analisar?',
    ('SELIC (%)', 'IPCA (%)', 'Câmbio'))

if opcao == 'SELIC (%)':
   cl = "SELIC"
   tipo = " %"
   dif = 4
   coint = 1
   tend = "li"
   pfrente = 24
   index = 0
   
elif opcao == 'IPCA (%)':
    cl = "IPCA"
    tipo = " %"
    dif = 3
    coint = 2
    tend = "li"
    pfrente = 24
    index = 1

else:
    cl = "CAMB"
    tipo = " R$"
    dif = 4
    coint = 1
    tend = "co"
    pfrente = 24
    index = 2

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
st.line_chart(df_proj, x='Ano-Mês', y=cl, color="#FF4500")



