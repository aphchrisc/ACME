#!/usr/bin/env python3
"""
City of Austin Cultural Grants Community Survey Analysis
Dr. Anya Sharma - Civic Arts & Equity Consulting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings('ignore')

# Configure visualization settings
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Download necessary NLTK data
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

print("="*80)
print("CITY OF AUSTIN CULTURAL GRANTS COMMUNITY SURVEY ANALYSIS")
print("Dr. Anya Sharma - Civic Arts & Equity Consulting")
print("="*80)
print()

# Load the survey data
print("Loading survey data...")
df = pd.read_excel('ACME.xlsx')

# Basic dataset overview
print(f"\nDataset Shape: {df.shape}")
print(f"Total Responses: {df.shape[0]:,}")
print(f"Total Questions: {df.shape[1]}")
print("\n" + "="*50 + "\n")

# Display column names to understand survey structure
print("Survey Questions/Columns:")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

# Identify text response columns vs categorical columns
print("\n" + "="*50 + "\n")
print("Analyzing column types...")

text_columns = []
categorical_columns = []
numeric_columns = []

for col in df.columns:
    # Skip if column is mostly empty
    if df[col].notna().sum() < 10:
        continue
        
    # Get non-null values
    non_null = df[col].dropna()
    
    if len(non_null) == 0:
        continue
    
    # Check if numeric
    try:
        pd.to_numeric(non_null)
        numeric_columns.append(col)
        continue
    except:
        pass
    
    # Check average string length for text vs categorical distinction
    avg_length = non_null.astype(str).str.len().mean()
    unique_ratio = len(non_null.unique()) / len(non_null)
    
    if avg_length > 50 or unique_ratio > 0.5:
        text_columns.append(col)
    else:
        categorical_columns.append(col)

print(f"\nText Response Columns ({len(text_columns)}):")
for col in text_columns[:10]:  # Show first 10
    print(f"  - {col}")
if len(text_columns) > 10:
    print(f"  ... and {len(text_columns) - 10} more")

print(f"\nCategorical Columns ({len(categorical_columns)}):")
for col in categorical_columns[:10]:  # Show first 10
    print(f"  - {col}")
if len(categorical_columns) > 10:
    print(f"  ... and {len(categorical_columns) - 10} more")

# Check for grant program mentions
print("\n" + "="*50 + "\n")
print("Searching for grant program mentions...")

programs = ['Nexus', 'Heritage', 'AIPP', 'Thrive', 'Elevate', 'ALMF', 'CSAP']
program_mentions = {}

for program in programs:
    mentions = 0
    for col in text_columns:
        if col in df.columns:
            # Count mentions in this column
            mentions += df[col].astype(str).str.contains(program, case=False, na=False).sum()
    program_mentions[program] = mentions

print("\nGrant Program Mentions in Survey:")
for program, count in sorted(program_mentions.items(), key=lambda x: x[1], reverse=True):
    print(f"  {program}: {count} mentions")

# Export key findings for further analysis
print("\n" + "="*50 + "\n")
print("Exporting initial findings...")

# Save column classifications
with open('column_classifications.txt', 'w') as f:
    f.write("TEXT COLUMNS:\n")
    for col in text_columns:
        f.write(f"  - {col}\n")
    f.write("\nCATEGORICAL COLUMNS:\n")
    for col in categorical_columns:
        f.write(f"  - {col}\n")
    f.write("\nNUMERIC COLUMNS:\n")
    for col in numeric_columns:
        f.write(f"  - {col}\n")

print("\nInitial analysis complete. Column classifications saved to 'column_classifications.txt'")
print("Ready for deeper sentiment and thematic analysis...")