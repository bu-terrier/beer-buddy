import streamlit as st
import pandas as pd
from beer_recommender import BeerRecommender
import time

st.set_page_config(
    page_title="🍺 Beer Recommendation System",
    page_icon="🍺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    .beer-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .rating-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
    }
    .metric-container {
        background-color: #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommender():
    recommender = BeerRecommender()
    with st.spinner("🍺 Loading beer database..."):
        recommender.load_and_preprocess_data()
        recommender.train_regression_model()
    return recommender

def main():
    st.title("🍺 AI Beer Recommendation System")
    st.markdown("---")
    
    recommender = load_recommender()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### What kind of beer are you looking for?")
    with col2:
        if st.button("🎲 Random Example"):
            examples = [
                "I want a light citrusy beer",
                "Give me a hoppy IPA with tropical notes",
                "I want a strong orangey tart beer",
                "I need a dessert beer with chocolate notes",
                "Something sessionable and refreshing"
            ]
            import random
            st.session_state.example = random.choice(examples)
    
    user_input = st.text_input(
        "",
        placeholder="Try: 'I want a hoppy IPA' or 'Give me something light and fruity'",
        value=st.session_state.get('example', ''),
        key="beer_input"
    )
    
    if st.button("🔍 Get Recommendations", type="primary", use_container_width=True):
        if user_input:
            with st.spinner("🤖 Analyzing your preferences..."):
                try:
                    results = recommender.get_recommendations(user_input)
                    
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns(3)
                    with col2:
                        rating = results['predicted_rating']
                        if rating >= 4.0:
                            emoji = "🌟"
                            message = "Excellent choice!"
                        elif rating >= 3.5:
                            emoji = "✅"
                            message = "Great choice!"
                        elif rating >= 3.0:
                            emoji = "👍"
                            message = "Good choice!"
                        else:
                            emoji = "⚠️"
                            message = "Interesting choice..."
                        
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2>{emoji}</h2>
                            <h4>{message}</h4>
                            <div class="rating-badge">Predicted Rating: {rating:.2f}/5</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### 🍻 Top Recommendations for You")
                    
                    for i, beer in enumerate(results['recommendations'], 1):
                        with st.container():
                            st.markdown(f"""
                            <div class="beer-card">
                                <h3 style="color: #667eea; margin-bottom: 0.5rem;">
                                    {i}. {beer['name']}
                                </h3>
                                <div style="display: flex; gap: 2rem; margin-bottom: 1rem;">
                                    <span><strong>⭐ Rating:</strong> {beer['rating']:.2f}/5</span>
                                    <span><strong>📊 Reviews:</strong> {beer['num_reviews']}</span>
                                    <span><strong>📏 Match:</strong> {(1 - min(beer['distance'], 1)) * 100:.0f}%</span>
                                </div>
                                <p style="color: #495057; line-height: 1.6;">
                                    {beer['description'][:300]}{'...' if len(beer['description']) > 300 else ''}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with st.expander("🔬 View Flavor Profile Analysis"):
                        features = results['user_features']
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Primary Characteristics:**")
                            st.write(f"• Style: {features['style']}")
                            st.write(f"• ABV: {features['ABV']:.1f}%")
                            st.write(f"• Hoppiness: {features['Hoppy']}/172")
                            st.write(f"• Bitterness: {features['Bitter']}/150")
                            
                        with col2:
                            st.markdown("**Flavor Notes:**")
                            st.write(f"• Sweetness: {features['Sweet']}/263")
                            st.write(f"• Fruitiness: {features['Fruits']}/175")
                            st.write(f"• Maltiness: {features['Malty']}/239")
                            st.write(f"• Sourness: {features['Sour']}/284")
                    
                except Exception as e:
                    st.error(f"😞 Oops! Something went wrong: {str(e)}")
                    st.info("Please check your API key in the .env file or try a different query.")
        else:
            st.warning("🍺 Please describe what kind of beer you're looking for!")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 14px;">
        <p>Powered by AI • Analyzing 3,000+ craft beers • Built with ❤️ and 🍺</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
