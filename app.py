import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# CONFIGURACIÓN GENERAL
# =========================================

st.set_page_config(
    page_title="Dato Claro AI · Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# BRAND TOKENS — datoclaro.netlify.app
# =========================================
# Dorado principal : #D4A843
# Fondo oscuro     : #0f0f0f / #111111
# Superficie       : #1a1a1a
# Tarjeta          : #222222
# Borde            : rgba(212,168,67,0.25)
# Texto primario   : #f0ece0
# Texto secundario : #9a9485
# =========================================

GOLD    = "#D4A843"
GOLD_DIM= "#b8902d"
DARK_BG = "#0d1b2e"   # azul marino profundo
SURFACE = "#112240"   # azul oscuro superficie
CARD    = "#1a2f4a"   # azul tarjeta
BORDER  = "rgba(212,168,67,0.28)"
TEXT    = "#e8f0f8"   # blanco azulado — más legible
MUTED   = "#8aaac8"   # gris azulado

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ────────────────────────────── */
html, body, [class*="css"], .stApp {{
    background-color: {DARK_BG} !important;
    color: {TEXT};
    font-family: 'DM Sans', sans-serif;
}}

.block-container {{
    padding: 0 !important;
    max-width: 1100px !important;
    margin: 0 auto !important;
}}

/* ── Ocultar elementos Streamlit ─────── */
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

/* ── Hero ────────────────────────────── */
.dc-hero {{
    background: {DARK_BG};
    border-bottom: 1px solid {BORDER};
    padding: 3.5rem 3rem 3rem;
    position: relative;
    overflow: hidden;
}}
.dc-hero::before {{
    content: '';
    position: absolute;
    top: -120px; right: -80px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(212,168,67,0.06) 0%, transparent 65%), radial-gradient(circle at 80% 50%, rgba(26,70,130,0.3) 0%, transparent 60%);
    pointer-events: none;
}}
.dc-logo {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: {GOLD};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.dc-logo span {{
    display: inline-block;
    width: 28px; height: 28px;
    border: 1.5px solid {GOLD};
    border-radius: 6px;
    font-size: 14px;
    line-height: 27px;
    text-align: center;
}}
.dc-hero h1 {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 400;
    color: {TEXT};
    line-height: 1.15;
    margin: 0 0 1rem;
}}
.dc-hero h1 em {{
    color: {GOLD};
    font-style: italic;
}}
.dc-hero p {{
    font-size: 1rem;
    color: {MUTED};
    max-width: 540px;
    line-height: 1.7;
    margin: 0;
}}
.dc-tag {{
    display: inline-block;
    border: 1px solid {BORDER};
    color: {GOLD};
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 100px;
    margin-bottom: 1.25rem;
    background: rgba(212,168,67,0.06);
}}

/* ── Contenido principal ─────────────── */
.dc-body {{
    padding: 2.5rem 3rem;
    background: {DARK_BG};
}}

/* ── Upload zone ─────────────────────── */
.dc-section-label {{
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {GOLD};
    margin-bottom: 0.6rem;
    font-weight: 500;
}}
.dc-section-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: {TEXT};
    font-weight: 400;
    margin-bottom: 0.4rem;
    line-height: 1.3;
}}
.dc-section-sub {{
    font-size: 0.875rem;
    color: {MUTED};
    margin-bottom: 1.5rem;
}}

/* ── Cards ───────────────────────────── */
.dc-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
}}
.dc-card-sm {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
}}

/* ── KPI cards ───────────────────────── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 2rem;
}}
.kpi {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}}
.kpi::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, {GOLD}, transparent);
}}
.kpi-label {{
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {MUTED};
    margin-bottom: 8px;
}}
.kpi-value {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.85rem;
    color: {TEXT};
    line-height: 1;
    margin-bottom: 2px;
}}
.kpi-delta {{
    font-size: 12px;
    color: {GOLD};
}}

/* ── Insight box ─────────────────────── */
.insight-box {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 2rem 2.25rem;
    position: relative;
}}
.insight-box::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: {GOLD};
    border-radius: 14px 0 0 14px;
}}
.insight-box h3 {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    font-weight: 400;
    color: {TEXT};
    margin-bottom: 0.5rem;
}}
.insight-box p, .insight-box li {{
    color: {MUTED};
    font-size: 0.9rem;
    line-height: 1.75;
}}
.insight-box strong {{
    color: {GOLD};
    font-weight: 500;
}}

/* ── Divider ─────────────────────────── */
.dc-divider {{
    border: none;
    border-top: 1px solid {BORDER};
    margin: 2rem 0;
}}

/* ── Streamlit overrides ─────────────── */
.stFileUploader > div {{
    background: {CARD} !important;
    border: 1.5px dashed {BORDER} !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}}
.stFileUploader label {{
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important;
}}
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {{
    color: {MUTED} !important;
}}
.stFileUploader [data-testid="stFileUploaderDropzone"] {{
    background: {CARD} !important;
    border: none !important;
}}
/* Botón de upload */
.stFileUploader button {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {GOLD} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}}
.stFileUploader button:hover {{
    background: rgba(212,168,67,0.12) !important;
    border-color: {GOLD} !important;
}}
/* Texto de instrucciones */
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] span,
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] small,
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] p {{
    color: {MUTED} !important;
    font-family: 'DM Sans', sans-serif !important;
}}

.stTextArea textarea {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}}
.stTextArea textarea:focus {{
    border-color: {GOLD} !important;
    box-shadow: 0 0 0 2px rgba(212,168,67,0.15) !important;
}}
.stTextArea label {{
    color: {MUTED} !important;
    font-size: 13px !important;
}}

.stSelectbox > div > div {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
}}
.stSelectbox label {{
    color: {MUTED} !important;
    font-size: 13px !important;
}}

.stRadio > div {{
    gap: 12px;
}}
.stRadio label {{
    color: {MUTED} !important;
    font-size: 13px !important;
}}
.stRadio [data-testid="stMarkdownContainer"] p {{
    color: {TEXT} !important;
}}

/* Metric override */
[data-testid="stMetric"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1rem 1.25rem;
}}
[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
    font-size: 11px !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}
[data-testid="stMetricValue"] {{
    color: {TEXT} !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.75rem !important;
}}

/* Dataframe */
.stDataFrame {{
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    overflow: hidden;
}}

/* Spinner */
.stSpinner > div {{
    border-top-color: {GOLD} !important;
}}

/* Warning / info */
.stAlert {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
}}

/* Subheaders */
h2, h3 {{
    font-family: 'DM Serif Display', serif !important;
    font-weight: 400 !important;
    color: {TEXT} !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================================
# PLOTLY TEMPLATE — Dato Claro
# =========================================

DC_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="DM Sans", color=TEXT),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=CARD,
        colorway=[GOLD, "#c49030", "#a87828", "#8c6020", "#704808"],
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            linecolor=BORDER,
            tickfont=dict(color=MUTED, size=12),
            title_font=dict(color=MUTED),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            linecolor=BORDER,
            tickfont=dict(color=MUTED, size=12),
            title_font=dict(color=MUTED),
        ),
        title=dict(
            font=dict(family="DM Serif Display", size=18, color=TEXT),
            x=0, pad=dict(l=4)
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=MUTED),
            bordercolor=BORDER,
            borderwidth=1,
        ),
        margin=dict(t=52, b=36, l=48, r=24),
        hoverlabel=dict(
            bgcolor=CARD,
            bordercolor=BORDER,
            font=dict(family="DM Sans", color=TEXT),
        ),
    )
)

# =========================================
# HERO
# =========================================

st.markdown(f"""
<div class="dc-hero">
  <div class="dc-logo"><span>DC</span> Dato Claro</div>
  <div class="dc-tag">AI Insights · Beta</div>
  <h1>Tus datos,<br>tu <em>ventaja.</em></h1>
  <p>Sube un archivo Excel o CSV y obtén KPIs automáticos, visualizaciones inteligentes e insights ejecutivos en segundos.</p>
</div>
<div class="dc-body">
""", unsafe_allow_html=True)

# =========================================
# UPLOAD + CONTEXTO
# =========================================

col_up, col_ctx = st.columns([1, 1], gap="large")

with col_up:
    st.markdown('<div class="dc-section-label">Datos</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-section-title">Carga tu archivo</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-section-sub">Excel (.xlsx) o CSV — hasta 200 MB</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["xlsx", "csv"], label_visibility="collapsed")

with col_ctx:
    st.markdown('<div class="dc-section-label">Contexto</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-section-title">Describe tu negocio</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-section-sub">Ayuda al análisis con contexto del archivo</div>', unsafe_allow_html=True)
    contexto_usuario = st.text_area(
        "",
        placeholder="Ej: Ventas mensuales por sucursal. La columna 'Ventas' representa ingresos netos. Sector retail.",
        height=148,
        label_visibility="collapsed"
    )

st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

# =========================================
# FUNCIÓN INSIGHTS
# =========================================

def generar_insights(df, contexto, metric_col):
    insights = []
    promedio = df[metric_col].mean()
    maximo   = df[metric_col].max()
    minimo   = df[metric_col].min()
    total    = df[metric_col].sum()

    if contexto:
        insights.append(f"<h3>🧾 Contexto del negocio</h3><p>{contexto}</p>")

    insights.append(f"""
<h3>📌 Análisis ejecutivo de <em style='color:{GOLD}'>{metric_col}</em></h3>
<ul>
  <li>Total acumulado: <strong>{total:,.2f}</strong></li>
  <li>Promedio: <strong>{promedio:,.2f}</strong></li>
  <li>Máximo registrado: <strong>{maximo:,.2f}</strong></li>
  <li>Mínimo registrado: <strong>{minimo:,.2f}</strong></li>
</ul>""")

    if maximo > (promedio * 2):
        insights.append(f"""
<h3>⚠️ Comportamiento atípico detectado</h3>
<p>La métrica <strong>{metric_col}</strong> presenta valores significativamente superiores al promedio.
Esto puede indicar campañas exitosas, eventos extraordinarios, errores operativos o alta concentración de resultados.</p>""")

    insights.append(f"""
<h3>💼 Recomendación ejecutiva</h3>
<p>Monitorea continuamente <strong>{metric_col}</strong> para identificar tendencias y posibles desviaciones.
Valores superiores a <strong>{(promedio * 1.5):,.2f}</strong> deben revisarse con mayor detalle.</p>""")

    return "\n".join(insights)

# =========================================
# MAIN APP
# =========================================

if uploaded_file:

    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error leyendo archivo: {e}")
        st.stop()

    # ── Preview ──────────────────────────
    st.markdown('<div class="dc-section-label">Vista previa</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dc-section-title">{uploaded_file.name}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dc-section-sub">{len(df):,} registros · {len(df.columns)} columnas</div>', unsafe_allow_html=True)
    st.dataframe(df.head(8), use_container_width=True, hide_index=True)

    st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_columns  = df.columns.tolist()

    if numeric_cols:

        # ── Configuración ─────────────────
        st.markdown('<div class="dc-section-label">Configuración</div>', unsafe_allow_html=True)
        st.markdown('<div class="dc-section-title">Parámetros del análisis</div>', unsafe_allow_html=True)

        cfg1, cfg2 = st.columns(2, gap="large")
        with cfg1:
            metric_col    = st.selectbox("Métrica principal", numeric_cols)
            dimension_col = st.selectbox("Dimensión / categoría", all_columns)
        with cfg2:
            date_col   = st.selectbox("Columna de fecha (opcional)", ["Ninguna"] + all_columns)
            chart_type = st.radio("Tipo de gráfica", ["Línea", "Barras", "Pie"], horizontal=True)

        st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

        # ── KPIs ──────────────────────────
        st.markdown('<div class="dc-section-label">KPIs</div>', unsafe_allow_html=True)
        st.markdown('<div class="dc-section-title">Indicadores principales</div>', unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        with k1: st.metric("Registros",           f"{len(df):,}")
        with k2: st.metric("Variables numéricas",  len(numeric_cols))
        with k3: st.metric("Total",               f"{df[metric_col].sum():,.2f}")
        with k4: st.metric("Promedio",            f"{df[metric_col].mean():,.2f}")

        st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

        # ── Preparar datos ─────────────────
        chart_df = df.copy()
        if date_col != "Ninguna":
            try:
                chart_df[date_col] = pd.to_datetime(chart_df[date_col])
            except:
                st.warning("⚠️ No fue posible convertir la columna a fecha.")

        # ── Visualización principal ────────
        st.markdown('<div class="dc-section-label">Visualización</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dc-section-title">{metric_col} — análisis visual</div>', unsafe_allow_html=True)

        if chart_type == "Línea":
            if date_col != "Ninguna":
                gdf   = chart_df.groupby(date_col)[metric_col].sum().reset_index()
                chart = px.line(gdf, x=date_col, y=metric_col, markers=True,
                                title=f"{metric_col} a través del tiempo",
                                template=DC_TEMPLATE)
                chart.update_traces(line_color=GOLD, line_width=2,
                                    marker=dict(color=GOLD, size=6))
            else:
                chart = px.line(chart_df, y=metric_col,
                                title=f"Análisis de {metric_col}",
                                template=DC_TEMPLATE)
                chart.update_traces(line_color=GOLD, line_width=2)

        elif chart_type == "Barras":
            gdf   = chart_df.groupby(dimension_col)[metric_col].sum().reset_index()
            chart = px.bar(gdf, x=dimension_col, y=metric_col,
                           title=f"{metric_col} por {dimension_col}",
                           template=DC_TEMPLATE)
            chart.update_traces(marker_color=GOLD, marker_line_width=0)

        elif chart_type == "Pie":
            gdf   = chart_df.groupby(dimension_col)[metric_col].sum().reset_index()
            chart = px.pie(gdf, names=dimension_col, values=metric_col,
                           title=f"Distribución de {metric_col}",
                           template=DC_TEMPLATE,
                           color_discrete_sequence=[GOLD,"#b8902d","#9c7820","#806015","#644808"])

        chart.update_layout(height=500)
        st.plotly_chart(chart, use_container_width=True)

        # ── Histograma ─────────────────────
        st.markdown('<div class="dc-section-label">Distribución</div>', unsafe_allow_html=True)
        hist = px.histogram(chart_df, x=metric_col, nbins=20,
                            title=f"Distribución de {metric_col}",
                            template=DC_TEMPLATE)
        hist.update_traces(marker_color=GOLD, marker_line_width=0, opacity=0.85)
        hist.update_layout(height=360)
        st.plotly_chart(hist, use_container_width=True)

        st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

        # ── Insights ──────────────────────
        st.markdown('<div class="dc-section-label">Inteligencia</div>', unsafe_allow_html=True)
        st.markdown('<div class="dc-section-title">Executive Business Summary</div>', unsafe_allow_html=True)
        st.markdown('<div class="dc-section-sub">Análisis automático generado a partir de tu archivo</div>', unsafe_allow_html=True)

        with st.spinner("Analizando información..."):
            insights_html = generar_insights(chart_df, contexto_usuario, metric_col)

        st.markdown(
            f'<div class="insight-box">{insights_html}</div>',
            unsafe_allow_html=True
        )

    else:
        st.warning("⚠️ No se encontraron columnas numéricas en el archivo.")

else:
    # Estado vacío elegante
    st.markdown(f"""
<div style="text-align:center;padding:4rem 2rem;color:{MUTED}">
  <div style="font-size:2.5rem;margin-bottom:1rem;opacity:0.4">◈</div>
  <div style="font-family:'DM Serif Display',serif;font-size:1.25rem;color:{TEXT};margin-bottom:0.5rem">
    Carga un archivo para comenzar
  </div>
  <div style="font-size:0.875rem">
    Excel (.xlsx) o CSV · Análisis automático en segundos
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
  border-top: 1px solid {BORDER};
  padding: 1.5rem 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: {MUTED};
  margin-top: 3rem;
">
  <div style="font-family:'DM Serif Display',serif;color:{GOLD};font-size:14px">DC · Dato Claro</div>
  <div>Tus datos, tu ventaja. &nbsp;·&nbsp; Ciudad de México</div>
  <div><a href="https://dato-claro-ai.streamlit.app" style="color:{GOLD};text-decoration:none">dato-claro-ai.streamlit.app ↗</a></div>
</div>
""", unsafe_allow_html=True)
