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
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .main {
        padding: 0 !important;
    }
    /* Remove all default padding */
    .block-container {
        padding: 1rem 2rem 0 2rem !important;
        max-width: 100% !important;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styles */
    .header-text {
        text-align: center;
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0 0 1rem 0;
        padding: 0.5rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .section-header {
        color: #34495e;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .beer-card-compact {
        background: white;
        border-radius: 8px;
        padding: 0.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 3px solid #3498db;
        margin-bottom: 0.5rem;
        transition: transform 0.2s;
    }
    .beer-card-compact:hover {
        transform: translateX(3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .top-recommendation {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        height: 100%;
    }
    .match-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    .rank-badge {
        background: #ffd700;
        color: #333;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: bold;
        display: inline-block;
    }
    /* Input styling */
    .stTextArea textarea {
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
        border: 1px solid #ddd !important;
        border-radius: 6px !important;
    }
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.4rem 1rem !important;
        font-size: 0.85rem !important;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    /* Scrollable area */
    .more-beers {
        max-height: 150px;
        overflow-y: auto;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    .more-beers::-webkit-scrollbar {
        width: 5px;
    }
    .more-beers::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 5px;
    }
    /* Quick pick buttons */
    div[data-testid="column"] > div > div > div > button {
        font-size: 0.8rem !important;
        padding: 0.3rem !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    /* Reduce spacing */
    .element-container {
        margin: 0 !important;
    }
    .stMarkdown {
        margin-bottom: 0.2rem !important;
    }
    hr {
        margin: 0.3rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommender():
    recommender = BeerRecommender()
    with st.spinner("Loading..."):
        recommender.load_and_preprocess_data()
        recommender.train_regression_model()
    return recommender

def main():
    # Single line header
    st.markdown('<div class="header-text">🍺 "What\'ll it be?" - Tell us what you\'re craving and we\'ll find your perfect beer</div>', unsafe_allow_html=True)
    
    recommender = load_recommender()
    
    # Initialize session state
    if 'selected_prefs' not in st.session_state:
        st.session_state.selected_prefs = []
    if 'user_input_text' not in st.session_state:
        st.session_state.user_input_text = ""
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'last_results' not in st.session_state:
        st.session_state.last_results = None
    
    # Create main layout columns
    col1, col2, col3 = st.columns([1.5, 1.5, 2])
    
    with col1:
        st.markdown('<div class="section-header">🎯 Popular Orders (tap multiple):</div>', unsafe_allow_html=True)
        
        # Compact preference grid
        preferences = {
            "🌺 Hoppy": "hoppy IPA",
            "🍊 Citrus": "citrusy",
            "🍋 Sour": "sour",
            "🌾 Light": "light crisp",
            "🍫 Dark": "dark roasted",
            "🍓 Fruity": "fruity",
            "🌶️ Spicy": "spicy",
            "🥜 Nutty": "nutty",
            "🍯 Malty": "malty"
        }
        
        # 3x3 grid
        pref_rows = [st.columns(3) for _ in range(3)]
        for idx, (label, value) in enumerate(preferences.items()):
            row = idx // 3
            col = idx % 3
            with pref_rows[row][col]:
                if st.button(label, key=f"p{idx}", use_container_width=True, 
                           type="primary" if value in st.session_state.selected_prefs else "secondary"):
                    if value not in st.session_state.selected_prefs:
                        st.session_state.selected_prefs.append(value)
                    else:
                        st.session_state.selected_prefs.remove(value)
                    
                    if st.session_state.selected_prefs:
                        st.session_state.user_input_text = f"I want a {' and '.join(st.session_state.selected_prefs)} beer"
                    else:
                        st.session_state.user_input_text = ""
                    st.rerun()
        
        if st.session_state.selected_prefs:
            if st.button("Clear all", key="clr"):
                st.session_state.selected_prefs = []
                st.session_state.user_input_text = ""
                st.rerun()
    
    with col2:
        st.markdown('<div class="section-header">💭 Or describe it:</div>', unsafe_allow_html=True)
        
        # Bartender's surprise button
        if st.button("🎲 Bartender's Surprise", use_container_width=True):
            picks = [
                "Light summer wheat beer",
                "Hoppy tropical IPA",
                "Dark chocolate stout",
                "Crisp pilsner",
                "Funky sour ale",
                "Coffee porter"
            ]
            st.session_state.user_input_text = random.choice(picks)
            st.rerun()
        
        # Text input
        user_input = st.text_area(
            "",
            placeholder="e.g., 'hoppy but not bitter'",
            value=st.session_state.user_input_text,
            key="beer_input",
            height=55,
            label_visibility="collapsed"
        )
        
        # Search button
        if st.button("🔍 Find My Beer", type="primary", use_container_width=True):
            if user_input:
                with st.spinner("Finding..."):
                    try:
                        st.session_state.last_results = recommender.get_recommendations(user_input)
                        st.session_state.show_results = True
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please describe what you want!")
    
    with col3:
        if st.session_state.show_results and st.session_state.last_results:
            results = st.session_state.last_results
            
            # Match score
            rating = results['predicted_rating']
            score_color = "#27ae60" if rating >= 4 else "#f39c12" if rating >= 3.5 else "#e74c3c"
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 0.5rem;">
                    <span class="match-badge" style="background: {score_color};">
                        Match Score: {rating:.1f}/5 ⭐
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            # Top 2 recommendations
            st.markdown('<div class="section-header">🏆 Best Matches:</div>', unsafe_allow_html=True)
            
            rec_cols = st.columns(2)
            for i, (beer, col) in enumerate(zip(results['recommendations'][:2], rec_cols), 1):
                with col:
                    st.markdown(f"""
                    <div class="top-recommendation">
                        <div style="text-align: center; margin-bottom: 0.3rem;">
                            <span class="rank-badge">#{i}</span>
                        </div>
                        <h5 style="color: #2c3e50; margin: 0.3rem 0; font-size: 0.9rem; text-align: center;">
                            {beer['name'][:35]}{'...' if len(beer['name']) > 35 else ''}
                        </h5>
                        <div style="font-size: 0.75rem; color: #7f8c8d; text-align: center; margin: 0.3rem 0;">
                            ⭐ {beer['rating']:.1f} • {beer['num_reviews']} reviews
                        </div>
                        <div style="font-size: 0.7rem; color: #95a5a6; line-height: 1.2; margin-top: 0.5rem;">
                            {beer['description'][:80]}...
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # More options (scrollable)
            if len(results['recommendations']) > 2:
                st.markdown('<div class="section-header">More options:</div>', unsafe_allow_html=True)
                more_html = '<div class="more-beers">'
                for i, beer in enumerate(results['recommendations'][2:], 3):
                    more_html += f"""
                    <div style="padding: 0.3rem; border-bottom: 1px solid #eee;">
                        <strong style="font-size: 0.8rem;">#{i}. {beer['name'][:40]}</strong>
                        <span style="float: right; font-size: 0.75rem;">⭐ {beer['rating']:.1f}</span>
                    </div>
                    """
                more_html += '</div>'
                st.markdown(more_html, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="height: 250px; display: flex; align-items: center; justify-content: center; 
                            background: #f8f9fa; border-radius: 10px; color: #95a5a6;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🍺</div>
                        <div>Your recommendations will appear here</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()