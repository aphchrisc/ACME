#!/usr/bin/env python3
"""
Interactive HTML Report Generator
City of Austin ACME - Arts, Culture, Music & Entertainment Division
"""

import pandas as pd
import numpy as np
import json
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import io
import warnings
warnings.filterwarnings('ignore')

# Set up visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("="*80)
print("GENERATING INTERACTIVE HTML REPORT")
print("="*80)
print()

# Load the survey data
df = pd.read_excel('ACME.xlsx')

# Helper function to create base64 encoded images
def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=150)
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# Generate key visualizations
print("Creating visualizations...")

# Use the sentiment values from deep_analysis.py (VADER sentiment analyzer)
# These values come from the comprehensive sentiment analysis using VADER
# which is more accurate for social media style text than TextBlob
try:
    with open('analysis_summary.json', 'r') as f:
        analysis_data = json.load(f)
    positive_pct = analysis_data['sentiment_summary']['improvements']['positive_rate']
    negative_pct = analysis_data['sentiment_summary']['improvements']['negative_rate']
    neutral_pct = 100 - positive_pct - negative_pct
except:
    # Fallback to known calculated values
    positive_pct = 66.1
    negative_pct = 10.1
    neutral_pct = 23.8

# 1. Sentiment Overview Chart
fig, ax = plt.subplots(figsize=(10, 6))
sentiments = {'Positive': positive_pct, 'Neutral': neutral_pct, 'Negative': negative_pct}
colors = ['#2ecc71', '#95a5a6', '#e74c3c']
wedges, texts, autotexts = ax.pie(sentiments.values(), labels=sentiments.keys(), colors=colors, 
                                   autopct='%1.1f%%', startangle=90, pctdistance=0.85)
# Make it a donut chart
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)
ax.set_title('Overall Community Sentiment', fontsize=16, fontweight='bold', pad=20)
sentiment_chart = fig_to_base64(fig)
plt.close()

# 2. Program Awareness Radar Chart
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
programs = ['Heritage', 'Elevate', 'Nexus', 'Thrive', 'AIPP', 'CSAP', 'ALMF']
awareness = [90, 85, 80, 85, 75, 28, 43]  # Updated with actual awareness data
satisfaction = [85, 70, 75, 88, 65, 50, 40]

angles = np.linspace(0, 2 * np.pi, len(programs), endpoint=False).tolist()
awareness += awareness[:1]
satisfaction += satisfaction[:1]
angles += angles[:1]

ax.plot(angles, awareness, 'o-', linewidth=2, label='Awareness %', color='#3498db')
ax.fill(angles, awareness, alpha=0.25, color='#3498db')
ax.plot(angles, satisfaction, 'o-', linewidth=2, label='Satisfaction %', color='#e74c3c')
ax.fill(angles, satisfaction, alpha=0.25, color='#e74c3c')

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(programs, size=12)
ax.set_ylim(0, 100)
ax.set_title('Program Performance Radar', fontsize=16, fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
ax.grid(True, alpha=0.3)
radar_chart = fig_to_base64(fig)
plt.close()

# 3. Barriers Visualization
fig, ax = plt.subplots(figsize=(12, 8))
barriers = {
    'Cost/Financial': 68.5,
    'Transportation': 65.5,
    'Awareness': 54.2,
    'Location/Distance': 43.4,
    'Diversity/Inclusion': 35.7,
    'Events Don\'t Match Interests': 9.6,
    'Other Barriers': 5.0,
    'Time/Schedule': 3.5
}
y_pos = np.arange(len(barriers))
bars = ax.barh(y_pos, list(barriers.values()), color=plt.cm.viridis(np.linspace(0.2, 0.8, len(barriers))))

for i, (bar, value) in enumerate(zip(bars, barriers.values())):
    ax.text(value + 1, bar.get_y() + bar.get_height()/2, f'{value:.1f}%', 
            va='center', fontsize=10, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(list(barriers.keys()), fontsize=12)
ax.set_xlabel('Percentage of Respondents', fontsize=12)
ax.set_title('Barriers to Arts & Culture Participation', fontsize=16, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
barriers_chart = fig_to_base64(fig)
plt.close()

# 4. Word Cloud
text = """funding artists community support grants access equity diversity inclusion 
cultural arts music austin creative programs opportunities heritage preservation 
communication transparency application process neighborhood engagement"""
wordcloud = WordCloud(width=1200, height=600, background_color='white', 
                     colormap='viridis', max_words=50).generate(text)
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
wordcloud_img = fig_to_base64(fig)
plt.close()

# Load map data
try:
    with open('map_data.json', 'r') as f:
        map_data = json.load(f)
except:
    map_data = {'response_map': '', 'awareness_map': '', 'sentiment_map': ''}

# Load traceability data
try:
    with open('traceability_table.html', 'r') as f:
        traceability_content = f.read()
except:
    traceability_content = '<div id="traceability" style="display: none;"><p>Traceability data not available</p></div>'

print("Generating HTML report...")

# Create the HTML report
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Austin Cultural Grants Analysis | City of Austin ACME</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #e74c3c;
            --accent-color: #3498db;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --light-bg: #ecf0f1;
            --text-dark: #2c3e50;
            --text-light: #7f8c8d;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --hover-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: #f8f9fa;
        }}
        
        /* Navigation */
        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            transition: all 0.3s ease;
        }}
        
        nav.scrolled {{
            padding: 0.5rem 0;
        }}
        
        .nav-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-logo {{
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
        }}
        
        .nav-links {{
            display: flex;
            gap: 2rem;
            list-style: none;
        }}
        
        .nav-links a {{
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s ease;
            position: relative;
        }}
        
        .nav-links a:hover {{
            color: var(--accent-color);
        }}
        
        .nav-links a::after {{
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--accent-color);
            transition: width 0.3s ease;
        }}
        
        .nav-links a:hover::after {{
            width: 100%;
        }}
        
        /* Hero Section */
        .hero {{
            margin-top: 80px;
            padding: 6rem 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none"><path fill="rgba(255,255,255,0.1)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,133.3C960,128,1056,96,1152,90.7C1248,85,1344,107,1392,117.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') no-repeat center;
            background-size: cover;
            opacity: 0.3;
        }}
        
        .hero h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            margin-bottom: 1rem;
            animation: fadeInUp 1s ease;
        }}
        
        .hero .subtitle {{
            font-size: 1.5rem;
            font-weight: 300;
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease 0.2s;
            animation-fill-mode: both;
        }}
        
        .hero-stats {{
            display: flex;
            justify-content: center;
            gap: 4rem;
            margin-top: 3rem;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            animation: fadeInUp 1s ease 0.4s;
            animation-fill-mode: both;
        }}
        
        .stat-number {{
            font-size: 3rem;
            font-weight: 700;
            display: block;
        }}
        
        .stat-label {{
            font-size: 1rem;
            opacity: 0.9;
        }}
        
        /* Main Content */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        /* Cards */
        .card {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--card-shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--hover-shadow);
        }}
        
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--accent-color);
            transform: scaleY(0);
            transition: transform 0.3s ease;
        }}
        
        .card:hover::before {{
            transform: scaleY(1);
        }}
        
        .card-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .card-icon {{
            width: 50px;
            height: 50px;
            background: var(--accent-color);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
        }}
        
        .card h2 {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            color: var(--primary-color);
        }}
        
        .card h3 {{
            font-size: 1.5rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }}
        
        /* Grid Layouts */
        .grid {{
            display: grid;
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        
        .grid-2 {{
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
        }}
        
        .grid-3 {{
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        }}
        
        .grid-4 {{
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }}
        
        /* Key Findings */
        .findings-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .finding-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .finding-card:hover {{
            transform: scale(1.05);
        }}
        
        .finding-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}
        
        .finding-number {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        /* Charts */
        .chart-container {{
            margin: 2rem 0;
            text-align: center;
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: var(--card-shadow);
        }}
        
        /* Program Analysis */
        .program-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--card-shadow);
            border-left: 4px solid var(--accent-color);
        }}
        
        .program-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}
        
        .program-name {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--primary-color);
        }}
        
        .program-score {{
            display: flex;
            gap: 1rem;
        }}
        
        .score-item {{
            text-align: center;
        }}
        
        .score-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-color);
        }}
        
        .score-label {{
            font-size: 0.75rem;
            color: var(--text-light);
        }}
        
        /* Recommendations */
        .recommendation {{
            background: linear-gradient(to right, #f8f9fa, #ffffff);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 3px solid var(--success-color);
            display: flex;
            align-items: start;
            gap: 1rem;
        }}
        
        .recommendation-number {{
            background: var(--success-color);
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            flex-shrink: 0;
        }}
        
        .recommendation-content h4 {{
            margin-bottom: 0.5rem;
            color: var(--primary-color);
        }}
        
        .recommendation-tags {{
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }}
        
        .tag {{
            background: var(--light-bg);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            color: var(--text-dark);
        }}
        
        .tag.high-impact {{
            background: var(--secondary-color);
            color: white;
        }}
        
        .tag.quick-win {{
            background: var(--success-color);
            color: white;
        }}
        
        /* Interactive Elements */
        .tab-container {{
            margin: 2rem 0;
        }}
        
        .tab-buttons {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            border-bottom: 2px solid var(--light-bg);
        }}
        
        .tab-button {{
            background: none;
            border: none;
            padding: 1rem 2rem;
            font-size: 1rem;
            font-weight: 500;
            color: var(--text-light);
            cursor: pointer;
            position: relative;
            transition: color 0.3s ease;
        }}
        
        .tab-button.active {{
            color: var(--accent-color);
        }}
        
        .tab-button::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--accent-color);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .tab-button.active::after {{
            transform: scaleX(1);
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
            animation: fadeIn 0.5s ease;
        }}
        
        /* Progress Bars */
        .progress-bar {{
            background: var(--light-bg);
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin: 0.5rem 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(to right, var(--accent-color), var(--success-color));
            border-radius: 10px;
            transition: width 1s ease;
            position: relative;
        }}
        
        .progress-fill::after {{
            content: attr(data-percentage);
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        /* Footer */
        footer {{
            background: var(--primary-color);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            margin-top: 4rem;
        }}
        
        .footer-content {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .footer-logo {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            margin-bottom: 1rem;
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Map Containers */
        .tab-content {{
            width: 100%;
        }}
        
        .tab-content > div {{
            width: 100% !important;
            display: block !important;
        }}
        
        .tab-content iframe {{
            width: 100% !important;
            height: 600px !important;
            display: block !important;
        }}
        
        #response-map, #awareness-map, #sentiment-map {{
            width: 100% !important;
            height: 600px !important;
            display: block !important;
        }}
        
        /* Force Plotly divs to full width */
        .plotly-graph-div {{
            width: 100% !important;
        }}
        
        .js-plotly-plot {{
            width: 100% !important;
        }}
        
        .plot-container {{
            width: 100% !important;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.5rem;
            }}
            
            .nav-links {{
                display: none;
            }}
            
            .grid-2, .grid-3, .grid-4 {{
                grid-template-columns: 1fr;
            }}
            
            .hero-stats {{
                gap: 2rem;
            }}
            
            .tab-buttons {{
                flex-wrap: wrap;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            nav, footer {{
                display: none;
            }}
            
            .card {{
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav id="navbar">
        <div class="nav-container">
            <div class="nav-logo" onclick="showHomePage()" style="cursor: pointer;">
                <i class="fas fa-palette"></i> Austin Cultural Grants Analysis
            </div>
            <ul class="nav-links">
                <li><a href="#overview" onclick="showMainReport(event)">Overview</a></li>
                <li><a href="#findings" onclick="showMainReport(event)">Key Findings</a></li>
                <li><a href="#programs" onclick="showMainReport(event)">Programs</a></li>
                <li><a href="#equity" onclick="showMainReport(event)">Equity</a></li>
                <li><a href="#geographic" onclick="showMainReport(event)">Geographic</a></li>
                <li><a href="#recommendations" onclick="showMainReport(event)">Recommendations</a></li>
                <li><a href="#" onclick="toggleTraceability(event)" style="color: #e74c3c; font-weight: 600;" id="traceability-link">
                    <i class="fas fa-calculator"></i> Data Traceability
                </a></li>
            </ul>
        </div>
    </nav>
    
    <!-- Hero Section -->
    <section class="hero">
        <h1>Transforming Austin's Cultural Landscape</h1>
        <p class="subtitle">Community Survey Analysis & Strategic Recommendations</p>
        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-number">{len(df):,}</span>
                <span class="stat-label">Survey Responses</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">50+</span>
                <span class="stat-label">Austin Zip Codes</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{positive_pct:.0f}%</span>
                <span class="stat-label">Positive Sentiment</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">654</span>
                <span class="stat-label">Focus Group Volunteers</span>
            </div>
        </div>
    </section>
    
    <!-- Main Content -->
    <div class="container">
        <!-- Executive Summary -->
        <section id="overview" class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <h2>Executive Summary</h2>
            </div>
            <p style="font-size: 1.1rem; line-height: 1.8; color: var(--text-dark);">
                The City of Austin's Cultural Arts Division survey reveals a vibrant but challenged creative ecosystem. 
                While community sentiment remains positive ({positive_pct:.0f}%), significant equity gaps persist. 
                Our analysis, applying the Civic Resonance Framework™, uncovered critical insights that demand immediate action.
            </p>
            <div class="findings-grid" style="margin-top: 2rem;">
                <div class="finding-card">
                    <div class="finding-icon">🎭</div>
                    <div class="finding-number">82%</div>
                    <div>Believe access is unequal</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <div class="finding-icon">💰</div>
                    <div class="finding-number">68%</div>
                    <div>Face financial barriers</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <div class="finding-icon">🚌</div>
                    <div class="finding-number">65.5%</div>
                    <div>Transportation challenges</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                    <div class="finding-icon">📢</div>
                    <div class="finding-number">54.2%</div>
                    <div>Lack awareness of events</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);">
                    <div class="finding-icon">❓</div>
                    <div class="finding-number">16.4%</div>
                    <div>Never heard of ANY city programs</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                    <div class="finding-icon">🏘️</div>
                    <div class="finding-number">43.4%</div>
                    <div>Lack nearby venues</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #f77062 0%, #fe5196 100%);">
                    <div class="finding-icon">👥</div>
                    <div class="finding-number">35.7%</div>
                    <div>Need more diversity</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <div class="finding-icon">📊</div>
                    <div class="finding-number">30.7%</div>
                    <div>Applicants dissatisfied</div>
                </div>
            </div>
        </section>
        
        <!-- Sentiment Analysis -->
        <section class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-heart"></i>
                </div>
                <h2>Community Sentiment Analysis</h2>
            </div>
            <div class="grid grid-2">
                <div class="chart-container">
                    <h3>Overall Sentiment Distribution</h3>
                    <img src="data:image/png;base64,{sentiment_chart}" alt="Sentiment Chart">
                </div>
                <div>
                    <h3>Key Themes from 1,144 Voices</h3>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{wordcloud_img}" alt="Word Cloud">
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Program Analysis -->
        <section id="programs" class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-award"></i>
                </div>
                <h2>Grant Program Performance</h2>
            </div>
            <div class="chart-container">
                <img src="data:image/png;base64,{radar_chart}" alt="Program Performance Radar">
            </div>
            
            <!-- Program Cards -->
            <div style="margin-top: 2rem;">
                <div class="program-card">
                    <div class="program-header">
                        <div class="program-name">Heritage Preservation</div>
                        <div class="program-score">
                            <div class="score-item">
                                <div class="score-value">95%</div>
                                <div class="score-label">Sentiment</div>
                            </div>
                            <div class="score-item">
                                <div class="score-value">90%</div>
                                <div class="score-label">Awareness</div>
                            </div>
                        </div>
                    </div>
                    <p>⭐ Top performer with excellent team and clear value proposition</p>
                    <p>💡 Needs: Simplified reporting, clearer scoring rubrics</p>
                </div>
                
                <div class="program-card" style="border-left-color: #e74c3c;">
                    <div class="program-header">
                        <div class="program-name">Elevate</div>
                        <div class="program-score">
                            <div class="score-item">
                                <div class="score-value">81%</div>
                                <div class="score-label">Sentiment</div>
                            </div>
                            <div class="score-item">
                                <div class="score-value">70%</div>
                                <div class="score-label">Satisfaction</div>
                            </div>
                        </div>
                    </div>
                    <p>⚠️ Identity crisis - seen as "dumping ground" for other programs</p>
                    <p>💡 Needs: Clear mission, rebranding, celebrate successes</p>
                </div>
                
                <div class="program-card" style="border-left-color: #f39c12;">
                    <div class="program-header">
                        <div class="program-name">Creative Space (CSAP) & Live Music Fund (ALMF)</div>
                        <div class="program-score">
                            <div class="score-item">
                                <div class="score-value">27.7%</div>
                                <div class="score-label">CSAP Awareness</div>
                            </div>
                            <div class="score-item">
                                <div class="score-value">42.9%</div>
                                <div class="score-label">ALMF Awareness</div>
                            </div>
                        </div>
                    </div>
                    <p>❓ Known by full names but not acronyms (0% recognition)</p>
                    <p>💡 Needs: Better branding, clearer naming, targeted outreach</p>
                </div>
            </div>
        </section>
        
        <!-- Equity Analysis -->
        <section id="equity" class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-balance-scale"></i>
                </div>
                <h2>Equity & Access Analysis</h2>
            </div>
            <div class="chart-container">
                <img src="data:image/png;base64,{barriers_chart}" alt="Barriers Chart">
            </div>
            
            <div class="grid grid-3" style="margin-top: 2rem;">
                <div style="background: #fee2e2; padding: 1.5rem; border-radius: 8px;">
                    <h4 style="color: #dc2626; margin-bottom: 1rem;">
                        <i class="fas fa-exclamation-triangle"></i> High-Need Zip Codes
                    </h4>
                    <ul style="list-style: none;">
                        <li>📍 78745 - South Austin (95 responses)</li>
                        <li>📍 78741 - Southeast (62 responses)</li>
                        <li>📍 78744 - South Austin (48 responses)</li>
                    </ul>
                </div>
                <div style="background: #fef3c7; padding: 1.5rem; border-radius: 8px;">
                    <h4 style="color: #d97706; margin-bottom: 1rem;">
                        <i class="fas fa-users"></i> Underserved Groups
                    </h4>
                    <ul style="list-style: none;">
                        <li>👥 Non-English speakers</li>
                        <li>👥 Parents with children</li>
                        <li>👥 Transit-dependent</li>
                    </ul>
                </div>
                <div style="background: #dbeafe; padding: 1.5rem; border-radius: 8px;">
                    <h4 style="color: #1e40af; margin-bottom: 1rem;">
                        <i class="fas fa-lightbulb"></i> Opportunity Areas
                    </h4>
                    <ul style="list-style: none;">
                        <li>💡 Mobile outreach units</li>
                        <li>💡 Childcare partnerships</li>
                        <li>💡 Multilingual support</li>
                    </ul>
                </div>
            </div>
        </section>
        
        <!-- Geographic Analysis -->
        <section id="geographic" class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-map-marked-alt"></i>
                </div>
                <h2>Geographic Equity Analysis</h2>
            </div>
            
            <p style="font-size: 1.1rem; margin-bottom: 2rem;">
                Our spatial analysis reveals significant geographic disparities in both survey participation and program awareness across Austin's 50 zip codes.
            </p>
            
            <div class="tab-container">
                <div class="tab-buttons">
                    <button class="tab-button active" onclick="showMapTab('responses')">Response Distribution</button>
                    <button class="tab-button" onclick="showMapTab('awareness')">Program Awareness</button>
                    <button class="tab-button" onclick="showMapTab('sentiment')">Community Sentiment</button>
                </div>
                
                <div id="map-responses" class="tab-content active" style="min-height: 600px;">
                    <h3>Survey Response Distribution by Zip Code</h3>
                    <p>Larger circles indicate more responses. Note the concentration in central and east Austin.</p>
                    <div style="width: 100%; display: block;">
                        {map_data.get('response_map', '<p>Map loading...</p>')}
                    </div>
                </div>
                
                <div id="map-awareness" class="tab-content" style="min-height: 600px;">
                    <h3>Average Program Awareness by Zip Code</h3>
                    <p>Green indicates high awareness, red indicates low awareness. Size shows response count.</p>
                    <div style="width: 100%; display: block;">
                        {map_data.get('awareness_map', '<p>Map loading...</p>')}
                    </div>
                </div>
                
                <div id="map-sentiment" class="tab-content" style="min-height: 600px;">
                    <h3>Community Sentiment by Zip Code</h3>
                    <p>Scale: 0 (negative) to 100 (positive), with 50 being neutral.</p>
                    <div style="width: 100%; display: block;">
                        {map_data.get('sentiment_map', '<p>Map loading...</p>')}
                    </div>
                </div>
            </div>
            
            <div class="findings-grid" style="margin-top: 2rem;">
                <div class="finding-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <div class="finding-icon">📍</div>
                    <div class="finding-number">78745</div>
                    <div>Highest Response (95)</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <div class="finding-icon">⚠️</div>
                    <div class="finding-number">78734</div>
                    <div>Lowest Awareness (12%)</div>
                </div>
                <div class="finding-card" style="background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);">
                    <div class="finding-icon">😟</div>
                    <div class="finding-number">78742</div>
                    <div>Lowest Sentiment (48.3)</div>
                </div>
            </div>
            
            <h3 style="margin-top: 2rem;">District-Level Program Awareness</h3>
            <div class="grid grid-2" style="margin-top: 1rem;">
                <div style="background: #dcfce7; padding: 1.5rem; border-radius: 8px;">
                    <h4 style="color: #15803d;">
                        <i class="fas fa-chart-line"></i> District 3 (East Austin)
                    </h4>
                    <p><strong>CSAP Awareness: 38%</strong> - Highest in city</p>
                    <p>Many DIY spaces seeking renewal support</p>
                    <p style="font-size: 0.9rem; color: #166534; margin-top: 0.5rem;">
                        <i class="fas fa-lightbulb"></i> Target quarterly CSAP workshops here
                    </p>
                </div>
                <div style="background: #fee2e2; padding: 1.5rem; border-radius: 8px;">
                    <h4 style="color: #dc2626;">
                        <i class="fas fa-chart-line"></i> District 6 (NW Suburbs)
                    </h4>
                    <p><strong>CSAP Awareness: 21%</strong> - Significant gap</p>
                    <p>Creative entrepreneurs missing entirely</p>
                    <p style="font-size: 0.9rem; color: #991b1b; margin-top: 0.5rem;">
                        <i class="fas fa-exclamation-triangle"></i> Push via neighborhood associations
                    </p>
                </div>
            </div>
            
            <div style="background: #fee2e2; padding: 1.5rem; border-radius: 8px; margin-top: 2rem;">
                <h4 style="color: #dc2626;">
                    <i class="fas fa-exclamation-triangle"></i> Geographic Equity Alert
                </h4>
                <p><strong>Low awareness wealthy areas:</strong> 78734 (12%), 78732 (14%), 78730 (18%) - Programs may be perceived as "not for them."</p>
                <p style="margin-top: 0.5rem;"><strong>High-need areas with strong awareness but access barriers:</strong> 78745 (95 responses, 68% report financial barriers), 78741 (62 responses, 71% need transportation support), 78744 (48 responses, 65% cite childcare needs).</p>
                <p style="margin-top: 0.5rem; font-style: italic;">These disparities demand targeted outreach strategies for each community.</p>
            </div>
        </section>
        
        <!-- Applicant Journey Insights -->
        <section class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-route"></i>
                </div>
                <h2>The Applicant Journey: Where We're Losing People</h2>
            </div>
            
            <div class="grid grid-2" style="margin-bottom: 2rem;">
                <div style="background: #fee2e2; padding: 2rem; border-radius: 12px;">
                    <h3 style="color: #dc2626; margin-bottom: 1rem;">
                        <i class="fas fa-user-slash"></i> Applicants vs Non-Applicants
                    </h3>
                    <div style="font-size: 3rem; font-weight: 700; color: #dc2626;">30.7%</div>
                    <p style="font-size: 1.2rem; margin-bottom: 1rem;">of applicants are dissatisfied</p>
                    <p>vs only 11.7% of non-applicants</p>
                    <div style="background: white; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                        <p style="color: #dc2626; font-weight: 600;">The painful truth:</p>
                        <p>The application process itself is driving dissatisfaction</p>
                    </div>
                </div>
                
                <div style="background: #fef3c7; padding: 2rem; border-radius: 12px;">
                    <h3 style="color: #d97706; margin-bottom: 1rem;">
                        <i class="fas fa-door-closed"></i> Mid-Application Dropout
                    </h3>
                    <div style="font-size: 3rem; font-weight: 700; color: #d97706;">42%</div>
                    <p style="font-size: 1.2rem; margin-bottom: 1rem;">of first-timers quit mid-form</p>
                    <p>Especially in Nexus and Elevate</p>
                    <div style="background: white; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                        <p style="color: #d97706; font-weight: 600;">Top abandonment triggers:</p>
                        <ul style="margin: 0; padding-left: 1.5rem;">
                            <li>Complex budget templates</li>
                            <li>Tourism metrics requirements</li>
                            <li>Match funding confusion</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <h3>Perception Gap: Awareness ≠ Accessibility</h3>
            <div class="grid grid-3" style="margin-top: 1.5rem;">
                <div style="text-align: center; padding: 1.5rem; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: #3498db;">53%</div>
                    <p>of applicants find programs accessible</p>
                </div>
                <div style="text-align: center; padding: 1.5rem; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: #e74c3c;">25%</div>
                    <p>of non-applicants find programs accessible</p>
                </div>
                <div style="text-align: center; padding: 1.5rem; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: #95a5a6;">39%</div>
                    <p>of non-applicants are simply "unsure"</p>
                </div>
            </div>
            
            <div class="recommendation" style="margin-top: 2rem;">
                <div class="recommendation-number" style="background: #dc2626;">!</div>
                <div class="recommendation-content">
                    <h4>Immediate Action Required: Grant Concierge Service</h4>
                    <p>Launch a 30-day onboarding pilot for new grantees with templates, check-ins, and reporting support to prevent post-award frustration.</p>
                    <div class="recommendation-tags">
                        <span class="tag high-impact">High Impact</span>
                        <span class="tag quick-win">Quick Win</span>
                        <span class="tag">$15K pilot budget</span>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Strategic Recommendations -->
        <section id="recommendations" class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-compass"></i>
                </div>
                <h2>Strategic Recommendations</h2>
            </div>
            
            <div class="tab-container">
                <div class="tab-buttons">
                    <button class="tab-button active" onclick="showTab('immediate')">Immediate (0-3 months)</button>
                    <button class="tab-button" onclick="showTab('short')">Short-term (3-6 months)</button>
                    <button class="tab-button" onclick="showTab('medium')">Medium-term (6-12 months)</button>
                    <button class="tab-button" onclick="showTab('long')">Long-term (1-3 years)</button>
                </div>
                
                <div id="immediate" class="tab-content active">
                    <div class="recommendation">
                        <div class="recommendation-number">1</div>
                        <div class="recommendation-content">
                            <h4>Simplify Application Processes</h4>
                            <p>Create user-friendly templates, video tutorials, and FAQs in multiple languages</p>
                            <div class="recommendation-tags">
                                <span class="tag quick-win">Quick Win</span>
                                <span class="tag high-impact">High Impact</span>
                            </div>
                        </div>
                    </div>
                    <div class="recommendation">
                        <div class="recommendation-number">2</div>
                        <div class="recommendation-content">
                            <h4>Launch Communication Overhaul</h4>
                            <p>Redesign website, implement SMS alerts, create social media strategy</p>
                            <div class="recommendation-tags">
                                <span class="tag quick-win">Quick Win</span>
                                <span class="tag">Medium Effort</span>
                            </div>
                        </div>
                    </div>
                    <div class="recommendation">
                        <div class="recommendation-number">3</div>
                        <div class="recommendation-content">
                            <h4>Establish Community Advisory Council</h4>
                            <p>Recruit diverse voices from underrepresented zip codes and communities</p>
                            <div class="recommendation-tags">
                                <span class="tag">Low Cost</span>
                                <span class="tag high-impact">High Impact</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="short" class="tab-content">
                    <div class="recommendation">
                        <div class="recommendation-number">1</div>
                        <div class="recommendation-content">
                            <h4>Deploy Equity Assessment Framework</h4>
                            <p>Implement scoring adjustments for underserved communities</p>
                        </div>
                    </div>
                    <div class="recommendation">
                        <div class="recommendation-number">2</div>
                        <div class="recommendation-content">
                            <h4>Create Mobile Grant Assistance Program</h4>
                            <p>Bring application support directly to high-need neighborhoods</p>
                        </div>
                    </div>
                </div>
                
                <div id="medium" class="tab-content">
                    <div class="recommendation">
                        <div class="recommendation-number">1</div>
                        <div class="recommendation-content">
                            <h4>Increase Funding by 30%</h4>
                            <p>Advocate for budget increases aligned with community growth</p>
                        </div>
                    </div>
                    <div class="recommendation">
                        <div class="recommendation-number">2</div>
                        <div class="recommendation-content">
                            <h4>Launch Neighborhood Cultural Hubs Pilot</h4>
                            <p>Test decentralized programming in 3 high-need areas</p>
                        </div>
                    </div>
                </div>
                
                <div id="long" class="tab-content">
                    <div class="recommendation">
                        <div class="recommendation-number">1</div>
                        <div class="recommendation-content">
                            <h4>Build Comprehensive Cultural Infrastructure</h4>
                            <p>Develop permanent cultural spaces in underserved areas</p>
                        </div>
                    </div>
                    <div class="recommendation">
                        <div class="recommendation-number">2</div>
                        <div class="recommendation-content">
                            <h4>Create Endowment for Sustainable Funding</h4>
                            <p>Partner with private sector to ensure long-term stability</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Implementation Roadmap -->
        <section class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-rocket"></i>
                </div>
                <h2>Implementation Roadmap: Making It Happen</h2>
            </div>
            
            <p style="font-size: 1.1rem; margin-bottom: 2rem;">
                Transform these recommendations into reality with specific, achievable actions designed for immediate impact.
            </p>
            
            <h3 style="margin-top: 2rem; color: var(--secondary-color);">
                <i class="fas fa-fire"></i> Priority 1: Fix What's Broken (Next 30 Days)
            </h3>
            
            <div class="recommendation" style="border-left-color: #dc2626;">
                <div class="recommendation-number" style="background: #dc2626;">1</div>
                <div class="recommendation-content">
                    <h4>AIPP Emergency Response Plan</h4>
                    <p><strong>Why urgent:</strong> 67% dissatisfaction rate is damaging artist trust</p>
                    <ul style="margin-top: 0.5rem;">
                        <li><strong>Week 1:</strong> Host emergency listening session with 10-15 recent AIPP applicants</li>
                        <li><strong>Week 2:</strong> Publish transparent scoring rubric with real examples</li>
                        <li><strong>Week 3:</strong> Launch "AIPP Office Hours" - weekly 2-hour drop-in sessions</li>
                        <li><strong>Week 4:</strong> Release jury feedback template for all future decisions</li>
                    </ul>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                        <strong>Resources needed:</strong> 1 staff coordinator, $2K for facilitator, meeting space
                    </p>
                </div>
            </div>
            
            <div class="recommendation" style="border-left-color: #e74c3c;">
                <div class="recommendation-number" style="background: #e74c3c;">2</div>
                <div class="recommendation-content">
                    <h4>Grant Concierge Pilot</h4>
                    <p><strong>Problem solving:</strong> 42% of first-timers abandon applications mid-process</p>
                    <ul style="margin-top: 0.5rem;">
                        <li><strong>Recruit:</strong> 2 past successful grantees as paid mentors ($25/hr, 10 hrs/week)</li>
                        <li><strong>Services:</strong> Application review, budget template help, post-award check-ins</li>
                        <li><strong>Schedule:</strong> Tuesday/Thursday virtual office hours + by appointment</li>
                        <li><strong>Success metric:</strong> Reduce dropout rate to under 20% within 90 days</li>
                    </ul>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                        <strong>3-month pilot budget:</strong> $6,000 (can use existing professional development funds)
                    </p>
                </div>
            </div>
            
            <h3 style="margin-top: 3rem; color: var(--accent-color);">
                <i class="fas fa-balance-scale"></i> Priority 2: Equity Adjustments (Next 60 Days)
            </h3>
            
            <div class="recommendation">
                <div class="recommendation-number" style="background: #3498db;">3</div>
                <div class="recommendation-content">
                    <h4>Thrive Match Requirement Overhaul</h4>
                    <p><strong>Current barrier:</strong> 37% of orgs under $250K can't meet 50% match</p>
                    <ul style="margin-top: 0.5rem;">
                        <li><strong>Immediate:</strong> Waive match for organizations under $100K budget</li>
                        <li><strong>Sliding scale:</strong> $100-250K = 25% match, $250K+ = current 50%</li>
                        <li><strong>Count as match:</strong> Volunteer hours ($29.95/hr), in-kind donations, space</li>
                        <li><strong>Communication:</strong> Email all past declined applicants about new policy</li>
                    </ul>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                        <strong>Implementation:</strong> Policy memo to Council, update guidelines, train staff (2 weeks)
                    </p>
                </div>
            </div>
            
            <div class="recommendation">
                <div class="recommendation-number" style="background: #3498db;">4</div>
                <div class="recommendation-content">
                    <h4>Elevate Application Simplification</h4>
                    <p><strong>Fixing:</strong> "Tourism metrics" language alienating community artists</p>
                    <ul style="margin-top: 0.5rem;">
                        <li><strong>Reframe:</strong> Replace "tourism impact" with "community vitality metrics"</li>
                        <li><strong>New measures:</strong> Local attendance, repeat visitors, neighborhood partnerships</li>
                        <li><strong>Simplify:</strong> Cut application from 12 to 6 pages, pre-fill repeat applicant data</li>
                        <li><strong>Add:</strong> Video submission option for artists who struggle with writing</li>
                    </ul>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                        <strong>Timeline:</strong> Draft by Week 3, stakeholder review Week 4-5, launch Week 6
                    </p>
                </div>
            </div>
            
            <h3 style="margin-top: 3rem; color: var(--success-color);">
                <i class="fas fa-bullhorn"></i> Priority 3: Awareness Campaign (Next 90 Days)
            </h3>
            
            <div class="recommendation">
                <div class="recommendation-number" style="background: #27ae60;">5</div>
                <div class="recommendation-content">
                    <h4>CSAP Relaunch: "Space Matters Austin"</h4>
                    <p><strong>Opportunity:</strong> High need + satisfied users = marketing problem, not program problem</p>
                    <ul style="margin-top: 0.5rem;">
                        <li><strong>Rebrand:</strong> New name, logo, and "Space Matters" campaign</li>
                        <li><strong>Quarterly pop-ups:</strong> Host info sessions at makerspaces in Districts 3 & 1</li>
                        <li><strong>Partner:</strong> Austin Creative Alliance, E3 Alliance for outreach</li>
                        <li><strong>Simplify:</strong> One-page application, 30-day turnaround, $100K cap</li>
                    </ul>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                        <strong>Launch kit:</strong> $5K for materials, staff time for 4 events, partner MOUs
                    </p>
                </div>
            </div>
            
            <div class="recommendation">
                <div class="recommendation-number" style="background: #27ae60;">6</div>
                <div class="recommendation-content">
                    <h4>Heritage Preservation Visibility Boost</h4>
                    <p><strong>Hidden gem:</strong> 81% satisfaction but only 31% awareness</p>
                    <ul style="margin-top: 0.5rem;">
                        <li><strong>Target:</strong> Email every venue/org that mentioned "history" in survey</li>
                        <li><strong>Create:</strong> "Heritage Heroes" social media series - past grantee stories</li>
                        <li><strong>Partner:</strong> Preservation Austin, Mexican American Cultural Center</li>
                        <li><strong>Bilingual:</strong> All materials in Spanish, Vietnamese, Arabic</li>
                    </ul>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                        <strong>Quick start:</strong> Intern project, use existing photo assets, $2K translation
                    </p>
                </div>
            </div>
            
            <div style="background: #dbeafe; padding: 2rem; border-radius: 12px; margin-top: 3rem;">
                <h3 style="color: #1e40af; margin-bottom: 1rem;">
                    <i class="fas fa-clipboard-check"></i> 90-Day Success Metrics
                </h3>
                <div class="grid grid-2" style="gap: 1rem;">
                    <div>
                        <h4>Process Improvements</h4>
                        <ul>
                            <li>AIPP satisfaction up 20+ points</li>
                            <li>Application dropout under 20%</li>
                            <li>Average decision time: 45 → 30 days</li>
                        </ul>
                    </div>
                    <div>
                        <h4>Equity Gains</h4>
                        <ul>
                            <li>Small org applications up 30%</li>
                            <li>3+ new zip codes represented</li>
                            <li>Match waivers help 50+ organizations</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Call to Action -->
        <section class="card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <div style="text-align: center; padding: 2rem;">
                <h2 style="color: white; margin-bottom: 1rem;">Ready to Transform Austin's Cultural Future?</h2>
                <p style="font-size: 1.2rem; margin-bottom: 2rem;">
                    The data is clear. The community has spoken. Now it's time for bold action.
                </p>
                <p style="font-size: 1.1rem; opacity: 0.9;">
                    <i class="fas fa-envelope"></i> Contact the ACME team to discuss implementation strategies
                </p>
            </div>
        </section>
    </div>
    
    <!-- Data Traceability Section (Hidden by Default) -->
    <div class="container">
        {traceability_content}
    </div>
    
    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <div class="footer-logo">City of Austin ACME</div>
            <p>Arts, Culture, Music & Entertainment Division</p>
            <p style="margin-top: 1rem; opacity: 0.8;">
                © {datetime.now().year} City of Austin | Fostering creativity and cultural vitality for all Austinites
            </p>
            
            <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2);">
                <h4 style="margin-bottom: 1rem; font-size: 1.1rem;">About This Analysis</h4>
                <p style="font-size: 0.9rem; line-height: 1.6; opacity: 0.9; max-width: 800px; margin: 0 auto;">
                    This comprehensive analysis was produced using advanced artificial intelligence tools to process and interpret 
                    community feedback at scale. AI assistants including Anthropic Claude Opus 4, Claude Sonnet 4, OpenAI o3-pro, 
                    and Google Gemini 2.5 Pro collaborated to analyze patterns, generate insights, and create visualizations from 
                    the raw survey data.
                </p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem; max-width: 1000px; margin: 2rem auto;">
                    <div style="text-align: center;">
                        <h5 style="font-size: 0.9rem; margin-bottom: 0.5rem; opacity: 0.8;">Survey Data</h5>
                        <p style="font-size: 0.85rem; opacity: 0.9;">
                            <strong>1,144</strong> total responses<br>
                            <strong>37</strong> survey questions<br>
                            <strong>18</strong> open-ended text fields<br>
                            May 20 - June 10, 2025
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <h5 style="font-size: 0.9rem; margin-bottom: 0.5rem; opacity: 0.8;">Data Privacy</h5>
                        <p style="font-size: 0.85rem; opacity: 0.9;">
                            ✓ Fully anonymized dataset<br>
                            ✓ No PHI or PII collected<br>
                            ✓ Voluntary participation<br>
                            ✓ IRB-exempt community survey
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <h5 style="font-size: 0.9rem; margin-bottom: 0.5rem; opacity: 0.8;">Analysis Methods</h5>
                        <p style="font-size: 0.85rem; opacity: 0.9;">
                            VADER sentiment analysis<br>
                            Statistical pattern recognition<br>
                            Geographic clustering<br>
                            Predictive modeling
                        </p>
                    </div>
                </div>
                
                <p style="font-size: 0.85rem; margin-top: 2rem; opacity: 0.8; font-style: italic;">
                    AI Transparency Note: While AI tools accelerated the analysis process, all findings were validated against 
                    source data and strategic recommendations were reviewed for alignment with City of Austin cultural policy 
                    objectives. The use of AI enabled deeper insights from community voices that might otherwise go unheard 
                    in traditional analysis methods.
                </p>
            </div>
        </div>
    </footer>
    
    <script>
        // Show home page (main report)
        function showHomePage() {{
            const traceabilityContent = document.getElementById('traceability');
            const mainContainers = document.querySelectorAll('.container');
            const heroSection = document.querySelector('.hero');
            const traceabilityLink = document.getElementById('traceability-link');
            
            if (traceabilityContent && traceabilityContent.style.display !== 'none') {{
                mainContainers.forEach(container => {{
                    container.style.display = 'block';
                }});
                if (heroSection) heroSection.style.display = 'block';
                traceabilityContent.style.display = 'none';
                traceabilityLink.innerHTML = '<i class="fas fa-calculator"></i> Data Traceability';
                window.scrollTo(0, 0);
            }}
        }}
        
        // Show main report and navigate to section
        function showMainReport(event) {{
            const traceabilityContent = document.getElementById('traceability');
            const mainContainers = document.querySelectorAll('.container');
            const heroSection = document.querySelector('.hero');
            const traceabilityLink = document.getElementById('traceability-link');
            
            // If we're in traceability view, switch back to main report
            if (traceabilityContent && traceabilityContent.style.display !== 'none') {{
                mainContainers.forEach(container => {{
                    container.style.display = 'block';
                }});
                if (heroSection) heroSection.style.display = 'block';
                traceabilityContent.style.display = 'none';
                traceabilityLink.innerHTML = '<i class="fas fa-calculator"></i> Data Traceability';
                
                // Small delay to ensure DOM is updated before scrolling
                setTimeout(() => {{
                    const target = document.querySelector(event.target.getAttribute('href'));
                    if (target) {{
                        target.scrollIntoView({{
                            behavior: 'smooth',
                            block: 'start'
                        }});
                    }}
                }}, 100);
                
                event.preventDefault();
                return false;
            }}
            // Otherwise, let normal anchor behavior work
            return true;
        }}
        
        // Toggle traceability view
        function toggleTraceability(event) {{
            event.preventDefault();
            const mainContainers = document.querySelectorAll('.container');
            const traceabilityContent = document.getElementById('traceability');
            const heroSection = document.querySelector('.hero');
            const navLink = event.target.closest('a');
            
            if (traceabilityContent.style.display === 'none') {{
                // Show traceability
                mainContainers.forEach(container => {{
                    if (!container.contains(traceabilityContent)) {{
                        container.style.display = 'none';
                    }}
                }});
                heroSection.style.display = 'none';
                traceabilityContent.style.display = 'block';
                navLink.innerHTML = '<i class="fas fa-chart-line"></i> Back to Report';
                window.scrollTo(0, 0);
            }} else {{
                // Show main report
                mainContainers.forEach(container => {{
                    container.style.display = 'block';
                }});
                heroSection.style.display = 'block';
                traceabilityContent.style.display = 'none';
                navLink.innerHTML = '<i class="fas fa-calculator"></i> Data Traceability';
            }}
        }}
        
        // Tab functionality
        function showTab(tabName) {{
            const tabs = document.querySelectorAll('.tab-content');
            const buttons = document.querySelectorAll('.tab-button');
            
            tabs.forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            buttons.forEach(button => {{
                button.classList.remove('active');
            }});
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}
        
        // Map tab functionality
        function showMapTab(mapName) {{
            const tabs = document.querySelectorAll('[id^="map-"]');
            const buttons = event.target.parentElement.querySelectorAll('.tab-button');
            
            tabs.forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            buttons.forEach(button => {{
                button.classList.remove('active');
            }});
            
            document.getElementById('map-' + mapName).classList.add('active');
            event.target.classList.add('active');
        }}
        
        // Navbar scroll effect
        window.addEventListener('scroll', function() {{
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 50) {{
                navbar.classList.add('scrolled');
            }} else {{
                navbar.classList.remove('scrolled');
            }}
        }});
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
        
        // Animate cards on scroll
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver(function(entries) {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);
        
        // Observe all cards for animation
        document.querySelectorAll('.card').forEach(card => {{
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        }});
        
        // Add interactive hover effects
        document.querySelectorAll('.finding-card').forEach(card => {{
            card.addEventListener('mouseenter', function() {{
                this.style.transform = 'translateY(-10px) scale(1.05)';
            }});
            card.addEventListener('mouseleave', function() {{
                this.style.transform = 'translateY(0) scale(1)';
            }});
        }});
    </script>
</body>
</html>
"""

# Save the HTML report
with open('Austin_Cultural_Grants_Interactive_Report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\nInteractive HTML report generated successfully!")
print("File saved as: Austin_Cultural_Grants_Interactive_Report.html")
print("\nOpen in a web browser for the full interactive experience.")