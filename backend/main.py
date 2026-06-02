from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import json
import requests
from typing import List, Optional

app = FastAPI(
    title="Food Recommender API",
    description="Rekomendasi makanan/restoran menggunakan TOPSIS",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Pydantic Models
# =====================================================

class LocationInput(BaseModel):
    latitude: float
    longitude: float
    top_n: int = 10


class RecommendationItem(BaseModel):
    rank: int
    nama: str
    kategori: str
    harga: float
    jarak: float
    rating: float
    skor_topsis: float
    latitude: float
    longitude: float


class RecommendationResponse(BaseModel):
    user_location: dict
    recommendations: List[RecommendationItem]
    total_items: int


# =====================================================
# Fungsi Helper
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


def load_bobot():
    """Load bobot dari JSON file"""
    try:
        with open("bobot_kriteria.json", "r") as f:
            bobot_config = json.load(f)
        
        bobot = np.array([
            bobot_config["harga"],
            bobot_config["jarak"],
            bobot_config["rating"]
        ])
        return bobot
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="File bobot_kriteria.json tidak ditemukan!"
        )


def load_data_topsis():
    """Load data alternatif makanan/restoran"""
    try:
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
        
        return df_topsis
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="File data_untuk_topsis.xlsx tidak ditemukan!"
        )


def hitung_topsis(df_topsis, bobot):
    """Hitung TOPSIS score"""
    # Matriks keputusan TOPSIS
    X_matrix = df_topsis[
        ["harga", "jarak", "rating"]
    ].values.astype(float)
    
    # harga = cost, jarak = cost, rating = benefit
    kriteria_tipe = np.array([-1, -1, 1])
    
    # Normalisasi
    norm_X = X_matrix / np.sqrt(
        (X_matrix ** 2).sum(axis=0)
    )
    
    # Matriks ternormalisasi terbobot
    terbobot_X = norm_X * bobot
    
    # Solusi ideal positif dan negatif
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
    
    # Hitung D+ dan D-
    D_positif = np.sqrt(
        ((terbobot_X - A_positif) ** 2).sum(axis=1)
    )
    
    D_negatif = np.sqrt(
        ((terbobot_X - A_negatif) ** 2).sum(axis=1)
    )
    
    # Nilai preferensi TOPSIS
    V = D_negatif / (
        D_positif + D_negatif + 1e-9
    )
    
    return V


# =====================================================
# Endpoints
# =====================================================

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Selamat datang di Food Recommender API",
        "docs": "/docs",
        "endpoints": {
            "auto_location": "GET /recommendations/auto",
            "custom_location": "POST /recommendations"
        }
    }


@app.get("/recommendations/auto", response_model=RecommendationResponse)
def get_recommendations_auto(top_n: int = 10):
    """
    Dapatkan rekomendasi makanan berdasarkan lokasi otomatis (IP geolocation)
    
    Args:
        top_n: Jumlah rekomendasi yang ditampilkan (default: 10)
    """
    try:
        # Ambil lokasi pengguna saat ini via IP
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        user_lat, user_lon = map(float, data["loc"].split(","))
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal mendapatkan lokasi pengguna: {str(e)}"
        )
    
    return _process_recommendations(user_lat, user_lon, top_n)


@app.post("/recommendations", response_model=RecommendationResponse)
def get_recommendations(location: LocationInput):
    """
    Dapatkan rekomendasi makanan berdasarkan lokasi yang diberikan
    
    Args:
        location: Object berisi latitude, longitude, dan top_n
    """
    return _process_recommendations(
        location.latitude,
        location.longitude,
        location.top_n
    )


def _process_recommendations(user_lat: float, user_lon: float, top_n: int):
    """Internal function untuk memproses rekomendasi"""
    
    # Load data dan bobot
    df_topsis = load_data_topsis()
    bobot = load_bobot()
    
    # Hitung jarak
    df_topsis["jarak"] = hitung_jarak(
        user_lat,
        user_lon,
        df_topsis["latitude"],
        df_topsis["longitude"]
    )
    
    # Hitung TOPSIS score
    skor_topsis = hitung_topsis(df_topsis, bobot)
    df_topsis["skor_topsis"] = skor_topsis
    
    # Ranking
    hasil_rekomendasi = df_topsis.sort_values(
        by="skor_topsis",
        ascending=False
    ).reset_index(drop=True)
    
    # Ambil top N
    top_recommendations = hasil_rekomendasi.head(top_n)
    
    # Format response
    recommendations = []
    for idx, row in top_recommendations.iterrows():
        rec = RecommendationItem(
            rank=idx + 1,
            nama=row["nama"],
            kategori=row.get("kategori", ""),
            harga=float(row["harga"]),
            jarak=round(float(row["jarak"]), 2),
            rating=float(row["rating"]),
            skor_topsis=round(float(row["skor_topsis"]), 4),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"])
        )
        recommendations.append(rec)
    
    return RecommendationResponse(
        user_location={
            "latitude": user_lat,
            "longitude": user_lon
        },
        recommendations=recommendations,
        total_items=len(recommendations)
    )


@app.get("/bobot")
def get_bobot():
    """Tampilkan bobot kriteria"""
    bobot = load_bobot()
    return {
        "harga": float(bobot[0]),
        "jarak": float(bobot[1]),
        "rating": float(bobot[2])
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
