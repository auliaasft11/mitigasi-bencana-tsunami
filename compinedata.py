import pandas as pd

# 1. Membaca kedua file dataset
file_balanced = '/home/aafil/tugas/mitigasi bencana SI/mitigasi/kaggle/tsunami_dataset_balanced.csv'
file_recent = '/home/aafil/tugas/mitigasi bencana SI/mitigasi/tsunami_clustering_output.csv'

try:
    df_balanced = pd.read_csv(file_balanced)
    df_recent = pd.read_csv(file_recent)
    print("Berhasil membaca kedua file.")
except FileNotFoundError:
    print("Salah satu file tidak ditemukan.")
    exit()

# 2. Menyamakan nama kolom
# Dataset recent memiliki kolom 'tweet_id' dan 'tweet_text', 
# sedangkan dataset balanced memiliki 'id' dan 'text'.
# Kita ubah dataset recent agar sesuai dengan dataset balanced.
df_recent = df_recent.rename(columns={
    'tweet_id': 'id', 
    'tweet_text': 'text'
})

# Pastikan kita hanya mengambil kolom yang relevan dan urutannya sama
target_columns = ['id', 'text', 'cluster_label', 'cluster_name']

# Cek apakah kolom tersedia di kedua dataframe
if set(target_columns).issubset(df_balanced.columns) and set(target_columns).issubset(df_recent.columns):
    df_balanced = df_balanced[target_columns]
    df_recent = df_recent[target_columns]
else:
    print("Error: Nama kolom tidak sesuai. Pastikan kolom id, text, cluster_label, cluster_name ada.")
    # (Opsional) Print kolom yang ada untuk debugging
    print("Kolom Balanced:", df_balanced.columns)
    print("Kolom Recent:", df_recent.columns)
    exit()

# 3. Menggabungkan dataset (Concatenate)
df_combined = pd.concat([df_balanced, df_recent], ignore_index=True)

# 4. Cek hasil penggabungan
print(f"\nTotal data setelah digabung: {len(df_combined)}")
print(df_combined['cluster_name'].value_counts())

# 5. Simpan ke file CSV baru
output_filename = 'combined_tsunami_dataset.csv'
df_combined.to_csv(output_filename, index=False)
print(f"\nFile berhasil disimpan: {output_filename}")