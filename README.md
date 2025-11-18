# 📊 Product Analytics Toolkit

> A comprehensive Product Analytics Toolkit showcasing data science and product management skills through real-world analytics, A/B testing, feature prioritization, and SQL-based insights.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SQL](https://img.shields.io/badge/SQL-Analytics-orange.svg)](https://www.sql.org/)

## 🎯 Project Overview

This repository demonstrates end-to-end product analytics capabilities essential for Product Management roles, combining:
- **Data Analysis**: Python-based analytics dashboards with conversion funnels and cohort analysis
- **Statistical Testing**: A/B testing framework with statistical significance testing
- **SQL Analytics**: Complex queries for product metrics, user retention, and revenue analysis
- **PM Tools**: RICE framework for feature prioritization
- **Real Data**: 45+ rows of e-commerce user behavior data

## 📁 Project Structure

```
product-analytics-toolkit/
├── data/
│   └── ecommerce_data.csv          # Sample e-commerce dataset
├── analysis/
│   └── product_analytics_dashboard.py   # Main analytics dashboard
├── ab_testing/
│   └── ab_test_framework.py        # A/B testing with z-tests
├── sql_queries/
│   └── product_metrics.sql         # SQL queries for product KPIs
├── pm_tools/
│   └── feature_prioritization_RICE.py  # RICE scoring framework
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
pandas
numpy
matplotlib
seaborn
scipy
```

### Installation

1. Clone the repository
```bash
git clone https://github.com/sagarmandavkar-UX/product-analytics-toolkit.git
cd product-analytics-toolkit
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the analytics dashboard
```bash
cd analysis
python product_analytics_dashboard.py
```

## 💡 Key Features

### 1. Product Analytics Dashboard
**File**: `analysis/product_analytics_dashboard.py`

- **Conversion Metrics**: Track sessions, users, conversion rates, revenue
- **Funnel Analysis**: Page view → Add to cart → Purchase funnel with drop-off rates
- **Cohort Analysis**: User retention and repeat purchase behavior
- **Device/Channel Performance**: Conversion rates by device type and marketing channel
- **Revenue Trends**: Daily revenue tracking and visualization

**Key Metrics Calculated**:
- Conversion Rate
- Average Order Value (AOV)
- Customer Lifetime Value (CLV)
- Cart Abandonment Rate

### 2. A/B Testing Framework
**File**: `ab_testing/ab_test_framework.py`

- Statistical hypothesis testing using z-tests
- P-value calculation for significance testing
- Lift percentage calculation
- Automated test result reporting

**Example Use Case**: Testing new checkout flow (control vs treatment)

### 3. SQL Product Metrics
**File**: `sql_queries/product_metrics.sql`

**Queries Include**:
- Daily Active Users (DAU) / Monthly Active Users (MAU)
- Conversion funnel analysis with stage-wise drop-offs
- Revenue breakdown by product category
- User retention cohort analysis
- Device and channel performance metrics

### 4. RICE Feature Prioritization
**File**: `pm_tools/feature_prioritization_RICE.py`

**RICE Score = (Reach × Impact × Confidence) / Effort**

- Automated scoring for feature prioritization
- Visualization of prioritized features
- Example features with real-world context

**Example Features Analyzed**:
- Personalized Recommendations
- One-Click Checkout
- Loyalty Program
- Push Notifications

## 📊 Sample Data

The dataset (`data/ecommerce_data.csv`) includes:
- **45+ user sessions** with complete journey tracking
- **Multiple product categories**: Electronics, Clothing, Home, Beauty
- **A/B test groups**: Control and Treatment variants
- **Multi-channel data**: Organic, Paid, Email, Social
- **Device types**: Mobile, Desktop, Tablet
- **Full event tracking**: page_view, add_to_cart, purchase

## 🎓 Skills Demonstrated

### Technical Skills
- **Python**: pandas, numpy, matplotlib, seaborn, scipy
- **SQL**: CTEs, window functions, aggregations, joins
- **Statistics**: Hypothesis testing, z-tests, significance testing
- **Data Visualization**: Charts, graphs, dashboards

### Product Management Skills
- Conversion funnel analysis
- A/B testing design and interpretation
- Feature prioritization frameworks (RICE)
- KPI definition and tracking
- Data-driven decision making
- User behavior analysis

## 📈 Example Output

### Conversion Funnel Results
```
Stage              Sessions    Conversion_Rate
Page Views         20          100.00%
Add to Cart        15          75.00%
Purchase          8           40.00%
```

### A/B Test Results
```
Control Rate:     35.2%
Treatment Rate:   42.7%
Lift:             +21.3%
P-value:          0.023 (Significant)
```

## 🔧 Usage Examples

### Run Product Analytics Dashboard
```python
from analysis.product_analytics_dashboard import ProductAnalyticsDashboard

dashboard = ProductAnalyticsDashboard('../data/ecommerce_data.csv')
dashboard.generate_full_report()
```

### Run A/B Test Analysis
```python
from ab_testing.ab_test_framework import ABTestFramework

ab_test = ABTestFramework('../data/ecommerce_data.csv')
results = ab_test.run_statistical_test()
print(results)
```

### Prioritize Features with RICE
```python
from pm_tools.feature_prioritization_RICE import RICEPrioritization

rice = RICEPrioritization()
rice.add_feature('Feature Name', reach=10000, impact=3, confidence=80, effort=4)
prioritized = rice.get_prioritized_list()
```

## 📚 Use Cases

This toolkit is ideal for:
- **Product Managers**: Analyzing user behavior and making data-driven decisions
- **Data Analysts**: Building comprehensive product dashboards
- **Growth Teams**: Running and analyzing A/B tests
- **PM Interviews**: Demonstrating technical and analytical skills
- **Portfolio Projects**: Showcasing PM and data science capabilities

## 🎯 Learning Outcomes

By exploring this project, you'll learn:
1. How to structure product analytics projects
2. Statistical testing for product experiments
3. SQL queries for product metrics
4. Feature prioritization frameworks
5. Data visualization for stakeholder communication

## 📝 Future Enhancements

- [ ] Add R-based statistical analysis
- [ ] Implement cohort retention heatmaps
- [ ] Build interactive Streamlit dashboard
- [ ] Add user segmentation analysis
- [ ] Include predictive modeling (churn, LTV)
- [ ] Create product roadmap templates

## 👤 Author

**Sagar Mandavkar**
- GitHub: [@sagarmandavkar-UX](https://github.com/sagarmandavkar-UX)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/sagar-mandavkar)
- Education: Vanderbilt University

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built to demonstrate Product Management and Data Analytics skills
- Sample data structure inspired by real-world e-commerce platforms
- RICE framework based on Intercom's prioritization methodology

---

⭐ If you find this project helpful for your PM journey, please consider starring the repository!
