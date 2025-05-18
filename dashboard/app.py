import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from io import BytesIO
from fpdf import FPDF
import os
import sys

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from features.feature_engineering import generate_features

model = joblib.load('models/churn_model.pkl')
pastel_colors = px.colors.qualitative.Pastel1

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

# --- Helper Functions ---
def generate_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Churn Prediction Report", ln=True, align='C')
    pdf.ln(10)
    for i in range(min(30, len(dataframe))):
        line = ', '.join([str(x) for x in dataframe.iloc[i]])
        pdf.multi_cell(0, 10, txt=line)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

def show_dashboard():
    df_original = st.session_state['df']

    # Theme
    theme = st.sidebar.radio("Select Theme", ("Light", "Dark"))
    if theme == "Dark":
        st.markdown("""<style> .main { background-color: #1e1e1e; color: white; } </style>""", unsafe_allow_html=True)

    # Filters
    segment_filter = st.sidebar.multiselect("Filter by Segment", options=df_original['segment'].unique(), default=df_original['segment'].unique())
    region_filter = st.sidebar.multiselect("Filter by Region", options=df_original['region'].unique(), default=df_original['region'].unique())
    df = df_original[df_original['segment'].isin(segment_filter) & df_original['region'].isin(region_filter)]

    st.title("Customer Churn Prediction Dashboard")
    churn_rate = df['churn_prediction'].mean()
    st.metric("Predicted Churn Rate", f"{churn_rate * 100:.1f}%")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Top Customers", "Raw Data"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names='segment', title="Customer Segment Distribution", hole=0.4, color_discrete_sequence=pastel_colors)
            fig1.update_traces(textinfo='percent+label', pull=[0.05] * len(df['segment'].unique()))
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            region_churn = df.groupby('region')['churn_prediction'].mean().reset_index()
            fig2 = px.bar(region_churn, x='region', y='churn_prediction', color='region', title="Avg Churn Rate by Region", color_discrete_sequence=pastel_colors)
            fig2.update_layout(transition_duration=500)
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Recent Buyer Trend Over Time")
        df['last_purchase'] = pd.to_datetime(df['last_purchase'], errors='coerce')
        buyer_trend = df.groupby(df['last_purchase'].dt.to_period('M'))['recent_buyer'].sum().reset_index()
        buyer_trend['last_purchase'] = buyer_trend['last_purchase'].astype(str)
        fig3 = px.line(buyer_trend, x='last_purchase', y='recent_buyer', markers=True)
        fig3.update_traces(line=dict(color=pastel_colors[3], width=2), marker=dict(color=pastel_colors[1], size=8))
        fig3.update_layout(transition_duration=500)
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.subheader("Top 10 Customers by Spending")
        top_spenders = df.sort_values(by='total_spent', ascending=False).head(10)
        fig4 = px.bar(top_spenders, x='customer_id', y='total_spent', color='total_spent',
                      title="Top 10 Customers", color_continuous_scale=["#37fbb3", "#ffdac1", "#fd2234"])
        fig4.update_layout(transition_duration=500)
        st.plotly_chart(fig4, use_container_width=True)

    with tab4:
        st.subheader("Data with Churn Predictions")
        st.dataframe(df)

    st.download_button("Download Results as CSV", df.to_csv(index=False), "churn_predictions.csv")

    if st.button("Download PDF Report"):
        pdf = generate_pdf(df)
        st.download_button("Click to Download PDF", pdf, file_name="churn_report.pdf")

    st.markdown("---")
    if st.button("Upload Another CSV"):
        reset_app()

# --- Main Logic ---
if 'df' not in st.session_state:
    uploaded_file = st.file_uploader("Upload customer data (CSV)", type="csv")

    if uploaded_file:
        raw_df = pd.read_csv(uploaded_file)
        df = generate_features(raw_df)

        try:
            df['recent_buyer'] = df['recent_buyer'].astype(int)
            df['churn_prediction'] = model.predict(df[['total_spent', 'visits', 'avg_spent_per_visit', 'recent_buyer', 'segment_encoded', 'region_encoded']])
            st.session_state['df'] = df
            st.rerun()
        except KeyError as e:
            st.error(f"Missing required columns: {e}")
    else:
        st.info("Please upload a CSV file to begin.")
else:
    show_dashboard()