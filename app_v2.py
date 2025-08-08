import streamlit as st
import pandas as pd
from beer_recommender import BeerRecommender
import time
import random

st.set_page_config(
    page_title="🍺 Beer Buddy",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Background and main container */
    .stApp {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    .main {
        background-color: transparent;
    }
    .block-container {
        padding: 0.5rem 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto;
    }
    
    /* Title styling - even more compact */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 900;
        font-family: 'Arial Black', sans-serif;
        letter-spacing: -3px;
        margin-bottom: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #ffd700;
        font-size: 1.1rem;
        font-style: italic;
        margin-top: -5px;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Card containers - even more compact */
    .selection-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Special yellow buttons - Bartender and Find Beer */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #f6f6f6 0%, #f6f6f6 100%) !important;
        color: #000000 !important;
        border: 2px solid #ffc700 !important;
        padding: 0.5rem 1rem !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        transition: all 0.3s !important;
        width: 100% !important;
        margin: 0.3rem 0 !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .stButton > button[kind="secondary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #ffed4e 0%, #ffd700 100%) !important;
    }
    
    /* Text area styling - single line */
    .stTextInput input {
        background: white !important;
        border: 2px solid #2a5298 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        font-size: 0.9rem !important;
        transition: border-color 0.3s !important;
    }
    .stTextInput input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2) !important;
    }
    
    /* Recommendation cards - even more compact */
    .rec-card {
        background: white;
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    .rec-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #ffd700;
    }
    .rec-card-top {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        border: 2px solid #ffd700;
        padding: 0.8rem;
    }
    
    /* Badges - smaller */
    .rank-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1e3c72;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.75rem;
        display: inline-block;
        margin-bottom: 0.2rem;
    }
    .score-badge {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    /* Section headers - GOLDEN COLOR */
    .section-header {
        color: #ffd700;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Selected preferences display - more compact */
    .selected-display {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 6px;
        padding: 0.3rem 0.5rem;
        margin: 0.3rem 0;
        border: 1px solid #2196f3;
        font-size: 0.85rem;
    }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom flavor button styling - smaller */
    div[data-testid="column"] button {
        background: white !important;
        border: 2px solid #2a5298 !important;
        color: #2a5298 !important;
        border-radius: 6px !important;
        transition: all 0.2s !important;
        font-weight: 600 !important;
        padding: 0.3rem !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="column"] button:hover {
        background: #2a5298 !important;
        color: white !important;
        transform: scale(1.05);
    }
    div[data-testid="column"] button[kind="primary"] {
        background: #2a5298 !important;
        color: white !important;
        border-color: #1e3c72 !important;
    }
    
    /* Results section - more compact */
    .results-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 0.8rem;
        margin-top: 0.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    /* Beer image styling - smaller */
    .beer-image {
        width: 80px;
        height: 80px;
        object-fit: cover;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin: 0.2rem auto;
        display: block;
    }
    
    /* Reduce all spacing */
    .stMarkdown {
        margin-bottom: 0 !important;
    }
    hr {
        margin: 0.3rem 0 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0.3rem !important;
    }
    
    /* Warning and alternative styles */
    .warning-header {
        background: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .alt-section {
        background: #e8f5e9;
        border-radius: 8px;
        padding: 0.5rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommender():
    recommender = BeerRecommender()
    with st.spinner("🍺 Loading craft beer database..."):
        recommender.load_and_preprocess_data()
        recommender.train_regression_model()
    return recommender

def main():
    # Title and subtitle - compact
    st.markdown('<h1 class="main-title">🍺 BEER BUDDY 🍺</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">"What\'ll it be?" - Tell us what you\'re craving and we\'ll find your perfect beer</p>', unsafe_allow_html=True)
    
    recommender = load_recommender()
    
    # Initialize session state
    if 'selected_prefs' not in st.session_state:
        st.session_state.selected_prefs = []
    if 'user_input_text' not in st.session_state:
        st.session_state.user_input_text = ""
    
    # Flavor selection section
    st.markdown('<div class="section-header"> Tap Your Favorite Flavors (select multiple):</div>', unsafe_allow_html=True)
    
    # Preferences
    preferences = {
        "🌺 Hoppy IPA": "hoppy IPA",
        "🍊 Citrusy": "citrusy and refreshing",
        "🍋 Sour": "sour",
        "🌾 Light": "light and crisp",
        "🍫 Dark": "dark and roasted",
        "🍓 Fruity": "fruity and sweet",
        "🌶️ Spicy": "spicy and complex",
        "🥜 Nutty": "nutty and smooth",
        "🍯 Malty": "malty and rich",
        "☕ Coffee": "coffee and chocolate"
    }
    
    # Display in 2 rows of 5 - compact
    row1_cols = st.columns(5)
    row2_cols = st.columns(5)
    all_cols = row1_cols + row2_cols
    
    for idx, (label, value) in enumerate(preferences.items()):
        with all_cols[idx]:
            button_type = "primary" if value in st.session_state.selected_prefs else "secondary"
            if st.button(label, key=f"pref_{idx}", use_container_width=True, type=button_type):
                if value not in st.session_state.selected_prefs:
                    st.session_state.selected_prefs.append(value)
                else:
                    st.session_state.selected_prefs.remove(value)
                
                # Update text
                if st.session_state.selected_prefs:
                    if len(st.session_state.selected_prefs) == 1:
                        st.session_state.user_input_text = f"I want a {st.session_state.selected_prefs[0]} beer"
                    else:
                        prefs_text = ', '.join(st.session_state.selected_prefs[:-1])
                        prefs_text += f" and {st.session_state.selected_prefs[-1]}"
                        st.session_state.user_input_text = f"I want a {prefs_text} beer"
                else:
                    st.session_state.user_input_text = ""
                st.rerun()
    
    # Show selected preferences - compact
    if st.session_state.selected_prefs:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
                <div class="selected-display">
                    <strong>✅</strong> {', '.join(st.session_state.selected_prefs)}
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Clear", use_container_width=True):
                st.session_state.selected_prefs = []
                st.session_state.user_input_text = ""
                st.rerun()
    
    # Minimal spacing
    st.markdown("<div style='margin: 0.2rem 0;'></div>", unsafe_allow_html=True)
    
    # Bartender's Choice - Yellow button with black text
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 BARTENDER'S SURPRISE", key="bartender_btn", use_container_width=True, type="secondary"):
            bartender_picks = [
                "I want a light citrusy wheat beer perfect for summer",
                "Give me your hoppiest IPA with tropical fruit notes",
                "I need a strong Belgian tripel with spicy complexity",
                "Something dark and chocolatey like a dessert in a glass",
                "A crisp refreshing pilsner for a hot day",
                "I want a funky sour wild ale with brett character",
                "Give me a smooth porter with coffee and caramel notes",
                "I want a sessionable ale that won't knock me out"
            ]
            st.session_state.user_input_text = random.choice(bartender_picks)
            st.rerun()
    
    st.markdown("<div style='margin: 0.2rem 0;'></div>", unsafe_allow_html=True)
    
    # Text input section
    st.markdown('<div class="section-header">💭 Or Describe Your Perfect Pour:</div>', unsafe_allow_html=True)
    
    # Single line text input
    user_input = st.text_input(
        "",
        placeholder="Example: 'I want something hoppy but not too bitter' or 'Give me a beer that pairs well with BBQ'",
        value=st.session_state.user_input_text,
        key="beer_input",
        label_visibility="collapsed"
    )
    
    # Search button - Yellow with black text
    if st.button("🔍 FIND MY PERFECT BEER", type="secondary", use_container_width=True):
        if user_input:
            with st.spinner("🍻 Searching..."):
                try:
                    results = recommender.get_recommendations(user_input)
                    rating = results['predicted_rating']
                    
                    # Different display based on rating
                    if rating < 3.0:
                        # Low rating warning display
                        st.markdown(f"""
                        <div class="warning-header">
                            <div style="text-align: center;">
                                <span style="font-size: 1.2rem; color: #856404;">
                                    ⚠️ <strong>Warning: This flavor combination typically rates {rating:.2f}/5</strong>
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Regular recommendations
                        st.markdown('<div style="color: #1e3c72; font-weight: bold; margin: 0.5rem 0;">📍 Here\'s what matches your exact request:</div>', unsafe_allow_html=True)
                        
                        if results['recommendations']:
                            rec_cols = st.columns(2)
                            for i, (beer, column) in enumerate(zip(results['recommendations'][:2], rec_cols), 1):
                                with column:
                                    st.markdown(f"""
                                    <div class="rec-card">
                                        <div style="text-align: center;">
                                            <span class="rank-badge">#{i}</span>
                                        </div>
                                        <h5 style="color: #1e3c72; text-align: center; margin: 0.3rem 0; font-size: 0.9rem;">
                                            {beer['name'][:35]}{'...' if len(beer['name']) > 35 else ''}
                                        </h5>
                                        <div style="text-align: center; margin: 0.3rem 0;">
                                            <span style="color: #ffd700; font-size: 0.9rem;">⭐ {beer['rating']:.2f}/5</span>
                                            <div style="color: #666; font-size: 0.75rem; margin-top: 0.2rem;">
                                                {beer['num_reviews']:,} reviews
                                            </div>
                                            <div style="color: #495057; font-size: 0.7rem; margin-top: 0.2rem;">
                                                Distance: {beer['distance']:.3f}
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info("No exact matches found in our database.")
                        
                        # Alternative recommendations
                        if results.get('alt_recommendations'):
                            st.markdown('<div style="color: #1e3c72; font-weight: bold; margin: 0.5rem 0;">💡 Suggested Alternatives (similar but better rated):</div>', unsafe_allow_html=True)
                            
                            alt_cols = st.columns(2)
                            for i, (beer, column) in enumerate(zip(results['alt_recommendations'][:2], alt_cols), 1):
                                with column:
                                    st.markdown(f"""
                                    <div class="rec-card" style="background: #e8f5e9;">
                                        <div style="text-align: center;">
                                            <span class="rank-badge">🌟 #{i}</span>
                                        </div>
                                        <h5 style="color: #1e3c72; text-align: center; margin: 0.3rem 0; font-size: 0.9rem;">
                                            {beer['name'][:35]}{'...' if len(beer['name']) > 35 else ''}
                                        </h5>
                                        <div style="text-align: center; margin: 0.3rem 0;">
                                            <span style="color: #ffd700; font-size: 0.9rem;">⭐ {beer['rating']:.2f}/5</span>
                                            <div style="color: #666; font-size: 0.75rem; margin-top: 0.2rem;">
                                                {beer['num_reviews']:,} reviews
                                            </div>
                                            <div style="color: #495057; font-size: 0.7rem; margin-top: 0.2rem;">
                                                Distance: {beer['distance']:.3f}
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info("No high-rated alternatives found with your criteria.")
                        
                        st.markdown("""
                        <div style="background: #f8f9fa; border-radius: 8px; padding: 0.5rem; margin-top: 0.5rem;">
                            <p style="color: #495057; font-size: 0.85rem; margin: 0;">
                                💭 <strong>Tip:</strong> The flavor combination you requested is uncommon. The alternatives above
                                maintain similar characteristics but with proven appeal to beer enthusiasts.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:
                        # Good rating display (original with distance added)
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if rating >= 4.0:
                                emoji, message = "🏆", "PERFECT!"
                            elif rating >= 3.5:
                                emoji, message = "⭐", "GREAT!"
                            else:
                                emoji, message = "👍", "GOOD!"
                            
                            st.markdown(f"""
                            <div style="text-align: center; margin: 0.3rem 0;">
                                <span style="color: #1e3c72; font-weight: bold;">{emoji} {message}</span>
                                <span class="score-badge" style="margin-left: 0.5rem;">Predicted rating: {rating:.2f}/5</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<hr style='margin: 0.3rem 0;'>", unsafe_allow_html=True)
                        
                        # Top 2 recommendations with distance
                        st.markdown('<h5 style="color: #1e3c72; text-align: center; margin: 0.3rem 0; font-size: 1rem;">🍺 Top Recommendations:</h5>', unsafe_allow_html=True)
                        
                        rec_cols = st.columns(2)
                        
                        # Beer images
                        style_images = {
                            'ipa': 'https://images.unsplash.com/photo-1618183479302-1e0aa382c36b?w=200&h=200&fit=crop',
                            'stout': 'https://images.unsplash.com/photo-1566633806327-68e152aaf26d?w=200&h=200&fit=crop',
                            'porter': 'https://images.unsplash.com/photo-1566633806327-68e152aaf26d?w=200&h=200&fit=crop',
                            'lager': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=200&h=200&fit=crop',
                            'pilsner': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=200&h=200&fit=crop',
                            'wheat': 'https://images.unsplash.com/photo-1571613316887-6f8d5cbf7ef7?w=200&h=200&fit=crop',
                            'ale': 'https://images.unsplash.com/photo-1518176258769-f227c798150e?w=200&h=200&fit=crop',
                            'sour': 'https://images.unsplash.com/photo-1559818454-1b46997bfe30?w=200&h=200&fit=crop'
                        }
                        
                        for i, (beer, column) in enumerate(zip(results['recommendations'][:2], rec_cols), 1):
                            with column:
                                beer_name_lower = beer['name'].lower()
                                image_url = 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=200&h=200&fit=crop'
                                for style, url in style_images.items():
                                    if style in beer_name_lower or style in beer.get('description', '').lower():
                                        image_url = url
                                        break
                                
                                st.markdown(f"""
                                <div class="rec-card rec-card-top">
                                    <div style="text-align: center;">
                                        <span class="rank-badge">🥇 #{i}</span>
                                    </div>
                                    <h5 style="color: #1e3c72; text-align: center; margin: 0.3rem 0; font-size: 0.9rem;">
                                        {beer['name'][:35]}{'...' if len(beer['name']) > 35 else ''}
                                    </h5>
                                    <img src="{image_url}" class="beer-image">
                                    <div style="text-align: center; margin: 0.3rem 0;">
                                        <span style="color: #ffd700; font-size: 0.95rem;">⭐ {beer['rating']:.2f}/5</span>
                                        <div style="color: #666; font-size: 0.75rem; margin-top: 0.2rem;">
                                            {beer['num_reviews']:,} reviews
                                        </div>
                                        <div style="color: #495057; font-size: 0.7rem; margin-top: 0.2rem;">
                                            Distance: {beer['distance']:.3f}
                                        </div>
                                    </div>
                                    <p style="color: #495057; font-size: 0.7rem; line-height: 1.3; text-align: center; margin-top: 0.3rem;">
                                        Notes: {beer['description'][:100]}...
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"😞 Error: {str(e)}")
                    st.info("💡 Try a different description.")
        else:
            st.warning("🍺 Please tell us what you're looking for!")
    
    # Footer - compact
    st.markdown("""
    <div style="text-align: center; color: white; margin-top: 0.5rem; padding: 0.3rem;">
        <p style="font-size: 0.8rem;">
            <strong>🍻 Smart Pour System™</strong> • 3,197 craft beers • ML-powered
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
