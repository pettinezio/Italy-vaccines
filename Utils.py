import pandas as pd
from datetime import date, timedelta
import streamlit as st
class DataAnalysis: 
    def __init__(self): # constructor method
        print('Constructor invoked')
        self.df=self.readVaccineData()
        self.regionData=self.readRegionsData()
    def readVaccineData(self):
        url = 'https://github.com/italia/covid19-opendata-vaccini/blob/master/dati/somministrazioni-vaccini-summary-latest.csv?raw=true'
        df = pd.read_csv(url, index_col=0)        
        mid = df['nome_area']
        #convert name of column flsor have match with file excel regioni
        df.drop(labels=['nome_area'], axis=1, inplace = True)
        df.insert(1, 'nome_regione', mid)
        df.drop(labels=['area'], axis=1, inplace = True)
        df[(df['nome_regione']=="Provincia Autonoma Bolzano / Bozen")|(df['nome_regione']=="Valle d'Aosta / Vallée d'Aoste") ]
        df['nome_regione']=df['nome_regione'].str.replace('Provincia Autonoma Bolzano / Bozen','Trentino-Alto Adige')
        df['nome_regione']=df['nome_regione'].str.replace('Provincia Autonoma Trento','Trentino-Alto Adige')
        df['nome_regione']=df['nome_regione'].str.replace("Valle d'Aosta / Vallée d'Aoste","Valle d'Aosta/Vallée d'Aoste")
        #st.dataframe(df.head(4))
        #show list of regions
        return df
    def readRegionsData(self):
        #read population for regions from a file
        regioni=pd.read_excel("regioni.xlsx")
        regioni=regioni.drop(0)
        regioni_s=regioni[['Regioni','Popolazione fine periodo']]
        regioni_s=regioni_s.dropna()
        dict_region={}
        self.totalPopulation=0
        for index, row in regioni_s.iterrows():
            dict_region[row[0]] = row[1]
            self.totalPopulation = self.totalPopulation + row[1]
        return dict_region
    def readSummaryData(self):
        url = 'https://github.com/italia/covid19-opendata-vaccini/blob/master/dati/vaccini-summary-latest.csv?raw=true'
        self.dfSummary=pd.read_csv(url, index_col=False)
    
    def sumDf(self):
        self.sum_df=self.df.groupby(["nome_regione"]).sum()
        self.sum_df=self.sum_df.reset_index()
        self.sum_df=self.sum_df.rename({'nome_regione': 'Region'}, axis=1)
        
    def yesterdayDf(self):
        yesterday = date.today() - timedelta(days=1)
        d1 = yesterday.strftime("%Y-%m-%d")
        self.df_Y=self.df.loc[d1]       