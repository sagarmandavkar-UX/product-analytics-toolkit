# A/B Testing Framework for Product Analytics
# Statistical testing for conversion rate experiments

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

class ABTestFramework:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        
    def calculate_conversion_rates(self):
        results = self.df.groupby('experiment_group').agg({
            'session_id': 'nunique',
            'conversion': 'sum'
        })
        results['conversion_rate'] = results['conversion'] / results['session_id']
        return results
    
    def run_statistical_test(self, alpha=0.05):
        control = self.df[self.df['experiment_group'] == 'control']
        treatment = self.df[self.df['experiment_group'] == 'treatment']
        
        control_conv = control['conversion'].sum()
        control_total = control['session_id'].nunique()
        
        treatment_conv = treatment['conversion'].sum()
        treatment_total = treatment['session_id'].nunique()
        
        # Z-test for proportions
        p_control = control_conv / control_total
        p_treatment = treatment_conv / treatment_total
        p_pooled = (control_conv + treatment_conv) / (control_total + treatment_total)
        
        se = np.sqrt(p_pooled * (1 - p_pooled) * (1/control_total + 1/treatment_total))
        z_score = (p_treatment - p_control) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        lift = ((p_treatment - p_control) / p_control) * 100
        
        return {
            'control_rate': p_control,
            'treatment_rate': p_treatment,
            'lift_percent': lift,
            'z_score': z_score,
            'p_value': p_value,
            'statistically_significant': p_value < alpha
        }

if __name__ == "__main__":
    ab_test = ABTestFramework('../data/ecommerce_data.csv')
    results = ab_test.run_statistical_test()
    print("A/B Test Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
