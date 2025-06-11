#!/usr/bin/env python3
"""
Deep Analysis: Sentiment Analysis and Program-Specific Insights
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
from nltk.corpus import stopwords
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Initialize NLTK components
try:
    sia = SentimentIntensityAnalyzer()
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('stopwords', quiet=True)
    sia = SentimentIntensityAnalyzer()
    stop_words = set(stopwords.words('english'))

print("="*80)
print("DEEP ANALYSIS: SENTIMENT & PROGRAM-SPECIFIC INSIGHTS")
print("="*80)
print()

# Load the survey data
df = pd.read_excel('ACME.xlsx')

# Key questions for sentiment analysis
key_questions = {
    'improvements': 'What improvements would you like to see in these cultural funding programs?',
    'barriers': 'What barriers do you or your community face in accessing support or services related to arts, culture, music, and entertainment?',
    'additional_feedback': 'Do you have any additional ideas, concerns, or feedback you would like to share to help ACME better serve the public?',
    'more_opportunities': 'What type of cultural arts or entertainment opportunities would you like to see more of in Austin?',
    'programs_services': 'What kinds of programs or services would you like ACME to offer that currently do not exist or are underrepresented?',
    'support_organizations': 'Austin\'s creative community has built a strong foundation of existing organizations that informs ACME\'s goals and mission. How do you believe ACME should better support these organizations and cul...'
}

# Sentiment Analysis Function
def analyze_sentiment(text):
    if pd.isna(text) or str(text).strip() == '':
        return None
    
    # Get VADER sentiment scores
    scores = sia.polarity_scores(str(text))
    
    # Classify sentiment
    if scores['compound'] >= 0.05:
        sentiment = 'positive'
    elif scores['compound'] <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'sentiment': sentiment,
        'compound': scores['compound'],
        'positive': scores['pos'],
        'negative': scores['neg'],
        'neutral': scores['neu']
    }

# Analyze sentiment for each key question
print("Analyzing sentiment across key questions...\n")
sentiment_results = {}

for key, question in key_questions.items():
    if question in df.columns:
        print(f"Analyzing: {key}")
        
        # Get responses
        responses = df[question].dropna()
        
        # Analyze sentiment
        sentiments = responses.apply(analyze_sentiment)
        sentiments_df = pd.DataFrame(list(sentiments.dropna()))
        
        if len(sentiments_df) > 0:
            sentiment_summary = {
                'total_responses': len(responses),
                'positive': (sentiments_df['sentiment'] == 'positive').sum(),
                'negative': (sentiments_df['sentiment'] == 'negative').sum(),
                'neutral': (sentiments_df['sentiment'] == 'neutral').sum(),
                'avg_compound': sentiments_df['compound'].mean(),
                'responses': responses
            }
            
            sentiment_results[key] = sentiment_summary
            
            print(f"  Total Responses: {sentiment_summary['total_responses']}")
            print(f"  Positive: {sentiment_summary['positive']} ({sentiment_summary['positive']/sentiment_summary['total_responses']*100:.1f}%)")
            print(f"  Negative: {sentiment_summary['negative']} ({sentiment_summary['negative']/sentiment_summary['total_responses']*100:.1f}%)")
            print(f"  Neutral: {sentiment_summary['neutral']} ({sentiment_summary['neutral']/sentiment_summary['total_responses']*100:.1f}%)")
            print(f"  Average Sentiment Score: {sentiment_summary['avg_compound']:.3f}")
            print()

# Extract key themes from text responses
print("\n" + "="*50)
print("EXTRACTING KEY THEMES")
print("="*50 + "\n")

def extract_themes(texts, n_themes=10):
    """Extract most common themes from text responses"""
    all_words = []
    
    for text in texts:
        if pd.notna(text):
            # Clean text
            text = str(text).lower()
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            
            # Extract words
            words = text.split()
            
            # Filter stopwords and short words
            words = [w for w in words if w not in stop_words and len(w) > 3]
            all_words.extend(words)
    
    # Get most common words
    word_freq = Counter(all_words)
    return word_freq.most_common(n_themes)

# Analyze themes for key questions
for key, data in sentiment_results.items():
    print(f"\nTop themes for '{key}':")
    themes = extract_themes(data['responses'], n_themes=15)
    for word, count in themes:
        print(f"  - {word}: {count} mentions")

# Program-specific analysis
print("\n" + "="*50)
print("PROGRAM-SPECIFIC FEEDBACK ANALYSIS")
print("="*50 + "\n")

# Check awareness question
awareness_col = 'Prior to this survey, were you aware of the following programs administered by the City of Austin/ACME? \n(Select all that you are aware of; checkboxes for each program) '

if awareness_col in df.columns:
    awareness_responses = df[awareness_col].dropna()
    
    # Count program mentions
    programs = ['Nexus', 'Heritage', 'AIPP', 'Thrive', 'Elevate', 'ALMF', 'CSAP']
    program_awareness = {}
    
    for program in programs:
        count = awareness_responses.str.contains(program, case=False, na=False).sum()
        program_awareness[program] = {
            'aware_count': count,
            'awareness_rate': count / len(awareness_responses) * 100
        }
    
    print("Program Awareness Rates:")
    for program, data in sorted(program_awareness.items(), key=lambda x: x[1]['awareness_rate'], reverse=True):
        print(f"  {program}: {data['aware_count']} respondents ({data['awareness_rate']:.1f}%)")

# Analyze satisfaction levels
satisfaction_col = 'How would you rate your level of satisfaction with these programs overall?'
if satisfaction_col in df.columns:
    satisfaction = df[satisfaction_col].value_counts()
    print(f"\nOverall Program Satisfaction:")
    for level, count in satisfaction.items():
        print(f"  {level}: {count} ({count/satisfaction.sum()*100:.1f}%)")

# Analyze accessibility perception
accessibility_col = 'How accessible do you think these programs are for historically underrepresented artists, organizations, and communities?'
if accessibility_col in df.columns:
    accessibility = df[accessibility_col].value_counts()
    print(f"\nAccessibility for Underrepresented Communities:")
    for level, count in accessibility.items():
        print(f"  {level}: {count} ({count/accessibility.sum()*100:.1f}%)")

# Extract specific program feedback
print("\n" + "="*50)
print("EXTRACTING SPECIFIC PROGRAM FEEDBACK")
print("="*50 + "\n")

# Search for program-specific mentions in improvement suggestions
improvements_col = 'What improvements would you like to see in these cultural funding programs?'
if improvements_col in df.columns:
    improvements = df[improvements_col].dropna()
    
    for program in ['Nexus', 'Heritage', 'AIPP', 'Thrive', 'Elevate']:
        print(f"\n{program} Program - Specific Feedback:")
        program_feedback = improvements[improvements.str.contains(program, case=False, na=False)]
        
        if len(program_feedback) > 0:
            print(f"  Found {len(program_feedback)} specific mentions")
            
            # Analyze sentiment of program-specific feedback
            sentiments = program_feedback.apply(analyze_sentiment)
            sentiments_df = pd.DataFrame(list(sentiments.dropna()))
            
            if len(sentiments_df) > 0:
                pos = (sentiments_df['sentiment'] == 'positive').sum()
                neg = (sentiments_df['sentiment'] == 'negative').sum()
                print(f"  Sentiment: {pos} positive, {neg} negative")
                
                # Show sample feedback
                print("  Sample feedback:")
                for i, feedback in enumerate(program_feedback.head(3)):
                    print(f"    {i+1}. \"{feedback[:150]}...\"" if len(feedback) > 150 else f"    {i+1}. \"{feedback}\"")

# Save key findings
print("\n" + "="*50)
print("Saving analysis results...")

# Create summary report
summary = {
    'total_responses': len(df),
    'sentiment_summary': {},
    'key_themes': {}
}

# Add program awareness if it exists
if 'program_awareness' in locals():
    summary['program_awareness'] = program_awareness

for key, data in sentiment_results.items():
    summary['sentiment_summary'][key] = {
        'positive_rate': data['positive'] / data['total_responses'] * 100,
        'negative_rate': data['negative'] / data['total_responses'] * 100,
        'avg_sentiment': data['avg_compound']
    }

# Save summary to JSON
import json
with open('analysis_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("\nAnalysis complete. Summary saved to 'analysis_summary.json'")
print("Ready for visualization and report generation...")