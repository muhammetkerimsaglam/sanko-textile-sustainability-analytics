import streamlit as st
import pandas as pd
import plotly.express as px

# Sayfa Ayarları
st.set_page_config(page_title="Sanko Sürdürülebilirlik Dashboard", layout="wide")
st.title("🌱 Sanko Tekstil Sürdürülebilirlik & İklim Riski Simülasyonu")
st.markdown("Analist: **Muhammet Kerim Sağlam** | Metodoloji: **GRI & TCFD**")

# Sol Menü (Sidebar) - Senaryo Simülasyonu
st.sidebar.header("🔄 Dinamik Senaryo Testi")
st.sidebar.markdown("Şirketin sürdürülebilirlik hedeflerini simüle edin:")

# Kullanıcının oynayabileceği dinamik butonlar (Slider)
sim_yenilenebilir = st.sidebar.slider("Yenilenebilir Enerji Payı (%)", min_value=24, max_value=100, value=24)
sim_su = st.sidebar.slider("Su Geri Kazanım Oranı (%)", min_value=32, max_value=100, value=32)
sim_karbon_hedef = st.sidebar.slider("Karbon İyileştirme Hedefi (%)", min_value=0, max_value=30, value=5)

# Dinamik Hesaplamalar (Kullanıcı sliderı kaydırdıkça değişecek)
# Yenilenebilir enerji arttıkça ve karbon iyileştikçe SKDM risk skoru düşer
guncel_skdm = max(40, 90 - (sim_yenilenebilir - 24) - sim_karbon_hedef)

# Üst KPI Kartları
st.markdown("### 📊 Anlık Performans Göstergeleri")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Yenilenebilir Enerji (GRI 302)", value=f"% {sim_yenilenebilir}", delta=f"{sim_yenilenebilir - 24}% Artış" if sim_yenilenebilir > 24 else "Mevcut")
with col2:
    st.metric(label="Geri Kazanılan Su (GRI 303)", value=f"% {sim_su}", delta=f"{sim_su - 32}% Artış" if sim_su > 32 else "Mevcut")
with col3:
    st.metric(label="SKDM Risk Skoru (TCFD)", value=f"{guncel_skdm} / 100", delta=f"-{90 - guncel_skdm} Risk Azalışı" if guncel_skdm < 90 else "Kritik Seviye", delta_color="inverse")

st.markdown("---")

# Risk Matrisi Grafiği
st.markdown("### ⚠️ Güncel İklim ve Geçiş Riskleri")
risk_data = pd.DataFrame({
    'Risk Kategorisi': ['Fiziksel', 'Fiziksel', 'Geçiş', 'Geçiş'],
    'Risk Faktörü': ['Su Kıtlığı / Kuraklık', 'Aşırı Sıcaklıklar', 'Sınırda Karbon (SKDM)', 'Müşteri Talebi Kayması'],
    'Risk Skoru': [82, 65, guncel_skdm, 74], # SKDM skoru dinamik oldu!
    'Uyum Stratejisi': [
        f'Su geri kazanımını %{sim_su}\'ye çıkarma.',
        'Isı yalıtımı ve enerji verimli soğutma sistemleri.',
        f'Yenilenebilir payını %{sim_yenilenebilir}\'ye çıkarmak.',
        'Üretimin %100 sertifikalı liflere kaydırılması.'
    ]
})

fig_risk = px.bar(risk_data, x='Risk Faktörü', y='Risk Skoru', color='Risk Kategorisi', text='Risk Skoru',
                  color_discrete_sequence=['#e74c3c', '#3498db'], template='plotly_white')
fig_risk.update_layout(yaxis=dict(range=[0, 100]))
st.plotly_chart(fig_risk, use_container_width=True)

# Bilgi Tablosu
st.table(risk_data[['Risk Faktörü', 'Risk Skoru', 'Uyum Stratejisi']])
