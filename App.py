import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from Utils import  *
import os
st.title('Vaccines Dashboard')
data=DataAnalysis()
#st.dataframe(data.df)
#show list of regions
listRegion=data.df.nome_regione.unique()
selectedRegion= st.selectbox("Choose a region", listRegion, 0)
#select radio button for type of dose
listTypeDose={'Total','First dose','Second dose'}
selectedTypeDose = st.radio("Choose Dose Type ", list(listTypeDose))
dictTypeDose={'Total': 'totale', 'First dose': 'prima_dose', 'Second dose': 'seconda_dose'}
regione=data.df[data.df['nome_regione']==selectedRegion]
all_data = regione.sort_index()
fig=px.line(all_data,all_data.index,y=dictTypeDose[selectedTypeDose],labels={
                     dictTypeDose[selectedTypeDose]: selectedTypeDose,
                     "data_somministrazione": "Date",
                 },title=selectedRegion)
st.plotly_chart(fig)

##show the percentage vaccines for regions
st.title("Plot Percentage vaccines for regions")
selectedTypeDose=st.selectbox("Choose Dose Type ", list(listTypeDose), 0)
percent=[]
data.sumDf()
for index, row in data.sum_df.iterrows():
    percent.append(row[dictTypeDose[selectedTypeDose]]/data.regionData[row['Region']]*100)
data.sum_df['percentage']=percent
fig = px.bar(data.sum_df, x="Region", y="percentage", color="Region")
fig.update_layout(width=800,height=600,
   title="Percentage "+selectedTypeDose+" vaccines for region ",
    xaxis_title="Regions",
    yaxis_title="Percentage",
    legend_title="Regions Name",
)
st.plotly_chart(fig)

#plot yesterday
st.title("Plot Yesterday vaccines for regions")
data.yesterdayDf()
selectedTypeDose= st.selectbox("Choose Dose Type ", list(listTypeDose), 0,key='Yesterday')
fig = px.bar(data.df_Y, x="nome_regione", y=dictTypeDose[selectedTypeDose], color="nome_regione")
fig.update_layout(width=800,height=600,
    xaxis_title="Regions",
    yaxis_title=selectedTypeDose,
    legend_title="Regions Name",
)
st.plotly_chart(fig)

#rapporto vaccini consegnati e fatti
st.title("Plot ratio vaccine done over delivered")
data.readSummaryData()
fig = px.bar(data.dfSummary, x="nome_area", y=data.dfSummary['dosi_somministrate']/data.dfSummary['dosi_consegnate'], color="nome_area")
fig.update_layout(width=800,height=600,
    xaxis_title="Regions",
    yaxis_title="Ratio vaccine done over delivered",
    legend_title="Regions Name",
)
st.plotly_chart(fig)



##previsione immunità di gregge
st.title("Statistics vaccinated people")
totalDoses=data.df[dictTypeDose[selectedTypeDose]].sum()
#print(totalDoses)
#print(totalPopulation)
st.text("Percentage "+selectedTypeDose+" vaccinated people " +str((totalDoses/data.totalPopulation)*100))
dfOrder = data.df.sort_index()
sumRegions=dfOrder.groupby('data_somministrazione').sum()
st.markdown("__Trend overall Italy__")
fig=px.line(sumRegions,sumRegions.index,y=dictTypeDose[selectedTypeDose],labels={
                     dictTypeDose[selectedTypeDose]: selectedTypeDose,
                     "data_somministrazione": "Date",
                 },title=dictTypeDose[selectedTypeDose])
st.plotly_chart(fig)
#prediction
today = date.today()
#today + pd.to_timedelta(np.arange(12), 'D')
st.markdown("__Herd Immunity__")
name_cols=st.beta_columns(2)
immunità = name_cols[0].slider('Herd immunity', min_value=0,max_value=100,value=60, step=5)
numDaysBefore=name_cols[1].text_input("Number average days before",value=7)

daysBefore = date.today() - timedelta(days=int(numDaysBefore)+1)
mean=sumRegions.loc[daysBefore.strftime("%Y-%m-%d"):today.strftime("%Y-%m-%d")]['totale'].mean()
i=0
while ((totalDoses/data.totalPopulation)*100<immunità):
  totalDoses=totalDoses+mean
  i=i+1
st.text("Date "+str((date.today() + timedelta(days=i))))
st.text("Percentage "+selectedTypeDose+" vaccinated people " +str((totalDoses/data.totalPopulation)*100))
