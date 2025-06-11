#!/usr/bin/env python3
"""
Check available columns for equity analysis
"""

import pandas as pd

# Load the survey data
df = pd.read_excel('ACME.xlsx')

print("Checking for equity-related columns...\n")

# Look for columns containing key equity terms
equity_keywords = ['equal', 'access', 'barrier', 'underrepresent', 'histor', 'communit']

print("Columns that might contain equity-related questions:")
for col in df.columns:
    col_lower = col.lower()
    if any(keyword in col_lower for keyword in equity_keywords):
        print(f"\n{df.columns.tolist().index(col) + 1}. {col}")
        # Show sample responses
        non_null = df[col].dropna()
        if len(non_null) > 0:
            print(f"   Sample responses: {non_null.value_counts().head(3).to_dict()}")

# Check specific columns
print("\n\nChecking specific columns:")
print("\nColumn 17:", df.columns[16] if len(df.columns) > 16 else "Not found")
print("Column 18:", df.columns[17] if len(df.columns) > 17 else "Not found")
print("Column 26:", df.columns[25] if len(df.columns) > 25 else "Not found")
print("Column 29:", df.columns[28] if len(df.columns) > 28 else "Not found")