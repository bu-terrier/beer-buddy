# 🍺 Beer Recommendation System

AI-powered beer recommendation system that suggests perfect beers based on your preferences.

## Features
- Natural language input for beer preferences
- Predicts rating based on flavor profile
- Returns top 5 beer recommendations
- Beautiful and simple UI

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your GROQ API key:
```
GROQ_API_KEY=your_api_key_here
```

3. Run the app:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push this repository to GitHub (without .env file)

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Connect your GitHub account and select this repository

4. In Advanced Settings, add your secrets:
```
GROQ_API_KEY = "your_api_key_here"
```

5. Click Deploy!

## File Structure
- `app.py` - Streamlit frontend
- `beer_recommender.py` - Core recommendation logic
- `beer.ipynb` - Original Jupyter notebook
- `data/` - Beer dataset
- `requirements.txt` - Python dependencies

## Usage Examples
- "I want a light citrusy beer"
- "Give me a hoppy IPA with tropical notes"
- "I need a dessert stout with chocolate notes"
- "Something sessionable and refreshing"