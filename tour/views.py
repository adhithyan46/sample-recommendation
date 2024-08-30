from django.shortcuts import render
from .models import Tour,UserProfile
import pandas as pd
from .recommendations import tour_recommend

# Create your views here.

data = {
    'TourID': [1, 2, 3, 4, 5],
    'Name': ['Paris Adventure', 'London Royal Experience', 'New York City Highlights', 'Tokyo Cultural Tour', 'Sydney Coastal Escape'],
    'Location': ['Paris', 'London', 'New York', 'Tokyo', 'Sydney'],
    'Description': [
        'Explore the city of lights with guided tours to iconic landmarks like the Eiffel Tower and the Louvre.',
        'A royal tour of London\'s historical sites including Buckingham Palace and the Tower of London.',
        'Discover the Big Apple with visits to Times Square, Central Park, and the Statue of Liberty.',
        'Experience the rich culture of Tokyo with a mix of traditional and modern attractions.',
        'Enjoy the beauty of Sydney with beach visits, harbour cruises, and the Sydney Opera House.',
    ],
    'Price': [1500.00, 1800.00, 2000.00, 2200.00, 1700.00],
    'Image': ['images/paris.jpg', 'images/london.jpg', 'images/newyork.jpg', 'images/tokyo.jpg', 'images/sydney.jpg']
}



def tour_list(request):
    tours = Tour.objects.all()
    return render(request,'tour_list.html',{'tours':tours})



def tour_recommend(user_profile, filtered_tours):
    # Filter based on budget
    recommended_tours = filtered_tours[filtered_tours['Price'] <= user_profile['budget']]

    # Further filter or rank based on interests
    recommended_tours['Score'] = 0
    for interest in user_profile['interests']:
        recommended_tours['Score'] += recommended_tours['Description'].str.contains(interest, case=False).astype(int)
    
    # Sort the tours by the score
    recommended_tours = recommended_tours.sort_values(by='Score', ascending=False)
    
    return recommended_tours

# Example usage in your tour_recommendation function
def tour_recommendation(request):
    # Convert dataset to DataFrame
    all_tours = pd.DataFrame(data)
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        filtered_tours = all_tours[all_tours['Location'].str.contains(search_query, case=False)]
    else:
        filtered_tours = all_tours

    # Dummy user profile, can be replaced with real data
    user_profile = {
        'interests': ['culture', 'history', 'sightseeing'],  # Example interests
        'budget': 2000  # Example budget
    }
    
    # Get recommendations (Using your existing tour_recommend function)
    recommendations = tour_recommend(user_profile, filtered_tours)
    
    # Convert to list of dictionaries
    recommendation_list = recommendations.to_dict('records')
    
    # Render the template with the recommendations
    return render(request, 'tour_recommendation.html', {'tours': recommendation_list})