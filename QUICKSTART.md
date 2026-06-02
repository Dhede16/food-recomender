# 🚀 Quick Start Guide

Panduan cepat untuk menjalankan Food Recommender dalam 5 menit.

---

## ⚡ Cara Tercepat (Windows)

### 1. Buka Terminal di Folder Project Root

```powershell
# Di Windows PowerShell
cd C:\Users\NITRO\Desktop\SUPER CODE PROJECT\food-recommender
```

### 2. Jalankan Backend (Terminal 1)

```powershell
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Tunggu sampai muncul:
```
Uvicorn running on http://127.0.0.1:8000
Application startup complete
```

### 3. Jalankan Frontend (Terminal 2)

```powershell
cd frontend
npm install
npm run dev
```

Tunggu sampai muncul:
```
Local:   http://localhost:5173
```

### 4. Buka Browser
Pergi ke: **http://localhost:5173**

---

## ⚡ Cara Tercepat (Mac/Linux)

### 1. Terminal
```bash
cd ~/Desktop/food-recommender  # Adjust path sesuai lokasi Anda

# Terminal 1: Backend
cd backend
pip3 install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

### 2. Buka Browser
```
http://localhost:5173
```

---

## ✅ Cek Apakah Sudah Berjalan

### Backend
- Buka: **http://localhost:8000/health**
- Harus muncul: `{"status":"OK"}`
- Swagger UI: **http://localhost:8000/docs**

### Frontend
- Buka: **http://localhost:5173**
- Harus ada form dengan input latitude/longitude

---

## 🎯 Gunakan Aplikasi

1. **Input Lokasi**:
   - Masukkan latitude: `-0.5022`
   - Masukkan longitude: `117.1536`
   - Atau klik "📡 Gunakan Lokasi Saya"

2. **Cari**:
   - Pilih Top N (misalnya 10)
   - Klik "🔍 Cari Rekomendasi"
   - Tunggu 1-2 detik

3. **Lihat Hasil**:
   - Tabel dengan rekomendasi terurut
   - Peta dengan pin lokasi
   - Klik item untuk detail modal

---

## 🔧 Troubleshooting Cepat

| Problem | Solution |
|---------|----------|
| **"Connection refused"** | Backend belum dijalankan, cek terminal backend |
| **"Cannot find module"** | Jalankan `npm install` di folder frontend |
| **"ModuleNotFoundError"** | Jalankan `pip install -r requirements.txt` di backend |
| **Port 8000 already in use** | `netstat -ano \| findstr :8000` (Windows) atau cek aplikasi lain |
| **Port 5173 already in use** | Ganti port di vite.config.js atau stop aplikasi lain |
| **Peta tidak muncul** | Refresh browser (Ctrl+R), cek internet connection |

---

## 📊 Default Koordinat (Samarinda)

Jika ingin test cepat, gunakan koordinat ini:

```
Latitude:  -0.5022
Longitude: 117.1536
Top N:     10
```

---

## 🌍 Gunakan Lokasi Real Anda

Klik tombol "📡 Gunakan Lokasi Saya" untuk auto-detect:
- Browser akan minta permission
- Approve/Allow untuk geolocation
- Koordinat akan di-fill otomatis

---

## 📱 Test Responsif

Buka DevTools (F12) dan:
- Toggle device toolbar
- Test di mobile, tablet, desktop
- Lihat layout berubah

---

## 🛑 Stop Aplikasi

- Backend: Tekan `Ctrl+C` di terminal 1
- Frontend: Tekan `Ctrl+C` di terminal 2

---

## 📚 Dokumentasi Lengkap

- Backend: Baca `backend/README.md` (jika ada)
- Frontend: Baca `frontend/README.md`
- API: Buka **http://localhost:8000/docs**

---

## 🎉 Selesai!

Aplikasi sudah running dan siap digunakan!

---

**Pertanyaan?** Baca README.md di root folder untuk dokumentasi lengkap.
