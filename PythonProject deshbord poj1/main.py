import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from plotly.express import colors

###########################################################
@st.cache_data
def load_data():
    df=pd.read_csv('netflix_titles.csv')
    df["date_added"]=pd.to_datetime(df["date_added"],errors="coerce")
    df["year_added"]=df["date_added"].dt.year
    return df

df=load_data()
st.set_page_config("Netflix Deshbard",layout="wide")
st.header("Netflix Deshbard")
# st.write(df)
#########################################################################
st.sidebar.header("Dashboard filters")
type_filter=st.sidebar.multiselect("select content type",options=df["type"].dropna().unique(),default=df["type"].dropna().unique())

cnt_filter = st.sidebar.multiselect("select country", options=df["country"].str.split(",").explode().dropna().unique())

rating_filter = st.sidebar.multiselect("select rating", options=df["rating"].dropna().unique())

year_filter = st.sidebar.slider(
    "select release year",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (2000, 2023)
)


filter_df=df[df["type"].isin(type_filter)]
# st.write(filter_df)
if cnt_filter:
    filter_df=filter_df[filter_df["country"].isin(cnt_filter)]

if rating_filter:
    filter_df=filter_df[filter_df["rating"].isin(rating_filter)]

import pandas as pd
import plotly.express as px
import streamlit as st

if year_filter:
    filter_df = filter_df[
        (filter_df["release_year"] >= year_filter[0]) &
        (filter_df["release_year"] <= year_filter[1])
    ]

st.divider()
#####################################################
st.subheader("Key Metrics")
col1,col2,col3,col4=st.columns(4)
totcon=len(filter_df)
totmov=len(filter_df[filter_df["type"]=="Movie"])
tottvshow=len(filter_df[filter_df["type"]=="TV Show"])
totcnt=len(filter_df["country"].str.split(",").explode().dropna().unique())
col1.metric("Total Content",totcon)
col2.metric("Total Movies",totmov)
col3.metric("Total TV Shows",tottvshow)
col4.metric("Total Countries",totcnt)
st.divider()
col1,col2=st.columns(2)
with col1:
    st.subheader("Movies vs TV Shows")
    t=filter_df["type"].value_counts()
    fig = px.pie(values=t.values, names=t.index,
                 color_discrete_sequence=px.colors.sequential.Reds)
    st.plotly_chart(fig, width="stretch")
with col2:
    st.subheader("Content Added Over Years")
    t = filter_df["year_added"].value_counts().sort_index()
    fig = px.line(x=t.index, y=t.values, markers=True)
    fig.update_layout(xaxis_title="Year", yaxis_title="Titles Added")
    st.plotly_chart(fig, width="stretch")

###############################################################
st.divider()
col1,col2=st.columns(2)
with col1:
    st.subheader("top countries producing content added")
    cnt_counts=filter_df["country"].str.split(",").explode().value_counts().head(10)
    # st.write(cnt_counts)
    fig=px.bar(x=cnt_counts.values,y=cnt_counts.index,orientation="h",
    color=cnt_counts.values,color_continuous_scale="Reds"
               )
    fig.update_layout(xaxis_title="count",yaxis_title="country")
    st.plotly_chart(fig,width="stretch")
    # st.write(cnt_counts)

with col2:
    rating_counts=filter_df["rating"].value_counts()
    fig=px.bar(x=rating_counts,y=rating_counts.index,color_continuous_scale="Reds")
    fig.update_layout(xaxis_title="rating",yaxis_title="count")
    st.plotly_chart(fig,width="stretch")
    # st.write(rating_counts)

####################
st.divider()
st.subheader("top genres")
genres=filter_df["listed_in"].str.split(",").explode().value_counts()
fig=px.bar(x=genres.index,y=genres.values,color=genres.values,color_continuous_scale="Reds")
fig.update_layout(xaxis_title="genre",yaxis_title="count")
st.plotly_chart(fig,width="stretch")
# st.write(genres)

st.divider()
st.subheader("global distribution of content")
cnt_counts=filter_df["country"].str.split(",").explode().value_counts().reset_index()
# st.write(cnt_counts)
cnt_counts.columns=["country","count"]
fig=px.choropleth(cnt_counts,
                  locations="country",
                  locationmode="country names",
                  color="count",
                  color_continuous_scale="Reds")
st.plotly_chart(fig,width="stretch")
st.write(cnt_counts)

########################
st.divider()
st.subheader("dataset preview")
srcstr=st.text_input("search title")
if srcstr:
    filter_df=filter_df[filter_df["title"].str.contains(srcstr,case=False)]
    st.dataframe(filter_df.head(100))