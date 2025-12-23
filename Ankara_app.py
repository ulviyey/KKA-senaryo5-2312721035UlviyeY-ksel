import streamlit as st
import googlemaps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import folium

# --- AYARLAR VE SAYFA DÜZENİ ---
st.set_page_config(page_title="Ankara Su Numunesi Rota Optimizasyonu", layout="wide")

st.title("💧 Ankara Çevre Bakanlığı - Su Numunesi Rota Optimizasyonu")
st.markdown("""
**Senaryo 5:** Çevre Bakanlığına ait birimlerin, Ankara'daki **10 farklı göletten** su numunesi toplaması için 
**Karınca Kolonisi Algoritması (ACO)** kullanılarak en kısa rotanın belirlenmesi.
""")

# --- 1. VERİ TANIMLAMA (ANKARA LOKASYONLARI) ---
locations = [
    {"name": "BAKANLIK MERKEZ (Çankaya)", "lat": 39.9055, "lon": 32.8360}, # Başlangıç
    {"name": "Mogan Gölü (Gölbaşı)", "lat": 39.7750, "lon": 32.7850},
    {"name": "Eymir Gölü", "lat": 39.8250, "lon": 32.8100},
    {"name": "Mavi Göl (Bayındır Barajı)", "lat": 39.9250, "lon": 32.9350},
    {"name": "Göksu Parkı Göleti (Eryaman)", "lat": 39.9850, "lon": 32.6500},
    {"name": "Çubuk-1 Barajı", "lat": 40.0200, "lon": 32.9500},
    {"name": "Gençlik Parkı Havuzu (Ulus)", "lat": 39.9380, "lon": 32.8480},
    {"name": "Altınpark Göleti", "lat": 39.9600, "lon": 32.8800},
    {"name": "Harikalar Diyarı (Sincan)", "lat": 39.9950, "lon": 32.5850},
    {"name": "Dikmen Vadisi Havuzu", "lat": 39.8800, "lon": 32.8300},
    {"name": "Kurtboğazı Barajı", "lat": 40.2800, "lon": 32.6800}, 
]

# --- SIDEBAR (PARAMETRELER) ---
st.sidebar.header("⚙️ ACO Parametreleri")

col1, col2 = st.sidebar.columns(2)
with col1:
    ant_count = st.number_input("Karınca Sayısı", min_value=1, value=20)
    iterations = st.number_input("İterasyon Sayısı", min_value=1, value=50)
    alpha = st.slider("Alpha (Feromon)", 0.1, 5.0, 1.0)

with col2:
    beta = st.slider("Beta (Mesafe)", 0.1, 5.0, 2.0)
    evaporation_rate = st.slider("Buharlaşma", 0.0, 1.0, 0.5)

# API Anahtarı Yönetimi
api_key = None
try:
    api_key = st.secrets["general"]["GOOGLE_MAPS_API_KEY"]
    gmaps = googlemaps.Client(key=api_key)
    api_status = "✅ API Anahtarı Yüklendi"
except:
    api_status = "❌ API Anahtarı Bulunamadı"
    st.error("Google Maps API anahtarı bulunamadı. Lütfen .streamlit/secrets.toml dosyasını oluşturun.")

st.sidebar.markdown(f"**Durum:** {api_status}")

# --- 2. FONKSİYONLAR ---

def get_google_distance_matrix(locations, gmaps_client):
    """
    Google Maps Limitini (Max 100 elements) aşmamak için
    verileri satır satır çeker.
    """
    coords = [(loc["lat"], loc["lon"]) for loc in locations]
    size = len(coords)
    matrix = np.zeros((size, size))

    try:
        # Hepsini birden sormak yerine döngüyle TEK TEK soruyoruz.
        # Böylece 11x11=121 yerine 1x11=11'lik paketler halinde gidiyor ve limit aşılmıyor.
        for i in range(size):
            origin = [coords[i]] # Sadece 1 başlangıç noktası
            destinations = coords # Tüm varış noktaları
            
            # API Çağrısı
            result = gmaps_client.distance_matrix(origin, destinations, mode="driving")
            
            if 'rows' in result and len(result['rows']) > 0:
                elements = result['rows'][0]['elements']
                for j, element in enumerate(elements):
                    if element['status'] == 'OK':
                        matrix[i][j] = element['distance']['value']
                    else:
                        matrix[i][j] = 999999 # Yol yoksa veya hata varsa
            else:
                 st.warning(f"{locations[i]['name']} için veri çekilemedi.")
                 
        return matrix
    except Exception as e:
        st.error(f"API Hatası: {e}")
        return None

# --- ACO ALGORİTMASI ---
class AntColonyOptimization:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        np.fill_diagonal(self.distances, np.inf)

    def run(self):
        all_time_shortest_path = ("placeholder", np.inf)
        history = []

        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best)
            shortest_path = min(all_paths, key=lambda x: x[1])
            
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            
            self.pheromone = self.pheromone * self.decay
            history.append(all_time_shortest_path[1])
        return all_time_shortest_path, history

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = [start]
        visited = set(path)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append(move)
            prev = move
            visited.add(move)
        path.append(start)
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        if row.sum() == 0:
            return np.random.choice(list(set(self.all_inds) - visited))
        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move

    def gen_path_dist(self, path):
        total_dist = 0
        for i in range(len(path) - 1):
            total_dist += self.distances[path[i]][path[i+1]]
        return total_dist

    def spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for i in range(len(path) - 1):
                self.pheromone[path[i]][path[i+1]] += 1.0 / self.distances[path[i]][path[i+1]]

# --- 3. UYGULAMA MANTIĞI ---

# Session State (Hafıza)
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False
    st.session_state.best_path = None
    st.session_state.history = None
    st.session_state.total_km = 0

if st.button("🚀 Rotayı Hesapla (Ankara)"):
    if api_key:
        with st.spinner('Ankara numune rotası hesaplanıyor (Google Maps API)...'):
            distance_matrix = get_google_distance_matrix(locations, gmaps)
        
        if distance_matrix is not None:
            # ACO Başlat
            aco = AntColonyOptimization(
                distances=distance_matrix, 
                n_ants=ant_count, 
                n_best=int(ant_count/2), 
                n_iterations=iterations, 
                decay=evaporation_rate, 
                alpha=alpha, 
                beta=beta
            )
            
            best_path, history = aco.run()
            
            st.session_state.calculation_done = True
            st.session_state.best_path = best_path
            st.session_state.history = history
            st.session_state.total_km = best_path[1] / 1000.0
            
            st.success("Hesaplama Tamamlandı!")
    else:
        st.error("API Anahtarı eksik!")

# Sonuçları Göster
if st.session_state.calculation_done:
    path_indices = st.session_state.best_path[0]
    total_km = st.session_state.total_km
    history = st.session_state.history
    
    col_res1, col_res2 = st.columns([1, 2])
    
    with col_res1:
        st.info(f"**Toplam Mesafe:** {total_km:.2f} km")
        st.write("**Uğranacak Numune Noktaları Sırası:**")
        for i, idx in enumerate(path_indices):
            st.write(f"{i+1}. {locations[idx]['name']}")
        
        fig, ax = plt.subplots()
        ax.plot(history)
        ax.set_title("Optimizasyon Grafiği")
        st.pyplot(fig)

    with col_res2:
        m = folium.Map(location=[39.9208, 32.8541], zoom_start=9)
        
        for i, loc in enumerate(locations):
            color = 'red' if i == 0 else 'blue'
            icon = 'home' if i == 0 else 'tint'
            folium.Marker([loc['lat'], loc['lon']], popup=loc['name'], icon=folium.Icon(color=color, icon=icon)).add_to(m)
        
        route_coords = [[locations[i]['lat'], locations[i]['lon']] for i in path_indices]
        folium.PolyLine(route_coords, color="red", weight=4, opacity=0.7).add_to(m)
        
        st_folium(m, width=700, height=500)

if not st.session_state.calculation_done:
    st.info("Ankara'daki göletleri görmek için butona basın.")
    m_start = folium.Map(location=[39.9208, 32.8541], zoom_start=10)
    for loc in locations:
        folium.Marker([loc['lat'], loc['lon']], popup=loc['name']).add_to(m_start)
    st_folium(m_start, width=800, height=400)