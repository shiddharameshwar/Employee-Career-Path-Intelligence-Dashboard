import streamlit as st
import pandas as pd

st.title("Employee Career Path Intelligence Dashboard")

# Load data
df = pd.read_csv("employee_data.csv.csv")

# Show dataset
st.subheader("Employee Dataset")
st.dataframe(df)

# Feature Employee's

df["PromotionGapRatio"] = (
    df["YearsSinceLastPromotion"] /
    (df["YearsAtCompany"] + 1)
)

df["RoleStagnationIndex"] = (
    df["YearsInCurrentRole"] /
    (df["YearsAtCompany"] + 1)
)

df["TrainingIntensityScore"] = (
    df["TrainingTimesLastYear"] /
    (df["YearsAtCompany"] + 1)
)

df["ManagerStabilityIndicator"] = (
    df["YearsWithCurrManager"] /
    (df["YearsAtCompany"] + 1)
)

from sklearn.preprocessing import LabelEncoder

categorical_cols = [
    "Department",
    "JobRole",
    "Gender",
    "BusinessTravel",
    "MaritalStatus",
    "EducationField",
    "OverTime"
]

le = LabelEncoder()

for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

from sklearn.preprocessing import LabelEncoder

categorical_cols = [
    "Department",
    "JobRole",
    "Gender",
    "BusinessTravel",
    "MaritalStatus",
    "EducationField",
    "OverTime"
]

le = LabelEncoder()

for col in categorical_cols:
    df[col] = le.fit_transform(df[col])


from sklearn.preprocessing import StandardScaler

features = [
    "Age",
    "MonthlyIncome",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "PromotionGapRatio",
    "RoleStagnationIndex",
    "TrainingIntensityScore"
]

scaler = StandardScaler()

scaled_data = scaler.fit_transform(df[features])

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4, random_state=42)

df["CareerCluster"] = kmeans.fit_predict(scaled_data)

cluster_labels = {
    0: "Fast-Track Performers",
    1: "Stable Contributors",
    2: "Promotion-Stalled",
    3: "Early Career Explorers"
}

df["ClusterLabel"] = df["CareerCluster"].map(cluster_labels)

df["PromotionGapScore"] = (
    0.4 * df["PromotionGapRatio"] +
    0.3 * df["RoleStagnationIndex"] +
    0.2 * (1 - df["TrainingIntensityScore"]) +
    0.1 * (1 - df["ManagerStabilityIndicator"])
)
df["RetentionOpportunityIndex"] = (
    0.35 * df["JobInvolvement"] +
    0.25 * df["PerformanceRating"] +
    0.25 * (1 - df["Attrition"]) +
    0.15 * df["PromotionGapScore"]
)

st.sidebar.header("Filters")

department = st.sidebar.selectbox(
    "Select Department",
    df["Department"].unique()
)

filtered_df = df[df["Department"] == department]

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Employees",
    len(filtered_df)
)

col2.metric(
    "Avg Promotion Gap",
    round(filtered_df["PromotionGapScore"].mean(), 2)
)

col3.metric(
    "Retention Opportunities",
    len(filtered_df[filtered_df["RetentionOpportunityIndex"] > 2])
)
import plotly.express as px

fig = px.histogram(
    filtered_df,
    x="ClusterLabel",
    color="ClusterLabel",
    title="Career Cluster Distribution"
)

st.plotly_chart(fig)

fig2 = px.box(
    filtered_df,
    x="ClusterLabel",
    y="PromotionGapScore",
    color="ClusterLabel",
    title="Promotion Gap Analysis"
)

st.plotly_chart(fig2)
st.subheader("High Promotion Gap Employees")

high_risk = filtered_df[
    filtered_df["PromotionGapScore"] > 0.6
]

st.dataframe(high_risk)
fig3 = px.scatter(
    filtered_df,
    x="YearsWithCurrManager",
    y="PromotionGapScore",
    color="ClusterLabel",
    title="Manager Stability vs Promotion Gap"
)

st.plotly_chart(fig3)
