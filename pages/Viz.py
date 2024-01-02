import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import date
import plotly.express as px
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="Data Viz",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Data Viz")

# Load data from csv
def load_csv_data():
    df = pd.read_csv("clean_data.csv")
    return df

df = load_csv_data()

st.dataframe(df, use_container_width=True, hide_index=True,)

addcol1, addcol2 = st.columns([5, 5])

addcol1.subheader("Location Distribution")
location_count = df["location"].value_counts().reset_index(name='counts')
fig = px.treemap(location_count, path= ["location"], values="counts", color_continuous_scale="sunset")
addcol1.plotly_chart(fig)

addcol2.subheader("Emission Type Distribution")
emission_count = df["emission_type"].value_counts().reset_index(name='counts')

fig = px.pie(emission_count, names= "emission_type", values="counts", color_discrete_sequence=px.colors.sequential.RdBu)
addcol2.plotly_chart(fig)

#Category level averages
addcol1.subheader("Category level CO2f averages")
df_avg = df.groupby(['cat_1'],as_index=False)['CO2f'].mean().rename(columns={'CO2f':'Avg_CO2f'})

fig = px.bar(df_avg, x= "cat_1", y="Avg_CO2f",
                      )
addcol1.plotly_chart(fig)

#Category level uncertainity averages
df['uncertainty_float'] = df['uncertainty'].str.rstrip('%').astype('float') / 100.0
addcol2.subheader("Category 1 Uncertainity averages")
df_avg = df.groupby(['cat_1'],as_index=False)['uncertainty_float'].mean().rename(columns={'uncertainty_float':'Avg_uncertainty'})

fig = px.bar(df_avg, x= "cat_1", y="Avg_uncertainty",)
addcol2.plotly_chart(fig)