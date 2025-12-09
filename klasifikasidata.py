import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# 1. Membaca Dataset
# Pastikan file 'combined_tsunami_dataset.csv' ada di direktori yang sama
df = pd.read_csv('combined_tsunami_dataset.csv')

# 2. Preprocessing (Pembersihan Data Teks)
def clean_text(text):
    text = str(text).lower()                 # Ubah ke huruf kecil
    text = re.sub(r'http\S+', '', text)      # Hapus URL
    text = re.sub(r'@\w+', '', text)         # Hapus mention (@username)
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Hapus angka dan tanda baca
    return text.strip()

df['cleaned_text'] = df['text'].apply(clean_text)

# 3. Ekstraksi Fitur (TF-IDF)
# Mengubah teks menjadi angka agar bisa diproses oleh model
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
X = tfidf.fit_transform(df['cleaned_text'])
y = df['cluster_label']  # Label: 1 = Tsunami, 0 = Non-Tsunami

# 4. Membagi Data (Training & Testing)
# Kita gunakan 80% untuk latihan dan 20% untuk pengujian
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Melatih Model (Logistic Regression)
model = LogisticRegression()
model.fit(X_train, y_train)

# 6. Evaluasi Model
y_pred = model.predict(X_test)

print("=== Hasil Evaluasi Model ===")
print(f"Akurasi: {accuracy_score(y_test, y_pred):.2f}")
print("\nLaporan Klasifikasi:")
print(classification_report(y_test, y_pred, target_names=['Non-Tsunami', 'Tsunami']))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Contoh Prediksi Teks Baru (Opsional)
print("\n=== Tes Prediksi Baru ===")
new_texts = [
    "Huge tsunami waves are hitting the coast after the earthquake!",
    "I am watching a movie about a disaster."
]
new_texts_cleaned = [clean_text(t) for t in new_texts]
new_features = tfidf.transform(new_texts_cleaned)
predictions = model.predict(new_features)

for text, pred in zip(new_texts, predictions):
    label = "Tsunami" if pred == 1 else "Non-Tsunami"
    print(f"Text: '{text}' -> Prediksi: {label}")