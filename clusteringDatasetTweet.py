import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# 1. Load the Dataset
df = pd.read_csv('tsunami_dataset_recent.csv')

# 2. Preprocessing Function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)     # Remove mentions
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove punctuation/numbers
    return text

df['cleaned_text'] = df['tweet_text'].apply(clean_text)

# 3. Vectorization (Convert text to numbers)
# We ignore words that appear in >95% of tweets (common stopwords)
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
X = vectorizer.fit_transform(df['cleaned_text'])

# 4. Apply K-Means Clustering (k=2)
kmeans = KMeans(n_clusters=2, random_state=42)
df['cluster_raw'] = kmeans.fit_predict(X)

# 5. Logic to Assign "Tsunami" (1) vs "Non-Tsunami" (0) correctly
# We look at the top keywords of each cluster to see which one is more "physical"
feature_names = vectorizer.get_feature_names_out()
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

# Define keywords that strongly indicate a physical/geological tsunami
physical_keywords = ['flood', 'water', 'wave', 'ocean', 'sea', 'survivor', 'earthquake', 'height']

cluster_scores = {}
for i in range(2):
    # Get top 20 words for this cluster
    top_words = [feature_names[ind] for ind in order_centroids[i, :20]]
    # Count how many physical keywords are in the top words
    score = sum([1 for w in top_words if w in physical_keywords])
    cluster_scores[i] = score

# The cluster with the higher score for physical words becomes Label 1
tsunami_cluster_idx = max(cluster_scores, key=cluster_scores.get)

# Apply the final labels
df['cluster_label'] = df['cluster_raw'].apply(lambda x: 1 if x == tsunami_cluster_idx else 0)
df['cluster_name'] = df['cluster_label'].apply(lambda x: 'Tsunami' if x == 1 else 'Non-Tsunami')

# 6. Save the Results
output_file = 'tsunami_clustering_output.csv'
df[['tweet_id', 'tweet_text', 'cluster_label', 'cluster_name']].to_csv(output_file, index=False)

print(f"Processing complete. Saved to {output_file}")
print(f"Cluster {tsunami_cluster_idx} was identified as the Tsunami group.")