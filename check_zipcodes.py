#!/usr/bin/env python3
"""
Verify Austin Zip Codes
"""

import pandas as pd

# Load the survey data
df = pd.read_excel('ACME.xlsx')

# Valid Austin zip codes (including some ETJ areas)
austin_zips = [
    # Central Austin
    '78701', '78702', '78703', '78704', '78705',
    # North Central
    '78751', '78752', '78756', '78757', '78758', '78759',
    # East Austin
    '78721', '78722', '78723', '78724', '78725',
    # South Austin
    '78741', '78742', '78744', '78745', '78746', '78747', '78748', '78749',
    # North Austin
    '78727', '78728', '78729', '78750', '78753', '78754',
    # Northwest Austin
    '78726', '78730', '78731', '78732', '78733', '78734', '78735', '78736', '78737', '78738', '78739',
    # West/Southwest Austin (including some ETJ)
    '78652', '78653', '78660', '78664', '78669',
    # Other nearby areas often included
    '78613', '78617', '78641', '78645', '78654', '78665', '78681', '78682'
]

# Get zip code column
zip_col = 'What zip code do you reside in?'

# Clean zip codes - convert to string and strip
df['clean_zip'] = df[zip_col].astype(str).str.strip()

# Filter for valid Austin zips
austin_responses = df[df['clean_zip'].isin(austin_zips)]
non_austin = df[~df['clean_zip'].isin(austin_zips)]

print("ZIP CODE ANALYSIS")
print("="*50)
print(f"Total survey responses: {len(df)}")
print(f"Responses with valid Austin zip codes: {len(austin_responses)}")
print(f"Responses with non-Austin or invalid zips: {len(non_austin)}")
print(f"Unique Austin zip codes represented: {austin_responses['clean_zip'].nunique()}")

print("\nTop 10 Austin Zip Codes by Response Count:")
austin_zip_counts = austin_responses['clean_zip'].value_counts().head(10)
for zip_code, count in austin_zip_counts.items():
    print(f"  {zip_code}: {count} responses")

print("\nNon-Austin or Invalid Entries (first 20):")
non_austin_zips = non_austin['clean_zip'].value_counts().head(20)
for zip_code, count in non_austin_zips.items():
    if zip_code != 'nan':
        print(f"  {zip_code}: {count} responses")

# Save the corrected count
corrected_stats = {
    'total_responses': len(df),
    'austin_responses': len(austin_responses),
    'unique_austin_zips': austin_responses['clean_zip'].nunique(),
    'non_austin_responses': len(non_austin)
}

import json
with open('corrected_zip_stats.json', 'w') as f:
    json.dump(corrected_stats, f, indent=2)

print(f"\nCORRECTED METRIC: {austin_responses['clean_zip'].nunique()} Austin zip codes represented")