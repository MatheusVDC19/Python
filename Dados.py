import pandas as pd

class DT:

    def obter_dados(caminho):

        df = pd.read_excel(caminho)

        return df

    def ult_dado(coluna, df):

        ult_dado = df[coluna].iloc[-1]

        return ult_dado
    
    def var_dado(coluna, df):

        ult_dado = df[coluna].iloc[-1]
        Pult_dado = df[coluna].iloc[-2]

        var_dado =  ult_dado - Pult_dado

        return var_dado
