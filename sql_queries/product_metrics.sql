-- Product Analytics SQL Queries
-- Key metrics and KPIs for product performance tracking

-- Query 1: Daily Active Users (DAU) and Monthly Active Users (MAU)
WITH daily_users AS (
    SELECT
        DATE(timestamp) as date,
        COUNT(DISTINCT user_id) as dau
    FROM ecommerce_data
    GROUP BY DATE(timestamp)
),
monthly_users AS (
    SELECT
        DATE_TRUNC('month', timestamp) as month,
        COUNT(DISTINCT user_id) as mau
    FROM ecommerce_data
    GROUP BY DATE_TRUNC('month', timestamp)
)
SELECT * FROM daily_users;

-- Query 2: Conversion Funnel Analysis
SELECT
    event_type,
    COUNT(DISTINCT session_id) as sessions,
    COUNT(DISTINCT user_id) as users,
    ROUND(100.0 * COUNT(DISTINCT session_id) / 
        FIRST_VALUE(COUNT(DISTINCT session_id)) OVER (ORDER BY event_type), 2) as conversion_rate
FROM ecommerce_data
GROUP BY event_type
ORDER BY CASE event_type
    WHEN 'page_view' THEN 1
    WHEN 'add_to_cart' THEN 2
    WHEN 'purchase' THEN 3
END;

-- Query 3: Revenue by Product Category
SELECT
    category,
    COUNT(DISTINCT user_id) as customers,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_revenue_per_transaction,
    COUNT(DISTINCT CASE WHEN revenue > 0 THEN session_id END) as purchases
FROM ecommerce_data
WHERE revenue > 0
GROUP BY category
ORDER BY total_revenue DESC;

-- Query 4: User Retention Cohort
WITH first_purchase AS (
    SELECT
        user_id,
        MIN(DATE(timestamp)) as cohort_date
    FROM ecommerce_data
    WHERE conversion = 1
    GROUP BY user_id
),
user_activity AS (
    SELECT
        e.user_id,
        f.cohort_date,
        DATE(e.timestamp) as activity_date,
        DATEDIFF(DATE(e.timestamp), f.cohort_date) as days_since_first
    FROM ecommerce_data e
    JOIN first_purchase f ON e.user_id = f.user_id
    WHERE e.conversion = 1
)
SELECT
    cohort_date,
    COUNT(DISTINCT user_id) as cohort_size,
    COUNT(DISTINCT CASE WHEN days_since_first <= 7 THEN user_id END) as week_1,
    COUNT(DISTINCT CASE WHEN days_since_first <= 30 THEN user_id END) as month_1
FROM user_activity
GROUP BY cohort_date
ORDER BY cohort_date;

-- Query 5: Device and Channel Performance
SELECT
    device,
    channel,
    COUNT(DISTINCT session_id) as sessions,
    SUM(CASE WHEN conversion = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(100.0 * SUM(CASE WHEN conversion = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT session_id), 2) as conversion_rate,
    SUM(revenue) as total_revenue
FROM ecommerce_data
GROUP BY device, channel
ORDER BY total_revenue DESC;
