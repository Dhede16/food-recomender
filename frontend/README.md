# Food Recommender Frontend

Modern Vue 3 frontend untuk sistem rekomendasi makanan berbasis lokasi menggunakan algoritma TOPSIS.

## 🚀 Fitur

- **Input Lokasi Fleksibel**: Manual coordinates atau gunakan GPS device
- **Peta Interaktif**: Visualisasi lokasi user dan rekomendasi tempat makan dengan Leaflet
- **Responsive Design**: Mobile-first design yang berfungsi di semua ukuran layar
- **Ranking TOPSIS**: Rekomendasi diurutkan berdasarkan multi-criteria decision making
- **Detail Modal**: Klik rekomendasi untuk melihhat detail lengkap
- **Google Maps Integration**: Tombol untuk membuka lokasi di Google Maps

## 📋 Requirements

- Node.js 16+ 
- npm atau yarn
- Backend FastAPI berjalan di `http://localhost:8000`

## 🔧 Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Backend URL (Optional)
Edit `src/App.vue` dan ubah `API_BASE` jika backend tidak berjalan di localhost:8000:
```javascript
const API_BASE = 'http://localhost:8000' // Ubah sesuai kebutuhan
```

### 3. Run Development Server
```bash
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

## 📦 Build Production

```bash
npm run build
npm run preview
```

## 🎯 Cara Penggunaan

1. **Buka aplikasi** di `http://localhost:5173`
2. **Masukkan koordinat**:
   - Ketik latitude dan longitude secara manual
   - Atau klik tombol "📡 Gunakan Lokasi Saya" untuk auto-detect
3. **Pilih jumlah rekomendasi** (Top 5-20)
4. **Klik "🔍 Cari Rekomendasi"**
5. **Lihat hasil**:
   - Table dengan rekomendasi terurut
   - Peta dengan sebaran lokasi
   - Klik item untuk detail modal
6. **Buka di Google Maps** dengan tombol "🗺️"

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── App.vue          # Main component (form + results + map)
│   ├── main.js          # Entry point
│   └── components/      # (Untuk komponen terpisah di masa depan)
├── index.html           # HTML template
├── vite.config.js       # Vite configuration dengan proxy API
├── package.json         # Dependencies
└── README.md            # Dokumentasi
```

## 🌐 API Endpoints yang Digunakan

### POST /recommendations
Mendapatkan rekomendasi tempat makan berdasarkan lokasi

**Request:**
```json
{
  "latitude": -0.5022,
  "longitude": 117.1536,
  "top_n": 10
}
```

**Response:**
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
      "jarak": 0.5,
      "rating": 4.5,
      "skor_topsis": 0.856,
      "latitude": -0.5025,
      "longitude": 117.1540
    },
    // ... more recommendations
  ],
  "total_items": 10
}
```

## 🎨 Styling

- **Color Scheme**: Purple gradient (#667eea - #764ba2)
- **Framework**: Pure CSS3 (Scoped Vue styles)
- **Responsive Breakpoints**: 768px, 1024px
- **Card-based design** dengan shadows dan transitions

## 📱 Responsive Behavior

- **Desktop**: Table view untuk rekomendasi
- **Tablet**: Cards grid view (3 kolom)
- **Mobile**: Cards single column

## 🗺️ Map Integration

- **Library**: Leaflet 1.9.4
- **Tile Provider**: OpenStreetMap
- **Marker Types**:
  - Blue circle: Lokasi user
  - Blue dot: Tempat makan
- **Popup**: Hover/click marker untuk melihat detail

## 🐛 Troubleshooting

### Backend tidak terhubung
- Pastikan backend berjalan di port 8000
- Check CORS headers di backend FastAPI
- Verify `API_BASE` URL di App.vue

### Peta tidak muncul
- Check console untuk leaflet error
- Verify internet connection (untuk tile layer)
- Ensure map container (#map-container) ada di DOM

### Geolocation error
- Browser harus HTTPS atau localhost
- User harus approve geolocation permission
- Check browser console untuk error message

## 📚 Dependencies

```json
{
  "vue": "^3.4.0",
  "axios": "^1.6.0",
  "leaflet": "^1.9.4"
}
```

## 🔄 Development Workflow

1. Edit komponen di `src/App.vue`
2. Perubahan auto-reload di development server
3. Check console (F12) untuk errors
4. Test di berbagai ukuran layar

## 📝 Notes

- Koordinat default: Pusat Samarinda (-0.5022, 117.1536)
- TOPSIS weights: Harga 32%, Jarak 43%, Rating 25%
- Distance calculation: Haversine formula
- Timeout untuk API: default axios

## 🤝 Contributing

- Fork repository
- Create feature branch
- Submit pull request

## 📄 License

MIT License
