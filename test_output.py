#!/usr/bin/env python3
"""
Test script to verify beer recommendations match expected output
Run this from the beer-buddy directory: python test_output.py
"""

import sys
sys.path.append('.')

from beer_recommender import BeerRecommender

def display_results(predicted_rating, regular_recommendations, alt_recommendations=None):
    """Display recommendations exactly like beer_expected.ipynb"""
    
    if alt_recommendations is not None:
        # Low rating case - show warning and alternatives
        print("━" * 60)
        print(f"⚠️  Warning: This flavor combination typically rates {predicted_rating:.2f}/5")
        print("━" * 60)
        
        print("\n📍 Here's what matches your exact request:")
        if regular_recommendations:
            for i, beer in enumerate(regular_recommendations[:2], 1):
                print(f"{i}. {beer['name']} ({beer['rating']:.2f}★ - {int(beer['num_reviews'])} reviews)")
                print(f"   Distance: {beer['distance']:.3f}")
        else:
            print("   No exact matches found in our database.")
        
        print("\n💡 Suggested Alternatives (similar but better rated):")
        if alt_recommendations:
            for i, beer in enumerate(alt_recommendations[:2], 1):
                print(f"{i}. {beer['name']} ({beer['rating']:.2f}★ - {int(beer['num_reviews'])} reviews)")
                print(f"   Distance: {beer['distance']:.3f}")
        else:
            print("   No high-rated alternatives found with your criteria.")
            
        print("\n💭 Tip: The flavor combination you requested is uncommon. The alternatives above")
        print("   maintain similar characteristics but with proven appeal to beer enthusiasts.")
        
    else:
        # Good rating case - normal display
        print("━" * 60)
        print(f"✅ Great choice! Predicted rating: {predicted_rating:.2f}/5")
        print("━" * 60)
        
        print("\n🍺 Top Recommendations:")
        for i, beer in enumerate(regular_recommendations[:2], 1):
            print(f"\n{i}. {beer['name']}")
            print(f"   Rating: {beer['rating']:.2f}/5 ({int(beer['num_reviews'])} reviews)")
            print(f"   Distance: {beer['distance']:.3f}")
            
            # Format description
            desc = beer.get('description', '')
            if desc:
                if len(desc) > 120:
                    desc = desc[:120] + "..."
                print(f"   Notes: Notes:{desc}")
            else:
                print("   Notes: Notes:...")
    
    print("\n" + "─" * 60)

def test_beer_recommendations():
    """Test the beer recommendation system with various inputs"""
    
    print("Loading beer recommender system...")
    recommender = BeerRecommender()
    recommender.load_and_preprocess_data()
    recommender.train_regression_model()
    print("System loaded successfully!\n")
    
    # Test cases
    test_cases = [
        "I want a light citrusy beer",
        "I want a sessionable pilsner",
        "Just a Bad beer"
    ]
    
    for query in test_cases:
        print(f"User Prompt = {query}")
        
        try:
            # Get recommendations
            results = recommender.get_recommendations(query)
            
            # Display results
            display_results(
                results['predicted_rating'],
                results['recommendations'],
                results.get('alt_recommendations')
            )
            
        except Exception as e:
            print(f"Error processing '{query}': {e}")
        
        print("=" * 133)
        print()

if __name__ == "__main__":
    test_beer_recommendations()
