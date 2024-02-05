import pandas as pd
import numpy as np
import statsmodels
from statsmodels.tsa.vector_ar.vecm import VECM

class modelo:

    def vecm(df, cl, dif, coint, tend, pfrente, index):
        
        df_temp = df.copy()
        df_proj = df.copy()
        del df_proj["Ano-Mês"]
        
        if cl == "SELIC":
             del df_proj["DES"]
        elif cl == "IPCA":
            del df_proj["DES"]
        elif cl == "CAMB":
            del df_proj["DES"]

        df_proj = np.asarray(df_proj)

        #Instanciando modelo
        model = VECM(df_proj, k_ar_diff=dif, coint_rank=coint,deterministic=tend)
        vecm_res = model.fit()

        #Inserir períodos à frente
        predict = vecm_res.predict(steps=pfrente)

        #Pegando valores gerados pelo modelo
        array_predict = np.empty(pfrente, dtype = float)
        array_datas = np.empty(pfrente, dtype = 'datetime64[D]')

        #Iterando para prencher o DataFrame
        for i in range(pfrente):
        
            array_predict[i] = predict[i,index].round(2)

        for i in range(pfrente):

            prox_data = df_temp['Ano-Mês'].iloc[-1] + pd.DateOffset(months=i+1)
            array_datas[i] = str(prox_data)

        #Concatenando os DFs
        proj = pd.DataFrame({"Ano-Mês": array_datas,
                            cl : array_predict})

        proj.set_index("Ano-Mês",inplace = True)

        proj["Ano-Mês"] = proj.index

        
        #df = pd.concat([df, proj], ignore_index = False)
        #df["Ano-Mês"] = df.index

        return proj
