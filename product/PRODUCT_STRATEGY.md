# Product Analytics Toolkit — Product Strategy

## Purpose

This project is designed to answer a PM question rather than simply display metrics:

> **Where is the highest-leverage opportunity in the customer journey, and what evidence should a product team gather before shipping a change?**

The toolkit uses an illustrative e-commerce journey to connect behavioral analytics, experimentation, segmentation, SQL, and prioritization into one product decision workflow.

## Target users

- Product managers diagnosing growth or conversion problems
- Product analysts translating event data into recommendations
- Growth teams designing and evaluating experiments
- Early-stage teams establishing a lightweight product measurement system

## Core jobs to be done

1. Understand whether users reach the product's value moment.
2. Identify where the largest funnel friction occurs.
3. Determine which user segments behave differently.
4. Convert observations into testable hypotheses.
5. Evaluate experiments with statistical and practical context.
6. Prioritize opportunities by expected impact and effort.

## Decision loop

**Measure → Diagnose → Segment → Hypothesize → Experiment → Decide → Prioritize**

### Measure
Track a small set of decision-oriented KPIs rather than every available event.

### Diagnose
Find the largest meaningful loss in the user journey.

### Segment
Check whether the problem is concentrated by device, channel, geography, or experiment group.

### Hypothesize
State the suspected user problem and expected behavioral change.

### Experiment
Define primary metric, guardrails, sample needs, and decision criteria before examining the result.

### Decide
Interpret statistical evidence together with effect size and product risk.

### Prioritize
Use RICE or another framework to compare validated opportunities against competing work.

## KPI tree

### Primary outcome

**Completed Purchases**

This is the clearest value-producing event in the sample commerce journey.

### Driver metrics

- Product/session traffic
- Add-to-cart rate
- Cart-to-purchase conversion
- Overall purchase conversion
- Average order value
- Revenue per session

### Diagnostic metrics

- Conversion by device
- Conversion by acquisition channel
- Conversion by geography
- Funnel stage drop-off
- Experiment-group performance

### Guardrails for future experiments

A real production experiment should consider guardrails such as:

- checkout error rate
- cancellation/refund rate
- page latency
- support-contact rate
- margin or contribution profit
- repeat purchase / retention

The current sample dataset does not contain all of these fields, so they are product requirements rather than measured outputs.

## Product questions supported by the repository

### Funnel
- What percentage of sessions reach add-to-cart?
- Where is the largest stage-to-stage drop-off?
- Is checkout or product discovery the stronger optimization opportunity?

### Segmentation
- Which device has the highest purchase conversion?
- Which acquisition channel produces the strongest revenue per session?
- Does a conversion problem appear broad or segment-specific?

### Experimentation
- Does treatment outperform control on session-level conversion?
- What is the absolute and relative lift?
- Is the result statistically significant?
- What does the confidence interval imply about uncertainty?
- Should the team ship, reject, or continue collecting evidence?

### Prioritization
- Which opportunity reaches the most users?
- How large is the expected impact?
- How confident is the team in the evidence?
- What engineering/design effort is required?

## Product principles

### 1. Count the user journey correctly
The source data is event-level, but conversion decisions should often be evaluated at a user or session grain. The toolkit creates session-level views to reduce accidental double counting.

### 2. Diagnose before optimizing
A PM should identify the actual bottleneck before proposing a solution.

### 3. Segment before generalizing
An overall average can hide meaningful differences between devices, channels, or user populations.

### 4. Experiments need decisions, not just p-values
Experiment output includes effect size, confidence interval, and a recommendation instead of stopping at statistical significance.

### 5. Synthetic data is for methodology, not business claims
The bundled dataset is illustrative. Repository outputs demonstrate analytical methods and should not be presented as results from a live commercial product.

## Portfolio narrative

A concise way to describe the project:

> Built a product analytics decision toolkit that converts event-level commerce data into session-level funnels, segmentation, experimentation, and prioritization workflows. Designed the system around the PM decision loop—diagnose friction, validate hypotheses, quantify uncertainty, and prioritize the next product action.

## Next priorities

### P0
- Add automated tests for funnel and A/B-test calculations
- Add a lightweight interactive dashboard
- Add experiment guardrail configuration

### P1
- Cohort retention table and heatmap using a dataset with repeated user activity
- Sample-size and power calculator
- Experiment registry with hypothesis and decision logs
- User segmentation based on behavioral patterns

### P2
- Churn/LTV modeling when the data supports longitudinal outcomes
- Automated anomaly detection
- Metric-definition catalog and event instrumentation schema
