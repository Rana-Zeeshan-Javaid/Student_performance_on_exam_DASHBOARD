import numpy as np 
import pandas as pd 
import streamlit as st 
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("StudentsPerformance.csv")
st.title("Student's Performance Analysis")

st.markdown("A high-level interactive analysis of student performance.")
st.sidebar.header("Feature Selection")
gender_feature = st.sidebar.multiselect("Select Gender", options=df["gender"].unique())
race_feature = st.sidebar.multiselect("Select Race/Ethnicity", options=df["race/ethnicity"].unique())
parental_edu_feature = st.sidebar.multiselect("Select Parental Level of Education", options=df["parental level of education"].unique())
test_prep_feature = st.sidebar.multiselect("Select Test Preparation Course", options=df["test preparation course"].unique())
df_filtered = df[
    (df["gender"].isin(gender_feature)) &
    (df["race/ethnicity"].isin(race_feature)) &
    (df["parental level of education"].isin(parental_edu_feature)) &
    (df["test preparation course"].isin(test_prep_feature))
]
st.sidebar.header("Visualization Type")
plot_types=["Bar Plot","Line Plot","Dot Plot","Scatter Plot","Pairplot"]
selected_plots=st.sidebar.multiselect("Select plots:",plot_types)
if not df_filtered.empty:
    if "Bar Plot" in selected_plots:
        st.subheader("Average Scores by Gender")
        fig_bar=px.bar(
            df_filtered.groupby("gender")[["math score","reading score","writing score"]].mean().reset_index(),
            x="gender",
            y=["math score","reading score","writing score"],
            barmode="group",
            title="Average Scores by Gender",
            labels={"value":"Average Score","variable":"Subjects"},
            color_discrete_map={"math score":"blue","reading score":"green","writing score":"red"},
        )
        st.plotly_chart(fig_bar)

    if "Line Plot" in selected_plots:
        st.subheader("Scores by Parental Education Level")
        fig_line = px.line(
            df_filtered.groupby("parental level of education")[["math score","reading score","writing score"]].mean().reset_index(),
            x="parental level of education",
            y=["math score","reading score","writing score"],
            markers=True,
            title="Scores Trend by Parental Education",
            labels={"value":"Average Score","variable":"Subjects"},
        )
        st.plotly_chart(fig_line)

    if "Dot Plot" in selected_plots:
        st.subheader("Relationship Between Reading And Writing Scores")
        fig_dot=px.scatter(
            df_filtered, 
            x="reading score", 
            y="writing score", 
            color="gender",
            title="Relationship Between Reading And Writing Scores",
        )
        st.plotly_chart(fig_dot)

    if "Scatter Plot" in selected_plots:
        st.subheader("Math vs Reading Score")
        fig_scatter=px.scatter(
            df_filtered, 
            x="math score", 
            y="reading score", 
            color="gender",
            size="writing score",
            title="Relationship Between Math and Reading Scores",
        )
        st.plotly_chart(fig_scatter)

    if "Pairplot" in selected_plots:
        st.subheader("Pairplot: Subject Score Relationships")
        fig_pairplot = sns.pairplot(df_filtered, hue="gender", palette="husl")
        st.pyplot(fig_pairplot)
else:
    st.warning("No data to display.Please adjust your selection.")

