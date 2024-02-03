import pandas as pd

class dataframe:

    def extracao_bcb(codigo, data_inicio, data_fim):

        url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}&dataFinal={}'.format(codigo, data_inicio, data_fim)
        df = pd.read_json(url)
        df.set_index('data', inplace = True)
        df.index.name = 'Ano-Mês'
        df.index = pd.to_datetime(df.index, dayfirst= True)

        return df
    
    def unir_DFs(df1, df2, df3):

        df12 = pd.merge(df1, df2, how='inner', on='Ano-Mês')
        df23 = pd.merge(df2, df3, how='inner', on='Ano-Mês')
        df = pd.merge(df12, df23, how='inner', on='Ano-Mês' )

        return df
    

    def ult_dado(coluna, df):

        ult_dado = df[coluna].iloc[-1]

        return ult_dado
    
    
    def var_dado(coluna, df):

        ult_dado = df[coluna].iloc[-1]
        Pult_dado = df[coluna].iloc[-2]

        var_dado =  ult_dado - Pult_dado

        return var_dado
