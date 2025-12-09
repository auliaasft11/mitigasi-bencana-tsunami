import pandas as pd

# 1. Membaca file CSV
filename = 'tsunami_clustering_output.csv'
try:
    df = pd.read_csv(filename)
    print(f"Berhasil membaca file: {filename}")
    print(f"Total data awal: {len(df)}")
except FileNotFoundError:
    print(f"File {filename} tidak ditemukan. Pastikan nama file dan lokasi sudah benar.")
    exit()

# 2. Cek jumlah data per label sebelum dihapus
print("\nJumlah data per kategori (Awal):")
print(df['cluster_name'].value_counts())

# 3. Memisahkan data Tsunami dan Non-Tsunami
# Pastikan nama kolom label sesuai (misal: 'cluster_name' atau 'cluster_label')
tsunami_data = df[df['cluster_name'] == 'Tsunami']
non_tsunami_data = df[df['cluster_name'] == 'Non-Tsunami']

# 4. Menentukan jumlah data Non-Tsunami yang ingin diambil
# OPSI A: Samakan jumlahnya dengan data Tsunami (Balance 50:50)
jumlah_target = 60

# OPSI B: Tentukan jumlah manual (misal: ambil 1000 data non-tsunami saja)
# jumlah_target = 1000 

# Pastikan kita tidak mengambil lebih banyak dari yang tersedia
jumlah_ambil = min(len(non_tsunami_data), jumlah_target)

# 5. Lakukan pengambilan acak (Random Sampling) pada data Non-Tsunami
non_tsunami_reduced = non_tsunami_data.sample(n=jumlah_ambil, random_state=42)

# 6. Menggabungkan kembali data
df_final = pd.concat([tsunami_data, non_tsunami_reduced])

# Acak urutan baris agar data Tsunami dan Non-Tsunami tidak berkelompok
df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

# 7. Cek hasil akhir
print("\nJumlah data per kategori (Setelah Penghapusan):")
print(df_final['cluster_name'].value_counts())

# 8. Simpan ke file baru
output_filename = 'tsunami_dataset_balanced.csv'
df_final.to_csv(output_filename, index=False)
print(f"\nFile baru berhasil disimpan sebagai: {output_filename}")