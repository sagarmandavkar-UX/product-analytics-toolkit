"""
Product Analytics Dashboard
Author: Sagar Mandavkar
Description: Comprehensive product analytics dashboard for e-commerce data analysis
including conversion funnels, cohort analysis, and revenue metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set styling
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

class ProductAnalyticsDashboard:
    """
    Main class for product analytics operations
    """
    
    def __init__(self, data_path):
        """Initialize dashboard with data"""
        self.df = pd.read_csv(data_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['date'] = self.df['timestamp'].dt.date
        print(f"Loaded {len(self.df)} rows of data")
    
    def calculate_conversion_metrics(self):
        """Calculate key conversion metrics"""
        total_sessions = self.df['session_id'].nunique()
        total_users = self.df['user_id'].nunique()
        
        # Calculate conversions
        conversions = self.df[self.df['conversion'] == 1]['session_id'].nunique()
        conversion_rate = (conversions / total_sessions) * 100
        
        # Revenue metrics
        total_revenue = self.df['revenue'].sum()
        avg_order_value = self.df[self.df['revenue'] > 0]['revenue'].mean()
        
        metrics = {
            'Total Sessions': total_sessions,
            'Total Users': total_users,
            'Conversions': conversions,
            'Conversion Rate': f"{conversion_rate:.2f}%",
            'Total Revenue': f"${total_revenue:,.2f}",
            'Average Order Value': f"${avg_order_value:,.2f}"
        }
        
        return metrics
    
    def funnel_analysis(self):
        """Analyze conversion funnel"""
        funnel_data = {}
        
        # Page views
        funnel_data['Page Views'] = self.df[self.df['event_type'] == 'page_view']['session_id'].nunique()
        
        # Add to cart
        funnel_data['Add to Cart'] = self.df[self.df['event_type'] == 'add_to_cart']['session_id'].nunique()
        
        # Purchases
        funnel_data['Purchase'] = self.df[self.df['event_type'] == 'purchase']['session_id'].nunique()
        
        # Calculate drop-off rates
        funnel_df = pd.DataFrame({
            'Stage': funnel_data.keys(),
            'Sessions': funnel_data.values()
        })
        
        funnel_df['Conversion_Rate'] = (funnel_df['Sessions'] / funnel_df['Sessions'].iloc[0] * 100).round(2)
        funnel_df['Drop_Off'] = funnel_df['Conversion_Rate'].diff().fillna(0).abs()
        
        return funnel_df
    
    def cohort_analysis(self):
        """Perform cohort analysis"""
        # Group by user and get first purchase date
        user_cohorts = self.df[self.df['conversion'] == 1].groupby('user_id').agg({
            'date': 'min'
        }).reset_index()
        user_cohorts.columns = ['user_id', 'cohort_date']
        
        # Merge back with main data
        cohort_df = self.df.merge(user_cohorts, on='user_id', how='left')
        
        return cohort_df
    
    def device_channel_analysis(self):
        """Analyze performance by device and channel"""
        # Device analysis
        device_metrics = self.df.groupby('device').agg({
            'session_id': 'nunique',
            'conversion': 'sum',
            'revenue': 'sum'
        }).reset_index()
        device_metrics['conversion_rate'] = (device_metrics['conversion'] / device_metrics['session_id'] * 100).round(2)
        
        # Channel analysis
        channel_metrics = self.df.groupby('channel').agg({
            'session_id': 'nunique',
            'conversion': 'sum',
            'revenue': 'sum'
        }).reset_index()
        channel_metrics['conversion_rate'] = (channel_metrics['conversion'] / channel_metrics['session_id'] * 100).round(2)
        
        return device_metrics, channel_metrics
    
    def plot_funnel(self, funnel_df):
        """Visualize conversion funnel"""
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.barh(funnel_df['Stage'], funnel_df['Sessions'], color='steelblue')
        plt.xlabel('Number of Sessions')
        plt.title('Conversion Funnel')
        plt.gca().invert_yaxis()
        
        plt.subplot(1, 2, 2)
        plt.barh(funnel_df['Stage'], funnel_df['Conversion_Rate'], color='coral')
        plt.xlabel('Conversion Rate (%)')
        plt.title('Conversion Rate by Stage')
        plt.gca().invert_yaxis()
        
        plt.tight_layout()
        plt.savefig('outputs/funnel_analysis.png', dpi=300, bbox_inches='tight')
        print("Funnel analysis chart saved!")
    
    def plot_revenue_trends(self):
        """Plot revenue trends over time"""
        daily_revenue = self.df.groupby('date')['revenue'].sum().reset_index()
        
        plt.figure(figsize=(14, 6))
        plt.plot(daily_revenue['date'], daily_revenue['revenue'], marker='o', linewidth=2)
        plt.xlabel('Date')
        plt.ylabel('Revenue ($)')
        plt.title('Daily Revenue Trends')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('outputs/revenue_trends.png', dpi=300, bbox_inches='tight')
        print("Revenue trends chart saved!")
    
    def generate_full_report(self):
        """Generate comprehensive analytics report"""
        print("=" * 60)
        print("PRODUCT ANALYTICS DASHBOARD REPORT")
        print("=" * 60)
        
        # Key metrics
        print("\n1. KEY METRICS")
        print("-" * 60)
        metrics = self.calculate_conversion_metrics()
        for key, value in metrics.items():
            print(f"{key:25s}: {value}")
        
        # Funnel analysis
        print("\n2. CONVERSION FUNNEL")
        print("-" * 60)
        funnel_df = self.funnel_analysis()
        print(funnel_df.to_string(index=False))
        self.plot_funnel(funnel_df)
        
        # Device & Channel
        print("\n3. DEVICE PERFORMANCE")
        print("-" * 60)
        device_metrics, channel_metrics = self.device_channel_analysis()
        print(device_metrics.to_string(index=False))
        
        print("\n4. CHANNEL PERFORMANCE")
        print("-" * 60)
        print(channel_metrics.to_string(index=False))
        
        # Visualizations
        self.plot_revenue_trends()
        
        print("\n" + "=" * 60)
        print("Report generation complete!")
        print("=" * 60)

if __name__ == "__main__":
    # Initialize dashboard
    dashboard = ProductAnalyticsDashboard('../data/ecommerce_data.csv')
    
    # Generate full report
    dashboard.generate_full_report()
