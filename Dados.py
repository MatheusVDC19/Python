import pandas as pd

class dataframe:

    def extracao_bcb(codigo, data_inicio, data_fim):

        url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}&dataFinal={}'.format(codigo, data_inicio, data_fim)
        df = pd.read_json(url)
        df.set_index('data', inplace = True)
        df.index.name = 'Ano-Mês'
        df.index = pd.to_datetime(df.index, dayfirst= True)

        return df
    
    
    def unir_DFs(df1, cl1, df2, cl2, df3, cl3):

        df12 = pd.merge(df1, df2, how='inner', on='Ano-Mês')
        df23 = pd.merge(df2, df3, how='inner', on='Ano-Mês')
        df = pd.merge(df12, df23, how='inner', on='Ano-Mês', suffixes=(".",""))

        df.drop(columns=[cl2+'.'], inplace= True)

        df['Ano-Mês'] = df.index

        return df
    

    def ult_dado(coluna, df):

        ult_dado = df[coluna].iloc[-1]

        return ult_dado
    
    
    def var_dado(coluna, df):

        ult_dado = df[coluna].iloc[-1]
        Pult_dado = df[coluna].iloc[-2]

        var_dado =  ult_dado - Pult_dado

        return var_dado
    
    
    def ult_mes_ano (df, cl_data, data, cl):

        valor = df.loc[df[cl_data]==data, [cl]].values.round(2)

        valor = valor [0,0]

        return valor

    def var_12M(cl, df, cl_data, dataIN, dataOUT):

        valorIN = dataframe.ult_mes_ano (df, cl_data, dataIN, cl)
        valorOUT = dataframe.ult_mes_ano (df, cl_data, dataOUT, cl)

        var_12M = (((valorOUT - valorIN) / valorIN)*100).round(2)

        return var_12M
