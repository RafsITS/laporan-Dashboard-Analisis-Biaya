import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import base64
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Analisis Biaya Kendaraan",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# HELPER FUNCTION
# ==========================================
def get_image_as_base64(image_path):
    """Convert local image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None
# CUSTOM CSS STYLING (HYBRID & THEME AWARE)
# ==========================================
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Global Settings */
    * { font-family: 'Poppins', sans-serif; }

    /* --- CHART CARD CONTAINER (Template Baru) --- */
    .chart-card {
        background-color: var(--secondary-background-color);
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.1);
        overflow: hidden;
    }

    /* Header Chart */
    .chart-header {
        background-color: var(--background-color);
        padding: 15px 20px;
        border-left: 6px solid #667eea;
        border-bottom: 1px solid rgba(128, 128, 128, 0.1);
    }

    .chart-header-title {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-color);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .chart-body {
        padding: 10px;
    }

    /* --- METRIC CARDS --- */
    .metric-card {
        background: linear-gradient(135deg, var(--secondary-background-color) 0%, var(--background-color) 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid rgba(128, 128, 128, 0.1);
    }
    .metric-card:hover { transform: translateY(-5px); }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    
    .metric-label {
        color: var(--text-color);
        font-size: 0.9em;
        text-transform: uppercase;
        font-weight: 600;
        opacity: 0.8;
    }

    /* --- ANIMATIONS --- */
    @keyframes slideInLeft { from { transform: translateX(-100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    @keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    .slide-left { animation: slideInLeft 0.8s ease-out; }
    .slide-right { animation: slideInRight 0.8s ease-out; }
    .fade-up { animation: fadeInUp 0.8s ease-out; }

    /* --- ALERTS & BOXES --- */
    .alert-box {
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        color: white; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .alert-danger { background: linear-gradient(135deg, #ef5350 0%, #e53935 100%); }
    .alert-warning { background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%); }
    .alert-success { background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%); }
    .alert-info { background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%); }

    /* --- INFO BOX --- */
    .info-box {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #764ba2;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* --- VEHICLE CARD --- */
    .vehicle-card {
        background-color: var(--secondary-background-color);
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* --- SIDEBAR DECORATION --- */
    .neon-text {
        font-weight: 700;
        color: var(--text-color); 
        text-shadow: 0 0 5px rgba(102, 126, 234, 0.5);
    }

    /* --- HEADER UTAMA --- */
    .main-header-container {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header-container h1 { color: white !important; }
    .main-header-container p { color: rgba(255,255,255,0.9) !important; }

    /* --- KP IDENTITY --- */
    .kp-container {
        display: flex;
        align-items: center;
        background: var(--secondary-background-color);
        padding: 15px 25px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.2);
        margin-bottom: 25px;
    }
    .kp-names {
        margin-left: 20px;
        border-left: 3px solid #667eea;
        padding-left: 20px;
    }
    .kp-title { font-weight: bold; font-size: 0.9em; opacity: 0.7; letter-spacing: 1px; text-transform: uppercase; }
    .kp-name-text { font-size: 1.1em; font-weight: 600; margin: 2px 0; }

    /* Hide default Streamlit anchors */
    .css-15zrgzn {display: none}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# DATA LOADING & PROCESSING
# ==========================================
@st.cache_data
def load_and_process_data(file_path=None):
    try:
        if file_path is None: file_path = 'Data_Kendaraan_Bersih.csv'
        try: df = pd.read_csv(file_path, sep=';')
        except: 
            try: df = pd.read_csv(file_path, sep=',')
            except: df = pd.read_csv(file_path)

        df.columns = df.columns.str.strip()
        df = df.dropna(subset=['Total Biaya', 'Nopol', 'Bulan', 'Tahun', 'Keterangan'])
        df = df.drop_duplicates(subset=['Tahun','Total Biaya'])
        df['Bulan'] = df['Bulan'].str.strip().str.capitalize()
        df['Keterangan'] = df['Keterangan'].str.strip().str.upper()
        df['Nopol'] = df['Nopol'].str.strip().str.upper()

        if 'Vendor_Clean' in df.columns:
            df['Vendor_Clean'] = df['Vendor_Clean'].fillna(df.get('Vendor', '')).str.strip().str.upper()
        elif 'Vendor' in df.columns:
            df['Vendor_Clean'] = df['Vendor'].str.strip().str.upper()
        else:
            df['Vendor_Clean'] = 'UNKNOWN'

        month_map = {
            'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5, 'Juni': 6,
            'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12, 'Nopember': 11
        }
        df['Bulan'] = df['Bulan'].replace({'Nopember': 'November'})
        df['Month_Num'] = df['Bulan'].map(month_map)
        df = df[df['Total Biaya'] >= 100000]
        df['Tahun'] = df['Tahun'].astype(int)
        
        if 'Type' in df.columns:
            df['Type'] = df.groupby('Nopol')['Type'].transform(lambda x: x.mode()[0] if not x.mode().empty else "UNKNOWN")
        else: df['Type'] = 'UNKNOWN'
            
        return df, None
    except Exception as e: return None, f"Error: {str(e)}"

# ==========================================
# HELPER: RENDER CHART WITH HEADER
# ==========================================
def render_chart_card(title, fig, height=450):
    if fig:
        # Force remove title from Plotly object to avoid duplication/undefined
        fig.update_layout(
            title_text="",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins'),
            margin=dict(l=20, r=20, t=20, b=20),
            height=height,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(128, 128, 128, 0.2)')
        )
        st.markdown(f"""
        <div class="chart-card fade-up">
            <div class="chart-header">
                <h3 class="chart-header-title">{title}</h3>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

# ==========================================
# ANALYSIS & CHART FUNCTIONS
# ==========================================
def calculate_yearly_summary(df):
    summary = df.groupby('Tahun').agg({'Total Biaya': ['sum', 'mean', 'count']}).round(0)
    summary.columns = ['Total_Pengeluaran', 'Rata_Rata', 'Jumlah_Transaksi']
    return summary

def get_top_vendors(df, top_n=10):
    return df.groupby('Vendor_Clean')['Total Biaya'].sum().sort_values(ascending=False).head(top_n)

def get_top_units(df, top_n=10):
    top_units = df.groupby(['Nopol', 'Type']).agg({'Total Biaya': 'sum', 'Bulan': 'count'})
    top_units.columns = ['Total_Biaya', 'Frekuensi_Servis']
    return top_units.sort_values(by='Total_Biaya', ascending=False).head(top_n)

def calculate_monthly_trend(df):
    monthly = df.groupby(['Tahun', 'Month_Num', 'Bulan'])['Total Biaya'].sum().reset_index()
    return monthly.sort_values(['Tahun', 'Month_Num'])

def calculate_category_distribution(df):
    return df.groupby('Keterangan')['Total Biaya'].agg(['sum', 'count']).sort_values('sum', ascending=False)

def calculate_type_statistics(df):
    type_stats = df.groupby('Type').agg({'Total Biaya': ['sum', 'mean', 'count'], 'Nopol': 'nunique'})
    type_stats.columns = ['Total_Biaya', 'Avg_Biaya', 'Transaksi', 'Jumlah_Unit']
    return type_stats.sort_values('Total_Biaya', ascending=False)

def detect_cost_anomalies(df):
    def get_upper_bound(group):
        q1 = group.quantile(0.25); q3 = group.quantile(0.75); iqr = q3 - q1
        return q3 + (1.5 * iqr)
    bounds = df.groupby('Tahun')['Total Biaya'].apply(get_upper_bound).to_dict()
    df['Batas_Wajar'] = df['Tahun'].map(bounds)
    return df[df['Total Biaya'] > df['Batas_Wajar']]

def detect_logic_anomalies(df):
    avg_berat = df[df['Keterangan'].str.contains('BERAT', na=False)]['Total Biaya'].mean()
    benchmark = avg_berat if not np.isnan(avg_berat) else df['Total Biaya'].quantile(0.9)
    return df[(df['Keterangan'].str.contains('RINGAN', na=False)) & (df['Total Biaya'] > benchmark)]

def detect_duplicates(df):
    # Hanya mengecek duplikasi berdasarkan kolom inti
    return df[df.duplicated(subset=['Bulan', 'Tahun', 'Nopol', 'Total Biaya', 'Vendor_Clean'], keep=False)]

# --- Chart Creators ---
def create_yearly_trend_chart(summary_df):
    if summary_df.empty: return None
    fig = go.Figure()
    years = summary_df.index.tolist(); costs = summary_df['Total_Pengeluaran'].tolist()
    fig.add_trace(go.Bar(
        x=years, y=costs,
        marker=dict(color=costs, colorscale='Blues', showscale=False),
        text=[f'Rp {val:,.0f}' for val in costs], textposition='outside',
        hovertemplate='<b>Tahun %{x}</b><br>Total: Rp %{y:,.0f}<extra></extra>'
    ))
    fig.update_layout(title_text="", xaxis_title="Tahun", yaxis_title="Total Pengeluaran (Rp)")
    return fig

def create_vendor_pie_chart(vendor_df):
    if vendor_df.empty: return None
    labels = vendor_df.index[:8].tolist() + ['Others'] if len(vendor_df) > 8 else vendor_df.index.tolist()
    values = vendor_df.values[:8].tolist() + [vendor_df.values[8:].sum()] if len(vendor_df) > 8 else vendor_df.values.tolist()
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set3, line=dict(color='white', width=1)),
        textinfo='percent', hovertemplate='<b>%{label}</b><br>Rp %{value:,.0f}<extra></extra>'
    )])
    fig.update_layout(title_text="", legend=dict(orientation="v", yanchor="middle", y=0.5))
    return fig

def create_timeline_chart(monthly_df):
    if monthly_df.empty: return None
    monthly_df = monthly_df.copy()
    monthly_df['Date'] = pd.to_datetime(monthly_df['Tahun'].astype(str) + '-' + monthly_df['Month_Num'].astype(str) + '-01')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_df['Date'], y=monthly_df['Total Biaya'],
        mode='lines+markers', line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2'), fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)',
        hovertemplate='<b>%{x|%B %Y}</b><br>Rp %{y:,.0f}<extra></extra>'
    ))
    fig.update_layout(title_text="")
    return fig

def create_monthly_heatmap(df):
    pivot = df.pivot_table(values='Total Biaya', index='Bulan', columns='Tahun', aggfunc='sum', fill_value=0)
    order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    pivot = pivot.reindex([m for m in order if m in pivot.index])
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index, colorscale='RdYlGn_r',
        text=[[f'{val/1e6:.1f}jt' if val>0 else '' for val in row] for row in pivot.values],
        texttemplate='%{text}', textfont={"size": 10},
        hovertemplate='<b>%{y} %{x}</b><br>Rp %{z:,.0f}<extra></extra>'
    ))
    fig.update_layout(title_text="")
    return fig

def create_box_plot(df):
    # Set title=None explicit
    fig = px.box(df, x='Tahun', y='Total Biaya', color='Tahun', color_discrete_sequence=px.colors.qualitative.Set2, title=None)
    fig.update_layout(title_text="", showlegend=False)
    return fig

def create_vendor_comparison_chart(vendor_df, top_n=10):
    top = vendor_df.head(top_n)
    fig = go.Figure(data=[go.Bar(
        y=top.index, x=top.values, orientation='h',
        marker=dict(color=top.values, colorscale='Plasma', showscale=False),
        text=[f'Rp {val:,.0f}' for val in top.values], textposition='outside',
        hovertemplate='<b>%{y}</b><br>Rp %{x:,.0f}<extra></extra>'
    )])
    fig.update_layout(title_text="", yaxis=dict(autorange="reversed"))
    return fig

def create_scatter_plot(df):
    stats = df.groupby('Nopol').agg({'Total Biaya': 'sum', 'Bulan': 'count', 'Type': 'first'}).reset_index()
    # Set title=None explicit
    fig = px.scatter(
        stats, x='Bulan', y='Total Biaya', hover_data=['Nopol', 'Type'], color='Type',
        size='Total Biaya', color_discrete_sequence=px.colors.qualitative.Vivid, title=None
    )
    fig.update_layout(title_text="", xaxis_title="Frekuensi Servis", yaxis_title="Total Biaya (Rp)")
    return fig

def create_type_distribution_chart(type_stats):
    if type_stats.empty: return None
    fig = go.Figure(data=[go.Pie(
        labels=type_stats.index,
        values=type_stats['Total_Biaya'],
        hole=0.35,
        marker=dict(colors=px.colors.qualitative.Pastel, line=dict(color='white', width=2)),
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>Rp %{value:,.0f}<extra></extra>'
    )])
    fig.update_layout(title_text="")
    return fig

def create_category_chart(category_df):
    fig = go.Figure(data=[go.Bar(
        y=category_df.index, x=category_df['sum'], orientation='h',
        marker=dict(color=category_df['sum'], colorscale='Viridis', showscale=False),
        text=[f'Rp {val:,.0f}' for val in category_df['sum']], textposition='outside',
        hovertemplate='<b>%{y}</b><br>Rp %{x:,.0f}<extra></extra>'
    )])
    fig.update_layout(title_text="", yaxis=dict(autorange="reversed"))
    return fig

# ==========================================
# MAIN APPLICATION
# ==========================================
def main():
    load_custom_css()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 3em; animation: float 3s ease-in-out infinite;'>🚗</h1>
            <h2 class='neon-text'>Dashboard Analisis</h2>
            <p style='font-size: 0.9em; opacity: 0.8;'>Pemeliharaan Kendaraan </p>
            <p style='font-size: 0.8em; opacity: 1; text-align: justify;'>Badan Pengelolaan Keuangan dan Aset Daerah Kota Surabaya</p>
        </div>
        """, unsafe_allow_html=True)    
        st.markdown("---")

        
        uploaded_file = st.file_uploader("📁 Upload CSV", type=['csv'])
        page = st.radio("Menu Navigasi", ["Dashboard Utama", "Analisis Detail", "Deteksi Anomali", "Laporan Audit"])
        
        if uploaded_file:
            df, error = load_and_process_data(uploaded_file)
        else:
            df, error = load_and_process_data()
            
        if error:
            st.error(error); st.stop()
        if df is None:
            st.warning("⚠️ Data belum dimuat."); st.stop()
            
        st.markdown("---")
        st.subheader("Filter Data")
        years = sorted(df['Tahun'].unique())
        selected_years = st.multiselect("Tahun", years, default=years)
        if selected_years: df = df[df['Tahun'].isin(selected_years)]
            
        vendors = ['Semua'] + sorted(df['Vendor_Clean'].unique().tolist())
        selected_vendor = st.selectbox("Vendor", vendors)
        if selected_vendor != 'Semua': df = df[df['Vendor_Clean'] == selected_vendor]

        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px; text-align: center;'>
            <div style='font-size: 1.5em; font-weight: bold;'>{len(df):,}</div>
            <div style='font-size: 0.8em;'>Total Transaksi</div>
        </div>
        """, unsafe_allow_html=True)

    # --- HALAMAN UTAMA ---
    if page == "Dashboard Utama":
        # IDENTITY SECTION (LOGO & NAMES)
        logo_base64 = get_image_as_base64("bpkad.png")
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="300" alt="Logo Surabaya">' if logo_base64 else '<div style="width: 150px; height: 150px; background: #ccc;"></div>'
        
        st.markdown(f"""
        <div class="kp-container fade-up">
            <div style="flex-shrink: 0;">
                {logo_html}
            </div>
            <div class="kp-names">
                <div class="kp-title">KERJA PRAKTIK - BPKAD KOTA SURABAYA</div>
                <div class="kp-name-text">Rafi Satrio Pratama - 5052231007</div>
                <div class="kp-name-text">Rahardian Putra - 5052231018</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="main-header-container fade-up">
            <h1>🚗 Dashboard Analisis Biaya</h1>
            <p>Monitoring dan Analisis Komprehensif</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Ringkasan Eksekutif")
        c1, c2, c3, c4 = st.columns(4)
        
        metrics = [
            ("💰 Total Pengeluaran", f"{df['Total Biaya'].sum()/1e9:,.1f} M", "Rupiah"),
            ("📈 Rata-rata Biaya", f"{df['Total Biaya'].mean()/1e6:,.1f} Jt", "Per Transaksi"),
            ("📋 Total Transaksi", f"{len(df):,}", "Transaksi"),
            ("🚗 Jumlah Unit", f"{df['Nopol'].nunique()}", "Kendaraan")
        ]
        
        for col, (label, val, sub) in zip([c1, c2, c3, c4], metrics):
            with col:
                st.markdown(f"""
                <div class="metric-card slide-left">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{val}</div>
                    <div style="font-size: 0.8em; opacity: 0.7;">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            summary = calculate_yearly_summary(df)
            render_chart_card("Tren Pengeluaran Tahunan", create_yearly_trend_chart(summary))
        with c2:
            vendors = get_top_vendors(df)
            render_chart_card("Distribusi Vendor Utama", create_vendor_pie_chart(vendors))

        monthly_trend = calculate_monthly_trend(df)
        render_chart_card("Timeline Pengeluaran Bulanan", create_timeline_chart(monthly_trend))
        
        st.markdown("### 🏆 10 Kendaraan Termahal")
        top_units = get_top_units(df, 10)
        
        if not top_units.empty:
            for idx, ((nopol, vtype), row) in enumerate(top_units.iterrows(), 1):
                badge_color = "#ffd700" if idx == 1 else "#c0c0c0" if idx == 2 else "#cd7f32" if idx == 3 else "#667eea"
                st.markdown(f"""
                <div class="vehicle-card slide-right" style="animation-delay: {idx*0.1}s;">
                    <div style="display: flex; align-items: center;">
                        <div style="background: {badge_color}; color: #333; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; margin-right: 15px;">#{idx}</div>
                        <div>
                            <div style="font-weight: 700; font-size: 1.1em; color: var(--text-color);">{nopol}</div>
                            <div style="font-size: 0.85em; opacity: 0.7; color: var(--text-color);">{vtype}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 800; font-size: 1.2em; color: #667eea;">Rp {row['Total_Biaya']:,.0f}</div>
                        <div style="font-size: 0.8em; opacity: 0.7; color: var(--text-color);">{int(row['Frekuensi_Servis'])}x Servis</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- ANALISIS DETAIL ---
    elif page == "Analisis Detail":
        st.markdown("""
        <div class="main-header-container fade-up">
            <h1>📈 Analisis Detail</h1>
            <p>Eksplorasi Data Mendalam</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["📅 ****Temporal****", "🏢 ****Vendor****", "🚗 ****Kendaraan****", "📊 ****Kategori****"])
        
        with tab1:
            render_chart_card("Heatmap Pengeluaran Bulanan", create_monthly_heatmap(df), height=500)
            
            c1, c2 = st.columns(2)
            with c1:
                render_chart_card("Distribusi Biaya per Tahun (Box Plot)", create_box_plot(df))
            with c2:
                monthly_data = calculate_monthly_trend(df)
                if not monthly_data.empty:
                    max_month = monthly_data.loc[monthly_data['Total Biaya'].idxmax()]
                    min_month = monthly_data.loc[monthly_data['Total Biaya'].idxmin()]
                    st.markdown(f"""
                    <div class="info-box fade-up">
                        <h4 style="margin:0; color:var(--text-color);">📊 Insight Temporal</h4>
                        <hr style="margin: 10px 0; opacity: 0.2;">
                        <div style="margin-bottom: 15px;">
                            <div style="font-weight: bold; color: #e74c3c;">🔝 Bulan Termahal</div>
                            <div style="font-size: 1.2em;">{max_month['Bulan']} {int(max_month['Tahun'])}</div>
                            <div style="font-weight: 800;">Rp {max_month['Total Biaya']:,.0f}</div>
                        </div>
                        <div>
                            <div style="font-weight: bold; color: #27ae60;">📉 Bulan Termurah</div>
                            <div style="font-size: 1.2em;">{min_month['Bulan']} {int(min_month['Tahun'])}</div>
                            <div style="font-weight: 800;">Rp {min_month['Total Biaya']:,.0f}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab2:
            c1, c2 = st.columns([2,1])
            with c1:
                render_chart_card("Top 15 Vendor", create_vendor_comparison_chart(get_top_vendors(df, 15), 15), height=600)
            with c2:
                st.markdown('<div class="info-box"><h4>🏆 Top 5 Vendor Detail</h4>', unsafe_allow_html=True)
                vendors = get_top_vendors(df, 5)
                for idx, (v, c) in enumerate(vendors.items(), 1):
                    pct = (c / df['Total Biaya'].sum()) * 100
                    st.markdown(f"**{idx}. {v[:20]}...**")
                    st.progress(pct/100)
                    st.caption(f"Rp {c:,.0f} ({pct:.1f}%)")
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            c1, c2 = st.columns([2,1])
            with c1:
                render_chart_card("Korelasi Frekuensi vs Biaya", create_scatter_plot(df))
            with c2:
                render_chart_card("Proporsi Tipe", create_type_distribution_chart(calculate_type_statistics(df).head(10)))
            
            st.markdown("### 📋 Tabel Efisiensi")
            eff = df.groupby(['Nopol', 'Type']).agg({'Total Biaya': ['sum', 'mean', 'count']})
            eff.columns = ['Total', 'Rata-rata', 'Frekuensi']
            st.dataframe(eff.sort_values('Total', ascending=False).style.format({'Total':'Rp {:,.0f}', 'Rata-rata':'Rp {:,.0f}'}), use_container_width=True)

        with tab4:
            cat_dist = calculate_category_distribution(df)
            render_chart_card("Biaya per Kategori Kerusakan", create_category_chart(cat_dist))

    # --- DETEKSI ANOMALI ---
    elif page == "Deteksi Anomali":
        st.markdown("""
        <div class="main-header-container fade-up">
            <h1>🔍 Deteksi Anomali</h1>
            <p>Identifikasi Transaksi Mencurigakan</p>
        </div>
        """, unsafe_allow_html=True)
        
        cost_anom = detect_cost_anomalies(df)
        logic_anom = detect_logic_anomalies(df)
        dups = detect_duplicates(df)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="alert-box alert-danger slide-left">
                <h3 style="margin:0">⚠️ {len(cost_anom)}</h3>
                <p style="margin:0">Biaya Ekstrim</p>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="alert-box alert-warning slide-left" style="animation-delay: 0.1s">
                <h3 style="margin:0">🤔 {len(logic_anom)}</h3>
                <p style="margin:0">Logika Kategori</p>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="alert-box alert-info slide-left" style="animation-delay: 0.2s">
                <h3 style="margin:0">📋 {len(dups)}</h3>
                <p style="margin:0">Duplikasi</p>
            </div>
            """, unsafe_allow_html=True)

        t1, t2, t3 = st.tabs([" ****Biaya Ekstrim****", "****Logika Kategori****", "****Duplikasi****"])
        
        with t1:
            if not cost_anom.empty:
                fig = px.scatter(cost_anom, x='Tahun', y='Total Biaya', color='Keterangan', size='Total Biaya', hover_data=['Nopol', 'Vendor_Clean'], title=None)
                fig.add_hline(
                    y=cost_anom['Batas_Wajar'].mean(), 
                    line_dash="dash", 
                    line_color="red",
                    annotation_text="Batas Wajar Rata-rata",
                    annotation_position="top right"
                )
                render_chart_card("Scatter Plot Anomali", fig)
                # UPDATE: SORT BY TOTAL BIAYA DESCENDING
                st.markdown("#### Tabel Anomali Biaya Ekstrim")
                st.dataframe(cost_anom.sort_values(by='Total Biaya', ascending=False)[['Tahun', 'Bulan', 'Type', 'Nopol', 'Total Biaya', 'Batas_Wajar', 'Keterangan']].style.format({'Total Biaya': 'Rp {:,.0f}', 'Batas_Wajar': 'Rp {:,.0f}'}), use_container_width=True)
            else:
                st.success("Tidak ada anomali biaya.")
            
        with t2:
            if not logic_anom.empty:
                st.warning(f"Ditemukan {len(logic_anom)} transaksi 'RINGAN' tapi biayanya tinggi.")
                # UPDATE: SORT BY TOTAL BIAYA DESCENDING
                st.dataframe(logic_anom.sort_values(by='Total Biaya', ascending=False)[['Tahun','Type','Nopol', 'Total Biaya', 'Keterangan']].style.format({'Total Biaya': 'Rp {:,.0f}'}), use_container_width=True)
            else: st.success("Logika kategori konsisten.")
            
        with t3:
            if not dups.empty:
                cols_to_show = ['Tahun', 'Bulan', 'Nopol', 'Vendor_Clean', 'Total Biaya', 'Keterangan']
                cols = [c for c in cols_to_show if c in dups.columns]
                # UPDATE: SORT BY TOTAL BIAYA DESCENDING
                st.dataframe(dups.sort_values(by='Total Biaya', ascending=False)[cols].style.format({'Total Biaya': 'Rp {:,.0f}'}), use_container_width=True)
            else: st.success("Data bersih dari duplikasi.")

    # --- LAPORAN AUDIT ---
    elif page == "Laporan Audit":
        st.markdown("""
        <div class="main-header-container fade-up">
            <h1>📋 Laporan Audit</h1>
            <p>Ringkasan Eksekutif & Rekomendasi</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="info-box"><h4>📊 Statistik Utama</h4>', unsafe_allow_html=True)
            st.markdown(f"""
            <ul style="line-height: 2;">
                <li><b>Total Pengeluaran:</b> Rp {df['Total Biaya'].sum():,.0f}</li>
                <li><b>Total Transaksi:</b> {len(df):,}</li>
                <li><b>Rata-rata per Unit:</b> Rp {df.groupby('Nopol')['Total Biaya'].sum().mean():,.0f}</li>
                <li><b>Vendor Terbesar:</b> {get_top_vendors(df,1).index[0]}</li>
            </ul>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="info-box" style="border-left-color: #f39c12;"><h4>💡 Rekomendasi Tindakan</h4>', unsafe_allow_html=True)
            recs = [
                ("⚠️", "Review Anomali", f"Periksa {len(detect_cost_anomalies(df))} transaksi ekstrim."),
                ("🏢", "Negosiasi Vendor", "Top 3 Vendor menguasai >50% biaya."),
                ("🚗", "Peremajaan", "Evaluasi unit dengan biaya maintenance > nilai buku.")
            ]
            for icon, title, desc in recs:
                st.markdown(f"""
                <div style="display:flex; align-items:center; margin-bottom:10px;">
                    <div style="font-size:1.5em; margin-right:10px;">{icon}</div>
                    <div><b>{title}:</b> {desc}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("📥 Download Laporan Excel", use_container_width=True):
            output = 'Laporan_Audit.xlsx'
            with pd.ExcelWriter(output) as writer:
                calculate_yearly_summary(df).to_excel(writer, sheet_name='Ringkasan')
                get_top_vendors(df, 20).to_excel(writer, sheet_name='Vendor')
                detect_cost_anomalies(df).to_excel(writer, sheet_name='Anomali', index=False)
            with open(output, 'rb') as f:
                st.download_button("Download File", f, file_name="Audit.xlsx")

if __name__ == "__main__":
    main()
