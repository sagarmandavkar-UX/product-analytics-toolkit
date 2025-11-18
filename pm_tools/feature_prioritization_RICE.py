# RICE Framework for Feature Prioritization
# Reach * Impact * Confidence / Effort

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class RICEPrioritization:
    def __init__(self):
        self.features = []
    
    def add_feature(self, name, reach, impact, confidence, effort):
        """
        Add a feature to prioritize
        reach: number of users affected per time period
        impact: 0.25 (minimal), 0.5 (low), 1 (medium), 2 (high), 3 (massive)
        confidence: percentage (0-100)
        effort: person-months
        """
        rice_score = (reach * impact * (confidence/100)) / effort
        
        self.features.append({
            'name': name,
            'reach': reach,
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'rice_score': round(rice_score, 2)
        })
    
    def get_prioritized_list(self):
        df = pd.DataFrame(self.features)
        return df.sort_values('rice_score', ascending=False).reset_index(drop=True)
    
    def visualize(self):
        df = self.get_prioritized_list()
        
        plt.figure(figsize=(12, 6))
        colors = sns.color_palette('RdYlGn', len(df))
        
        plt.barh(df['name'], df['rice_score'], color=colors)
        plt.xlabel('RICE Score')
        plt.title('Feature Prioritization using RICE Framework')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('outputs/rice_prioritization.png', dpi=300, bbox_inches='tight')
        print("Visualization saved!")

if __name__ == "__main__":
    rice = RICEPrioritization()
    
    # Example features
    rice.add_feature('Personalized Recommendations', 10000, 3, 80, 4)
    rice.add_feature('One-Click Checkout', 8000, 2, 90, 2)
    rice.add_feature('Loyalty Program', 15000, 2, 70, 6)
    rice.add_feature('Mobile App Push Notifications', 12000, 1, 85, 3)
    rice.add_feature('Advanced Search Filters', 5000, 1, 80, 2)
    rice.add_feature('Social Media Integration', 20000, 0.5, 60, 5)
    
    prioritized = rice.get_prioritized_list()
    print("\nFeature Prioritization (RICE Framework):")
    print("="*70)
    print(prioritized.to_string(index=False))
    
    rice.visualize()
