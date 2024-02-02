import streamlit as st
import Dados as dados

data_inicio = "01/01/2004"
data_fim = "01/01/2024"


#Baixando Dados via API
df_IPCA = dados.DT.extracao_bcb(13522, data_inicio, data_fim)
df_IPCA.rename(columns={'valor': 'IPCA'}, inplace = True)

df_SELIC = dados.DT.extracao_bcb(432, data_inicio, data_fim)
df_SELIC.rename(columns={'valor': 'SELIC'}, inplace = True)

df_CAMB = dados.DT.extracao_bcb(3697, data_inicio, data_fim)
df_CAMB.rename(columns={'valor': 'CAMB'}, inplace = True)

#Unindo os Dataframes
df = dados.DT.unir_DFs( df_SELIC, df_IPCA, df_CAMB)


#Tratando Coluna duplicada
df.drop(columns=['IPCA_x'], inplace= True)
df.rename(columns={'IPCA_y' : 'IPCA'}, inplace= True)
df['Ano-Mês'] = df.index
df.info()

st.header("Panorama Macro")

st.line_chart(df, x='Ano-Mês', y="SELIC")

col1, col2, col3 = st.columns(3)

ult_linha = dados.DT.ult_dado("SELIC", df)
var_linha = dados.DT.var_dado("SELIC", df)
var_perc = ((var_linha / ult_linha)*100).round(2)

col1.metric("SELIC", str(ult_linha) + " %", str(var_perc) +" %")

