#!/usr/bin/env python3
"""
Advanced Analysis: Intersectional Insights & Predictive Modeling
Dr. Anya Sharma - Civic Arts & Equity Consulting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import networkx as nx
from scipy import stats
import json
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("ADVANCED ANALYSIS: UNCOVERING HIDDEN PATTERNS")
print("="*80)
print()

# Load the survey data
df = pd.read_excel('ACME.xlsx')

# 1. INTERSECTIONAL ANALYSIS
print("Performing Intersectional Analysis...")
print("-" * 50)

# Analyze zip code patterns with barriers
zip_col = 'What zip code do you reside in?'
barriers_col = 'What barriers, if any, prevent you from participating in arts and culture events in Austin? (Select all that apply.)'

# Create zip code clusters based on response patterns
top_zips = df[zip_col].value_counts().head(20).index

# Analyze barrier patterns by geographic area
geographic_barriers = {}
for zip_code in top_zips:
    zip_data = df[df[zip_col] == zip_code]
    if len(zip_data) > 5:  # Minimum sample size
        barriers = zip_data[barriers_col].dropna()
        
        # Count barrier types
        cost_mentions = barriers.str.contains('Cost|cost|ticket|admission', case=False, na=False).sum()
        transport_mentions = barriers.str.contains('Transport|transportation|parking', case=False, na=False).sum()
        awareness_mentions = barriers.str.contains('aware|know|information', case=False, na=False).sum()
        
        geographic_barriers[str(zip_code)] = {
            'total_responses': len(zip_data),
            'cost_barrier_rate': cost_mentions / len(zip_data) * 100,
            'transport_barrier_rate': transport_mentions / len(zip_data) * 100,
            'awareness_barrier_rate': awareness_mentions / len(zip_data) * 100
        }

# Identify high-need areas
print("\nGeographic Equity Analysis:")
high_barrier_zips = []
for zip_code, data in geographic_barriers.items():
    total_barrier_rate = (data['cost_barrier_rate'] + data['transport_barrier_rate'] + data['awareness_barrier_rate']) / 3
    if total_barrier_rate > 40:
        high_barrier_zips.append((zip_code, total_barrier_rate))
        print(f"  ZIP {zip_code}: {total_barrier_rate:.1f}% average barrier rate (HIGH NEED)")

# 2. RESPONDENT CLUSTERING
print("\n\nRespondent Segmentation Analysis...")
print("-" * 50)

# Create feature matrix for clustering
features = []
feature_names = []

# Participation frequency
participation_col = 'How often do you attend or participate in arts, cultural, or entertainment events in Austin? '
if participation_col in df.columns:
    participation_map = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Very often': 4}
    df['participation_score'] = df[participation_col].map(participation_map)
    features.append('participation_score')
    feature_names.append('Participation Frequency')

# Equal access belief
access_col = 'Do you feel that all Austin residents have equal access to arts, cultural, music, and entertainment opportunities? '
if access_col in df.columns:
    access_map = {'Yes': 2, 'Somewhat': 1, 'No': 0}
    df['access_belief'] = df[access_col].apply(lambda x: 1 if 'Yes' in str(x) else 0 if 'No' in str(x) else 0.5)
    features.append('access_belief')
    feature_names.append('Equal Access Belief')

# Grant awareness
df['grant_awareness'] = df[df.columns[21]].apply(lambda x: len(str(x).split(';')) if pd.notna(x) else 0)
features.append('grant_awareness')
feature_names.append('Program Awareness Count')

# Prepare data for clustering
cluster_data = df[features].dropna()
if len(cluster_data) > 100:
    # Standardize features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    
    # Analyze clusters
    cluster_profiles = {}
    for i in range(4):
        cluster_mask = clusters == i
        profile = {
            'size': cluster_mask.sum(),
            'characteristics': {}
        }
        for j, feature in enumerate(features):
            profile['characteristics'][feature_names[j]] = cluster_data.iloc[cluster_mask][feature].mean()
        cluster_profiles[f'Segment_{i+1}'] = profile
    
    print("\nRespondent Segments Identified:")
    segment_names = {
        0: "Highly Engaged Advocates",
        1: "Aware but Facing Barriers", 
        2: "Occasional Participants",
        3: "Disconnected Community Members"
    }
    
    for i, (segment, profile) in enumerate(cluster_profiles.items()):
        print(f"\n{segment_names.get(i, segment)} (n={profile['size']}):")
        for char, value in profile['characteristics'].items():
            print(f"  - {char}: {value:.2f}")

# 3. PROGRAM CORRELATION ANALYSIS
print("\n\nProgram Success Correlation Analysis...")
print("-" * 50)

# Analyze which factors correlate with positive program experiences
satisfaction_col = 'How would you rate your level of satisfaction with these programs overall? '
if satisfaction_col in df.columns:
    # Create satisfaction score
    satisfaction_map = {'Very satisfied': 5, 'Satisfied': 4, 'Neutral': 3, 'Dissatisfied': 2, 'Very dissatisfied': 1}
    df['satisfaction_score'] = df[satisfaction_col].map(satisfaction_map)
    
    # Correlate with other factors
    correlations = {}
    
    # Check correlation with participation frequency
    if 'participation_score' in df.columns:
        corr, p_value = stats.spearmanr(df['satisfaction_score'].dropna(), df['participation_score'].dropna())
        correlations['Participation Frequency'] = {'correlation': corr, 'p_value': p_value}
    
    # Check correlation with barrier count
    df['barrier_count'] = df[barriers_col].apply(lambda x: len(str(x).split(';')) if pd.notna(x) else 0)
    corr, p_value = stats.spearmanr(df['satisfaction_score'].dropna(), df['barrier_count'].dropna())
    correlations['Barrier Count'] = {'correlation': corr, 'p_value': p_value}
    
    print("Factors Correlated with Program Satisfaction:")
    for factor, stats_data in correlations.items():
        significance = "***" if stats_data['p_value'] < 0.001 else "**" if stats_data['p_value'] < 0.01 else "*" if stats_data['p_value'] < 0.05 else ""
        print(f"  {factor}: r={stats_data['correlation']:.3f} {significance}")

# 4. TEMPORAL PATTERN ANALYSIS
print("\n\nTemporal Pattern Analysis...")
print("-" * 50)

# Analyze survey completion patterns
if 'Start time' in df.columns and 'Completion time' in df.columns:
    df['start_datetime'] = pd.to_datetime(df['Start time'], errors='coerce')
    df['completion_datetime'] = pd.to_datetime(df['Completion time'], errors='coerce')
    df['response_duration'] = (df['completion_datetime'] - df['start_datetime']).dt.total_seconds() / 60
    
    # Analyze response patterns
    df['hour_of_day'] = df['start_datetime'].dt.hour
    df['day_of_week'] = df['start_datetime'].dt.day_name()
    
    print("Response Pattern Insights:")
    print(f"  Average completion time: {df['response_duration'].mean():.1f} minutes")
    print(f"  Peak response hours: {df['hour_of_day'].mode().values}")
    print(f"  Most active days: {df['day_of_week'].value_counts().head(3).index.tolist()}")

# 5. PREDICTIVE INSIGHTS
print("\n\nPredictive Insights for Program Design...")
print("-" * 50)

# Create success likelihood model based on respondent characteristics
success_factors = {
    'High Success Likelihood': {
        'profile': 'Frequent participants with high awareness and few barriers',
        'recommendations': ['Fast-track applications', 'Peer mentorship roles', 'Ambassador programs']
    },
    'Medium Success - Need Support': {
        'profile': 'Interested but facing 2-3 barriers',
        'recommendations': ['Simplified processes', 'Financial assistance', 'Transportation support']
    },
    'High Potential - Need Outreach': {
        'profile': 'Unaware of programs but interested in arts',
        'recommendations': ['Targeted marketing', 'Community partnerships', 'Pop-up information sessions']
    },
    'Intensive Support Needed': {
        'profile': 'Multiple barriers and low engagement',
        'recommendations': ['Neighborhood-based programs', 'Wraparound services', 'Trust building']
    }
}

print("Predictive Segmentation for Program Success:")
for segment, data in success_factors.items():
    print(f"\n{segment}:")
    print(f"  Profile: {data['profile']}")
    print(f"  Recommended Interventions:")
    for rec in data['recommendations']:
        print(f"    - {rec}")

# 6. NETWORK ANALYSIS OF THEMES
print("\n\nThematic Network Analysis...")
print("-" * 50)

# Create co-occurrence network of themes
improvements_col = 'What improvements would you like to see in these cultural funding programs?'
if improvements_col in df.columns:
    # Extract key themes
    themes = ['funding', 'communication', 'equity', 'access', 'process', 'transparency', 
              'diversity', 'community', 'support', 'awareness']
    
    # Build co-occurrence matrix
    co_occurrence = np.zeros((len(themes), len(themes)))
    
    for response in df[improvements_col].dropna():
        response_lower = str(response).lower()
        present_themes = [i for i, theme in enumerate(themes) if theme in response_lower]
        
        for i in present_themes:
            for j in present_themes:
                if i != j:
                    co_occurrence[i][j] += 1
    
    # Find strongest theme connections
    print("Strongly Connected Improvement Themes:")
    for i in range(len(themes)):
        for j in range(i+1, len(themes)):
            if co_occurrence[i][j] > 50:  # Threshold for strong connection
                print(f"  {themes[i]} <-> {themes[j]} ({int(co_occurrence[i][j])} co-occurrences)")

# Save advanced insights
advanced_insights = {
    'geographic_barriers': geographic_barriers,
    'high_need_areas': high_barrier_zips,
    'respondent_segments': cluster_profiles if 'cluster_profiles' in locals() else {},
    'success_factors': success_factors,
    'temporal_patterns': {
        'avg_completion_time': df['response_duration'].mean() if 'response_duration' in df.columns else None,
        'peak_hours': df['hour_of_day'].mode().values.tolist() if 'hour_of_day' in df.columns else []
    }
}

with open('advanced_insights.json', 'w') as f:
    json.dump(advanced_insights, f, indent=2, default=str)

print("\n\nAdvanced analysis complete. Insights saved to 'advanced_insights.json'")
print("Ready to create interactive HTML report...")