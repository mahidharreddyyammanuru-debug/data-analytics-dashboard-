import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="InsightFlow | Professional Data Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    div.stButton > button:first-child {
        background-color: #2e7bcf;
        color: white;
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #1e3d59;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/analytics.png", width=80)
    st.title("InsightFlow")
    st.markdown("---")
    st.subheader("📁 Data Source")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    
    st.markdown("---")
    st.subheader("🛠️ Dashboard Settings")
    theme_color = st.selectbox("Chart Theme", ["plotly_white", "plotly_dark", "ggplot2", "seaborn"])
    
    st.markdown("---")
    st.info("InsightFlow helps you transform raw data into actionable insights instantly.")

# --- MAIN CONTENT ---
if uploaded_file is not None:
    # Loading State
    with st.spinner('Processing your data...'):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # --- HEADER ---
            col_title, col_date = st.columns([3, 1])
            with col_title:
                st.title("📊 Data Analytics Executive Summary")
                st.caption(f"Analyzing: {uploaded_file.name}")
            with col_date:
                st.write(f"**Generated on:**\n{datetime.now().strftime('%Y-%m-%d %H:%M')}")

            st.markdown("---")

            # --- KEY METRICS ---
            st.subheader("📌 Key Performance Indicators")
            m1, m2, m3, m4 = st.columns(4)
            
            numeric_df = df.select_dtypes(include=['number'])
            
            m1.metric("Total Records", f"{len(df):,}")
            m2.metric("Dimensions", f"{df.shape[1]}")
            m3.metric("Numeric Fields", f"{len(numeric_df.columns)}")
            
            missing_pct = (df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
            m4.metric("Data Quality", f"{100 - missing_pct:.1f}%", delta_color="normal")

            # --- DATA EXPLORER ---
            tab1, tab2, tab3 = st.tabs(["🔍 Data Explorer", "📈 Visual Analytics", "🧪 Advanced Stats"])

            with tab1:
                st.subheader("Data Preview")
                st.dataframe(df.head(100), use_container_width=True)
                
                col_down1, col_down2 = st.columns(2)
                with col_down1:
                    st.subheader("Column Types")
                    st.write(df.dtypes.to_frame(name="Type"))
                with col_down2:
                    st.subheader("Missing Values")
                    st.write(df.isna().sum().to_frame(name="Count"))

            with tab2:
                st.subheader("Interactive Visualization Engine")
                
                v_col1, v_col2 = st.columns([1, 3])
                
                with v_col1:
                    chart_type = st.radio("Select Chart Type", 
                                        ["Distribution", "Correlation", "Trend Analysis", "Composition"])
                    
                    all_cols = df.columns.tolist()
                    num_cols = numeric_df.columns.tolist()
                    cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()

                with v_col2:
                    if chart_type == "Distribution":
                        col = st.selectbox("Select Variable", num_cols)
                        fig = px.histogram(df, x=col, marginal="box", 
                                         title=f"Distribution Analysis of {col}",
                                         template=theme_color, color_discrete_sequence=['#2e7bcf'])
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "Correlation":
                        if len(num_cols) >= 2:
                            x_axis = st.selectbox("X Axis", num_cols, index=0)
                            y_axis = st.selectbox("Y Axis", num_cols, index=1)
                            color_by = st.selectbox("Color By (Categorical)", [None] + cat_cols)
                            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by,
                                           title=f"Correlation: {x_axis} vs {y_axis}",
                                           template=theme_color, trendline="ols" if not color_by else None)
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("Insufficient numeric data for correlation.")

                    elif chart_type == "Trend Analysis":
                        y_axis = st.selectbox("Value to Track", num_cols)
                        x_axis = st.selectbox("Time/Sequence Axis", all_cols)
                        fig = px.line(df, x=x_axis, y=y_axis, 
                                    title=f"Trend Analysis: {y_axis} over {x_axis}",
                                    template=theme_color)
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "Composition":
                        if cat_cols:
                            col = st.selectbox("Select Category", cat_cols)
                            val = st.selectbox("Select Value (Optional)", [None] + num_cols)
                            fig = px.pie(df, names=col, values=val, 
                                       title=f"Composition of {col}",
                                       template=theme_color, hole=0.4)
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("No categorical columns found.")

            with tab3:
                st.subheader("Statistical Deep Dive")
                if not numeric_df.empty:
                    st.write("### Descriptive Statistics")
                    st.write(numeric_df.describe().T)
                    
                    if len(num_cols) > 1:
                        st.write("### Correlation Matrix")
                        corr = numeric_df.corr()
                        fig_corr = px.imshow(corr, text_auto=True, aspect="auto",
                                           title="Feature Correlation Heatmap",
                                           color_continuous_scale='RdBu_r')
                        st.plotly_chart(fig_corr, use_container_width=True)
                else:
                    st.info("No numeric data available for statistical analysis.")

        except Exception as e:
            st.error(f"⚠️ An error occurred while processing the file: {e}")

else:
    # --- LANDING PAGE ---
    st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <img src="https://img.icons8.com/fluency/144/000000/cloud-lighting.png" width="120">
            <h1 style="font-size: 3rem;">Ready for Insights?</h1>
            <p style="font-size: 1.2rem; color: #666;">Upload your dataset in the sidebar to generate a professional analytics report instantly.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Pro Tip:** You can upload CSV or Excel files. Once uploaded, use the tabs to switch between different analysis views.")
    
    # Showcase features
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 📊 Visual Engine")
        st.write("Automatic generation of professional charts and graphs.")
    with c2:
        st.markdown("### 🧪 Deep Stats")
        st.write("Full statistical breakdown and correlation matrices.")
    with c3:
        st.markdown("### 🚀 Fast & Secure")
        st.write("Browser-based processing for maximum speed.")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #999; font-size: 0.8rem;">
        InsightFlow Professional Analytics Dashboard | Powered by Streamlit & Python
    </div>
    """,
    unsafe_allow_html=True
)
