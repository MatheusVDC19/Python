# Instale o Streamlit: pip install streamlit

#Importando as bibliotecas que serão utilizadas
import streamlit as st
import datetime as dt

#Importando os outras duas camadas do programa: Dados e Modelo
import Dados as dd
import Modelo as md

#Retirando avisos chatos
import warnings
warnings.filterwarnings("ignore") 

#Definindo Datas
data_inicio = "01/01/2004"
#Seta a data de Hoje
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

#Configurando o selectbox
opcao = st.selectbox(
    'Qual indicador deseja analisar?',
    ('SELIC (%)', 'IPCA (%)','Desemprego (%)','Câmbio (Real/Dólar)'))


#Setando os parâmetros necessários para cada escolha de indicador
if opcao == 'SELIC (%)':
   #Coluna alvo
   cl = "SELIC"

   #Coluna secundária para o gráfico
   cl2 = "IPCA"

   #Forma da variável
   tipo = " %"

   #Parâmetros do Modelo - VECM
   #Número de Defasagens
   dif = 4

   #Número de Cointegrações
   coint = 1
 
   #Forma da tendência(li: tendência exógena, lo: tendência endógena, ci: constante exógena, co: constante endógena)
   tend = "li"

   pfrente = 24

   #Posição da variável no vetor da projeções
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
    
#Configurando layout da colunas no streamlit
col1, col2, col3, col4 = st.columns(4)

#Últimpo valor para o indicador
ult_linha = dd.dataframe.ult_dado(cl, df).round(2)
#Variação
var_linha = dd.dataframe.var_dado(cl, df)
#Variação Percentual
var_perc = ((var_linha / ult_linha)*100).round(2)

#Últimpo valor para o indicador
col1.metric(opcao, str(ult_linha) + tipo, str(var_perc) +" %")
#Média Histórica
col2.metric("Média Histórica" , str(df[cl].mean().round(2)) + tipo)
#Máxima Histórica
col3.metric("Máxima Histórica", str(df[cl].max().round(2)) + tipo)
#Mínima Histórica
col4.metric("Mínima Histórica", str(df[cl].min().round(2)) + tipo)

st.header("Série Histórica")
#Gráfico de série temporal
st.line_chart(df, x='Ano-Mês', y=cl, color=	"#40E0D0")

st.header("Projeção 24 meses à frente")
#Projetando os valores dos indicadores 24 passos à frente
df_proj = md.modelo.vecm(df, cl, dif, coint, tend, pfrente, index)

col1, col2, col3, col4 = st.columns(4)

#Mostrando a projeção
col1.metric("Projeção para 2024-12" , str(dd.dataframe.ult_mes_ano(df_proj, "Ano-Mês", "2024-12", cl)) + tipo, str(dd.dataframe.var_12M(cl, df_proj, "Ano-Mês", "2024-01", "2024-12"))+" %")
col2.metric("Projeção para 2025-12" , str(dd.dataframe.ult_mes_ano(df_proj, "Ano-Mês", "2025-12", cl)) + tipo, str(dd.dataframe.var_12M(cl, df_proj, "Ano-Mês", "2025-01", "2025-12"))+" %")
col3.metric("Máxima Projetada", str(df_proj[cl].max().round(2)) + tipo)
col4.metric("Mínima Projetada", str(df_proj[cl].min().round(2)) + tipo)


st.line_chart(df_proj, x='Ano-Mês', y=cl, color="#0099ff")


#Gráfico de Relações Econômicas
st.header("Relações Econômicas")
st.line_chart(df, x=cl2, y=cl, color="#00FA9A")
