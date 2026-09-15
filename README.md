# Product Analytics Toolkit

A product analytics case study that connects **user behavior → funnel diagnosis → segmentation → experimentation → prioritization**.

The goal is not to build another dashboard full of charts. It is to show how a product manager or analyst can move from raw behavioral events to a defensible product decision.

> The bundled e-commerce dataset is illustrative/synthetic and is used to demonstrate methodology. Results should not be interpreted as live business performance.

---

## Product problem

Product teams often have plenty of event data but still struggle to answer the questions that matter:

- Where are users dropping out of the journey?
- Is the problem broad or concentrated in a specific segment?
- What hypothesis should we test next?
- Did an experiment actually improve the product?
- Which opportunity should the team prioritize?

This toolkit organizes those questions into one decision loop:

**Measure → Diagnose → Segment → Hypothesize → Experiment → Decide → Prioritize**

---

## What is shipped

### Product analytics engine

`analysis/product_analytics_dashboard.py`

- Converts event-level data into a session-level analytical table
- Tracks purchase conversion, cart abandonment, AOV, revenue per session, users, and sessions
- Measures page-view → add-to-cart → purchase funnel performance
- Calculates stage-to-stage conversion and drop-off
- Compares conversion and monetization by device, channel, geography, and experiment group
- Surfaces a simple product-opportunity summary based on the largest funnel loss
- Exports funnel and revenue visualizations to `outputs/`

### A/B testing framework

`ab_testing/ab_test_framework.py`

- Evaluates conversion at the session level
- Calculates control and treatment conversion rates
- Reports absolute difference and relative lift
- Runs a two-sided pooled proportion z-test
- Calculates a 95% confidence interval for the conversion difference
- Returns a decision-oriented recommendation rather than only a p-value

### SQL product metrics

`sql_queries/product_metrics.sql`

Example queries for:

- DAU / MAU
- conversion funnel analysis
- revenue by product category
- retention-style cohort analysis
- device and acquisition-channel performance

### RICE prioritization

`pm_tools/feature_prioritization_RICE.py`

Implements:

**RICE = (Reach × Impact × Confidence) / Effort**

for comparing product opportunities once evidence has been gathered.

### Product strategy

`product/PRODUCT_STRATEGY.md`

Documents:

- target users
- jobs to be done
- KPI tree
- product questions
- experimentation principles
- roadmap
- portfolio narrative

---

## Core product questions

### 1. Where is the biggest funnel problem?

The toolkit measures:

`Page View → Add to Cart → Purchase`

and separates overall conversion from stage-to-stage drop-off so the team can identify the highest-leverage problem before proposing a solution.

### 2. Which users are most affected?

The analysis can compare behavior across:

- device
- acquisition channel
- country
- experiment group

This helps avoid making a roadmap decision from an overall average that may hide a segment-specific issue.

### 3. Does a proposed change work?

The experiment framework answers more than “is p < 0.05?” It reports:

- control conversion
- treatment conversion
- absolute change
- relative lift
- p-value
- 95% confidence interval
- statistical significance
- ship / reject / continue-learning recommendation

### 4. What should we build next?

Once an opportunity has supporting evidence, the RICE module provides a simple structure for comparing reach, impact, confidence, and effort.

---

## Product metrics

### Primary outcome

**Completed Purchases**

### Driver metrics

- Add-to-cart rate
- Cart-to-purchase conversion
- Overall purchase conversion
- Average order value
- Revenue per session

### Diagnostic metrics

- Funnel stage drop-off
- Conversion by device
- Conversion by channel
- Conversion by geography
- Experiment-group performance

For a real production experiment, the product strategy also recommends guardrails such as checkout errors, refunds/cancellations, latency, support contacts, and margin. Those fields are not present in the bundled sample data, so the repository does not claim to measure them.

---

## Repository structure

```text
product-analytics-toolkit/
├── analysis/
│   └── product_analytics_dashboard.py
├── ab_testing/
│   └── ab_test_framework.py
├── data/
│   └── ecommerce_data.csv
├── pm_tools/
│   └── feature_prioritization_RICE.py
├── product/
│   └── PRODUCT_STRATEGY.md
├── sql_queries/
│   └── product_metrics.sql
├── requirements.txt
└── README.md
```

---

## Quick start

```bash
git clone https://github.com/sagarmandavkar-UX/product-analytics-toolkit.git
cd product-analytics-toolkit
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the product analytics report:

```bash
python analysis/product_analytics_dashboard.py
```

Run the A/B test report:

```bash
python ab_testing/ab_test_framework.py
```

Run RICE prioritization:

```bash
python pm_tools/feature_prioritization_RICE.py
```

---

## Example workflow

A PM using this toolkit would follow this sequence:

1. **Measure:** review purchase conversion, cart abandonment, AOV, and revenue per session.
2. **Diagnose:** identify the largest stage-to-stage funnel drop.
3. **Segment:** determine whether the problem is concentrated on a device or acquisition channel.
4. **Hypothesize:** define the user problem and expected behavior change.
5. **Experiment:** compare control and treatment with pre-defined success criteria.
6. **Decide:** interpret effect size, uncertainty, significance, and guardrails.
7. **Prioritize:** compare the validated opportunity against competing roadmap items using RICE.

This structure is intended to demonstrate product judgment as well as technical analysis.

---

## Technical stack

- **Python:** pandas, NumPy, SciPy
- **Visualization:** Matplotlib
- **Statistics:** proportion testing and confidence intervals
- **SQL:** CTEs, window functions, aggregation, cohort-style queries
- **Product:** funnel analysis, KPI design, experimentation, segmentation, RICE prioritization

---

## Product principles

**Use the correct grain.** Event rows should not automatically be treated as independent users or sessions.

**Diagnose before proposing features.** The largest visible metric is not always the most important problem.

**Segment before generalizing.** Overall conversion can hide substantial behavioral differences.

**Experiments are decision tools.** Statistical significance is one input, not the entire product decision.

**Do not present synthetic results as live impact.** This repository demonstrates methods and product thinking, not production-company performance.

---

## Roadmap

### P0

- Automated tests for funnel and experiment calculations
- Lightweight interactive dashboard
- Experiment guardrail configuration

### P1

- Sample-size and statistical-power calculator
- Experiment registry with hypothesis and decision logs
- Cohort retention analysis using longitudinal user data
- Behavioral segmentation

### P2

- Metric-definition catalog
- Event instrumentation schema
- Churn/LTV modeling when supported by appropriate longitudinal data
- Automated anomaly detection

---

## PM portfolio framing

**Product Analytics Toolkit | Product Analytics & PM**  
Python · SQL · Statistics · Experimentation

> Built a product analytics decision toolkit that transforms event-level commerce data into session-level funnels, segment analysis, A/B-test decisions, and RICE prioritization. Structured the workflow around diagnosing user friction, validating hypotheses, quantifying experiment uncertainty, and prioritizing the next product action.

---

## Author

**Sagar Mandavkar**  
Vanderbilt University  
GitHub: [@sagarmandavkar-UX](https://github.com/sagarmandavkar-UX)  
LinkedIn: [sagarmandavkar](https://www.linkedin.com/in/sagarmandavkar)

## License

MIT License
