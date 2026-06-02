import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier

print("=== LANGKAH 1: MENGHITUNG BOBOT DENGAN RANDOM FOREST ===")

# 1. Load data kuesioner
df_rf = pd.read_excel(r"C:\Users\NITRO\Desktop\SUPER CODE PROJECT\food-recommender\backend\data_untuk_random_forest.xlsx")

# Bersihkan spasi pada nama kolom
df_rf.columns = [col.strip() for col in df_rf.columns]

# 2. Mapping data teks ke angka ordinal
budget_map = {'10rb - 15rb': 1, '15k - 20k': 2, 'Diatas 20k': 3}
jarak_map = {'Dibawah 1km': 1, '1 - 2km': 2, '2 - 5km': 3, 'Diatas 5km': 4}
rating_map = {'1.0 - 2.0+': 1, '3.0 - 4.0+': 2, '4.0 - 5.0+': 3}

# Ambil kolom berdasarkan posisi indeks
X_rf = pd.DataFrame({
    'Budget': df_rf.iloc[:, 1].str.strip().map(budget_map),
    'Jarak': df_rf.iloc[:, 2].str.strip().map(jarak_map),
    'Rating': df_rf.iloc[:, 3].str.strip().map(rating_map)
})
y_rf = df_rf.iloc[:, 4].str.strip().astype('category').cat.codes

# Drop baris yang kosong atau gagal mapping
X_rf = X_rf.dropna()
y_rf = y_rf[X_rf.index]

# 3. Latih Model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_rf, y_rf)

# 4. Ambil Feature Importance
bobot = rf.feature_importances_

# 5. Simpan Hasil Bobot ke File JSON
data_bobot = {
    "harga": float(bobot[0]),   # Budget dipetakan ke harga di TOPSIS
    "jarak": float(bobot[1]),
    "rating": float(bobot[2])
}

with open("bobot_kriteria.json", "w") as f:
    json.dump(data_bobot, f, indent=4)

print("Selesai! Bobot berhasil dihitung dan disimpan ke 'bobot_kriteria.json':")
print(json.dumps(data_bobot, indent=4))