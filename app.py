import streamlit as st
import pandas as pd
from beer_recommender import BeerRecommender

st.set_page_config(
    page_title="🍺 Beer Buddy - Terminal Style",
    page_icon="🍺",
    layout="wide"
)

# Simple CSS for terminal-like appearance
st.markdown("""
<style>
    .stApp {
        background-color: #1e1e1e;
    }
    .output-box {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #333;
        white-space: pre-wrap;
        line-height: 1.5;
    }
    h1 {
        color: #ffd700;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput input {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommender():
    recommender = BeerRecommender()
    with st.spinner("Loading beer database..."):
        recommender.load_and_preprocess_data()
        recommender.train_regression_model()
    return recommender

def display_results(predicted_rating, regular_recommendations, alt_recommendations=None):
    """
    Display recommendations with warnings for low-rated combinations
    """
    output = ""
    
    if alt_recommendations is not None:
        # Low rating case - show warning and alternatives
        output += "━" * 60 + "\n"
        output += f"⚠️  Warning: This flavor combination typically rates {predicted_rating:.2f}/5\n"
        output += "━" * 60 + "\n"
        
        output += "\n📍 Here's what matches your exact request:\n"
        if regular_recommendations:
            for i, beer in enumerate(regular_recommendations[:2], 1):
                output += f"{i}. {beer['name']} ({beer['rating']:.2f}★ - {int(beer['num_reviews'])} reviews)\n"
                output += f"   Distance: {beer['distance']:.3f}\n"
        else:
            output += "   No exact matches found in our database.\n"
        
        output += "\n💡 Suggested Alternatives (similar but better rated):\n"
        if alt_recommendations:
            for i, beer in enumerate(alt_recommendations[:2], 1):
                output += f"{i}. {beer['name']} ({beer['rating']:.2f}★ - {int(beer['num_reviews'])} reviews)\n"
                output += f"   Distance: {beer['distance']:.3f}\n"
        else:
            output += "   No high-rated alternatives found with your criteria.\n"
            
        output += "\n💭 Tip: The flavor combination you requested is uncommon. The alternatives above\n"
        output += "   maintain similar characteristics but with proven appeal to beer enthusiasts.\n"
        
    else:
        # Good rating case - normal display
        output += "━" * 60 + "\n"
        output += f"✅ Great choice! Predicted rating: {predicted_rating:.2f}/5\n"
        output += "━" * 60 + "\n"
        
        output += "\n🍺 Top Recommendations:\n"
        for i, beer in enumerate(regular_recommendations[:2], 1):
            output += f"\n{i}. {beer['name']}\n"
            output += f"   Rating: {beer['rating']:.2f}/5 ({int(beer['num_reviews'])} reviews)\n"
            output += f"   Distance: {beer['distance']:.3f}\n"
            
            # Format description
            desc = beer['description'] if beer['description'] else ""
            if len(desc) > 120:
                desc = desc[:120] + "..."
            output += f"   Notes: {desc}\n" if desc else "   Notes: ...\n"
    
    output += "\n" + "─" * 60
    return output

def main():
    st.markdown("# 🍺 Beer Buddy - Recommendation System")
    
    recommender = load_recommender()
    
    # Simple input section
    st.markdown("---")
    
    # Pre-defined examples
    examples = [
        "I want a light citrusy beer",
        "I want a strong lager which is fruity and not too malty",
        "I want a strong orangey tart beer",
        "Give me a hoppy IPA with tropical notes",
        "I want a sessionable pilsner",
        "I need a dessert beer with chocolate and coffee notes",
        "Something light and refreshing with low alcohol",
        "I want a Belgian tripel with spicy notes",
        "Give me a bitter hoppy beer with no sweetness",
        "I want a sweet malty amber ale",
        "Something sour and funky with brett character",
        "I want a very sweet and very hoppy beer",
        "Just a Bad beer"
    ]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input(
            "Enter your beer preference:",
            placeholder="e.g., 'I want a hoppy IPA with tropical notes'",
            key="beer_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Get Recommendations", type="primary", use_container_width=True):
            if user_input:
                st.session_state.run_search = True
                st.session_state.search_query = user_input
            else:
                st.warning("Please enter a beer preference!")
    
    # Quick examples
    st.markdown("**Quick Examples:**")
    cols = st.columns(4)
    for idx, example in enumerate(examples):
        col_idx = idx % 4
        with cols[col_idx]:
            if st.button(example[:30] + "..." if len(example) > 30 else example, key=f"ex_{idx}"):
                st.session_state.run_search = True
                st.session_state.search_query = example
    
    st.markdown("---")
    
    # Process and display results
    if hasattr(st.session_state, 'run_search') and st.session_state.run_search:
        with st.spinner("Processing your request..."):
            try:
                # Get the query
                query = st.session_state.search_query
                
                # Display the prompt
                prompt_output = f"User Prompt = {query}"
                
                # Get recommendations
                results = recommender.get_recommendations(query)
                
                # Get rating and recommendations
                predicted_rating = results['predicted_rating']
                recommendations = results['recommendations']
                alt_recommendations = results.get('alt_recommendations')
                
                # Generate the display
                output = display_results(predicted_rating, recommendations, alt_recommendations)
                
                # Display in terminal style
                st.markdown(
                    f'<div class="output-box">{prompt_output}\n{output}\n{"=" * 133}</div>',
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # Reset the search flag
        st.session_state.run_search = False
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888; font-size: 0.9em;">
        Powered by ML • 3,197 craft beers • Gradient Boosting + KNN
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
