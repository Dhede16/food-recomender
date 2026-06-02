# 🍽️ Food Recommender — Sistem Rekomendasi Makanan Berbasis Lokasi

Aplikasi rekomendasi makanan berbasis **TOPSIS MCDM** dengan visualisasi peta interaktif untuk menemukan tempat makan terbaik berdasarkan lokasi, harga, rating, dan jarak.

---

## 🎯 Fitur Utama

✨ **Rekomendasi Cerdas**: Menggunakan algoritma TOPSIS untuk ranking multi-criteria  
📍 **Berbasis Lokasi**: Hitung jarak otomatis dari lokasi user ke setiap restoran  
🗺️ **Peta Interaktif**: Visualisasi dengan Leaflet menampilkan lokasi user dan restoran  
📱 **Responsive Design**: Optimal di desktop, tablet, dan mobile  
⚡ **Real-time API**: Backend FastAPI dengan performa tinggi

---

## 🛠️ Prasyarat

- Python 3.9+ (untuk backend)
- Node.js 16+ (untuk frontend)
- npm atau yarn

---

## 🚀 Cara Menjalankan

### Option 1: Jalankan Secara Manual (Recommended untuk Development)

#### 1️⃣ Backend (FastAPI)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Jalankan server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

✅ Backend berjalan di: **http://localhost:8000**  
📖 Dokumentasi Swagger: **http://localhost:8000/docs**

#### 2️⃣ Frontend (Vue.js 3)

Di terminal baru, jalankan:

```bash
cd frontend

# Install dependencies  
npm install

# Jalankan development server
npm run dev
```

✅ Frontend berjalan di: **http://localhost:5173**

---

### Option 2: Jalankan dengan Script (Linux/Mac)

```bash
bash start.sh
```

Atau di Windows (PowerShell):
```powershell
.\start.sh
```

---

## 📡 Backend API Endpoints

| Method | Endpoint           | Deskripsi                              |
|--------|--------------------|-----------------------------------------|
| GET    | `/`                | Info API                               |
| POST   | `/recommendations` | Dapatkan rekomendasi untuk lokasi      |
| GET    | `/recommendations/auto` | Rekomendasi berdasarkan IP geolocation |
| GET    | `/bobot`           | Lihat bobot kriteria TOPSIS            |
| GET    | `/health`          | Health check                           |

### POST `/recommendations` — Request
```json
{
  "latitude": -0.5022,
  "longitude": 117.1536,
  "top_n": 10
}
```

### POST `/recommendations` — Response
```json
{
  "user_location": {
    "latitude": -0.5022,
    "longitude": 117.1536
  },
  "recommendations": [
    {
      "rank": 1,
      "nama": "Warung Makan ABC",
      "kategori": "Murah",
      "harga": 15000,
      "jarak": 0.52,
      "rating": 4.5,
      "skor_topsis": 0.856,
      "latitude": -0.5025,
      "longitude": 117.1540
    }
    // ... lebih banyak rekomendasi
  ],
  "total_items": 10
}
```

---

## 🧮 Metode TOPSIS

**TOPSIS** (Technique for Order Preference by Similarity to Ideal Solution) adalah algoritma Multi-Criteria Decision Making yang mempertimbangkan:

| Kriteria | Bobot | Tipe     |
|----------|-------|----------|
| 💰 Harga | 32%   | Minimise |
| 📍 Jarak | 43%   | Minimise |
| ⭐ Rating| 25%   | Maximise |

Setiap tempat makan di-score berdasarkan ketiga kriteria ini, menghasilkan ranking yang optimal.

---

## 📊 Data & Sumber

- **Tempat Makan**: 113+ lokasi restoran/warung makan di Samarinda
- **Data Lokal**: Koordinat GPS, harga menu, dan user ratings
- **Jarak Dihitung**: Menggunakan rumus **Haversine** (akurat untuk jarak geografis)

---

## 🗂️ Struktur Proyek

```
food-recommender/
├── backend/
│   ├── main.py                    # FastAPI app + TOPSIS logic
│   ├── random_forest.py          # Random Forest classifier
│   ├── topsis.py                 # TOPSIS algorithm
│   ├── requirements.txt           # Python dependencies
│   ├── bobot_kriteria.json        # TOPSIS weights config
│   └── data_untuk_topsis.xlsx    # Food location data
│
├── frontend/
│   ├── src/
│   │   ├── App.vue               # Main component
│   │   ├── main.js               # Entry point
│   │   └── components/           # Additional components (future)
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── README.md                 # Frontend documentation
│
├── README.md                      # File ini
└── start.sh                       # Script untuk menjalankan keduanya
```

---

## 🎨 Frontend Features

### Input Form
- Manual coordinate input (latitude/longitude)
- Auto-detect location dengan Geolocation API
- Adjust jumlah rekomendasi (5-20)

### Hasil Rekomendasi
- **Desktop**: Table view dengan sorting
- **Mobile**: Card-based view yang responsive
- **Interactive Map**: Leaflet dengan markers dan popups

### Detail Modal
- Klik setiap rekomendasi untuk detail lengkap
- Tombol "Buka di Google Maps"
- Tampilan score, jarak, harga, dan rating

---

## 🔧 Development

### Frontend Build for Production
```bash
cd frontend
npm run build      # Build optimized files
npm run preview    # Preview production build locally
```

### Backend Production
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🐛 Troubleshooting

### Backend tidak terhubung
- ✅ Pastikan backend berjalan di port 8000
- ✅ Check terminal untuk error messages
- ✅ Verify `data_untuk_topsis.xlsx` ada di backend folder
- ✅ Check file path di main.py sesuai dengan sistem Anda

### Peta tidak muncul
- ✅ Check browser console (F12) untuk error
- ✅ Pastikan internet connection aktif (untuk tile layer OpenStreetMap)
- ✅ Verify leaflet CSS dimuat dengan benar

### Geolocation error
- ✅ Browser harus HTTPS atau localhost (untuk security)
- ✅ Approve permission ketika browser minta geolocation
- ✅ Cek console browser untuk detailed error

### Koordinat tidak valid
- ✅ Format: decimal format (e.g., -0.5022, 117.1536)
- ✅ Tidak boleh ada karakter khusus
- ✅ Gunakan default Samarinda jika perlu: -0.5022, 117.1536

---

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (Single column, full-width)
- **Tablet**: 768px - 1024px (2-column grid)
- **Desktop**: > 1024px (Full layout with table & sidebar)

---

## 🚀 Deployment

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy dist/ folder
```

### Backend (Heroku/Railway/PythonAnywhere)
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 📚 Dependencies

### Backend
- FastAPI (Web framework)
- Pandas (Data processing)
- Scikit-learn (ML)
- NumPy (Numerical computing)
- Uvicorn (ASGI server)

### Frontend
- Vue 3 (UI framework)
- Axios (HTTP client)
- Leaflet (Map library)
- Vite (Build tool)

---

## 📝 API Documentation

Setelah backend berjalan, buka **http://localhost:8000/docs** untuk interactive Swagger UI.

---

## 🤝 Kontribusi

1. Fork repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

---

## 📄 License

MIT License - Feel free to use untuk project Anda

---

## 💬 Support

Untuk pertanyaan atau issue, silakan buka GitHub Issues atau hubungi developer.

---

**Happy Coding! 🚀🍽️**
