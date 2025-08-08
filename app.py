import streamlit as st
import pandas as pd
from beer_recommender import BeerRecommender
import time
import random

st.set_page_config(
    page_title="🍺 Beer Buddy",
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
        margin: 0.5rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    .beer-card-main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 0.5rem;
        border: 2px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .rating-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
    }
    .title-style {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        letter-spacing: -2px;
        margin-bottom: 0;
    }
    .subtitle-style {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        font-style: italic;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .metric-container {
        background-color: #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    .preference-button {
        background-color: white;
        border: 2px solid #667eea;
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .preference-button:hover {
        background-color: #667eea;
        color: white;
    }
    .preference-selected {
        background-color: #667eea;
        color: white;
    }
    .beer-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin-right: 10px;
    }
    .recommendation-badge {
        background: #ffd700;
        color: #333;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
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
    # Creative Title with beer glass animation
    st.markdown("""
    <h1 class='title-style'>
        🍻 BEER BUDDY 
    </h1>
    """, unsafe_allow_html=True)
    
    # Bartender-style subtitle
    st.markdown("<p class='subtitle-style'>\"What'll it be?\" - Your personal craft beer concierge at your service</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    recommender = load_recommender()
    
    # Initialize session state
    if 'selected_prefs' not in st.session_state:
        st.session_state.selected_prefs = []
    if 'user_input_text' not in st.session_state:
        st.session_state.user_input_text = ""
    
    # Preference selection section with better UI
    st.markdown("### 🎯 Popular Orders - Tap to select (multiple allowed):")
    st.markdown("<small style='color: #6c757d;'>Just like ordering at the bar - tell us what you're craving!</small>", unsafe_allow_html=True)
    
    # Create columns for preference buttons
    col1, col2, col3 = st.columns(3)
    
    # More diverse preferences based on common bar requests
    preferences = {
        "🌺 Hoppy IPA": "hoppy IPA",
        "🍊 Citrus & Zest": "citrusy and refreshing",
        "🍋 Sour & Wild": "sour",
        "🌾 Light & Easy": "light and crisp",
        "🍫 Dark & Roasted": "dark and roasted",
        "🍓 Fruity & Sweet": "fruity",
        "🌶️ Spicy & Bold": "spicy and complex",
        "🥜 Nutty & Smooth": "nutty and smooth",
        "🍯 Malty & Rich": "malty and rich"
    }
    
    # Display preference buttons with better interaction
    cols = [col1, col2, col3]
    for idx, (label, value) in enumerate(preferences.items()):
        with cols[idx % 3]:
            button_type = "primary" if value in st.session_state.selected_prefs else "secondary"
            if st.button(label, key=f"pref_{idx}", use_container_width=True, type=button_type):
                if value not in st.session_state.selected_prefs:
                    st.session_state.selected_prefs.append(value)
                else:
                    st.session_state.selected_prefs.remove(value)
                
                # Update the text input automatically
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
    
    # Show selected preferences in a nice way
    if st.session_state.selected_prefs:
        st.success(f"🍺 Your order: Looking for something **{', '.join(st.session_state.selected_prefs)}**")
        if st.button("🔄 Clear selections", key="clear_btn", use_container_width=False):
            st.session_state.selected_prefs = []
            st.session_state.user_input_text = ""
            st.rerun()
    
    st.markdown("---")
    
    # Text input section with bartender's pick
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 💭 Or describe your perfect pour:")
        st.markdown("<small style='color: #6c757d;'>Try: 'Give me something light and fruity' or 'I want a hoppy IPA'</small>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### &nbsp;")  # Spacer for alignment
        if st.button("🎲 Bartender's Surprise", key="random_btn", help="Let our bartender surprise you!"):
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
    
    # Enhanced text input box
    user_input = st.text_area(
        "",
        placeholder="e.g., 'I'm looking for something hoppy but not too bitter' or 'Give me a beer that pairs well with BBQ'",
        value=st.session_state.user_input_text,
        key="beer_input",
        height=80
    )
    
    # Search button with better styling
    if st.button("🔍 Pour Me The Perfect Beer!", type="primary", use_container_width=True):
        if user_input:
            with st.spinner("🍻 Checking our tap list and bottle selection..."):
                try:
                    results = recommender.get_recommendations(user_input)
                    
                    st.markdown("---")
                    
                    # Predicted rating display with better messaging
                    col1, col2, col3 = st.columns(3)
                    with col2:
                        rating = results['predicted_rating']
                        if rating >= 4.0:
                            emoji = "🏆"
                            message = "Top Shelf Selection!"
                        elif rating >= 3.5:
                            emoji = "⭐"
                            message = "Crowd Favorite!"
                        elif rating >= 3.0:
                            emoji = "👍"
                            message = "Solid Choice!"
                        else:
                            emoji = "🎯"
                            message = "Adventurous Pick!"
                        
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2>{emoji}</h2>
                            <h4>{message}</h4>
                            <div class="rating-badge">Match Score: {rating:.2f}/5</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### 🏅 Top Recommendations - Fresh From The Tap:")
                    
                    # Display top 2 recommendations as premium cards
                    col1, col2 = st.columns(2)
                    
                    # Style-based image mapping for better visuals
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
                    
                    for i, (beer, column) in enumerate(zip(results['recommendations'][:2], [col1, col2]), 1):
                        with column:
                            # Determine beer style for image
                            beer_name_lower = beer['name'].lower()
                            image_url = 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=300&h=300&fit=crop'  # default
                            
                            for style, url in style_images.items():
                                if style in beer_name_lower or style in beer.get('description', '').lower():
                                    image_url = url
                                    break
                            
                            recommendation_label = "🥇 TOP PICK" if i == 1 else "🥈 RUNNER-UP"
                            
                            st.markdown(f"""
                            <div class="beer-card-main">
                                <div style="text-align: center;">
                                    <span class="recommendation-badge">{recommendation_label}</span>
                                </div>
                                <h3 style="color: #667eea; text-align: center; margin: 1rem 0;">
                                    {beer['name']}
                                </h3>
                                <div style="text-align: center; margin: 1rem 0;">
                                    <img src="{image_url}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                </div>
                                <div style="margin: 1rem 0;">
                                    <div style="margin-bottom: 0.8rem; padding: 8px; background: #f0f0f0; border-radius: 8px;">
                                        <strong>⭐ Community Rating:</strong> <span style="font-size: 1.1rem; color: #667eea;">{beer['rating']:.2f}/5</span>
                                    </div>
                                    <div style="margin-bottom: 0.5rem;">
                                        <strong>👥 Reviews:</strong> {beer['num_reviews']:,} beer lovers
                                    </div>
                                    <div style="margin-bottom: 0.5rem;">
                                        <strong>🎯 Match Score:</strong> {(1 - beer['distance']) * 100:.0f}%
                                    </div>
                                </div>
                                <hr style="margin: 1rem 0; border: 1px solid #e0e0e0;">
                                <p style="color: #495057; line-height: 1.6; font-size: 0.95rem;">
                                    <strong>Tasting Notes:</strong><br>
                                    {beer['description'][:200]}{'...' if len(beer['description']) > 200 else ''}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Show remaining recommendations in a simpler format
                    if len(results['recommendations']) > 2:
                        st.markdown("---")
                        st.markdown("### 🍺 More Great Options:")
                        
                        for i, beer in enumerate(results['recommendations'][2:], 3):
                            with st.container():
                                st.markdown(f"""
                                <div class="beer-card">
                                    <strong>#{i}. {beer['name']}</strong> - Rating: {beer['rating']:.2f}/5
                                    <br><small>{beer['description'][:150]}...</small>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Flavor profile analysis in a fun way
                    with st.expander("🧬 Your Beer DNA Profile - See What We Found"):
                        features = results['user_features']
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**🎨 Style Profile:**")
                            st.write(f"• Detected Style: **{features['style']}**")
                            st.write(f"• Strength (ABV): **{features['ABV']:.1f}%**")
                            st.write(f"• Hop Intensity: **{features['Hoppy']}/172** {'🌺' * min(5, int(features['Hoppy']/35))}")
                            st.write(f"• Bitterness Level: **{features['Bitter']}/150** {'🔥' * min(5, int(features['Bitter']/30))}")
                            
                        with col2:
                            st.markdown("**👅 Flavor Spectrum:**")
                            st.write(f"• Sweetness: **{features['Sweet']}/263** {'🍯' * min(5, int(features['Sweet']/53))}")
                            st.write(f"• Fruitiness: **{features['Fruits']}/175** {'🍓' * min(5, int(features['Fruits']/35))}")
                            st.write(f"• Malt Character: **{features['Malty']}/239** {'🌾' * min(5, int(features['Malty']/48))}")
                            st.write(f"• Sourness: **{features['Sour']}/284** {'🍋' * min(5, int(features['Sour']/57))}")
                    
                except Exception as e:
                    st.error(f"😞 Oops! The keg kicked! {str(e)}")
                    st.info("💡 Try describing your beer differently or check your API settings.")
        else:
            st.warning("🍺 Tell the bartender what you're thirsty for!")
    
    # Footer with better messaging
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 14px;">
        <p><strong>The Smart Pour System™</strong></p>
        <p>Trained on 3,197 craft beer reviews from real enthusiasts • Matching your taste buds with precision • Every recommendation is data-driven 🍻</p>
        <p style="font-size: 12px; margin-top: 10px;">Like having a beer sommelier in your pocket</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()