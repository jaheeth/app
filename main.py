import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Lanka Medical Center - Healthcare Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown('<h1 class="main-header">🏥 Lanka Medical Center</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; color: #666;">Healthcare Data Analytics Dashboard</h2>', unsafe_allow_html=True)

# Import analytics modules
from data_generator import generate_sample_data
from analytics_engine import AnalyticsEngine
from visualization_utils import create_visualizations

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Sidebar for navigation
st.sidebar.title("📊 Analytics Modules")
module = st.sidebar.selectbox(
    "Select Analysis Module",
    ["Dashboard Overview", "Most Utilized Services", "Doctor Performance", 
     "Patient Trends", "Patient Behavior", "Billing & Revenue"]
)

# Date range selector
st.sidebar.title("📅 Date Range")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime.now() - timedelta(days=365), datetime.now()),
    max_value=datetime.now()
)

# Load or generate data
@st.cache_data
def load_data():
    """Load or generate sample data for the application"""
    try:
        # Try to load existing data
        conn = sqlite3.connect('hospital_data.db')
        patients = pd.read_sql_query("SELECT * FROM patients", conn)
        conn.close()
        if len(patients) > 0:
            return True
    except:
        pass
    
    # Generate sample data if none exists
    generate_sample_data()
    return True

# Load data
if not st.session_state.data_loaded:
    with st.spinner("Loading healthcare data..."):
        load_data()
        st.session_state.data_loaded = True

# Initialize analytics engine
analytics = AnalyticsEngine()

# Main content based on selected module
if module == "Dashboard Overview":
    st.header("📈 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_patients = analytics.get_total_patients()
        st.metric("Total Patients", f"{total_patients:,}")
    
    with col2:
        total_revenue = analytics.get_total_revenue()
        st.metric("Total Revenue", f"Rs. {total_revenue:,.2f}")
    
    with col3:
        total_appointments = analytics.get_total_appointments()
        st.metric("Total Appointments", f"{total_appointments:,}")
    
    with col4:
        avg_revenue_per_patient = analytics.get_avg_revenue_per_patient()
        st.metric("Avg Revenue/Patient", f"Rs. {avg_revenue_per_patient:,.2f}")
    
    # Overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Trend (Last 12 Months)")
        revenue_trend = analytics.get_revenue_trend()
        fig = px.line(revenue_trend, x='month', y='revenue', 
                     title='Monthly Revenue Trend')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Service Utilization Distribution")
        service_util = analytics.get_service_utilization()
        fig = px.pie(service_util, values='count', names='service_name',
                     title='Services by Utilization')
        st.plotly_chart(fig, use_container_width=True)

elif module == "Most Utilized Services":
    st.header("🔬 Most Utilized Services Analysis")
    
    # Service utilization metrics
    service_analysis = analytics.analyze_service_utilization()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Most Utilized Services")
        st.dataframe(service_analysis['top_services'])
        
        st.subheader("Service Revenue Analysis")
        revenue_by_service = analytics.get_revenue_by_service()
        fig = px.bar(revenue_by_service.head(10), x='service_name', y='total_revenue',
                     title='Top 10 Services by Revenue')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Service Utilization Trends")
        service_trends = analytics.get_service_trends()
        fig = px.line(service_trends, x='month', y='appointments', 
                     color='service_name', title='Service Utilization Trends')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Department-wise Service Distribution")
        dept_services = analytics.get_department_service_distribution()
        fig = px.treemap(dept_services, path=['department_name', 'service_name'], 
                        values='count', title='Service Distribution by Department')
        st.plotly_chart(fig, use_container_width=True)

elif module == "Doctor Performance":
    st.header("👨‍⚕️ Doctor Performance Analysis")
    
    # Doctor performance metrics
    doctor_analysis = analytics.analyze_doctor_performance()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Doctors by Revenue")
        st.dataframe(doctor_analysis['top_doctors'])
        
        st.subheader("Doctor Performance Comparison")
        performance_metrics = analytics.get_doctor_performance_metrics()
        fig = px.scatter(performance_metrics, x='appointments_handled', y='revenue_generated',
                        size='patient_satisfaction', hover_data=['doctor_name'],
                        title='Doctor Performance: Appointments vs Revenue')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Doctor Revenue Trends")
        doctor_revenue_trends = analytics.get_doctor_revenue_trends()
        fig = px.line(doctor_revenue_trends, x='month', y='revenue', 
                     color='doctor_name', title='Monthly Revenue by Doctor')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Department-wise Doctor Performance")
        dept_performance = analytics.get_department_doctor_performance()
        fig = px.bar(dept_performance, x='department_name', y='avg_revenue_per_doctor',
                     title='Average Revenue per Doctor by Department')
        st.plotly_chart(fig, use_container_width=True)

elif module == "Patient Trends":
    st.header("📅 Patient Trends Analysis")
    
    # Patient trend analysis
    trend_analysis = analytics.analyze_patient_trends()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Appointment Trends")
        daily_trends = analytics.get_daily_appointment_trends()
        fig = px.line(daily_trends, x='date', y='appointments', 
                     title='Daily Appointment Trends')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Weekly Appointment Patterns")
        weekly_patterns = analytics.get_weekly_appointment_patterns()
        fig = px.bar(weekly_patterns, x='day_of_week', y='appointments',
                     title='Appointments by Day of Week')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Monthly Appointment Trends")
        monthly_trends = analytics.get_monthly_appointment_trends()
        fig = px.line(monthly_trends, x='month', y='appointments',
                     title='Monthly Appointment Trends')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Seasonal Appointment Analysis")
        seasonal_analysis = analytics.get_seasonal_appointment_analysis()
        fig = px.bar(seasonal_analysis, x='season', y='appointments',
                     title='Appointments by Season')
        st.plotly_chart(fig, use_container_width=True)

elif module == "Patient Behavior":
    st.header("👥 Patient Behavior Analysis")
    
    # Patient behavior analysis
    behavior_analysis = analytics.analyze_patient_behavior()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patient Visit Frequency Distribution")
        visit_frequency = analytics.get_patient_visit_frequency()
        fig = px.histogram(visit_frequency, x='visit_count', nbins=20,
                          title='Distribution of Patient Visit Frequency')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Patient Spending Patterns")
        spending_patterns = analytics.get_patient_spending_patterns()
        fig = px.scatter(spending_patterns, x='total_visits', y='total_spent',
                        size='avg_spend_per_visit', title='Patient Spending vs Visits')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Patient Segmentation by Value")
        patient_segments = analytics.get_patient_segments()
        fig = px.pie(patient_segments, values='count', names='segment',
                     title='Patient Segmentation')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Service Preference Analysis")
        service_preferences = analytics.get_service_preferences()
        fig = px.bar(service_preferences, x='service_name', y='preference_score',
                     title='Patient Service Preferences')
        st.plotly_chart(fig, use_container_width=True)

elif module == "Billing & Revenue":
    st.header("💰 Billing & Revenue Analysis")
    
    # Revenue analysis
    revenue_analysis = analytics.analyze_revenue()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Revenue Trends")
        monthly_revenue = analytics.get_monthly_revenue_trends()
        fig = px.line(monthly_revenue, x='month', y='revenue',
                     title='Monthly Revenue Trends')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Revenue by Department")
        dept_revenue = analytics.get_revenue_by_department()
        fig = px.bar(dept_revenue, x='department_name', y='total_revenue',
                     title='Revenue by Department')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Service Type")
        service_revenue = analytics.get_revenue_by_service_type()
        fig = px.pie(service_revenue, values='revenue', names='service_type',
                     title='Revenue Distribution by Service Type')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Revenue per Doctor Analysis")
        doctor_revenue = analytics.get_revenue_per_doctor()
        fig = px.bar(doctor_revenue.head(15), x='doctor_name', y='total_revenue',
                     title='Top 15 Doctors by Revenue')
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🏥 Lanka Medical Center (PVT) Ltd | Developed by Spera Labs (PVT) Ltd</p>
    <p>Data last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
