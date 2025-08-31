import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_visualizations():
    """Placeholder for visualization utilities"""
    pass

def create_revenue_trend_chart(data):
    """Create revenue trend chart"""
    fig = px.line(data, x='month', y='revenue', 
                  title='Monthly Revenue Trend',
                  labels={'month': 'Month', 'revenue': 'Revenue (Rs.)'})
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (Rs.)",
        hovermode='x unified'
    )
    return fig

def create_service_utilization_chart(data):
    """Create service utilization chart"""
    fig = px.pie(data, values='count', names='service_name',
                  title='Service Utilization Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_doctor_performance_scatter(data):
    """Create doctor performance scatter plot"""
    fig = px.scatter(data, x='appointments_handled', y='revenue_generated',
                     size='patient_satisfaction', hover_data=['doctor_name'],
                     title='Doctor Performance: Appointments vs Revenue')
    fig.update_layout(
        xaxis_title="Appointments Handled",
        yaxis_title="Revenue Generated (Rs.)",
        hovermode='closest'
    )
    return fig

def create_appointment_trends_chart(data):
    """Create appointment trends chart"""
    fig = px.line(data, x='date', y='appointments', 
                  title='Daily Appointment Trends')
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Appointments",
        hovermode='x unified'
    )
    return fig

def create_weekly_patterns_chart(data):
    """Create weekly patterns chart"""
    fig = px.bar(data, x='day_of_week', y='appointments',
                  title='Appointments by Day of Week')
    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Number of Appointments"
    )
    return fig

def create_patient_segmentation_chart(data):
    """Create patient segmentation chart"""
    fig = px.pie(data, values='count', names='segment',
                  title='Patient Segmentation by Value')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_revenue_by_department_chart(data):
    """Create revenue by department chart"""
    fig = px.bar(data, x='department_name', y='total_revenue',
                  title='Revenue by Department')
    fig.update_layout(
        xaxis_title="Department",
        yaxis_title="Total Revenue (Rs.)",
        xaxis_tickangle=-45
    )
    return fig

def create_service_type_revenue_chart(data):
    """Create service type revenue chart"""
    fig = px.pie(data, values='revenue', names='service_type',
                  title='Revenue Distribution by Service Type')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_visit_frequency_histogram(data):
    """Create visit frequency histogram"""
    fig = px.histogram(data, x='visit_count', nbins=20,
                       title='Distribution of Patient Visit Frequency')
    fig.update_layout(
        xaxis_title="Number of Visits",
        yaxis_title="Number of Patients"
    )
    return fig

def create_spending_patterns_scatter(data):
    """Create spending patterns scatter plot"""
    fig = px.scatter(data, x='total_visits', y='total_spent',
                     size='avg_spend_per_visit', title='Patient Spending vs Visits')
    fig.update_layout(
        xaxis_title="Total Visits",
        yaxis_title="Total Spent (Rs.)",
        hovermode='closest'
    )
    return fig

def create_service_preferences_chart(data):
    """Create service preferences chart"""
    fig = px.bar(data, x='service_name', y='preference_score',
                  title='Patient Service Preferences')
    fig.update_layout(
        xaxis_title="Service Name",
        yaxis_title="Preference Score",
        xaxis_tickangle=-45
    )
    return fig

def create_treemap_chart(data):
    """Create treemap chart for hierarchical data"""
    fig = px.treemap(data, path=['department_name', 'service_name'], 
                      values='count', title='Service Distribution by Department')
    return fig

def create_multi_line_chart(data, x_col, y_col, color_col, title):
    """Create multi-line chart for time series data"""
    fig = px.line(data, x=x_col, y=y_col, color=color_col, title=title)
    fig.update_layout(
        xaxis_title=x_col.title(),
        yaxis_title=y_col.title(),
        hovermode='x unified'
    )
    return fig

def create_combined_chart(data1, data2, title1, title2):
    """Create a combined chart with two subplots"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(title1, title2),
        specs=[[{"type": "bar"}, {"type": "pie"}]]
    )
    
    # Add bar chart
    fig.add_trace(
        go.Bar(x=data1.iloc[:, 0], y=data1.iloc[:, 1], name=title1),
        row=1, col=1
    )
    
    # Add pie chart
    fig.add_trace(
        go.Pie(labels=data2.iloc[:, 0], values=data2.iloc[:, 1], name=title2),
        row=1, col=2
    )
    
    fig.update_layout(height=500, showlegend=False)
    return fig

def format_currency(value):
    """Format value as currency"""
    return f"Rs. {value:,.2f}"

def format_percentage(value):
    """Format value as percentage"""
    return f"{value:.1f}%"

def create_summary_table(data, title):
    """Create a summary table"""
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(data.columns), fill_color='lightblue', align='left'),
        cells=dict(values=[data[col] for col in data.columns], fill_color='white', align='left'))
    ])
    fig.update_layout(title=title)
    return fig
