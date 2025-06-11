#!/usr/bin/env python3
"""
Geographic Analysis with Interactive Maps
Dr. Anya Sharma - Civic Arts & Equity Consulting
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("GEOGRAPHIC ANALYSIS: MAPPING CULTURAL EQUITY")
print("="*80)
print()

# Load the survey data
df = pd.read_excel('ACME.xlsx')

# Austin zip codes with approximate center coordinates
austin_zip_coords = {
    # Central Austin
    '78701': {'lat': 30.2672, 'lon': -97.7431, 'area': 'Downtown'},
    '78702': {'lat': 30.2619, 'lon': -97.7140, 'area': 'East Austin'},
    '78703': {'lat': 30.2872, 'lon': -97.7613, 'area': 'West Austin'},
    '78704': {'lat': 30.2452, 'lon': -97.7659, 'area': 'South Central'},
    '78705': {'lat': 30.2875, 'lon': -97.7419, 'area': 'University'},
    # North Central
    '78751': {'lat': 30.3119, 'lon': -97.7252, 'area': 'Hyde Park'},
    '78752': {'lat': 30.3343, 'lon': -97.7013, 'area': 'North Central'},
    '78756': {'lat': 30.3178, 'lon': -97.7411, 'area': 'Brentwood'},
    '78757': {'lat': 30.3502, 'lon': -97.7211, 'area': 'Crestview'},
    '78758': {'lat': 30.3736, 'lon': -97.7114, 'area': 'North Austin'},
    '78759': {'lat': 30.3967, 'lon': -97.7472, 'area': 'Northwest'},
    # East Austin
    '78721': {'lat': 30.2733, 'lon': -97.6889, 'area': 'East Austin'},
    '78722': {'lat': 30.2900, 'lon': -97.7168, 'area': 'East Central'},
    '78723': {'lat': 30.3047, 'lon': -97.6817, 'area': 'Northeast'},
    '78724': {'lat': 30.2901, 'lon': -97.6542, 'area': 'Far East'},
    '78725': {'lat': 30.2390, 'lon': -97.6669, 'area': 'Southeast'},
    # South Austin
    '78741': {'lat': 30.2301, 'lon': -97.7233, 'area': 'Southeast'},
    '78742': {'lat': 30.2369, 'lon': -97.6986, 'area': 'Del Valle'},
    '78744': {'lat': 30.1894, 'lon': -97.7473, 'area': 'South Austin'},
    '78745': {'lat': 30.2074, 'lon': -97.7954, 'area': 'South Austin'},
    '78746': {'lat': 30.2644, 'lon': -97.7982, 'area': 'West Lake Hills'},
    '78747': {'lat': 30.1417, 'lon': -97.7442, 'area': 'Far South'},
    '78748': {'lat': 30.1706, 'lon': -97.8316, 'area': 'Southwest'},
    '78749': {'lat': 30.2172, 'lon': -97.8497, 'area': 'Southwest'},
    # North Austin
    '78727': {'lat': 30.4208, 'lon': -97.7056, 'area': 'North Austin'},
    '78728': {'lat': 30.4378, 'lon': -97.6811, 'area': 'Wells Branch'},
    '78729': {'lat': 30.4556, 'lon': -97.7689, 'area': 'Anderson Mill'},
    '78750': {'lat': 30.4461, 'lon': -97.7967, 'area': 'Northwest'},
    '78753': {'lat': 30.3711, 'lon': -97.6722, 'area': 'North Austin'},
    '78754': {'lat': 30.3486, 'lon': -97.6544, 'area': 'Windsor Park'},
    # Northwest Austin
    '78726': {'lat': 30.4378, 'lon': -97.8436, 'area': 'Four Points'},
    '78730': {'lat': 30.3631, 'lon': -97.8300, 'area': 'Northwest Hills'},
    '78731': {'lat': 30.3392, 'lon': -97.7658, 'area': 'Northwest Hills'},
    '78732': {'lat': 30.3778, 'lon': -97.8897, 'area': 'Steiner Ranch'},
    '78733': {'lat': 30.3208, 'lon': -97.8664, 'area': 'West Lake Hills'},
    '78734': {'lat': 30.3808, 'lon': -97.9497, 'area': 'Lakeway'},
    '78735': {'lat': 30.2489, 'lon': -97.8556, 'area': 'Barton Creek'},
    '78736': {'lat': 30.2189, 'lon': -97.9342, 'area': 'Oak Hill'},
    '78737': {'lat': 30.1978, 'lon': -97.9286, 'area': 'Dripping Springs'},
    '78738': {'lat': 30.3083, 'lon': -97.9125, 'area': 'Bee Cave'},
    '78739': {'lat': 30.1589, 'lon': -97.8978, 'area': 'Driftwood'},
}

# Valid Austin zip codes
austin_zips = list(austin_zip_coords.keys())

# Add more ETJ zips without coords
additional_zips = ['78652', '78653', '78660', '78664', '78669', '78613', '78617', 
                   '78641', '78645', '78654', '78665', '78681', '78682']
austin_zips.extend(additional_zips)

# Clean zip codes
zip_col = 'What zip code do you reside in?'
df['clean_zip'] = df[zip_col].astype(str).str.strip()

# Filter for Austin responses
austin_df = df[df['clean_zip'].isin(austin_zips)].copy()

# ANALYSIS 1: Response counts by zip code
print("Analyzing response distribution by zip code...")
zip_counts = austin_df['clean_zip'].value_counts()

# ANALYSIS 2: Program awareness by zip code
print("Analyzing program awareness by zip code...")
# Use the actual column from the dataframe
awareness_col = df.columns[21] if len(df.columns) > 21 else None

programs = ['Heritage', 'Thrive', 'Nexus', 'Elevate', 'AIPP', 'CSAP', 'ALMF']

# Calculate awareness rates by zip
zip_awareness = {}
if awareness_col and awareness_col in austin_df.columns:
    for zip_code in zip_counts.index:
        if zip_code in austin_zip_coords:
            zip_data = austin_df[austin_df['clean_zip'] == zip_code]
            total_responses = len(zip_data)
            
            awareness_data = zip_data[awareness_col].dropna()
            if len(awareness_data) > 0:
                program_awareness = {}
                for program in programs:
                    aware_count = awareness_data.str.contains(program, case=False, na=False).sum()
                    program_awareness[program] = (aware_count / total_responses) * 100
                
                zip_awareness[zip_code] = {
                    'total_responses': total_responses,
                    'awareness_rates': program_awareness,
                    'avg_awareness': np.mean(list(program_awareness.values()))
                }

# ANALYSIS 3: Sentiment by zip code
print("Analyzing sentiment by zip code...")
sentiment_cols = [
    'What improvements would you like to see in these cultural funding programs?',
    'Do you have any additional ideas, concerns, or feedback you would like to share to help ACME better serve the public? '
]

from textblob import TextBlob

zip_sentiment = {}
for zip_code in zip_counts.index:
    if zip_code in austin_zip_coords:
        zip_data = austin_df[austin_df['clean_zip'] == zip_code]
        
        sentiments = []
        for col in sentiment_cols:
            if col in zip_data.columns:
                responses = zip_data[col].dropna()
                for response in responses:
                    try:
                        blob = TextBlob(str(response))
                        sentiments.append(blob.sentiment.polarity)
                    except:
                        pass
        
        if sentiments:
            avg_sentiment = np.mean(sentiments)
            # Convert to percentage (0-100 scale, where 50 is neutral)
            sentiment_score = (avg_sentiment + 1) * 50
            zip_sentiment[zip_code] = sentiment_score

# Create interactive visualizations
print("Creating interactive maps...")

# 1. Response Count Map
fig_responses = go.Figure()

# Add zip codes with responses
for zip_code, count in zip_counts.items():
    if zip_code in austin_zip_coords:
        coord = austin_zip_coords[zip_code]
        # Size based on response count
        size = min(count * 0.5, 50)  # Cap size at 50
        
        fig_responses.add_trace(go.Scattermapbox(
            lat=[coord['lat']],
            lon=[coord['lon']],
            mode='markers+text',
            marker=dict(
                size=size,
                color=count,
                colorscale='Viridis',
                cmin=0,
                cmax=zip_counts.max(),
                colorbar=dict(title="Responses")
            ),
            text=f"{zip_code}<br>{count} responses<br>{coord['area']}",
            textposition="top center",
            hoverinfo='text',
            name=zip_code
        ))

fig_responses.update_layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=30.2672, lon=-97.7431),
        zoom=10
    ),
    showlegend=False,
    height=600,
    width=None,  # Let it be responsive
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=0),
    title="Survey Responses by Austin Zip Code"
)

# 2. Program Awareness Heat Map
fig_awareness = go.Figure()

if zip_awareness:
    for zip_code, data in zip_awareness.items():
        if zip_code in austin_zip_coords:
            coord = austin_zip_coords[zip_code]
            # Size based on response count
            size = min(data['total_responses'] * 0.5, 50)
            
            # Color based on awareness
            awareness_pct = data['avg_awareness']
            
            # Create hover text
            hover_text = f"{zip_code}<br>{coord['area']}<br>"
            hover_text += f"Responses: {data['total_responses']}<br>"
            hover_text += f"Avg Awareness: {awareness_pct:.1f}%<br><br>"
            for prog, rate in data['awareness_rates'].items():
                hover_text += f"{prog}: {rate:.1f}%<br>"
            
            fig_awareness.add_trace(go.Scattermapbox(
                lat=[coord['lat']],
                lon=[coord['lon']],
                mode='markers+text',
                marker=dict(
                    size=size,
                    color=awareness_pct,
                    colorscale='RdYlGn',
                    cmin=0,
                    cmax=100,
                    colorbar=dict(title="Awareness %")
                ),
                text=f"{zip_code}",
                textposition="top center",
                hoverinfo='text',
                hovertext=hover_text,
                name=zip_code
            ))

fig_awareness.update_layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=30.2672, lon=-97.7431),
        zoom=10
    ),
    showlegend=False,
    height=600,
    width=None,
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=0),
    title="Average Program Awareness by Zip Code"
)

# 3. Sentiment Map
fig_sentiment = go.Figure()

for zip_code, sentiment in zip_sentiment.items():
    if zip_code in austin_zip_coords:
        coord = austin_zip_coords[zip_code]
        response_count = zip_counts.get(zip_code, 0)
        # Size based on response count
        size = min(response_count * 0.5, 50)
        
        # Create hover text
        hover_text = f"{zip_code}<br>{coord['area']}<br>"
        hover_text += f"Responses: {response_count}<br>"
        hover_text += f"Sentiment: {sentiment:.1f}/100<br>"
        if sentiment > 65:
            hover_text += "Positive"
        elif sentiment < 35:
            hover_text += "Negative"
        else:
            hover_text += "Neutral"
        
        fig_sentiment.add_trace(go.Scattermapbox(
            lat=[coord['lat']],
            lon=[coord['lon']],
            mode='markers+text',
            marker=dict(
                size=size,
                color=sentiment,
                colorscale='RdYlGn',
                cmin=0,
                cmax=100,
                colorbar=dict(title="Sentiment")
            ),
            text=f"{zip_code}",
            textposition="top center",
            hoverinfo='text',
            hovertext=hover_text,
            name=zip_code
        ))

fig_sentiment.update_layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=30.2672, lon=-97.7431),
        zoom=10
    ),
    showlegend=False,
    height=600,
    width=None,
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=0),
    title="Community Sentiment by Zip Code (0=Negative, 50=Neutral, 100=Positive)"
)

# 4. Combined Dashboard
fig_dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Response Distribution', 'Average Program Awareness', 
                    'Community Sentiment', 'Equity Analysis'),
    specs=[[{'type': 'mapbox'}, {'type': 'mapbox'}],
           [{'type': 'mapbox'}, {'type': 'bar'}]]
)

# Save individual maps as HTML
print("Saving interactive maps...")
fig_responses.write_html('map_responses.html')
fig_awareness.write_html('map_awareness.html')
fig_sentiment.write_html('map_sentiment.html')

# Export map data for integration into main report
# Add config to ensure full width display
config = {'responsive': True, 'displayModeBar': False}
map_data = {
    'response_map': fig_responses.to_html(include_plotlyjs='cdn', div_id="response-map", config=config),
    'awareness_map': fig_awareness.to_html(include_plotlyjs='cdn', div_id="awareness-map", config=config),
    'sentiment_map': fig_sentiment.to_html(include_plotlyjs='cdn', div_id="sentiment-map", config=config),
    'zip_stats': {
        'total_zips': len(zip_counts),
        'highest_response_zip': zip_counts.index[0],
        'highest_response_count': int(zip_counts.iloc[0]),
        'lowest_awareness_zips': [z for z, d in zip_awareness.items() if d['avg_awareness'] < 30],
        'highest_sentiment_zips': [z for z, s in zip_sentiment.items() if s > 70]
    }
}

with open('map_data.json', 'w') as f:
    json.dump(map_data, f)

# Print key insights
print("\n" + "="*50)
print("GEOGRAPHIC INSIGHTS")
print("="*50)

print(f"\nResponse Distribution:")
print(f"  - Highest response: {zip_counts.index[0]} ({zip_counts.iloc[0]} responses)")
print(f"  - Coverage: {len(zip_counts)} of 50 Austin zip codes")

if zip_awareness:
    low_awareness = [(z, d['avg_awareness']) for z, d in zip_awareness.items() if d['avg_awareness'] < 40]
    if low_awareness:
        print(f"\nLow Program Awareness Areas:")
        for zip_code, awareness in sorted(low_awareness, key=lambda x: x[1])[:5]:
            print(f"  - {zip_code}: {awareness:.1f}% average awareness")

print(f"\nSentiment Patterns:")
positive_zips = [z for z, s in zip_sentiment.items() if s > 65]
negative_zips = [z for z, s in zip_sentiment.items() if s < 35]
print(f"  - Most positive areas: {len(positive_zips)} zip codes")
print(f"  - Most negative areas: {len(negative_zips)} zip codes")

print("\nMaps saved as HTML files:")
print("  - map_responses.html")
print("  - map_awareness.html") 
print("  - map_sentiment.html")
print("\nReady for integration into main report.")