import streamlit as st
import Dados as dados

df = dados.DT.obter_dados("Dados.xlsx")

st.header("Panorama Macro")

st.line_chart(df, x="Ano-Mês", y="SELIC")

col1, col2, col3 = st.columns(3)

ult_linha = dados.DT.ult_dado("SELIC", df)
var_linha = dados.DT.var_dado("SELIC", df)
var_perc = ((var_linha / ult_linha)*100).round(2)

col1.metric("SELIC", str(ult_linha) + " %", str(var_perc) +" %")

