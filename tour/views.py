import pandas as pd
from django.shortcuts import render
from .models import Tour, UserProfile
from .recommendations import tour_recommend
import os
from django.conf import settings

# Path to the CSV file
csv_path = os.path.join(settings.BASE_DIR, 'tour', 'data', 'place_data.csv')

def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})

def tour_recommend(user_profile, filtered_tours):
    # Filter based on budget
    recommended_tours = filtered_tours.copy()

    # Further filter or rank based on interests
    recommended_tours['Score'] = 0
    for interest in user_profile['interests']:
        recommended_tours['Score'] += recommended_tours['Description'].str.contains(interest, case=False).astype(int)
    
    # Sort the tours by the score
    recommended_tours = recommended_tours.sort_values(by='Score', ascending=False)
    
    return recommended_tours

def tour_recommendation(request):
    # Load dataset from CSV into a DataFrame
    all_tours = pd.read_csv(csv_path)

    # Add a Description column combining the type and place for recommendation logic
    all_tours['Description'] = all_tours['type'].astype(str) + ' ' + all_tours['place'].astype(str)
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        filtered_tours = all_tours[all_tours['place'].str.contains(search_query, case=False)]
    else:
        filtered_tours = all_tours

    # Dummy user profile, can be replaced with real data
    user_profile = {
        'interests': ['Temple', 'Gardens', 'Palace'],  # Example interests
        # 'budget': 2000  # Example budget
    }
    
    # Get recommendations
    recommendations = tour_recommend(user_profile, filtered_tours)
    
    # Convert to list of dictionaries
    recommendation_list = recommendations.to_dict('records')
    
    # Render the template with the recommendations
    return render(request, 'tour_recommendation.html', {'tours': recommendation_list})
