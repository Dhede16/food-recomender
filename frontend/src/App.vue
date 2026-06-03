<template>
  <div class="app">
    <!-- Header -->
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">🍽️</span>
          <div>
            <h1>Food Recommender</h1>
            <p>Rekomendasi Makanan Berdasarkan Lokasi & TOPSIS</p>
          </div>
        </div>
      </div>
    </header>

    <main class="main">
      <!-- Form Card -->
      <div class="form-card">
        <div class="form-title">
          <span class="form-icon">📍</span>
          <h2>Rekomendasi Tempat Makan</h2>
        </div>
        <p class="form-subtitle" v-if="!locationReady">Mendapatkan lokasi Anda secara otomatis...</p>
        <p class="form-subtitle" v-else>📍 Lokasi Anda: {{ form.latitude.toFixed(4) }}, {{ form.longitude.toFixed(4) }}</p>

        <div class="form-grid">
          <!-- Category Selection -->
          <div class="field">
            <label>🍽️ Pilih Kategori</label>
            <select v-model="selectedCategory" class="form-input">
              <option value="">Semua Kategori</option>
              <option v-for="cat in availableCategories" :key="cat" :value="cat">
                {{ cat }}
              </option>
            </select>
          </div>

          <!-- Top N -->
          <div class="field">
            <label>🔢 Jumlah Rekomendasi</label>
            <select v-model.number="form.top_n" class="form-input">
              <option value="5">Top 5</option>
              <option value="10">Top 10</option>
              <option value="15">Top 15</option>
              <option value="20">Top 20</option>
            </select>
          </div>
        </div>

        <button class="btn-submit" :disabled="loading || !locationReady" @click="getRecommendation">
          <span v-if="loading" class="spinner"></span>
          <span v-else>🔍 Cari Rekomendasi</span>
        </button>
      </div>

      <!-- Error Alert -->
      <div v-if="error" class="alert-error">
        ⚠️ {{ error }}
      </div>

      <!-- Results -->
      <div v-if="result && result.recommendations.length > 0" class="results">

        <!-- Info -->
        <div class="info-bar">
          <span>📍 Lokasi Kamu: {{ result.user_location.latitude.toFixed(4) }}, {{ result.user_location.longitude.toFixed(4) }}</span>
          <span>📊 Total Rekomendasi: {{ result.total_items }}</span>
        </div>

        <!-- TOPSIS Result -->
        <div class="section-card">
          <div class="section-header">
            <span class="tag tag-blue">📊 TOPSIS Ranking</span>
            <h3>Rekomendasi Terbaik</h3>
          </div>
          <p class="section-sub">
            Diurutkan berdasarkan skor TOPSIS (kombinasi harga, rating, dan jarak)
          </p>

          <!-- Cards View (Mobile) -->
          <div class="cards-view">
            <div 
              v-for="r in result.recommendations" 
              :key="r.rank"
              :class="['card-item', r.rank === 1 ? 'card-top' : '']"
              @click="selectItem(r)"
            >
              <div class="card-header">
                <span class="rank-badge">
                  {{ r.rank === 1 ? '🥇' : r.rank === 2 ? '🥈' : r.rank === 3 ? '🥉' : '#' + r.rank }}
                </span>
                <h4>{{ r.nama }}</h4>
              </div>
              <div class="card-category">{{ r.kategori }}</div>
              <div class="card-stats">
                <div class="stat">
                  <span class="stat-icon">💰</span>
                  <span>Rp {{ formatRupiah(r.harga) }}</span>
                </div>
                <div class="stat">
                  <span class="stat-icon">⭐</span>
                  <span>{{ r.rating }}</span>
                </div>
                <div class="stat">
                  <span class="stat-icon">📍</span>
                  <span>{{ r.jarak.toFixed(2) }} km</span>
                </div>
              </div>
              <div class="card-score">
                <div class="score-bar">
                  <div class="score-fill" :style="{ width: (r.skor_topsis * 100) + '%' }"></div>
                </div>
                <span class="score-text">Skor: {{ (r.skor_topsis * 100).toFixed(1) }}%</span>
              </div>
              <button class="btn-map" @click.stop="openGoogleMaps(r)">🗺️ Lihat di Maps</button>
            </div>
          </div>

          <!-- Table View (Desktop) -->
          <div class="table-wrap">
            <table class="reko-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Nama</th>
                  <th>Kategori</th>
                  <th>Harga</th>
                  <th>Rating</th>
                  <th>Jarak</th>
                  <th>Skor TOPSIS</th>
                  <th>Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="r in result.recommendations" 
                  :key="r.rank"
                  :class="['row-item', r.rank === 1 ? 'row-top' : '']"
                  @click="selectItem(r)"
                >
                  <td>
                    <span class="rank-badge">
                      {{ r.rank === 1 ? '🥇' : r.rank === 2 ? '🥈' : r.rank === 3 ? '🥉' : '#' + r.rank }}
                    </span>
                  </td>
                  <td><strong>{{ r.nama }}</strong></td>
                  <td>{{ r.kategori }}</td>
                  <td class="harga-cell">Rp {{ formatRupiah(r.harga) }}</td>
                  <td><span class="rating-pill">⭐ {{ r.rating }}</span></td>
                  <td><span class="jarak-pill">📍 {{ r.jarak.toFixed(2) }} km</span></td>
                  <td>
                    <div class="score-bar-wrap">
                      <div class="score-bar" :style="{ width: (r.skor_topsis * 100) + '%' }"></div>
                      <span>{{ (r.skor_topsis * 100).toFixed(1) }}%</span>
                    </div>
                  </td>
                  <td>
                    <button class="btn-map" @click.stop="openGoogleMaps(r)">🗺️</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Map -->
        <div class="section-card" v-if="result.recommendations.length > 0">
          <div class="section-header">
            <span class="tag tag-orange">🗺️ Peta Lokasi</span>
            <h3>Sebaran Tempat Makan</h3>
          </div>
          <div id="map-container" class="map-box"></div>
        </div>

      </div>

      <!-- Empty State -->
      <div v-if="result && result.recommendations.length === 0" class="empty-state">
        <div class="empty-icon">😔</div>
        <h3>Tidak Ada Rekomendasi</h3>
        <p>Coba ubah lokasi atau jumlah rekomendasi yang diminta</p>
      </div>

      <!-- Method Info -->
      <div class="info-section">
        <div class="info-card">
          <div class="info-icon">📊</div>
          <h4>TOPSIS MCDM</h4>
          <p>Memberikan ranking optimal berdasarkan 3 kriteria: Harga, Jarak, dan Rating menggunakan metode TOPSIS.</p>
        </div>
        <div class="info-card">
          <div class="info-icon">🧮</div>
          <h4>Bobot Kriteria</h4>
          <p>Harga: 32%, Jarak: 43%, Rating: 25% (optimal dari analisis data).</p>
        </div>
        <div class="info-card">
          <div class="info-icon">📍</div>
          <h4>Berbasis Lokasi</h4>
          <p>Sistem rekomendasi berdasarkan jarak Haversine dari lokasi pengguna ke setiap tempat makan.</p>
        </div>
      </div>
    </main>

    <!-- Detail Modal -->
    <div v-if="selectedItem" class="modal-overlay" @click.self="selectedItem = null">
      <div class="modal">
        <button class="modal-close" @click="selectedItem = null">✕</button>
        <div class="modal-rank">
          {{ selectedItem.rank === 1 ? '🥇' : selectedItem.rank === 2 ? '🥈' : selectedItem.rank === 3 ? '🥉' : '#' + selectedItem.rank }}
        </div>
        <h3>{{ selectedItem.nama }}</h3>
        <span class="modal-category">{{ selectedItem.kategori }}</span>

        <div class="modal-grid">
          <div class="modal-stat">
            <span class="mstat-icon">💰</span>
            <span class="mstat-label">Harga</span>
            <span class="mstat-val">Rp {{ formatRupiah(selectedItem.harga) }}</span>
          </div>
          <div class="modal-stat">
            <span class="mstat-icon">⭐</span>
            <span class="mstat-label">Rating</span>
            <span class="mstat-val">{{ selectedItem.rating }}</span>
          </div>
          <div class="modal-stat">
            <span class="mstat-icon">📍</span>
            <span class="mstat-label">Jarak</span>
            <span class="mstat-val">{{ selectedItem.jarak.toFixed(2) }} km</span>
          </div>
          <div class="modal-stat">
            <span class="mstat-icon">📊</span>
            <span class="mstat-label">Skor TOPSIS</span>
            <span class="mstat-val">{{ (selectedItem.skor_topsis * 100).toFixed(1) }}%</span>
          </div>
        </div>

        <div class="modal-coords">
          <p><strong>Koordinat:</strong></p>
          <p>Lat: {{ selectedItem.latitude.toFixed(4) }}</p>
          <p>Lon: {{ selectedItem.longitude.toFixed(4) }}</p>
        </div>

        <div class="modal-actions">
          <button class="btn-gmaps" @click="openGoogleMaps(selectedItem)">
            🗺️ Buka di Google Maps
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Configure API endpoint - adjust based on your backend location
const API_BASE = 'http://localhost:8000'

export default {
  name: 'App',
  data() {
    return {
      form: {
        latitude: -0.5022,  // Samarinda center
        longitude: 117.1536,
        top_n: 10,
      },
      loading: false,
      error: null,
      result: null,
      selectedItem: null,
      map: null,
      locationReady: false,
      selectedCategory: '',
      availableCategories: [],
      allRecommendations: [],
    }
  },
  methods: {
    formatRupiah(value) {
      return parseInt(value).toLocaleString('id-ID')
    },
    
    getLocation() {
      if (!navigator.geolocation) {
        this.error = 'Geolocation tidak tersedia di browser Anda'
        return
      }
      
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          this.form.latitude = parseFloat(pos.coords.latitude.toFixed(4))
          this.form.longitude = parseFloat(pos.coords.longitude.toFixed(4))
          this.locationReady = true
          this.error = null
        },
        (err) => {
          this.error = 'Gagal mendapatkan lokasi. Menggunakan lokasi default.'
          this.locationReady = true
        }
      )
    },

    async getRecommendation() {
      this.loading = true
      this.error = null
      this.result = null
      this.allRecommendations = []

      try {
        const response = await axios.post(`${API_BASE}/recommendations`, {
          latitude: parseFloat(this.form.latitude),
          longitude: parseFloat(this.form.longitude),
          top_n: parseInt(this.form.top_n) + 10, // Fetch extra to account for filtering
        })

        this.allRecommendations = response.data.recommendations

        // Extract unique categories
        const categories = [...new Set(response.data.recommendations.map(r => r.kategori))].sort()
        this.availableCategories = categories

        // Filter by selected category if any
        const filtered = this.selectedCategory 
          ? response.data.recommendations.filter(r => r.kategori === this.selectedCategory)
          : response.data.recommendations

        // Re-rank after filtering
        const reranked = filtered
          .slice(0, parseInt(this.form.top_n))
          .map((item, idx) => ({
            ...item,
            rank: idx + 1
          }))

        this.result = {
          user_location: response.data.user_location,
          recommendations: reranked,
          total_items: reranked.length
        }
        
        // Initialize map after data is loaded
        this.$nextTick(() => {
          this.initMap()
        })
      } catch (err) {
        if (err.response) {
          this.error = `Error: ${err.response.data.detail || err.message}`
        } else if (err.request) {
          this.error = 'Gagal terhubung ke server. Pastikan backend berjalan di ' + API_BASE
        } else {
          this.error = err.message
        }
      } finally {
        this.loading = false
      }
    },

    initMap() {
      // Remove existing map
      if (this.map) {
        this.map.remove()
        this.map = null
      }

      const mapContainer = document.getElementById('map-container')
      if (!mapContainer || !this.result || !this.result.recommendations.length) {
        return
      }

      const userLat = this.result.user_location.latitude
      const userLon = this.result.user_location.longitude

      // Create map centered on user location
      this.map = L.map(mapContainer).setView([userLat, userLon], 14)

      // Add tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(this.map)

      // Add user location marker
      L.circleMarker([userLat, userLon], {
        radius: 12,
        color: '#6366f1',
        fillColor: '#6366f1',
        fillOpacity: 0.9,
        weight: 3,
        className: 'user-marker'
      }).addTo(this.map).bindPopup('<b>📍 Lokasi Kamu</b>', { closeButton: false })

      // Add recommendation markers
      const bounds = L.latLngBounds([[userLat, userLon]])

      this.result.recommendations.forEach((rec) => {
        const marker = L.circleMarker([rec.latitude, rec.longitude], {
          radius: 8,
          color: '#3b82f6',
          fillColor: '#3b82f6',
          fillOpacity: 0.7,
          weight: 2,
        }).addTo(this.map)

        const popupContent = `
          <div style="font-family:sans-serif;font-size:12px;min-width:160px">
            <div style="font-weight:bold;margin-bottom:4px">${rec.rank}. ${rec.nama}</div>
            <div style="font-size:11px;color:#666;margin-bottom:4px">${rec.kategori}</div>
            <div style="font-size:11px">
              💰 Rp ${this.formatRupiah(rec.harga)}<br>
              ⭐ ${rec.rating}<br>
              📍 ${rec.jarak.toFixed(2)} km<br>
              📊 Skor: ${(rec.skor_topsis * 100).toFixed(1)}%
            </div>
          </div>
        `
        marker.bindPopup(popupContent)

        bounds.extend([rec.latitude, rec.longitude])
      })

      // Fit bounds to show all markers
      if (bounds.isValid()) {
        this.map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 })
      }
    },

    selectItem(item) {
      this.selectedItem = item
    },

    openGoogleMaps(item) {
      const url = `https://www.google.com/maps?q=${item.latitude},${item.longitude}`
      window.open(url, '_blank')
    },
  },

  watch: {
    selectedCategory() {
      // Re-render when category changes
      if (this.allRecommendations.length > 0) {
        const filtered = this.selectedCategory 
          ? this.allRecommendations.filter(r => r.kategori === this.selectedCategory)
          : this.allRecommendations

        const reranked = filtered
          .slice(0, parseInt(this.form.top_n))
          .map((item, idx) => ({
            ...item,
            rank: idx + 1
          }))

        this.result = {
          user_location: this.result.user_location,
          recommendations: reranked,
          total_items: reranked.length
        }

        this.$nextTick(() => {
          this.initMap()
        })
      }
    }
  },

  mounted() {
    // Auto-get location on mount
    this.getLocation()
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body, #app {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  color: #1e293b;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ── Header ─────────────────────────── */
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px 0;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
  color: white;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-icon {
  font-size: 48px;
}

.logo h1 {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
}

.logo p {
  font-size: 14px;
  opacity: 0.9;
  margin-top: 4px;
}

/* ── Main layout ─────────────────────── */
.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px 60px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── Form Card ───────────────────────── */
.form-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.form-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.form-icon {
  font-size: 28px;
}

.form-title h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.form-subtitle {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 28px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  padding: 12px 14px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s;
  background: #f8fafc;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input option {
  padding: 8px;
}

.btn-auto-location {
  padding: 12px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-auto-location:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-auto-location:active {
  transform: translateY(0);
}

.btn-submit {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Alert ─────────────────────────── */
.alert-error {
  background: #fee2e2;
  border-left: 4px solid #dc2626;
  color: #991b1b;
  padding: 14px 16px;
  border-radius: 8px;
  font-size: 14px;
}

/* ── Results ─────────────────────────── */
.results {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 20px;
  border-radius: 10px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  font-size: 14px;
  font-weight: 600;
}

.section-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.section-header h3 {
  font-size: 20px;
  font-weight: 700;
}

.section-sub {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 20px;
}

.tag {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}

.tag-blue {
  background: #dbeafe;
  color: #1e40af;
}

.tag-orange {
  background: #ffedd5;
  color: #9a3412;
}

/* ── Cards View ─────────────────────── */
.cards-view {
  display: none;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

@media (max-width: 1024px) {
  .cards-view {
    display: grid;
  }
  .table-wrap {
    display: none;
  }
}

.card-item {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.card-item:hover {
  border-color: #667eea;
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

.card-item.card-top {
  background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
  border-color: #fcd34d;
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.rank-badge {
  font-size: 24px;
  flex-shrink: 0;
}

.card-header h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.card-category {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 12px;
}

.card-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.stat {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.stat-icon {
  font-size: 16px;
}

.card-score {
  margin-bottom: 12px;
}

.score-bar {
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 4px;
}

.score-fill {
  height: 100%;
  background: linear-gradient(to right, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.4s ease;
}

.score-text {
  font-size: 12px;
  font-weight: 600;
  color: #667eea;
}

.btn-map {
  width: 100%;
  padding: 10px;
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-map:hover {
  background: #667eea;
  color: white;
}

/* ── Table View ─────────────────────── */
.table-wrap {
  overflow-x: auto;
  margin-top: 20px;
}

.reko-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.reko-table thead {
  background: #f8fafc;
}

.reko-table th {
  padding: 12px 14px;
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #e2e8f0;
  white-space: nowrap;
}

.reko-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.2s;
  cursor: pointer;
}

.reko-table tbody tr:hover {
  background: #f8fafc;
}

.row-top {
  background: #fefce8 !important;
}

.reko-table td {
  padding: 12px 14px;
  vertical-align: middle;
}

.harga-cell {
  font-weight: 700;
  color: #059669;
}

.rating-pill {
  background: #fffbeb;
  color: #92400e;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.jarak-pill {
  background: #f0f9ff;
  color: #0369a1;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.score-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-bar-wrap .score-bar {
  flex: 1;
  min-width: 80px;
}

.score-bar-wrap span {
  font-size: 12px;
  font-weight: 700;
  color: #667eea;
  white-space: nowrap;
}

/* ── Map ─────────────────────────── */
.map-box {
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #e2e8f0;
  margin-bottom: 16px;
  z-index: 10;
}

.map-box :deep(.leaflet-container) {
  background: #e5e7eb;
}

/* ── Empty State ─────────────────────────── */
.empty-state {
  background: white;
  border-radius: 16px;
  padding: 60px 20px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #1e293b;
}

.empty-state p {
  color: #64748b;
  font-size: 14px;
}

/* ── Info Section ─────────────────────────── */
.info-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .info-section {
    grid-template-columns: 1fr;
  }
}

.info-card {
  background: white;
  border-radius: 14px;
  padding: 28px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.2s;
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.info-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.info-card h4 {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #1e293b;
}

.info-card p {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
}

/* ── Modal ─────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 32px;
  max-width: 450px;
  width: 100%;
  position: relative;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: #f1f5f9;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  font-weight: 700;
  color: #64748b;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.modal-rank {
  font-size: 52px;
  margin-bottom: 16px;
}

.modal h3 {
  font-size: 22px;
  font-weight: 800;
  margin-bottom: 8px;
  color: #1e293b;
}

.modal-category {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 20px;
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin: 24px 0;
}

.modal-stat {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.mstat-icon {
  font-size: 28px;
}

.mstat-label {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.mstat-val {
  font-size: 16px;
  font-weight: 800;
  color: #1e293b;
}

.modal-coords {
  background: #f8fafc;
  border-radius: 12px;
  padding: 14px;
  margin: 16px 0;
  font-size: 12px;
  color: #64748b;
  text-align: left;
}

.modal-coords p {
  margin: 4px 0;
  font-family: 'Courier New', monospace;
}

.modal-actions {
  margin-top: 16px;
}

.btn-gmaps {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-gmaps:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

/* ── Responsive ─────────────────────────── */
@media (max-width: 768px) {
  .header-inner {
    padding: 0 16px;
  }

  .logo h1 {
    font-size: 24px;
  }

  .logo p {
    font-size: 12px;
  }

  .main {
    padding: 20px 16px 40px;
  }

  .form-card {
    padding: 20px;
  }

  .form-title h2 {
    font-size: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .section-card {
    padding: 20px;
  }

  .section-header h3 {
    font-size: 18px;
  }

  .modal {
    padding: 24px;
  }

  .info-section {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .info-card {
    padding: 20px;
  }
}
</style>
