import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from Utils import  *
import numpy as np
import os
#Language
selectedLanguage= st.sidebar.selectbox("Choose a Language", ['Italian','English'], 0)
#Name dashboard
# Lambda function to check if a given vaue is from 10 to 20.
langFunc = lambda x : 'App vaccini in Italia' if (selectedLanguage=='Italian') else 'Italian Dashboard Vaccines'
st.title(langFunc(selectedLanguage))
data=DataAnalysis()
#st.dataframe(data.df)
#show list of regions
listRegion=data.df.nome_regione.unique()
langFunc = lambda x : 'Scegliere una regione'  if (selectedLanguage=='Italian') else "Choose a region"
selectedRegion= st.sidebar.selectbox(langFunc(selectedLanguage), listRegion, 0)
#select radio button for type of dose
if (selectedLanguage!='Italian'):
    listTypeDose={'Total','First dose','Second dose'}
    dictTypeDose={'Total': 'totale', 'First dose': 'prima_dose', 'Second dose': 'seconda_dose'}
else:
    listTypeDose={'Totale','Prima dose','Seconda dose'}
    dictTypeDose={'Totale': 'totale', 'Prima dose': 'prima_dose', 'Seconda dose': 'seconda_dose'}
langFunc = lambda x : 'Scegliere tipo di vaccino'  if (selectedLanguage=='Italian') else "Choose Dose Type "
selectedTypeDose = st.sidebar.radio(langFunc(selectedLanguage), list(listTypeDose))
#prediction
##previsione immunità di gregge
today = date.today()
#today + pd.to_timedelta(np.arange(12), 'D')
langFunc = lambda x : '__Immunità di gregge__'  if (selectedLanguage=='Italian') else "__Herd Immunity__"
st.markdown(langFunc(selectedLanguage))
name_cols=st.beta_columns(2)
dfOrder = data.df.sort_index()
totalDoses=data.df[dictTypeDose[selectedTypeDose]].sum()
sumRegions=dfOrder.groupby('data_somministrazione').sum()
langFunc = lambda x : 'Percentuale per Immunità di gregge'  if (selectedLanguage=='Italian') else "Herd Immunity"
immunità = name_cols[0].slider(langFunc(selectedLanguage), min_value=0,max_value=100,value=60, step=5)
langFunc = lambda x : 'Media mobile su numero di giorni precedenti'  if (selectedLanguage=='Italian') else "Average Number on days before"
numDaysBefore=name_cols[1].text_input(langFunc(selectedLanguage),value=7)
daysBefore = date.today() - timedelta(days=int(numDaysBefore)+1)
mean=sumRegions.loc[daysBefore.strftime("%Y-%m-%d"):today.strftime("%Y-%m-%d")]['totale'].mean()
i=0
while ((totalDoses/data.totalPopulation)*100<immunità):
  totalDoses=totalDoses+mean
  i=i+1
langFunc = lambda x : 'Prevista immunità di gregge in data '  if (selectedLanguage=='Italian') else "Predicted herd immunity on "
st.text(langFunc(selectedLanguage)+str((date.today() + timedelta(days=i))))
if(selectedLanguage=='Italian'):
    st.text("Percentuale persone vaccinate con " +selectedTypeDose+' '+str(np.round((totalDoses/data.totalPopulation)*100,3))+"%")
    st.title("Statistiche persone vaccinate")
    st.markdown("__Andamento vaccini in Italia__")    
else:  
    st.text("Percentage "+selectedTypeDose+" vaccinated people " +str(np.round((totalDoses/data.totalPopulation)*100,3))+"%")
    st.title("Statistics vaccinated people")
    st.markdown("__Trend overall Italy__")
fig=px.line(sumRegions,sumRegions.index,y=dictTypeDose[selectedTypeDose],labels={
                        dictTypeDose[selectedTypeDose]: selectedTypeDose,
                        "data_somministrazione": "Date",
                    },title=selectedTypeDose)
st.plotly_chart(fig)  

#***********************************************************************************************************************
langFunc = lambda x : 'Andamento giornaliero in '  if (selectedLanguage=='Italian') else "Daily trend on "
st.title(langFunc(selectedLanguage)+selectedRegion)
regione=data.df[data.df['nome_regione']==selectedRegion]
all_data = regione.sort_index()
if(selectedLanguage=='Italian'):
    fig=px.line(all_data,all_data.index,y=dictTypeDose[selectedTypeDose],labels={
                     dictTypeDose[selectedTypeDose]: selectedTypeDose,
                     "data_somministrazione": "Data",
                 },title=selectedRegion)
else:
     fig=px.line(all_data,all_data.index,y=dictTypeDose[selectedTypeDose],labels={
                     dictTypeDose[selectedTypeDose]: selectedTypeDose,
                     "data_somministrazione": "Date",
                 },title=selectedRegion)
st.plotly_chart(fig)
#show the percentage vaccines for regions
#***********************************************************************************************************************
langFunc = lambda x : 'Percentuale vaccini nelle regioni'  if (selectedLanguage=='Italian') else "Percentage vaccines for regions"
st.title(langFunc(selectedLanguage))
#selectedTypeDose=st.sidebar.selectbox("Choose Dose Type ", list(listTypeDose), 0)
percent=[]
data.sumDf()
for index, row in data.sum_df.iterrows():
    percent.append(row[dictTypeDose[selectedTypeDose]]/data.regionData[row['Region']]*100)
data.sum_df['percentage']=percent
fig = px.bar(data.sum_df, x="Region", y="percentage", color="Region")
if(selectedLanguage!='Italian'):
    fig.update_layout(width=800,height=600,
   title="Percentage "+selectedTypeDose+" vaccines for region ",
    xaxis_title="Regions",
    yaxis_title="Percentage",
    legend_title="Regions Name",
    )
else:
    fig.update_layout(width=800,height=600,
   title="Percentuale "+selectedTypeDose+" vaccini per regione ",
    xaxis_title="Regioni",
    yaxis_title="Percentuale",
    legend_title="Nome delle regioni",
    )
st.plotly_chart(fig)
#***********************************************************************************************************************
#plot yesterday
langFunc = lambda x : 'Vaccini fatti ieri nelle regioni'  if (selectedLanguage=='Italian') else "Yesterday vaccines for regions"
st.title(langFunc(selectedLanguage))
data.yesterdayDf()
#selectedTypeDose= st.selectbox("Choose Dose Type ", list(listTypeDose), 0,key='Yesterday')
fig = px.bar(data.df_Y, x="nome_regione", y=dictTypeDose[selectedTypeDose], color="nome_regione")
if(selectedLanguage!='Italian'):
    fig.update_layout(width=800,height=600,
        xaxis_title="Regions",
        yaxis_title=selectedTypeDose,
        legend_title="Regions Name",
    )
else:
    fig.update_layout(width=800,height=600,
        xaxis_title="Regioni",
        yaxis_title=selectedTypeDose,
        legend_title="Nome delle regioni",
    )
st.plotly_chart(fig)
#***********************************************************************************************************************
#rapporto vaccini consegnati e fatti
langFunc = lambda x : 'Rapporto vaccini fatti su vaccini ricevuti'  if (selectedLanguage=='Italian') else "Ratio vaccines done over delivered"
st.title(langFunc(selectedLanguage))
data.readSummaryData()
fig = px.bar(data.dfSummary, x="nome_area", y=data.dfSummary['dosi_somministrate']/data.dfSummary['dosi_consegnate'], color="nome_area")
if(selectedLanguage!='Italian'):
    fig.update_layout(width=800,height=600,
        xaxis_title="Regions",
        yaxis_title="Ratio vaccine done over delivered",
        legend_title="Regions Name",
    )
else:
    fig.update_layout(width=800,height=600,
        xaxis_title="Regioni",
        yaxis_title="Rapport vaccini fatti su ricevuti",
        legend_title="Nome delle regioni",
    )
st.plotly_chart(fig)
#***********************************************************************************************************************
#Groupby "fascia_anagrafica" selected region
langFunc = lambda x : 'Vaccini fatti ad intervalli d\'età in ' if (selectedLanguage=='Italian') else "Bar plot registry range on "
st.title(langFunc(selectedLanguage)+selectedRegion)
data.readDosingData()
grouped = data.dfDosing[data.dfDosing['nome_regione']==selectedRegion].groupby('fascia_anagrafica').sum()
grouped=grouped.reset_index()
if(dictTypeDose[selectedTypeDose]!='totale'):
    fig = px.bar(grouped, x="fascia_anagrafica", y=dictTypeDose[selectedTypeDose],color='fascia_anagrafica')
    if(selectedLanguage!='Italian'):
        fig.update_layout(width=600,height=300,
            xaxis_title="Registry Range",
            legend_title="Registry Range",
            yaxis_title=selectedTypeDose,
        ) 
    else:
        fig.update_layout(width=600,height=300,
            xaxis_title="Intervalli d\'età",
            legend_title="Intervalli d\'età",
            yaxis_title=selectedTypeDose,
        )           
    st.plotly_chart(fig)
else:
    if(selectedLanguage!='Italian'):
        st.text("Data not found") 
    else:
        st.text("Dati non trovati") 
#type vaccine selected region
#***********************************************************************************************************************
langFunc = lambda x : 'Tipi di vaccino fatti in ' if (selectedLanguage=='Italian') else "Vaccine types made on "
st.title(langFunc(selectedLanguage)+selectedRegion)
vax=data.dfDosing[data.dfDosing['nome_regione']==selectedRegion].groupby('fornitore').sum()
vax=vax.reset_index()
if(dictTypeDose[selectedTypeDose]!='totale'):
    fig = px.bar(vax, x="fornitore", y=dictTypeDose[selectedTypeDose],color='fornitore')
    if(selectedLanguage!='Italian'):
        fig.update_layout(width=600,height=300,
            xaxis_title="Supplier",
            yaxis_title=selectedTypeDose,
            legend_title="Supplier",        
        ) 
    else:
        fig.update_layout(width=600,height=300,
            xaxis_title="Fornitore",
            yaxis_title=selectedTypeDose,
            legend_title="Fornitore",        
        ) 
    st.plotly_chart(fig)
else:
    if(selectedLanguage!='Italian'):
        st.text("Data not found") 
    else:
        st.text("Dati non trovati")   
