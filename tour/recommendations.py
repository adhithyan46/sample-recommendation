import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def tour_recommend(user_profile, all_tour):
    # Convert user interests into a single string
    user_interests = ' '.join(user_profile['interests'])
    
    all_tour['Description'] = all_tour['type'].astype(str) + ' ' + all_tour['place'].astype(str)
    
    # Include the user interests in the dataset for TF-IDF calculation
    all_tour_with_profile = all_tour.copy()
    all_tour_with_profile = all_tour_with_profile.append(
        {'Description': user_interests},
        ignore_index=True
    )
    
    # Vectorize the descriptions including the user interests
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(all_tour_with_profile['Description'])
    
    # Calculate cosine similarity between the user's interests and all tours
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Get the indices of the top 5 most similar tours
    top_indices = cosine_sim.argsort()[0][-5:][::-1]
    
    # Select and return the top 5 recommendations
    recommendations = all_tour.iloc[top_indices]
    return recommendations