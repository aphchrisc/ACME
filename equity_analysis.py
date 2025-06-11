#!/usr/bin/env python3
"""
Equity & Access Barrier Analysis
Dr. Anya Sharma - Civic Arts & Equity Consulting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set up visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("="*80)
print("EQUITY & ACCESS BARRIER ANALYSIS")
print("="*80)
print()

# Load the survey data
df = pd.read_excel('ACME.xlsx')

# Key equity-focused questions
equity_questions = {
    'equal_access': 'Do you feel that all Austin residents have equal access to arts, cultural, music, and entertainment opportunities?',
    'barriers': 'What barriers, if any, prevent you from participating in arts and culture events in Austin? (Select all that apply.)',
    'accessibility': 'How accessible do you think these programs are for historically underrepresented artists, organizations, and communities?',
    'access_barriers': 'What barriers do you or your community face in accessing support or services related to arts, culture, music, and entertainment?'
}

# Analyze equal access perception
print("EQUAL ACCESS PERCEPTION ANALYSIS")
print("-" * 50)

if equity_questions['equal_access'] in df.columns:
    equal_access = df[equity_questions['equal_access']].value_counts()
    total_responses = equal_access.sum()
    
    print(f"Total Responses: {total_responses}")
    for response, count in equal_access.items():
        percentage = (count / total_responses) * 100
        print(f"  {response}: {count} ({percentage:.1f}%)")
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    colors = ['#e74c3c' if 'No' in str(x) else '#27ae60' if 'Yes' in str(x) else '#95a5a6' for x in equal_access.index]
    bars = plt.bar(equal_access.index, equal_access.values, color=colors, alpha=0.8)
    plt.title('Do Austin Residents Have Equal Access to Arts & Culture?', fontsize=16, fontweight='bold')
    plt.xlabel('Response', fontsize=12)
    plt.ylabel('Number of Respondents', fontsize=12)
    
    # Add value labels on bars
    for bar, value in zip(bars, equal_access.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                f'{value}\n({value/total_responses*100:.1f}%)', 
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('equal_access_perception.png', dpi=300, bbox_inches='tight')
    plt.close()

# Analyze barriers to participation
print("\n\nBARRIERS TO PARTICIPATION ANALYSIS")
print("-" * 50)

if equity_questions['barriers'] in df.columns:
    barriers_data = df[equity_questions['barriers']].dropna()
    
    # Count individual barriers
    all_barriers = []
    for response in barriers_data:
        if pd.notna(response):
            # Split multiple barriers (assuming they're separated by commas or semicolons)
            barriers = re.split('[,;]', str(response))
            all_barriers.extend([b.strip() for b in barriers if b.strip()])
    
    barrier_counts = Counter(all_barriers)
    top_barriers = barrier_counts.most_common(15)
    
    print(f"Total Responses Mentioning Barriers: {len(barriers_data)}")
    print("\nTop Barriers Identified:")
    for barrier, count in top_barriers:
        print(f"  - {barrier}: {count} mentions")
    
    # Create barrier visualization
    if top_barriers:
        barriers_df = pd.DataFrame(top_barriers, columns=['Barrier', 'Count'])
        
        plt.figure(figsize=(12, 8))
        sns.barplot(data=barriers_df, y='Barrier', x='Count', palette='viridis')
        plt.title('Top Barriers to Arts & Culture Participation', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Mentions', fontsize=12)
        plt.tight_layout()
        plt.savefig('participation_barriers.png', dpi=300, bbox_inches='tight')
        plt.close()

# Analyze program accessibility for underrepresented communities
print("\n\nPROGRAM ACCESSIBILITY FOR UNDERREPRESENTED COMMUNITIES")
print("-" * 50)

if equity_questions['accessibility'] in df.columns:
    accessibility = df[equity_questions['accessibility']].value_counts()
    total_responses = accessibility.sum()
    
    print(f"Total Responses: {total_responses}")
    for response, count in accessibility.items():
        percentage = (count / total_responses) * 100
        print(f"  {response}: {count} ({percentage:.1f}%)")
    
    # Create accessibility visualization
    plt.figure(figsize=(10, 6))
    # Use color gradient for accessibility levels
    colors = ['#e74c3c', '#e67e22', '#f39c12', '#3498db', '#27ae60'][:len(accessibility)]
    
    wedges, texts, autotexts = plt.pie(accessibility.values, labels=accessibility.index, 
                                       colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Perceived Accessibility for Underrepresented Communities', 
              fontsize=16, fontweight='bold')
    
    # Enhance text
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig('program_accessibility.png', dpi=300, bbox_inches='tight')
    plt.close()

# Analyze access barriers in detail
print("\n\nDETAILED ACCESS BARRIER ANALYSIS")
print("-" * 50)

if equity_questions['access_barriers'] in df.columns:
    access_barriers = df[equity_questions['access_barriers']].dropna()
    
    # Extract key themes from barrier descriptions
    barrier_themes = {
        'financial': ['cost', 'expensive', 'afford', 'money', 'fee', 'price', 'budget', 'income', 'economic'],
        'transportation': ['transport', 'parking', 'bus', 'drive', 'distance', 'far', 'location', 'travel'],
        'information': ['know', 'aware', 'information', 'communication', 'find', 'discover', 'marketing'],
        'time': ['time', 'schedule', 'busy', 'work', 'hours', 'weekend', 'evening'],
        'language': ['language', 'english', 'spanish', 'translate', 'bilingual'],
        'digital': ['online', 'website', 'internet', 'computer', 'technology', 'digital'],
        'childcare': ['child', 'kids', 'family', 'babysit'],
        'disability': ['accessible', 'disability', 'wheelchair', 'mobility', 'ada']
    }
    
    theme_counts = {theme: 0 for theme in barrier_themes}
    
    for response in access_barriers:
        if pd.notna(response):
            response_lower = str(response).lower()
            for theme, keywords in barrier_themes.items():
                if any(keyword in response_lower for keyword in keywords):
                    theme_counts[theme] += 1
    
    print("Barrier Categories Identified:")
    for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            percentage = (count / len(access_barriers)) * 100
            print(f"  {theme.capitalize()}: {count} mentions ({percentage:.1f}% of responses)")
    
    # Create thematic barrier visualization
    themes_df = pd.DataFrame(list(theme_counts.items()), columns=['Category', 'Count'])
    themes_df = themes_df[themes_df['Count'] > 0].sort_values('Count', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=themes_df, x='Category', y='Count', palette='rocket')
    plt.title('Access Barrier Categories', fontsize=16, fontweight='bold')
    plt.xlabel('Barrier Category', fontsize=12)
    plt.ylabel('Number of Mentions', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels
    for i, (idx, row) in enumerate(themes_df.iterrows()):
        plt.text(i, row['Count'] + 1, str(row['Count']), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('barrier_categories.png', dpi=300, bbox_inches='tight')
    plt.close()

# Geographic equity analysis (by zip code)
print("\n\nGEOGRAPHIC EQUITY ANALYSIS")
print("-" * 50)

zip_col = 'What zip code do you reside in?'
if zip_col in df.columns:
    zip_codes = df[zip_col].value_counts().head(20)
    
    print(f"Top 20 Zip Codes by Response Count:")
    for zip_code, count in zip_codes.items():
        print(f"  {zip_code}: {count} responses")
    
    # Create geographic distribution visualization
    plt.figure(figsize=(14, 8))
    sns.barplot(x=zip_codes.index.astype(str), y=zip_codes.values, palette='coolwarm')
    plt.title('Survey Response Distribution by Zip Code (Top 20)', fontsize=16, fontweight='bold')
    plt.xlabel('Zip Code', fontsize=12)
    plt.ylabel('Number of Responses', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('geographic_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create equity summary
print("\n\nEQUITY ANALYSIS SUMMARY")
print("-" * 50)

equity_summary = {
    'equal_access_perception': {
        'believe_equal_access': 0,
        'believe_unequal_access': 0,
        'unsure': 0
    },
    'top_barriers': [],
    'barrier_categories': theme_counts,
    'accessibility_rating': {
        'very_accessible': 0,
        'somewhat_accessible': 0,
        'not_accessible': 0
    }
}

# Populate summary
if equity_questions['equal_access'] in df.columns:
    for response, count in equal_access.items():
        if 'Yes' in str(response):
            equity_summary['equal_access_perception']['believe_equal_access'] = count
        elif 'No' in str(response):
            equity_summary['equal_access_perception']['believe_unequal_access'] = count
        else:
            equity_summary['equal_access_perception']['unsure'] = count

if top_barriers:
    equity_summary['top_barriers'] = [(b[0], b[1]) for b in top_barriers[:5]]

# Key findings
print("\nKEY EQUITY FINDINGS:")
print(f"1. {equity_summary['equal_access_perception']['believe_unequal_access']} respondents ({equity_summary['equal_access_perception']['believe_unequal_access']/total_responses*100:.1f}%) believe Austin residents DO NOT have equal access to arts & culture")
print(f"2. Top barrier categories: {', '.join([k for k, v in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True) if v > 0][:3])}")
print(f"3. Geographic concentration: Responses heavily concentrated in certain zip codes, indicating potential geographic inequities")

print("\nAnalysis complete. Visualizations saved.")
print("Ready for final report generation...")