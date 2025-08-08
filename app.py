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
        padding: 1rem 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto;
    }
    
    /* Title styling - more compact */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3.5rem;
        font-weight: 900;
        font-family: 'Arial Black', sans-serif;
        letter-spacing: -3px;
        margin-bottom: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #ffd700;
        font-size: 1.2rem;
        font-style: italic;
        margin-top: -8px;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Card containers - more compact */
    .selection-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Bartender's choice button - smaller */
    .bartender-button {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1e3c72;
        border: none;
        border-radius: 12px;
        padding: 0.8rem;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        margin: 0.8rem 0;
        width: 100%;
        text-align: center;
    }
    .bartender-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
    }
    
    /* Text area styling - more compact */
    .stTextArea textarea {
        background: white;
        border: 2px solid #2a5298;
        border-radius: 10px;
        padding: 0.8rem !important;
        font-size: 0.95rem !important;
        transition: border-color 0.3s;
    }
    .stTextArea textarea:focus {
        border-color: #ffd700;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2);
    }
    
    /* Search button - more compact */
    .stButton > button {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem !important;
        font-size: 1rem !important;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
        margin-top: 0.5rem;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(42, 82, 152, 0.4);
    }
    
    /* Recommendation cards - more compact */
    .rec-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    .rec-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #ffd700;
    }
    .rec-card-top {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        border: 2px solid #ffd700;
        padding: 1rem;
    }
    
    /* Badges - smaller */
    .rank-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1e3c72;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 0.3rem;
    }
    .score-badge {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    /* Section headers - GOLDEN COLOR like subtitle */
    .section-header {
        color: #ffd700;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Selected preferences display - more compact */
    .selected-display {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #2196f3;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom flavor button styling */
    div[data-testid="column"] button {
        background: white !important;
        border: 2px solid #2a5298 !important;
        color: #2a5298 !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
        font-weight: 600 !important;
        padding: 0.4rem !important;
        font-size: 0.9rem !important;
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
        border-radius: 15px;
        padding: 1.2rem;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    /* Beer image styling - smaller */
    .beer-image {
        width: 100px;
        height: 100px;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin: 0.3rem auto;
        display: block;
    }
    
    /* Reduce all spacing */
    .stMarkdown {
        margin-bottom: 0 !important;
    }
    hr {
        margin: 0.5rem 0 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
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
    # Title and subtitle - more compact
    st.markdown('<h1 class="main-title">🍺 BEER BUDDY 🍺</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">"What\'ll it be?" - Tell us what you\'re craving and we\'ll find your perfect beer</p>', unsafe_allow_html=True)
    
    recommender = load_recommender()
    
    # Initialize session state
    if 'selected_prefs' not in st.session_state:
        st.session_state.selected_prefs = []
    if 'user_input_text' not in st.session_state:
        st.session_state.user_input_text = ""
    
    # Selection card
    # st.markdown('<div class="selection-card">', unsafe_allow_html=True)
    
    # Flavor selection section - with golden header
    st.markdown('<div class="section-header">🎯 Tap Your Favorite Flavors (select multiple):</div>', unsafe_allow_html=True)
    
    # Create 2 rows of 5 columns for better layout
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
    
    # Display in 2 rows of 5 - more compact
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
    
    # Show selected preferences - more compact
    if st.session_state.selected_prefs:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
                <div class="selected-display">
                    <strong>✅ Selected:</strong> {', '.join(st.session_state.selected_prefs)}
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Clear", use_container_width=True):
                st.session_state.selected_prefs = []
                st.session_state.user_input_text = ""
                st.rerun()
    
    # Reduced spacing
    st.markdown("<div style='margin: 0.5rem 0;'><hr></div>", unsafe_allow_html=True)
    
    # Bartender's Choice - more compact
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 BARTENDER'S SURPRISE - Let Us Choose For You!", key="bartender_btn", use_container_width=True):
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
    
    st.markdown("<div style='margin: 0.3rem 0;'><hr></div>", unsafe_allow_html=True)
    
    # Text input section - with golden header
    st.markdown('<div class="section-header">💭 Or Describe Your Perfect Pour:</div>', unsafe_allow_html=True)
    
    user_input = st.text_area(
        "",
        placeholder="Example: 'I want something hoppy but not too bitter' or 'Give me a beer that pairs well with BBQ'",
        value=st.session_state.user_input_text,
        key="beer_input",
        height=60,
        label_visibility="collapsed"
    )
    
    # Search button
    if st.button("🔍 FIND MY PERFECT BEER", type="primary", use_container_width=True):
        if user_input:
            with st.spinner("🍻 Searching through our craft beer collection..."):
                try:
                    results = recommender.get_recommendations(user_input)
                    
                    # Results container - more compact
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    
                    # Match score - more compact
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        rating = results['predicted_rating']
                        if rating >= 4.0:
                            emoji = "🏆"
                            message = "PERFECT MATCH!"
                        elif rating >= 3.5:
                            emoji = "⭐"
                            message = "GREAT MATCH!"
                        elif rating >= 3.0:
                            emoji = "👍"
                            message = "GOOD MATCH!"
                        else:
                            emoji = "🎯"
                            message = "UNIQUE CHOICE!"
                        
                        st.markdown(f"""
                        <div style="text-align: center; margin: 0.5rem 0;">
                            <h3 style="color: #1e3c72; margin: 0;">{emoji} {message}</h3>
                            <div class="score-badge">Match Score: {rating:.2f}/5</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
                    
                    # Top 2 recommendations - more compact
                    st.markdown('<h4 style="color: #1e3c72; text-align: center; margin: 0.5rem 0;">🏅 Top Recommendations</h4>', unsafe_allow_html=True)
                    
                    rec_cols = st.columns(2)
                    
                    # Beer images based on style
                    style_images = {
                        'ipa': 'https://images.unsplash.com/photo-1618183479302-1e0aa382c36b?w=300&h=300&fit=crop',
                        'stout': 'https://images.unsplash.com/photo-1566633806327-68e152aaf26d?w=300&h=300&fit=crop',
                        'porter': 'https://images.unsplash.com/photo-1566633806327-68e152aaf26d?w=300&h=300&fit=crop',
                        'lager': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300&h=300&fit=crop',
                        'pilsner': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=300&h=300&fit=crop',
                        'wheat': 'https://images.unsplash.com/photo-1571613316887-6f8d5cbf7ef7?w=300&h=300&fit=crop',
                        'ale': 'https://images.unsplash.com/photo-1518176258769-f227c798150e?w=300&h=300&fit=crop',
                        'sour': 'https://images.unsplash.com/photo-1559818454-1b46997bfe30?w=300&h=300&fit=crop'
                    }
                    
                    for i, (beer, column) in enumerate(zip(results['recommendations'][:2], rec_cols), 1):
                        with column:
                            # Find appropriate image
                            beer_name_lower = beer['name'].lower()
                            image_url = 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=300&h=300&fit=crop'
                            for style, url in style_images.items():
                                if style in beer_name_lower or style in beer.get('description', '').lower():
                                    image_url = url
                                    break
                            
                            st.markdown(f"""
                            <div class="rec-card rec-card-top">
                                <div style="text-align: center;">
                                    <span class="rank-badge">🥇 TOP PICK #{i}</span>
                                </div>
                                <h4 style="color: #1e3c72; text-align: center; margin: 0.5rem 0; font-size: 1rem;">
                                    {beer['name'][:40]}{'...' if len(beer['name']) > 40 else ''}
                                </h4>
                                <img src="{image_url}" class="beer-image">
                                <div style="text-align: center; margin: 0.5rem 0;">
                                    <div style="margin-bottom: 0.3rem;">
                                        <strong style="color: #1e3c72;">⭐</strong> 
                                        <span style="font-size: 1.1rem; color: #ffd700;">{beer['rating']:.2f}/5</span>
                                    </div>
                                    <div style="color: #666; font-size: 0.85rem;">
                                        {beer['num_reviews']:,} reviews | {(1 - beer['distance']) * 100:.0f}% match
                                    </div>
                                </div>
                                <hr style="border: 1px solid #e0e0e0; margin: 0.5rem 0;">
                                <p style="color: #495057; font-size: 0.8rem; line-height: 1.4; text-align: center;">
                                    {beer['description'][:150]}...
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Additional recommendations - more compact
                    if len(results['recommendations']) > 2:
                        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
                        st.markdown('<h4 style="color: #1e3c72; text-align: center; margin: 0.5rem 0;">🍺 More Great Options</h4>', unsafe_allow_html=True)
                        
                        # Display remaining beers in 2 columns - more compact
                        more_cols = st.columns(2)
                        for i, beer in enumerate(results['recommendations'][2:], 3):
                            with more_cols[(i-3) % 2]:
                                st.markdown(f"""
                                <div class="rec-card" style="padding: 0.8rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                                        <span style="background: #e3f2fd; color: #1e3c72; padding: 0.2rem 0.5rem; border-radius: 8px; font-weight: 600; font-size: 0.8rem;">
                                            #{i}
                                        </span>
                                        <span style="color: #ffd700; font-weight: 600; font-size: 0.9rem;">
                                            ⭐ {beer['rating']:.2f}
                                        </span>
                                    </div>
                                    <h5 style="color: #1e3c72; margin: 0.3rem 0; font-size: 0.95rem;">
                                        {beer['name'][:45]}{'...' if len(beer['name']) > 45 else ''}
                                    </h5>
                                    <p style="color: #666; font-size: 0.8rem; margin: 0.3rem 0;">
                                        {beer['num_reviews']:,} reviews | {(1 - beer['distance']) * 100:.0f}% match
                                    </p>
                                    <p style="color: #495057; font-size: 0.75rem; line-height: 1.3; margin-top: 0.3rem;">
                                        {beer['description'][:120]}...
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"😞 Oops! Something went wrong: {str(e)}")
                    st.info("💡 Try describing your beer differently or check your API settings.")
        else:
            st.warning("🍺 Please tell us what kind of beer you're looking for!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer - more compact
    st.markdown("""
    <div style="text-align: center; color: white; margin-top: 1.5rem; padding: 0.5rem;">
        <p style="font-size: 0.85rem;">
            <strong>🍻 Smart Pour System™</strong> • 3,197 craft beers analyzed • ML-powered recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()