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
# CUSTOM CSS STYLING (THEME AWARE & HIGH CONTRAST)
# ==========================================
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    /* Global Styles */
    * { font-family: 'Poppins', sans-serif; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid rgba(128,128,128,0.2);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-bottom: 100px; 
    }

    /* --- KP IDENTITY HEADER (KOTAK PUTIH ATAS) --- */
    .kp-header-container {
        background-color: var(--secondary-background-color);
        border-radius: 15px;
        padding: 20px 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid rgba(128,128,128,0.2);
        display: flex;
        align-items: center;
        gap: 25px;
        margin-bottom: 25px;
        animation: slideInDown 0.8s ease-out;
    }

    .kp-logo-section { flex-shrink: 0; }
    .kp-logo-section img { max-height: 80px; width: auto; }

    .kp-text-section {
        border-left: 3px solid #667eea;
        padding-left: 25px;
        flex-grow: 1;
    }

    .kp-subtitle {
        font-size: 0.85em;
        font-weight: 700;
        color: #667eea;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .kp-name {
        font-size: 1.1em;
        font-weight: 600;
        margin: 2px 0;
        color: var(--text-color);
    }

    /* --- MAIN DASHBOARD HEADER --- */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        color: white;
        animation: slideInUp 0.8s ease-out;
    }
    
    .dashboard-header h1 {
        font-size: 2.5em;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .dashboard-header p {
        font-size: 1.1em;
        opacity: 0.9;
        margin-top: 10px;
    }

    /* Metric Card Styling */
    .metric-card {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
        margin-bottom: 15px;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    
    .metric-label {
        color: var(--text-color);
        opacity: 0.8;
        font-size: 0.85em;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }

    /* Chart Container */
    .chart-container {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border: 1px solid rgba(128, 128, 128, 0.1);
    }

    /* Alert Boxes */
    .alert-box {
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .alert-danger { background: linear-gradient(135deg, #ef5350 0%, #e53935 100%); }
    .alert-warning { background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%); }
    .alert-info { background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%); }
    .alert-success { background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%); }

    /* SIDEBAR INFO CARDS (SOLID COLOR) */
    .sidebar-card {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .sidebar-value {
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 5px;
        color: white !important;
    }
    
    .sidebar-label {
        font-size: 0.8rem;
        opacity: 0.9;
        font-weight: 500;
        color: white !important;
    }

    /* Section Header */
    .section-header {
        color: var(--text-color);
        font-size: 1.4em;
        font-weight: 700;
        margin: 25px 0 15px 0;
        border-left: 5px solid #667eea;
        padding-left: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        opacity: 0.7;
        border-top: 1px solid rgba(128,128,128,0.2);
    }
    
    /* Animations */
    @keyframes slideInDown { from { transform: translateY(-50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes slideInUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes slideInLeft { from { transform: translateX(-50px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    @keyframes slideInRight { from { transform: translateX(50px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    
    .slide-left { animation: slideInLeft 0.6s ease-out; }
    .slide-right { animation: slideInRight 0.6s ease-out; }
    
    /* Hide Streamlit Elements */
    .css-15zrgzn {display: none}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
        fig.update_layout(
            separators=".,",
            title_text="",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins'),
            margin=dict(l=40, r=40, t=20, b=40),
            height=height,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(128, 128, 128, 0.1)', zeroline=False),
            legend=dict(font=dict(family='Poppins'))
        )
        st.markdown(f"""
        <div class="chart-container">
            <div style="font-weight: 700; font-size: 1.1em; margin-bottom: 15px; text-transform: uppercase; border-bottom: 2px solid rgba(128,128,128,0.1); padding-bottom: 10px;">
                {title}
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

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
    load_custom_css()
    
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
                        <div class="chart-container">
                            <div style="font-weight: 700; font-size: 1.1em; margin-bottom: 15px; text-transform: uppercase; border-bottom: 2px solid rgba(128,128,128,0.1); padding-bottom: 10px;">
                                🏆 10 Kendaraan Biaya Tertinggi
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            top_units = get_top_units(df, 10)

            if not top_units.empty:
                display_units = top_units.reset_index().copy()
                display_units.index = display_units.index + 1
                display_units.columns = ['Nopol', 'Tipe', 'Total Biaya', 'Frekuensi']
                
                st.dataframe(
                    display_units.style
                    .format({'Total Biaya': 'Rp {:,.0f}', 'Frekuensi': '{:.0f}x'})
                    .background_gradient(subset=['Total Biaya'], cmap='Reds'),
                    use_container_width=True
                )
            else:
                st.info("Data kendaraan (TOP 10) belum tersedia.")
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
            
            st.markdown("<div class='section-header'>📋 Tabel Efisiensi</div>", unsafe_allow_html=True)
            eff = df.groupby(['Nopol', 'Type']).agg({'Total Biaya': ['sum', 'mean', 'count']})
            eff.columns = ['Total_Biaya', 'Rata_Rata', 'Frekuensi']
            
            st.dataframe(
                eff.sort_values('Total_Biaya', ascending=False)
                .style.format({'Total_Biaya': 'Rp {:,.0f}', 'Rata_Rata': 'Rp {:,.0f}', 'Frekuensi': '{:.0f}'})
                .background_gradient(subset=['Total_Biaya'], cmap='Reds'),
                use_container_width=True
            )

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
        st.markdown(f"**Menampilkan {len(filtered_df):,} baris data terfilter:**")
        
        cols_display = ['Tahun', 'Bulan', 'Nopol', 'Type', 'Vendor_Clean', 'Keterangan', 'Total Biaya']
        
        st.dataframe(
            filtered_df[cols_display].style.format({'Total Biaya': 'Rp {:,.0f}'})
            .background_gradient(subset=['Total Biaya'], cmap='Blues'),
            use_container_width=True, height=500
        )
        
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
            
            its_logo = get_image_as_base64('Logo ITS-Biru.png')
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
