import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="MCA E-Consultation Insights", page_icon="⚖️", layout="wide")

st.title("⚖️ MCA Legal Sentiment & Consultation Dashboard")
st.markdown("Automated sentiment and intent extraction for public consultation feedback on draft policies.")

# Load analyzed data
@st.cache_data
def load_data():
    return pd.read_csv("mca_analyzed_comments.csv")

try:
    df = load_data()
except Exception as e:
    st.error("Could not find 'mca_analyzed_comments.csv'. Please make sure nlp_analysis.py has run successfully!")
    st.stop()

# --- TOP METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)

total_comments = len(df)
support_count = len(df[df["legal_intent"] == "Support"])
oppose_count = len(df[df["legal_intent"] == "Oppose"])
amend_count = len(df[df["legal_intent"] == "Amendment Suggestion"])

col1.metric("Total Submissions", total_comments)
col2.metric("Support", f"{support_count} ({round(support_count/total_comments*100)}%)")
col3.metric("Oppose", f"{oppose_count} ({round(oppose_count/total_comments*100)}%)")
col4.metric("Amendment Suggestions", f"{amend_count} ({round(amend_count/total_comments*100)}%)")

st.divider()

# --- CHARTS ROW ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Sentiment Breakdown by Legal Clause")
    clause_chart = px.histogram(
        df, 
        x="target_clause", 
        color="legal_intent", 
        barmode="group",
        color_discrete_map={
            "Support": "#2ecc71", 
            "Oppose": "#e74c3c", 
            "Amendment Suggestion": "#f39c12", 
            "Neutral / Clarification": "#95a5a6"
        }
    )
    st.plotly_chart(clause_chart, use_container_width=True)

with chart_col2:
    st.subheader("👥 Feedback by Stakeholder Type")
    stakeholder_chart = px.pie(
        df, 
        names="stakeholder_type", 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(stakeholder_chart, use_container_width=True)

st.divider()

# --- SEARCHABLE DATA TABLE ---
st.subheader("🔍 Public Comments Explorer")

# Filter by clause or intent
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    selected_clause = st.selectbox("Filter by Clause:", ["All"] + list(df["target_clause"].unique()))
with filter_col2:
    selected_intent = st.selectbox("Filter by Legal Intent:", ["All"] + list(df["legal_intent"].unique()))

filtered_df = df.copy()
if selected_clause != "All":
    filtered_df = filtered_df[filtered_df["target_clause"] == selected_clause]
if selected_intent != "All":
    filtered_df = filtered_df[filtered_df["legal_intent"] == selected_intent]

st.dataframe(
    filtered_df[["comment_id", "stakeholder_type", "target_clause", "legal_intent", "sentiment_score", "comment_text"]],
    use_container_width=True
)