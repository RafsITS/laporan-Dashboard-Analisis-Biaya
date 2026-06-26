import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import io

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

# ==========================================
# CUSTOM CSS STYLING (LIGHT / DARK / AUTO)
# ==========================================
def get_theme_tokens(theme_mode="Ikuti Tema Pengguna"):
    """Return CSS tokens and Plotly template based on selected theme mode."""
    themes = {
        "Gelap": {
            "app_bg": "#0b1020",
            "app_bg_2": "#111827",
            "card_bg": "#111827",
            "card_bg_2": "#151f32",
            "sidebar_bg": "#0f172a",
            "text_main": "#f8fafc",
            "text_muted": "#cbd5e1",
            "text_soft": "#94a3b8",
            "border": "rgba(148, 163, 184, 0.22)",
            "shadow": "0 12px 30px rgba(0,0,0,0.35)",
            "header_start": "#312e81",
            "header_mid": "#6d28d9",
            "header_end": "#0e7490",
            "accent_1": "#818cf8",
            "accent_2": "#a78bfa",
            "accent_3": "#22d3ee",
            "plotly_template": "plotly_dark",
            "plot_grid": "rgba(148, 163, 184, 0.16)",
            "plot_text": "#f8fafc",
        },
        "Terang": {
            "app_bg": "#f8fafc",
            "app_bg_2": "#eef2ff",
            "card_bg": "#ffffff",
            "card_bg_2": "#f8fafc",
            "sidebar_bg": "#eef2ff",
            "text_main": "#0f172a",
            "text_muted": "#334155",
            "text_soft": "#64748b",
            "border": "rgba(15, 23, 42, 0.12)",
            "shadow": "0 12px 28px rgba(15,23,42,0.09)",
            "header_start": "#667eea",
            "header_mid": "#764ba2",
            "header_end": "#0ea5e9",
            "accent_1": "#4f46e5",
            "accent_2": "#7c3aed",
            "accent_3": "#0891b2",
            "plotly_template": "plotly_white",
            "plot_grid": "rgba(15, 23, 42, 0.12)",
            "plot_text": "#0f172a",
        },
    }

    # "Ikuti Tema Pengguna" dibuat default gelap di Python supaya chart tidak bentrok.
    # Warna CSS tetap bisa mengikuti preferensi browser melalui media query di bawah.
    return themes.get(theme_mode, themes["Gelap"])


def load_custom_css(theme_mode="Ikuti Tema Pengguna"):
    tokens = get_theme_tokens(theme_mode)
    auto_css = """
    @media (prefers-color-scheme: light) {
        :root {
            --app-bg: #f8fafc;
            --app-bg-2: #eef2ff;
            --card-bg: #ffffff;
            --card-bg-2: #f8fafc;
            --sidebar-bg: #eef2ff;
            --text-main: #0f172a;
            --text-muted: #334155;
            --text-soft: #64748b;
            --border-theme: rgba(15, 23, 42, 0.12);
            --shadow-theme: 0 12px 28px rgba(15,23,42,0.09);
            --accent-1: #4f46e5;
            --accent-2: #7c3aed;
            --accent-3: #0891b2;
            --header-start: #667eea;
            --header-mid: #764ba2;
            --header-end: #0ea5e9;
        }
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --app-bg: #0b1020;
            --app-bg-2: #111827;
            --card-bg: #111827;
            --card-bg-2: #151f32;
            --sidebar-bg: #0f172a;
            --text-main: #f8fafc;
            --text-muted: #cbd5e1;
            --text-soft: #94a3b8;
            --border-theme: rgba(148, 163, 184, 0.22);
            --shadow-theme: 0 12px 30px rgba(0,0,0,0.35);
            --accent-1: #818cf8;
            --accent-2: #a78bfa;
            --accent-3: #22d3ee;
            --header-start: #312e81;
            --header-mid: #6d28d9;
            --header-end: #0e7490;
        }
    }
    """ if theme_mode == "Ikuti Tema Pengguna" else """
    :root {
        --app-bg: %(app_bg)s;
        --app-bg-2: %(app_bg_2)s;
        --card-bg: %(card_bg)s;
        --card-bg-2: %(card_bg_2)s;
        --sidebar-bg: %(sidebar_bg)s;
        --text-main: %(text_main)s;
        --text-muted: %(text_muted)s;
        --text-soft: %(text_soft)s;
        --border-theme: %(border)s;
        --shadow-theme: %(shadow)s;
        --accent-1: %(accent_1)s;
        --accent-2: %(accent_2)s;
        --accent-3: %(accent_3)s;
        --header-start: %(header_start)s;
        --header-mid: %(header_mid)s;
        --header-end: %(header_end)s;
    }
    """ % tokens

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

    {auto_css}

    * {{ font-family: 'Poppins', sans-serif; }}

    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background: radial-gradient(circle at top left, color-mix(in srgb, var(--accent-1) 16%, transparent), transparent 30%),
                    radial-gradient(circle at top right, color-mix(in srgb, var(--accent-3) 10%, transparent), transparent 28%),
                    var(--app-bg) !important;
        color: var(--text-main) !important;
    }}

    [data-testid="stHeader"] {{
        background: color-mix(in srgb, var(--app-bg) 78%, transparent) !important;
        backdrop-filter: blur(12px);
    }}

    [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        background: transparent !important;
    }}

    .block-container {{
        padding-top: 2rem;
        color: var(--text-main) !important;
    }}

    p, li, span, label, div, h1, h2, h3, h4, h5, h6 {{
        color: inherit;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--sidebar-bg) 0%, var(--card-bg) 100%) !important;
        border-right: 1px solid var(--border-theme);
    }}

    [data-testid="stSidebar"] .block-container {{ padding-bottom: 100px; }}
    [data-testid="stSidebar"] * {{ color: var(--text-main) !important; }}
    [data-testid="stSidebar"] hr {{ border-color: var(--border-theme) !important; }}

    /* Input controls */
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div,
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {{
        background-color: var(--card-bg) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border-theme) !important;
        border-radius: 10px !important;
    }}

    .stRadio label, .stCheckbox label, .stFileUploader label {{ color: var(--text-main) !important; }}

    /* KP identity header */
    .kp-header-container {{
        background: linear-gradient(135deg, var(--card-bg) 0%, var(--card-bg-2) 100%);
        border-radius: 18px;
        padding: 20px 30px;
        box-shadow: var(--shadow-theme);
        border: 1px solid var(--border-theme);
        display: flex;
        align-items: center;
        gap: 25px;
        margin-bottom: 25px;
        animation: slideInDown 0.8s ease-out;
    }}

    .kp-logo-section {{ flex-shrink: 0; }}
    .kp-logo-section img {{ max-height: 80px; width: auto; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.24)); }}

    .kp-text-section {{
        border-left: 3px solid var(--accent-1);
        padding-left: 25px;
        flex-grow: 1;
    }}

    .kp-subtitle {{
        font-size: 0.85em;
        font-weight: 700;
        color: var(--accent-1) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }}

    .kp-name {{ font-size: 1.1em; font-weight: 600; margin: 2px 0; color: var(--text-main) !important; }}

    /* Main dashboard header */
    .dashboard-header {{
        background: linear-gradient(135deg, var(--header-start) 0%, var(--header-mid) 55%, var(--header-end) 100%);
        padding: 35px;
        border-radius: 22px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 16px 35px color-mix(in srgb, var(--accent-1) 28%, transparent);
        color: white !important;
        animation: slideInUp 0.8s ease-out;
        border: 1px solid rgba(255,255,255,0.16);
    }}

    .dashboard-header h1 {{
        font-size: 2.5em;
        font-weight: 700;
        margin: 0;
        color: white !important;
        text-shadow: 0 4px 12px rgba(0,0,0,0.28);
    }}

    .dashboard-header p {{ font-size: 1.1em; opacity: 0.92; margin-top: 10px; color: #eef2ff !important; }}

    /* Cards */
    .metric-card, .chart-container {{
        background: linear-gradient(180deg, var(--card-bg) 0%, var(--card-bg-2) 100%);
        border-radius: 16px;
        box-shadow: var(--shadow-theme);
        border: 1px solid var(--border-theme);
    }}

    .metric-card {{
        padding: 20px;
        border-left: 5px solid var(--accent-1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 15px;
    }}

    .metric-card:hover {{ transform: translateY(-5px); box-shadow: 0 18px 35px rgba(0,0,0,0.18); }}

    .metric-value {{
        font-size: 2em;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 50%, var(--accent-3) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }}

    .metric-label {{
        color: var(--text-muted) !important;
        font-size: 0.85em;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }}

    .chart-container {{ padding: 20px; margin-bottom: 25px; color: var(--text-main) !important; }}
    .chart-container > div:first-child {{ color: var(--text-main) !important; }}

    /* Alert Boxes */
    .alert-box {{
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        color: white !important;
        box-shadow: var(--shadow-theme);
        border: 1px solid rgba(255,255,255,0.12);
    }}
    .alert-danger {{ background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%); }}
    .alert-warning {{ background: linear-gradient(135deg, #92400e 0%, #f59e0b 100%); }}
    .alert-info {{ background: linear-gradient(135deg, #075985 0%, #0284c7 100%); }}
    .alert-success {{ background: linear-gradient(135deg, #166534 0%, #16a34a 100%); }}

    /* Sidebar Cards */
    .sidebar-card {{
        background: linear-gradient(135deg, var(--header-start) 0%, var(--header-mid) 55%, var(--header-end) 100%);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        text-align: center;
        color: white !important;
        box-shadow: 0 10px 22px rgba(0,0,0,0.18);
        border: 1px solid rgba(255,255,255,0.14);
    }}

    .sidebar-value {{ font-size: 1.6rem; font-weight: 800; margin-bottom: 5px; color: white !important; }}
    .sidebar-label {{ font-size: 0.8rem; opacity: 0.9; font-weight: 500; color: #eef2ff !important; }}

    .section-header {{
        color: var(--text-main) !important;
        font-size: 1.4em;
        font-weight: 700;
        margin: 25px 0 15px 0;
        border-left: 5px solid var(--accent-1);
        padding-left: 10px;
    }}

    /* File uploader - dibuat menyatu dengan light/dark theme */
    [data-testid="stFileUploader"] {{
        background: linear-gradient(180deg, var(--card-bg) 0%, var(--card-bg-2) 100%) !important;
        border: 1px solid var(--border-theme) !important;
        border-radius: 14px !important;
        padding: 12px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.10);
    }}

    [data-testid="stFileUploaderDropzone"] {{
        background: color-mix(in srgb, var(--card-bg-2) 92%, var(--accent-1) 8%) !important;
        border: 1.5px dashed color-mix(in srgb, var(--accent-1) 50%, var(--border-theme)) !important;
        border-radius: 12px !important;
        color: var(--text-main) !important;
    }}

    [data-testid="stFileUploaderDropzone"] * {{ color: var(--text-main) !important; }}
    [data-testid="stFileUploaderDropzone"] small {{ color: var(--text-soft) !important; }}

    [data-testid="stFileUploaderDropzone"] button {{
        background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 100%) !important;
        color: white !important;
        border: 0 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }}

    [data-testid="stUploadedFile"] {{
        background: var(--card-bg-2) !important;
        border: 1px solid var(--border-theme) !important;
        border-radius: 10px !important;
        color: var(--text-main) !important;
    }}

    /* Section card khusus untuk tabel agar judul dan isi tidak tampak terpisah */
    .table-card {{
        background: linear-gradient(180deg, var(--card-bg) 0%, var(--card-bg-2) 100%);
        border-radius: 16px;
        box-shadow: var(--shadow-theme);
        border: 1px solid var(--border-theme);
        padding: 18px 18px 12px 18px;
        margin-bottom: 25px;
        color: var(--text-main) !important;
    }}

    .table-card-title {{
        font-weight: 800;
        font-size: 1.08em;
        margin-bottom: 14px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        color: var(--text-main) !important;
        border-bottom: 1px solid var(--border-theme);
        padding-bottom: 10px;
    }}

    .table-card-caption {{
        color: var(--text-muted) !important;
        font-weight: 600;
        margin-bottom: 10px;
    }}

    /* Tables / Dataframes */
    [data-testid="stDataFrame"], [data-testid="stTable"] {{
        background: var(--card-bg) !important;
        border-radius: 14px !important;
        border: 1px solid var(--border-theme) !important;
        overflow: hidden;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }}

    [data-testid="stDataFrame"] div[role="grid"],
    [data-testid="stDataFrame"] canvas,
    [data-testid="stDataFrameResizable"] {{
        background-color: var(--card-bg) !important;
    }}

    [data-testid="stDataFrame"] button,
    [data-testid="stDataFrame"] [data-testid="stElementToolbar"] {{
        background: var(--card-bg-2) !important;
        color: var(--text-main) !important;
        border-color: var(--border-theme) !important;
    }}

    /* Perbaikan tambahan: beberapa versi Streamlit memakai struktur glide-data-grid.
       Selector ini memaksa area grid mengikuti tema gelap/terang. */
    [data-testid="stDataFrame"] .glideDataEditor,
    [data-testid="stDataFrame"] .dvn-scroller,
    [data-testid="stDataFrame"] .dvn-underlay,
    [data-testid="stDataFrame"] [class*="glide"],
    [data-testid="stDataFrame"] [class*="data-grid"],
    [data-testid="stDataFrame"] [class*="DataFrame"] {{
        background: var(--card-bg) !important;
        color: var(--text-main) !important;
    }}

    [data-testid="stDataFrame"] input,
    [data-testid="stDataFrame"] textarea {{
        background: var(--card-bg-2) !important;
        color: var(--text-main) !important;
        border-color: var(--border-theme) !important;
    }}


    /* HTML table: aman untuk mode terang, gelap, dan auto */
    .theme-table-scroll {{
        background: var(--card-bg) !important;
        box-shadow: inset 0 1px 0 color-mix(in srgb, var(--text-main) 4%, transparent);
    }}

    .theme-html-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.86rem;
        color: var(--text-main) !important;
        background: var(--card-bg) !important;
    }}

    .theme-html-table thead th {{
        position: sticky;
        top: 0;
        z-index: 2;
        background: var(--card-bg-2) !important;
        color: var(--text-main) !important;
        border-bottom: 1px solid var(--border-theme) !important;
        padding: 10px 12px;
        text-align: left;
        font-weight: 800;
        white-space: nowrap;
    }}

    .theme-html-table tbody th {{
        background: var(--card-bg-2) !important;
        color: var(--text-muted) !important;
        border-bottom: 1px solid var(--border-theme) !important;
        padding: 9px 12px;
        font-weight: 600;
        white-space: nowrap;
    }}

    .theme-html-table td {{
        background: var(--card-bg) !important;
        color: var(--text-main) !important;
        border-bottom: 1px solid var(--border-theme) !important;
        padding: 9px 12px;
        white-space: nowrap;
    }}

    .theme-html-table tbody tr:nth-child(even) td,
    .theme-html-table tbody tr:nth-child(even) th {{
        background: color-mix(in srgb, var(--card-bg-2) 72%, var(--card-bg)) !important;
    }}

    .theme-html-table tbody tr:hover td,
    .theme-html-table tbody tr:hover th {{
        background: color-mix(in srgb, var(--accent-1) 16%, var(--card-bg)) !important;
        color: var(--text-main) !important;
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{ color: var(--text-muted) !important; background: transparent !important; }}
    button[data-baseweb="tab"][aria-selected="true"] {{ color: var(--accent-1) !important; border-bottom-color: var(--accent-1) !important; }}

    /* Buttons */
    .stDownloadButton button, .stButton button {{
        background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 100%) !important;
        color: white !important;
        border: 0 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 20px color-mix(in srgb, var(--accent-1) 24%, transparent);
    }}

    .footer {{
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        color: var(--text-muted) !important;
        border-top: 1px solid var(--border-theme);
    }}

    .footer * {{ color: var(--text-muted) !important; }}

    @keyframes slideInDown {{ from {{ transform: translateY(-50px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
    @keyframes slideInUp {{ from {{ transform: translateY(50px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
    @keyframes slideInLeft {{ from {{ transform: translateX(-50px); opacity: 0; }} to {{ transform: translateX(0); opacity: 1; }} }}
    @keyframes slideInRight {{ from {{ transform: translateX(50px); opacity: 0; }} to {{ transform: translateX(0); opacity: 1; }} }}

    .slide-left {{ animation: slideInLeft 0.6s ease-out; }}
    .slide-right {{ animation: slideInRight 0.6s ease-out; }}

    .css-15zrgzn {{display: none}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# DATA LOADING & PROCESSING
# ==========================================
@st.cache_data
def load_and_process_data(file_path=None):
    try:
        if file_path is None: 
            file_path = 'Data_Kendaraan_Bersih.csv'
            
        try: 
            df = pd.read_csv(file_path, sep=';')
        except pd.errors.ParserError: 
            try: 
                df = pd.read_csv(file_path, sep=',')
            except pd.errors.ParserError: 
                df = pd.read_csv(file_path)
        except Exception:
            df = pd.read_csv(file_path)

        df.columns = df.columns.str.strip()
        
        required_cols = ['Total Biaya', 'Nopol', 'Bulan', 'Tahun', 'Keterangan']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return None, f"Data tidak valid: Kolom wajib yang hilang - {', '.join(missing_cols)}"
            
        df = df.dropna(subset=['Total Biaya', 'Nopol', 'Bulan', 'Tahun', 'Keterangan'])
        df = df.drop_duplicates(subset=['Bulan', 'Tahun', 'Nopol', 'Total Biaya', 'Vendor_Clean'])
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
        df = df[df['Total Biaya'] > 1]
        df['Tahun'] = df['Tahun'].astype(int)
        
        if 'Type' in df.columns:
            df['Type'] = df.groupby('Nopol')['Type'].transform(lambda x: x.mode()[0] if not x.mode().empty else "UNKNOWN")
        else: 
            df['Type'] = 'UNKNOWN'
            
        return df, None
    except Exception as e: 
        return None, f"Error: {str(e)}"

# ==========================================
# CHART HELPER (RESPONSIVE)
# ==========================================
def render_chart_card(title, fig, height=450):
    if fig:
        current_theme = st.session_state.get("theme_mode", "Ikuti Tema Pengguna")
        tokens = get_theme_tokens(current_theme)
        fig.update_layout(
            template=tokens["plotly_template"],
            separators=".,",
            title_text="",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins', color=tokens["plot_text"]),
            margin=dict(l=40, r=40, t=20, b=40),
            height=height,
            xaxis=dict(showgrid=False, zeroline=False, color=tokens["plot_text"]),
            yaxis=dict(showgrid=True, gridcolor=tokens["plot_grid"], zeroline=False, color=tokens["plot_text"]),
            legend=dict(font=dict(family='Poppins', color=tokens["plot_text"]))
        )
        st.markdown(f"""
        <div class="chart-container">
            <div style="font-weight: 700; font-size: 1.1em; margin-bottom: 15px; text-transform: uppercase; border-bottom: 2px solid var(--border-theme); padding-bottom: 10px;">
                {title}
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def apply_table_theme(styler, gradient_subset=None, cmap="Blues"):
    """Make pandas Styler tables readable in both dark and light modes.

    Catatan penting:
    - Pada dark mode, background_gradient bawaan Pandas cenderung menghasilkan warna
      putih/biru muda sehingga teks menjadi tidak terlihat.
    - Karena itu gradient hanya dipakai pada mode terang. Pada mode gelap, tabel
      dibuat solid dark agar kontras dan tetap rapi.
    """
    current_theme = st.session_state.get("theme_mode", "Ikuti Tema Pengguna")
    is_dark = current_theme in ["Gelap", "Ikuti Tema Pengguna"]

    if is_dark:
        # Jangan pakai background_gradient di dark mode karena membuat sel menjadi putih.
        styler = styler.set_table_styles([
            {"selector": "thead th", "props": [
                ("background-color", "#020617"),
                ("color", "#f8fafc"),
                ("border-color", "rgba(148,163,184,0.24)"),
                ("font-weight", "700")
            ]},
            {"selector": "tbody th", "props": [
                ("background-color", "#0f172a"),
                ("color", "#e2e8f0"),
                ("border-color", "rgba(148,163,184,0.18)")
            ]},
            {"selector": "td", "props": [
                ("background-color", "#111827"),
                ("color", "#f8fafc"),
                ("border-color", "rgba(148,163,184,0.16)")
            ]},
            {"selector": "tr:nth-child(even) td", "props": [
                ("background-color", "#0f172a")
            ]},
            {"selector": "tr:hover td", "props": [
                ("background-color", "#1e293b"),
                ("color", "#ffffff")
            ]},
        ], overwrite=True)
        styler = styler.set_properties(**{
            "background-color": "#111827",
            "color": "#f8fafc",
            "border-color": "rgba(148,163,184,0.16)",
        })
    else:
        if gradient_subset:
            styler = styler.background_gradient(subset=gradient_subset, cmap=cmap)
        styler = styler.set_table_styles([
            {"selector": "thead th", "props": [("background-color", "#eef2ff"), ("color", "#0f172a"), ("border-color", "rgba(15,23,42,0.12)")]},
            {"selector": "tbody th", "props": [("background-color", "#f8fafc"), ("color", "#0f172a"), ("border-color", "rgba(15,23,42,0.10)")]},
            {"selector": "td", "props": [("color", "#0f172a"), ("border-color", "rgba(15,23,42,0.10)")]},
        ], overwrite=False)

    return styler


def render_theme_table(df_to_show, formatters=None, gradient_subset=None, cmap="Blues", height=360, use_container_width=True):
    """Render tabel HTML agar tidak blank di Streamlit Cloud.

    Alasan: st.dataframe memakai canvas/grid internal. Pada beberapa theme custom,
    isi tabel bisa terlihat putih/kosong. HTML table lebih stabil karena seluruh
    warna dikontrol lewat CSS token tema.
    """
    styled_df = df_to_show.copy()

    if formatters:
        for col, fmt in formatters.items():
            if col in styled_df.columns:
                if callable(fmt):
                    styled_df[col] = styled_df[col].apply(fmt)
                elif isinstance(fmt, str):
                    styled_df[col] = styled_df[col].apply(lambda x, f=fmt: f.format(x))

    html_table = styled_df.to_html(escape=False, index=True, classes="theme-html-table")
    st.markdown(f"""
    <div class="theme-table-scroll" style="max-height:{height}px; overflow:auto; border-radius:14px; border:1px solid var(--border-theme);">
        {html_table}
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# ANALYSIS FUNCTIONS
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

def calculate_monthly_category_trend(df):
    trend = df.groupby(['Tahun', 'Month_Num', 'Bulan', 'Keterangan'])['Total Biaya'].sum().reset_index()
    
    if not trend.empty:
        tahuns = trend['Tahun'].unique()
        kategoris = trend['Keterangan'].unique()
        month_map_local = {
            'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5, 'Juni': 6,
            'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
        }
        
        all_combinations = []
        for y in tahuns:
            for name, num in month_map_local.items():
                for k in kategoris:
                    all_combinations.append({'Tahun': y, 'Month_Num': num, 'Bulan': name, 'Keterangan': k})
                    
        all_df = pd.DataFrame(all_combinations)
        trend = pd.merge(all_df, trend, on=['Tahun', 'Month_Num', 'Bulan', 'Keterangan'], how='left')
        trend['Total Biaya'] = trend['Total Biaya'].fillna(0)
        
    return trend.sort_values(['Tahun', 'Month_Num'])


def calculate_monthly_trend(df):
    monthly = df.groupby(['Tahun', 'Month_Num', 'Bulan'])['Total Biaya'].sum().reset_index()
    
    if not monthly.empty:
        tahuns = monthly['Tahun'].unique()
        month_map_local = {
            'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5, 'Juni': 6,
            'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
        }
        all_months = pd.DataFrame([{ 'Tahun': y, 'Month_Num': num, 'Bulan': name } for y in tahuns for name, num in month_map_local.items()])
        monthly = pd.merge(all_months, monthly, on=['Tahun', 'Month_Num', 'Bulan'], how='left')
        monthly['Total Biaya'] = monthly['Total Biaya'].fillna(0)
        
    return monthly.sort_values(['Tahun', 'Month_Num'])

def calculate_category_distribution(df):
    return df.groupby('Keterangan')['Total Biaya'].agg(['sum', 'count']).sort_values('sum', ascending=False)

def calculate_type_statistics(df):
    type_stats = df.groupby('Type').agg({'Total Biaya': ['sum', 'mean', 'count'], 'Nopol': 'nunique'})
    type_stats.columns = ['Total_Biaya', 'Avg_Biaya', 'Transaksi', 'Jumlah_Unit']
    return type_stats.sort_values('Total_Biaya', ascending=False)


def detect_duplicates(df):
    return df[df.duplicated(subset=['Bulan', 'Tahun', 'Nopol', 'Total Biaya', 'Vendor_Clean'], keep=False)]

# --- Chart Creators ---
def format_currency_text(val):
    if val >= 1e9:
        return f"Rp {val/1e9:,.1f} Miliar"
    return f"Rp {val/1e6:,.0f} Juta"

def generate_tick_labels(max_value, num_ticks=6):
    '''Generates specific tick values and texts to avoid 1000 Juta and B/Billion'''
    if max_value <= 0:
        return [0], ["0 Juta"]
    
    step = max_value / num_ticks
    # Bulatkan step ke angka yang rapi (misalnya 100 juta, 200 juta, 500 juta)
    magnitude = 10 ** int(len(str(int(step))) - 1)
    step = round(step / magnitude) * magnitude
    if step == 0: step = magnitude
    
    tickvals = []
    ticktext = []
    
    current = 0
    while current <= max_value * 1.1:
        tickvals.append(current)
        if current == 0:
            ticktext.append("0 Juta")
        elif current >= 1e9:
            # Format to Miliar, remove trailing .0 if integer Miliar
            val_m = current / 1e9
            text = f"{val_m:.1f} Miliar".replace(".0 Miliar", " Miliar")
            ticktext.append(text)
        else:
            val_j = current / 1e6
            text = f"{val_j:.0f} Juta"
            ticktext.append(text)
        current += step

    return tickvals, ticktext

def create_yearly_trend_chart(summary_df):
    if summary_df.empty: return None
    years = summary_df.index.tolist()
    costs = summary_df['Total_Pengeluaran'].tolist()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=costs, customdata=costs, mode='lines+markers',
        line=dict(color='#667eea', width=3), marker=dict(size=10, color='#764ba2'),
        text=[format_currency_text(val) for val in costs], textposition='top center',
        hovertemplate='<b>Tahun %{x}</b><br>Total: %{text}<extra></extra>'
    ))
    
    max_cost = max(costs) if costs else 0
    t_vals, t_text = generate_tick_labels(max_cost)
    fig.update_layout(yaxis=dict(tickvals=t_vals, ticktext=t_text, range=[0, t_vals[-1] if t_vals else max_cost*1.2]))
    return fig

def create_vendor_pie_chart(vendor_df):
    if vendor_df.empty: return None
    labels = vendor_df.index[:8].tolist() + [f'Others ({len(vendor_df) - 8} Vendor)'] if len(vendor_df) > 8 else vendor_df.index.tolist()
    values = vendor_df.values[:8].tolist() + [vendor_df.values[8:].sum()] if len(vendor_df) > 8 else vendor_df.values.tolist()
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set3, line=dict(color='white', width=2)),
        textinfo='percent', hovertemplate='<b>%{label}</b><br>Rp %{value:,.0f}<extra></extra>'
    )])
    return fig

def create_timeline_chart(monthly_df):
    if monthly_df.empty: return None
    monthly_df = monthly_df.copy()
    monthly_df['Date'] = pd.to_datetime(monthly_df['Tahun'].astype(str) + '-' + monthly_df['Month_Num'].astype(str) + '-01')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_df['Date'], y=monthly_df['Total Biaya'], customdata=monthly_df['Total Biaya'],
        mode='lines+markers', line=dict(color='#667eea', width=3), marker=dict(size=8, color='#764ba2'),
        hovertemplate='<b>%{x|%B %Y}</b><br>Rp %{customdata:,.0f}<extra></extra>'
    ))

    max_cost = monthly_df['Total Biaya'].max() if not monthly_df.empty else 0
    t_vals, t_text = generate_tick_labels(max_cost)
    fig.update_yaxes(tickvals=t_vals, ticktext=t_text, range=[0, t_vals[-1] if t_vals else max_cost * 1.2])
    return fig

def create_category_timeline_chart(trend_df, top_n=5):
    if trend_df.empty: return None
    trend_df = trend_df.copy()
    
    # Filter to top N categories to avoid spaghetti chart
    top_cats = trend_df.groupby('Keterangan')['Total Biaya'].sum().nlargest(top_n).index
    trend_df = trend_df[trend_df['Keterangan'].isin(top_cats)]
    
    # Ensure every month has a data point for every top category
    tahuns = trend_df['Tahun'].unique()
    month_map_local = {
        'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5, 'Juni': 6,
        'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
    }
    
    all_combinations = []
    for y in tahuns:
        for name, num in month_map_local.items():
            for k in top_cats:
                all_combinations.append({'Tahun': y, 'Month_Num': num, 'Bulan': name, 'Keterangan': k})
                
    all_df = pd.DataFrame(all_combinations)
    trend_df = pd.merge(all_df, trend_df, on=['Tahun', 'Month_Num', 'Bulan', 'Keterangan'], how='left')
    trend_df['Total Biaya'] = trend_df['Total Biaya'].fillna(0)
    trend_df = trend_df.sort_values(['Tahun', 'Month_Num'])
    
    trend_df['Date'] = pd.to_datetime(trend_df['Tahun'].astype(str) + '-' + trend_df['Month_Num'].astype(str) + '-01')
    
    max_cost = trend_df['Total Biaya'].max() if not trend_df.empty else 0
    t_vals, t_text = generate_tick_labels(max_cost)
    
    fig = px.line(
        trend_df, x='Date', y='Total Biaya', color='Keterangan', markers=True,
        color_discrete_sequence=px.colors.qualitative.Bold, custom_data=['Total Biaya']
    )
    fig.update_traces(hovertemplate='<b>%{x|%B %Y}</b><br>Kategori: %{data.name}<br>Rp %{customdata[0]:,.0f}<extra></extra>')
    fig.update_yaxes(tickvals=t_vals, ticktext=t_text, range=[0, t_vals[-1] if t_vals else max_cost*1.2])
    return fig

def create_monthly_heatmap(df):
    pivot = df.pivot_table(values='Total Biaya', index='Bulan', columns='Tahun', aggfunc='sum', fill_value=0)
    order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    pivot = pivot.reindex(order, axis=0, fill_value=0)
    
    texts = [[(f'{val/1e9:.1f} Miliar'.replace('.0 Miliar', ' Miliar') if val>=1e9 else f'{val/1e6:.1f} Juta') if val>0 else '0' for val in row] for row in pivot.values]
        
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index, colorscale='Blues',
        text=texts, texttemplate='%{text}', textfont={"size": 10},
        hovertemplate='<b>%{y} %{x}</b><br>Rp %{z:,.0f}<extra></extra>',
        colorbar=dict(title="Biaya")
    ))
    
    max_cost = pivot.values.max() if pivot.size else 0
    t_vals, t_text = generate_tick_labels(max_cost, num_ticks=5)
    fig.update_layout(coloraxis_colorbar=dict(tickvals=t_vals, ticktext=t_text))
    # For go.Heatmap colorbar works slightly differently
    fig.update_traces(colorbar=dict(tickvals=t_vals, ticktext=t_text, title="Total Biaya"))

    return fig

def create_box_plot(df):
    fig = px.box(df, x='Tahun', y='Total Biaya', color_discrete_sequence=['#667eea'], title=None)
    fig.update_layout(showlegend=False)
    
    max_cost = df['Total Biaya'].max() if not df.empty else 0
    t_vals, t_text = generate_tick_labels(max_cost)
    fig.update_yaxes(tickvals=t_vals, ticktext=t_text)
    
    # Override default box plot hover formatting
    fig.update_traces(yhoverformat=",.0f")
    
    return fig

def create_vendor_comparison_chart(vendor_df, top_n=10):
    top = vendor_df.head(top_n)
    
    fig = go.Figure(data=[go.Bar(
        y=top.index, x=top.values, customdata=top.values, orientation='h',
        marker=dict(color=top.values, colorscale='Plasma', showscale=False),
        text=[format_currency_text(val) for val in top.values], 
        textposition='outside', cliponaxis=False,
        hovertemplate='<b>%{y}</b><br>Rp %{customdata:,.0f}<extra></extra>'
    )])
    
    max_val = top.values.max() if len(top) > 0 else 0
    t_vals, t_text = generate_tick_labels(max_val)
    fig.update_layout(
        yaxis=dict(autorange="reversed", automargin=True),
        xaxis=dict(showgrid=True, gridcolor='rgba(128, 128, 128, 0.1)', zeroline=False, tickvals=t_vals, ticktext=t_text, range=[0, t_vals[-1] if t_vals else max_val*1.4]),
        margin=dict(r=50)
    )
    return fig

def create_scatter_plot(df):
    stats = df.groupby('Nopol').agg({'Total Biaya': 'sum', 'Bulan': 'count', 'Type': 'first'}).reset_index()
    stats['Avg Biaya'] = stats['Total Biaya'] / stats['Bulan']
    
    fig = px.scatter(
        stats, x='Bulan', y='Total Biaya', hover_data=['Nopol', 'Type', 'Total Biaya', 'Avg Biaya'], color='Type',
        size='Avg Biaya', color_discrete_sequence=px.colors.qualitative.Vivid, title=None
    )
    
    max_cost = stats['Total Biaya'].max() if not stats.empty else 0
    t_vals, t_text = generate_tick_labels(max_cost)
    
    fig.update_layout(xaxis_title="Frekuensi Servis", yaxis_title="Total Biaya")
    fig.update_traces(hovertemplate='<b>Nopol: %{customdata[0]}</b><br>Tipe: %{customdata[1]}<br>Frekuensi: %{x}x<br>Total: Rp %{customdata[2]:,.0f}<br>Rata-rata/Servis: Rp %{customdata[3]:,.0f}<extra></extra>')
    fig.update_yaxes(tickvals=t_vals, ticktext=t_text, range=[0, t_vals[-1] if t_vals else max_cost*1.2])
    return fig

def create_type_distribution_chart(type_stats):
    if type_stats.empty: return None
    
    hover_texts = [format_currency_text(val) for val in type_stats['Total_Biaya']]
    
    fig = go.Figure(data=[go.Pie(
        labels=type_stats.index,
        values=type_stats['Total_Biaya'],
        hole=0.35,
        customdata=hover_texts,
        marker=dict(colors=px.colors.qualitative.Pastel, line=dict(color='white', width=2)),
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>%{customdata}<extra></extra>'
    )])
    return fig

def create_category_chart(category_df):
    fig = go.Figure(data=[go.Bar(
        y=category_df.index, x=category_df['sum'], customdata=category_df['sum'], orientation='h',
        marker=dict(color=category_df['sum'], colorscale='Viridis', showscale=False),
        text=[format_currency_text(val) for val in category_df['sum']], 
        textposition='outside', cliponaxis=False,
        hovertemplate='<b>%{y}</b><br>Rp %{customdata:,.0f}<extra></extra>'
    )])
    
    max_val = category_df['sum'].max() if not category_df.empty else 0
    t_vals, t_text = generate_tick_labels(max_val)
    
    fig.update_layout(
        yaxis=dict(autorange="reversed", automargin=True),
        xaxis=dict(showgrid=True, gridcolor='rgba(128, 128, 128, 0.1)', tickvals=t_vals, ticktext=t_text, range=[0, t_vals[-1] if t_vals else max_val*1.4]),
        margin=dict(r=50)
    )
    return fig

def render_footer():
    sby_logo = get_image_as_base64('SBY.png') or ''
    its_logo = get_image_as_base64('ITS.png') or ''
    
    st.markdown("""
    <div class="footer">
        <div style='display: flex; justify-content: center; align-items: center; gap: 40px; margin-bottom: 20px;'>
            <div style='text-align: center;'>
                {sby_logo_html}
                <div style="font-size: 0.7em; font-weight: bold; margin-top: 5px; color: var(--text-color);">PEMERINTAH<br>KOTA SURABAYA</div>
            </div>
            <div style='text-align: center;'>
                {its_logo_html}
            </div>
        </div>
        <div style='font-size: 0.8em; opacity: 0.8;'>
            <b>Dashboard Analisis Biaya Pemeliharaan Kendaraan</b><br>
            Badan Pengelolaan Keuangan dan Aset Daerah Kota Surabaya<br>
            <span style='opacity: 0.7;'>Kerja Praktik Institut Teknologi Sepuluh Nopember</span>
        </div>
        <div style="font-size: 0.7em; margin-top: 20px; opacity: 0.5;">© 2026 - Analisis Biaya Kendaraan</div>
    </div>
    """.format(
        sby_logo_html=f'<img src="data:image/png;base64,{sby_logo}" width="60">' if sby_logo else '',
        its_logo_html=f'<img src="data:image/png;base64,{its_logo}" width="180">' if its_logo else ''
    ), unsafe_allow_html=True)

# ==========================================
# MAIN APPLICATION
# ==========================================
def main():
    # Pilihan tema dibuat di sidebar agar pengguna bisa mengganti tampilan.
    with st.sidebar:
        theme_mode = st.selectbox(
            "🎨 Tema Tampilan",
            ["Ikuti Tema Pengguna", "Terang", "Gelap"],
            index=0,
            help="Pilih Terang/Gelap manual, atau Ikuti Tema Pengguna agar menyesuaikan preferensi perangkat/browser."
        )
        st.session_state["theme_mode"] = theme_mode

    load_custom_css(st.session_state.get("theme_mode", "Ikuti Tema Pengguna"))
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <h1 style='font-size: 3em; margin: 0;'>🚗</h1>
            <h3 style='margin: 0; font-weight:700;'>Dashboard<br>Analisis</h3>
        </div>
        <hr style="border-top: 1px solid rgba(128,128,128,0.2);">
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("📁 Upload CSV", type=['csv'])
        page = st.radio("Navigasi", ["Dashboard Utama", "Analisis Detail", "Detail Transaksi", "Laporan Audit", "Tentang Kami"])
        
        if uploaded_file:
            df, error = load_and_process_data(uploaded_file)
        else:
            df, error = load_and_process_data()
            
        if error:
            st.error(error)
            st.stop()
        if df is None:
            st.warning("⚠️ Data belum dimuat.")
            st.stop()

        # SIDEBAR INFO
        total_trx = len(df)
        min_tahun = int(df['Tahun'].min())
        max_tahun = int(df['Tahun'].max())
        periode_str = str(min_tahun) if min_tahun == max_tahun else f"{min_tahun}–{max_tahun}"
        total_unit = df['Nopol'].nunique()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight:700; margin-bottom:10px;'>ℹ️ Info Dataset</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-value">{total_trx:,}</div>
            <div class="sidebar-label">Total Transaksi</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-value">{periode_str}</div>
            <div class="sidebar-label">Periode Data</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-value">{total_unit}</div>
            <div class="sidebar-label">Jumlah Kendaraan</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border-top: 1px solid rgba(128,128,128,0.2);'>", unsafe_allow_html=True)
        st.subheader("Filter Data")
        
        years = sorted(df['Tahun'].unique())
        selected_years = st.multiselect("Tahun", years, default=years)
        if selected_years: 
            df = df[df['Tahun'].isin(selected_years)]
            
        vendors = ['Semua'] + sorted(df['Vendor_Clean'].unique().tolist())
        selected_vendor = st.selectbox("Vendor", vendors)
        if selected_vendor != 'Semua': 
            df = df[df['Vendor_Clean'] == selected_vendor]

        st.caption(f"Menampilkan: {len(df):,} baris")

    # --- DASHBOARD UTAMA ---
    if page == "Dashboard Utama":
        # 1. IDENTITAS HEADER
        logo_base64 = get_image_as_base64("bpkad.png")
        logo_html = f'<img src="data:image/png;base64,{logo_base64}">' if logo_base64 else ''
        st.markdown(f"""
        <div class="kp-header-container">
            <div class="kp-logo-section">{logo_html}</div>
            <div class="kp-text-section">
                <div class="kp-subtitle">KERJA PRAKTIK - BPKAD KOTA SURABAYA</div>
                <div class="kp-name">Rafi Satrio Pratama - 5052231007</div>
                <div class="kp-name">Rahardian Putra - 5052231018</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. DASHBOARD HEADER
        st.markdown("""
        <div class="dashboard-header">
            <h1>🚗 Dashboard Analisis Biaya</h1>
            <p>Monitoring & Evaluasi Pemeliharaan Kendaraan Dinas</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>📊 Ringkasan Eksekutif</div>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        
        monthly_avg_cost = df.groupby(['Tahun', 'Bulan'])['Total Biaya'].sum().mean()
        
        metrics = [
            ("💰 Total Pengeluaran", format_currency_text(df['Total Biaya'].sum()).replace('Rp ', ''), "Rupiah"),
            ("📈 Rata-rata / Bulan", format_currency_text(monthly_avg_cost).replace('Rp ', ''), "Pengeluaran per Bulan"),
            ("📋 Total Transaksi", f"{len(df):,}", "Service Record"),
            ("🚗 Jumlah Unit", f"{df['Nopol'].nunique()}", "Kendaraan Aktif")
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

        monthly_trend = calculate_monthly_trend(df)
        render_chart_card("Timeline Pengeluaran Bulanan", create_timeline_chart(monthly_trend))
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="table-card">
                <div class="table-card-title">🏆 10 Kendaraan Biaya Tertinggi</div>
            """, unsafe_allow_html=True)
            top_units = get_top_units(df, 10)

            if not top_units.empty:
                display_units = top_units.reset_index().copy()
                display_units.index = display_units.index + 1
                display_units.columns = ['Nopol', 'Tipe', 'Total Biaya', 'Frekuensi']
                
                render_theme_table(
                    display_units,
                    formatters={'Total Biaya': 'Rp {:,.0f}', 'Frekuensi': '{:.0f}x'},
                    gradient_subset=['Total Biaya'],
                    cmap='Reds',
                    height=360
                )
            else:
                st.info("Data kendaraan (TOP 10) belum tersedia.")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            vendors = get_top_vendors(df)
            render_chart_card("Distribusi Vendor Utama", create_vendor_pie_chart(vendors))

    # --- ANALISIS DETAIL ---
    elif page == "Analisis Detail":
        st.markdown("""
        <div class="dashboard-header" style="padding: 20px; margin-bottom: 20px;">
            <h1 style="font-size: 2em;">📈 Analisis Detail</h1>
            <p>Eksplorasi Data Mendalam</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Temporal", "🏢 Vendor", "🚗 Kendaraan", "📊 Kategori"])
        
        with tab1:
            render_chart_card("Heatmap Pengeluaran Bulanan", create_monthly_heatmap(df), height=500)
            
            c1, c2 = st.columns(2)
            with c1:
                render_chart_card("Distribusi Biaya per Tahun", create_box_plot(df))
            with c2:
                monthly_data = calculate_monthly_trend(df)
                if not monthly_data.empty:
                    max_month = monthly_data.loc[monthly_data['Total Biaya'].idxmax()]
                    min_month = monthly_data.loc[monthly_data['Total Biaya'].idxmin()]
                    
                    st.markdown(f"""
                    <div class="alert-box alert-danger">
                        <h4 style="margin:0;">🔝 Bulan Termahal</h4>
                        <div style="font-size: 1.2em; margin-top:5px;">{max_month['Bulan']} {int(max_month['Tahun'])}</div>
                        <div style="font-size: 1.5em; font-weight: 800;">Rp {max_month['Total Biaya']:,.0f}</div>
                    </div>
                    <div class="alert-box alert-success">
                        <h4 style="margin:0;">📉 Bulan Termurah</h4>
                        <div style="font-size: 1.2em; margin-top:5px;">{min_month['Bulan']} {int(min_month['Tahun'])}</div>
                        <div style="font-size: 1.5em; font-weight: 800;">Rp {min_month['Total Biaya']:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab2:
            c1, c2 = st.columns([2,1])
            with c1:
                render_chart_card("Peringkat Pengeluaran Service Kendaraan Dinas BPKAD per Vendor", create_vendor_comparison_chart(get_top_vendors(df, 15), 15), height=600)
            
            with c2:
                total_vendor = df['Vendor_Clean'].nunique()
                vendor_costs = df.groupby('Vendor_Clean')['Total Biaya'].sum().sort_values(ascending=False)
                top_3_pct = (vendor_costs.head(3).sum() / vendor_costs.sum() * 100) if vendor_costs.sum() > 0 else 0
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Vendor</div>
                    <div class="metric-value" style="font-size: 2.5em;">{total_vendor}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Konsentrasi Top 3</div>
                    <div class="metric-value" style="font-size: 2.5em; color: #764ba2;">{top_3_pct:.1f}%</div>
                    <div style="width: 100%; background: rgba(128,128,128,0.2); height: 8px; border-radius: 4px; margin-top: 5px;">
                        <div style="width: {top_3_pct}%; background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
        with tab3:
            c1, c2 = st.columns([2,1])
            with c1:
                render_chart_card("Korelasi Frekuensi vs Biaya", create_scatter_plot(df))
            with c2:
                render_chart_card("Proporsi Tipe", create_type_distribution_chart(calculate_type_statistics(df).head(10)))
            
            st.markdown("""
            <div class="table-card">
                <div class="table-card-title">📋 Tabel Efisiensi</div>
            """, unsafe_allow_html=True)
            eff = df.groupby(['Nopol', 'Type']).agg({'Total Biaya': ['sum', 'mean', 'count']})
            eff.columns = ['Total_Biaya', 'Rata_Rata', 'Frekuensi']
            
            render_theme_table(
                eff.sort_values('Total_Biaya', ascending=False),
                formatters={'Total_Biaya': 'Rp {:,.0f}', 'Rata_Rata': 'Rp {:,.0f}', 'Frekuensi': '{:.0f}'},
                gradient_subset=['Total_Biaya'],
                cmap='Reds',
                height=420
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with tab4:
            cat_dist = calculate_category_distribution(df)
            render_chart_card("Biaya per Kategori Kerusakan", create_category_chart(cat_dist))
            
            cat_trend = calculate_monthly_category_trend(df)
            render_chart_card("Tren Pengeluaran per Kategori", create_category_timeline_chart(cat_trend), height=500)


    # --- EKSPLORASI DATA ---
    elif page == "Detail Transaksi":
        st.markdown("""
        <div class="dashboard-header" style="padding: 20px; margin-bottom: 20px;">
            <h1 style="font-size: 2em;">🗃️ Detail Transaksi</h1>
            <p>Filter & Unduh Data Mentah Sesuai Kebutuhan</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: filter_keterangan = st.multiselect("Kategori Kerusakan", sorted(df['Keterangan'].unique()))
        with c2: filter_tipe = st.multiselect("Tipe Kendaraan", sorted(df['Type'].unique()))
        with c3: filter_nopol = st.multiselect("Nopol", sorted(df['Nopol'].unique()))
        
        filtered_df = df.copy()
        if filter_keterangan: filtered_df = filtered_df[filtered_df['Keterangan'].isin(filter_keterangan)]
        if filter_tipe: filtered_df = filtered_df[filtered_df['Type'].isin(filter_tipe)]
        if filter_nopol: filtered_df = filtered_df[filtered_df['Nopol'].isin(filter_nopol)]
        
        filtered_df = filtered_df.sort_values(['Tahun', 'Month_Num'])
        
        cols_display = ['Tahun', 'Bulan', 'Nopol', 'Type', 'Vendor_Clean', 'Keterangan', 'Total Biaya']
        
        st.markdown(f"""
        <div class="table-card">
            <div class="table-card-title">🗃️ Detail Transaksi</div>
            <div class="table-card-caption">Menampilkan {len(filtered_df):,} baris data terfilter</div>
        """, unsafe_allow_html=True)
        render_theme_table(
            filtered_df[cols_display],
            formatters={'Total Biaya': 'Rp {:,.0f}'},
            gradient_subset=['Total Biaya'],
            cmap='Blues',
            height=500
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        csv = filtered_df[cols_display].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data CSV",
            data=csv,
            file_name='Data_Eksplorasi.csv',
            mime='text/csv',
        )

    # --- LAPORAN AUDIT ---
    elif page == "Laporan Audit":
        st.markdown("""
        <div class="dashboard-header" style="padding: 20px; margin-bottom: 20px;">
            <h1 style="font-size: 2em;">📋 Laporan Audit</h1>
            <p>Ringkasan Eksekutif & Rekomendasi</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='section-header'>📊 Statistik Utama</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <ul style="line-height: 2.2; list-style: none; padding: 0; color: var(--text-color);">
                    <li>💰 <b>Total Pengeluaran:</b> {format_currency_text(df['Total Biaya'].sum())}</li>
                    <li>🧾 <b>Total Transaksi:</b> {len(df):,}</li>
                    <li>🚘 <b>Rata-rata per Unit:</b> {format_currency_text(df.groupby('Nopol')['Total Biaya'].sum().mean())}</li>
                    <li>🏢 <b>Vendor Terbesar:</b> {get_top_vendors(df,1).index[0]}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown("<div class='section-header'>💡 Rekomendasi Tindakan</div>", unsafe_allow_html=True)
            
            # --- Hitung data dinamis ---
            vendor_costs = df.groupby('Vendor_Clean')['Total Biaya'].sum().sort_values(ascending=False)
            top_3_pct = (vendor_costs.head(3).sum() / vendor_costs.sum() * 100) if vendor_costs.sum() > 0 else 0
            top_vendor = vendor_costs.index[0] if not vendor_costs.empty else '-'
            
            unit_costs = df.groupby(['Nopol', 'Type'])['Total Biaya'].sum().sort_values(ascending=False)
            top_unit = unit_costs.index[0] if not unit_costs.empty else ('-', '-')
            top_unit_cost = unit_costs.iloc[0] if not unit_costs.empty else 0
            
            cat_counts = df['Keterangan'].value_counts()
            top_cat = cat_counts.index[0] if not cat_counts.empty else '-'
            top_cat_pct = (cat_counts.iloc[0] / len(df) * 100) if not cat_counts.empty else 0

            monthly_cost = df.groupby(['Tahun', 'Bulan'])['Total Biaya'].sum()
            top_month_idx = monthly_cost.idxmax() if not monthly_cost.empty else (0, '-')
            top_month_cost = monthly_cost.max() if not monthly_cost.empty else 0
            
            type_avg = df.groupby('Type')['Total Biaya'].mean().sort_values(ascending=False)
            top_type = type_avg.index[0] if not type_avg.empty else '-'
            top_type_avg = type_avg.iloc[0] if not type_avg.empty else 0

            # --- Bangun rekomendasi ---
            if top_3_pct > 50:
                vendor_rec = f"Top 3 Vendor menguasai <b>{top_3_pct:.1f}%</b> total biaya. Lakukan negosiasi ulang kontrak dengan <b>{top_vendor}</b> dan pertimbangkan membuka tender terbuka untuk menciptakan kompetisi harga yang lebih sehat."
            else:
                vendor_rec = f"Distribusi vendor relatif sehat (Top 3 menguasai <b>{top_3_pct:.1f}%</b> biaya). Pertahankan keberagaman vendor untuk menjaga kompetisi dan efisiensi harga."

            unit_rec = f"Kendaraan <b>{top_unit[0]}</b> (Tipe: {top_unit[1]}) mencatatkan total biaya perawatan tertinggi sebesar <b>{format_currency_text(top_unit_cost)}</b>. Lakukan evaluasi kelayakan operasional dan pertimbangkan peremajaan unit tersebut."

            cat_rec = f"Kategori <b>{top_cat}</b> mendominasi {top_cat_pct:.1f}% dari seluruh transaksi. Tinjau apakah jenis kerusakan ini dapat dicegah melalui perawatan berkala (preventive maintenance) yang lebih terstruktur."

            month_rec = f"Pengeluaran tertinggi terjadi pada bulan <b>{top_month_idx[1]} {top_month_idx[0]}</b> sebesar <b>{format_currency_text(top_month_cost)}</b>. Pertimbangkan perencanaan anggaran yang lebih matang menjelang periode tersebut."

            type_rec = f"Tipe kendaraan <b>{top_type}</b> memiliki rata-rata biaya servis tertinggi sebesar <b>{format_currency_text(top_type_avg)}</b> per transaksi. Kaji ulang kebijakan pemeliharaan berkala untuk tipe kendaraan ini."

            recs = [
                ("🏢", "Evaluasi Vendor", vendor_rec),
                ("�", "Peremajaan Unit", unit_rec),
                ("📂", "Preventive Maintenance", cat_rec),
                ("📅", "Perencanaan Anggaran", month_rec),
                ("🚌", "Efisiensi Tipe Kendaraan", type_rec),
            ]
            for icon, title, desc in recs:
                st.markdown(f"""
                <div style="display:flex; align-items:flex-start; margin-bottom:12px; padding:12px 14px; background-color:var(--secondary-background-color); border-radius:10px; border-left:4px solid #764ba2; border:1px solid rgba(128,128,128,0.1);">
                    <div style="font-size:1.6em; margin-right:14px; margin-top:2px;">{icon}</div>
                    <div>
                        <div style="font-weight:700; color:var(--text-color); margin-bottom:3px;">{title}</div>
                        <div style="font-size:0.88em; opacity:0.85; line-height:1.5;">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        try:
            import xlsxwriter
            engine = 'xlsxwriter'
        except ImportError:
            engine = 'openpyxl'

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine=engine) as writer:
            calculate_yearly_summary(df).to_excel(writer, sheet_name='Ringkasan')
            get_top_vendors(df, 20).to_excel(writer, sheet_name='Vendor')
        
        st.download_button(
            label="📥 Download Laporan Excel",
            data=buffer.getvalue(),
            file_name="Laporan_Audit.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    # --- TENTANG KAMI ---
    elif page == "Tentang Kami":
        st.markdown("""
        <div class="dashboard-header" style="padding: 20px; margin-bottom: 20px;">
            <h1 style="font-size: 2em;">👥 Tentang Kami</h1>
            <p>Informasi Pengembang dan Aplikasi</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 2])
        
        with c1:
            logo_base64 = get_image_as_base64("bpkad.png")
            if logo_base64:
                st.markdown(f'<div style="text-align: center; margin-bottom: 20px;"><img src="data:image/png;base64,{logo_base64}" width="150" style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></div>', unsafe_allow_html=True)
            
            its_logo = get_image_as_base64('ITS.png')
            if its_logo:
                st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{its_logo}" width="200"></div>', unsafe_allow_html=True)
        
        with c2:
            st.markdown("""
            <div class="chart-container" style="animation: slideInUp 0.8s ease-out;">
                <div style="font-weight: 700; font-size: 1.2em; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px; color: #667eea; text-transform: uppercase;">🎓 Tim Pengembang</div>
                <p style="text-align: justify; margin-bottom: 10px;">Aplikasi ini dikembangkan sebagai bagian dari tugas <b>Kerja Praktik</b> di Badan Pengelolaan Keuangan dan Aset Daerah (BPKAD) Kota Surabaya oleh mahasiswa dari <b>Institut Teknologi Sepuluh Nopember (ITS)</b>.</p>
                <ul style="line-height: 1.8; margin-bottom: 25px;">
                    <li><b>Rafi Satrio Pratama</b> (5052231007)</li>
                    <li><b>Rahardian Putra</b> (5052231018)</li>
                </ul>
                <div style="font-weight: 700; font-size: 1.2em; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px; color: #667eea; text-transform: uppercase;">🚗 Tentang Aplikasi</div>
                <p style="text-align: justify; margin-bottom: 10px;"><b>Dashboard Analisis Biaya Kendaraan</b> adalah sebuah aplikasi cerdas yang dirancang untuk membantu instansi dalam memonitoring, dan mengevaluasi pengeluaran biaya pemeliharaan kendaraan dinas secara otomatis di lingkungan Pemerintah Kota Surabaya.</p>
                <div style="margin-top: 15px; margin-bottom: 5px; font-weight: 600;">Fitur Utama:</div>
                <ul style="line-height: 1.8; margin-bottom: 0;">
                    <li>Analisis komprehensif tren biaya secara hierarkis (Tahun/Bulan).</li>
                    <li>Perbandingan kinerja dan transparansi pengeluaran tiap vendor servis.</li>
                    <li>Pemantauan efektivitas pemeliharaan kendaraan.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
                
    render_footer()

if __name__ == "__main__":
    main()
