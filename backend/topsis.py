import pandas as pd
import numpy as np
import json
import requests

# =====================================================
# 1. Ambil lokasi pengguna saat ini
# =====================================================
response = requests.get("https://ipinfo.io/json")
data = response.json()

user_lat, user_lon = map(float, data["loc"].split(","))

print("Latitude :", user_lat)
print("Longitude:", user_lon)

print("\n=== LANGKAH 2: PROSES REKOMENDASI DENGAN TOPSIS ===")

# =====================================================
# 2. Load bobot hasil Random Forest
# =====================================================
try:
    with open("bobot_kriteria.json", "r") as f:
        bobot_config = json.load(f)

    # Urutan bobot: harga, jarak, rating
    bobot = np.array([
        bobot_config["harga"],
        bobot_config["jarak"],
        bobot_config["rating"]
    ])

    print("Berhasil memuat bobot dari JSON.")
    print("Bobot:", bobot)

except FileNotFoundError:
    print("Error: File bobot_kriteria.json tidak ditemukan!")
    exit()

# =====================================================
# 3. Load data alternatif makanan/restoran
# =====================================================
df_topsis = pd.read_excel(
    r"C:\Users\NITRO\Desktop\SUPER CODE PROJECT\food-recommender\backend\data_untuk_topsis.xlsx"
)

# Pastikan koordinat bertipe numerik
df_topsis["latitude"] = pd.to_numeric(
    df_topsis["latitude"],
    errors="coerce"
)

df_topsis["longitude"] = pd.to_numeric(
    df_topsis["longitude"],
    errors="coerce"
)

# Hapus data yang koordinatnya kosong
df_topsis = df_topsis.dropna(subset=["latitude", "longitude"])

# =====================================================
# 4. Hitung jarak menggunakan Haversine
# =====================================================
def hitung_jarak(lat1, lon1, lat2, lon2):
    """
    Menghitung jarak dalam kilometer menggunakan rumus Haversine
    """

    R = 6371  # Radius bumi (km)

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)

    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c

# Tambahkan kolom jarak
df_topsis["jarak"] = hitung_jarak(
    user_lat,
    user_lon,
    df_topsis["latitude"],
    df_topsis["longitude"]
)

# =====================================================
# 5. Matriks keputusan TOPSIS
# =====================================================
X_matrix = df_topsis[
    ["harga", "jarak", "rating"]
].values.astype(float)

# harga = cost
# jarak = cost
# rating = benefit
kriteria_tipe = np.array([-1, -1, 1])

# =====================================================
# 6. Normalisasi
# =====================================================
norm_X = X_matrix / np.sqrt(
    (X_matrix ** 2).sum(axis=0)
)

# =====================================================
# 7. Matriks ternormalisasi terbobot
# =====================================================
terbobot_X = norm_X * bobot

# =====================================================
# 8. Solusi ideal positif dan negatif
# =====================================================
A_positif = np.zeros(3)
A_negatif = np.zeros(3)

for i in range(3):

    if kriteria_tipe[i] == 1:
        # Benefit
        A_positif[i] = np.max(terbobot_X[:, i])
        A_negatif[i] = np.min(terbobot_X[:, i])

    else:
        # Cost
        A_positif[i] = np.min(terbobot_X[:, i])
        A_negatif[i] = np.max(terbobot_X[:, i])

# =====================================================
# 9. Hitung D+ dan D-
# =====================================================
D_positif = np.sqrt(
    ((terbobot_X - A_positif) ** 2).sum(axis=1)
)

D_negatif = np.sqrt(
    ((terbobot_X - A_negatif) ** 2).sum(axis=1)
)

# =====================================================
# 10. Nilai preferensi TOPSIS
# =====================================================
V = D_negatif / (
    D_positif + D_negatif + 1e-9
)

df_topsis["skor_topsis"] = V

# =====================================================
# 11. Ranking
# =====================================================
hasil_rekomendasi = df_topsis.sort_values(
    by="skor_topsis",
    ascending=False
)

# =====================================================
# 12. Tampilkan hasil
# =====================================================
print("\n=== TOP 10 REKOMENDASI MAKANAN ===")

print(
    hasil_rekomendasi[
        [
            "nama",
            "harga",
            "jarak",
            "rating",
            "kategori",
            "skor_topsis"
        ]
    ]
    .head(10)
    .to_string(index=False)
)