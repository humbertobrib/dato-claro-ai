import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# CONFIGURACIÓN
# =========================================

st.set_page_config(
    page_title="Dato Claro AI · Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# BRAND TOKENS
# =========================================

GOLD    = "#D4A843"
DARK_BG = "#0d1b2e"
SURFACE = "#112240"
CARD    = "#1a2f4a"
BORDER  = "rgba(212,168,67,0.28)"
TEXT    = "#e8f0f8"
MUTED   = "#8aaac8"
SUCCESS = "#4ade80"
DANGER  = "#f87171"
WARN    = "#fbbf24"

# =========================================
# CSS
# =========================================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

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
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER} !important;
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stTextArea textarea {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important;
}}
[data-testid="stSidebar"] label {{ color: {MUTED} !important; font-size: 12px !important; }}

.dc-hero {{
    background: {DARK_BG};
    border-bottom: 1px solid {BORDER};
    padding: 3rem 3rem 2.5rem;
    position: relative;
    overflow: hidden;
}}
.dc-hero::before {{
    content: '';
    position: absolute;
    top: -120px; right: -80px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(212,168,67,0.06) 0%, transparent 65%),
                radial-gradient(circle at 80% 50%, rgba(26,70,130,0.3) 0%, transparent 60%);
    pointer-events: none;
}}
.dc-logo {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: {GOLD};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.25rem;
    display: flex; align-items: center; gap: 8px;
}}
.dc-logo span {{
    display: inline-block;
    width: 28px; height: 28px;
    border: 1.5px solid {GOLD};
    border-radius: 6px;
    font-size: 14px; line-height: 27px; text-align: center;
}}
.dc-tag {{
    display: inline-block;
    border: 1px solid {BORDER};
    color: {GOLD};
    font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;
    padding: 4px 12px; border-radius: 100px; margin-bottom: 1rem;
    background: rgba(212,168,67,0.06);
}}
.dc-hero h1 {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(1.8rem, 3.5vw, 2.8rem);
    font-weight: 400; color: {TEXT}; line-height: 1.15; margin: 0 0 0.75rem;
}}
.dc-hero h1 em {{ color: {GOLD}; font-style: italic; }}
.dc-hero p {{ font-size: 0.95rem; color: {MUTED}; max-width: 580px; line-height: 1.7; margin: 0; }}

.dc-body {{ padding: 2rem 3rem; background: {DARK_BG}; }}
.dc-label {{
    font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase;
    color: {GOLD}; margin-bottom: 0.5rem; font-weight: 500;
}}
.dc-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem; color: {TEXT}; font-weight: 400;
    margin-bottom: 0.3rem; line-height: 1.3;
}}
.dc-sub {{ font-size: 0.85rem; color: {MUTED}; margin-bottom: 1.25rem; }}
.dc-divider {{ border: none; border-top: 1px solid {BORDER}; margin: 1.75rem 0; }}

[data-testid="stMetric"] {{
    background: {CARD}; border: 1px solid {BORDER};
    border-radius: 12px; padding: 1rem 1.25rem;
    position: relative; overflow: hidden;
}}
[data-testid="stMetric"]::after {{
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 2px; background: linear-gradient(90deg, {GOLD}, transparent);
}}
[data-testid="stMetricLabel"] {{
    color: {MUTED} !important; font-size: 11px !important;
    letter-spacing: 0.1em; text-transform: uppercase;
}}
[data-testid="stMetricValue"] {{
    color: {TEXT} !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.55rem !important;
}}

.insight-card {{
    background: {CARD}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 1.4rem 1.65rem;
    margin-bottom: 1rem; position: relative;
}}
.insight-card.gold  {{ border-left: 4px solid {GOLD}; }}
.insight-card.green {{ border-left: 4px solid {SUCCESS}; }}
.insight-card.red   {{ border-left: 4px solid {DANGER}; }}
.insight-card.warn  {{ border-left: 4px solid {WARN}; }}
.insight-card h4 {{
    font-family: 'DM Serif Display', serif;
    font-size: 1rem; font-weight: 400; color: {TEXT}; margin: 0 0 0.45rem;
}}
.insight-card p {{ font-size: 0.875rem; color: {MUTED}; line-height: 1.8; margin: 0; }}
.insight-card strong {{ color: {GOLD}; font-weight: 500; }}
.ic-badge {{
    display: inline-block; font-size: 10px; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 3px 10px; border-radius: 100px;
    margin-bottom: 0.55rem; font-weight: 500;
}}
.ic-badge.gold  {{ background: rgba(212,168,67,0.12); color: {GOLD};    border: 1px solid rgba(212,168,67,0.3); }}
.ic-badge.green {{ background: rgba(74,222,128,0.10); color: {SUCCESS}; border: 1px solid rgba(74,222,128,0.3); }}
.ic-badge.red   {{ background: rgba(248,113,113,0.10); color: {DANGER}; border: 1px solid rgba(248,113,113,0.3); }}
.ic-badge.warn  {{ background: rgba(251,191,36,0.10); color: {WARN};    border: 1px solid rgba(251,191,36,0.3); }}

.stat-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.stat-table td {{ padding: 7px 12px; border-bottom: 1px solid rgba(212,168,67,0.1); color: {MUTED}; }}
.stat-table td:first-child {{ color: {TEXT}; font-weight: 500; }}
.stat-table tr:last-child td {{ border-bottom: none; }}

.stFileUploader > div {{
    background: {CARD} !important; border: 1.5px dashed {BORDER} !important;
    border-radius: 12px !important; padding: 1.25rem !important;
}}
.stFileUploader [data-testid="stFileUploaderDropzone"] {{ background: {CARD} !important; border: none !important; }}
.stFileUploader button {{
    background: {CARD} !important; border: 1px solid {BORDER} !important;
    border-radius: 8px !important; color: {GOLD} !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 13px !important; font-weight: 500 !important;
}}
.stFileUploader button:hover {{ background: rgba(212,168,67,0.12) !important; border-color: {GOLD} !important; }}
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] span,
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] small,
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] p {{ color: {MUTED} !important; }}

.stTextArea textarea, .stTextInput input {{
    background: {CARD} !important; border: 1px solid {BORDER} !important;
    border-radius: 10px !important; color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 14px !important;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
    border-color: {GOLD} !important; box-shadow: 0 0 0 2px rgba(212,168,67,0.15) !important;
}}
.stTextArea label, .stTextInput label {{ color: {MUTED} !important; font-size: 13px !important; }}
.stSelectbox > div > div {{
    background: {CARD} !important; border: 1px solid {BORDER} !important;
    border-radius: 8px !important; color: {TEXT} !important;
}}
.stSelectbox label, .stRadio label, .stCheckbox label, .stMultiSelect label {{
    color: {MUTED} !important; font-size: 13px !important;
}}
.stDataFrame {{ border: 1px solid {BORDER} !important; border-radius: 10px !important; overflow: hidden; }}
.stAlert {{ background: {CARD} !important; border: 1px solid {BORDER} !important; border-radius: 10px !important; color: {TEXT} !important; }}
h2, h3 {{ font-family: 'DM Serif Display', serif !important; font-weight: 400 !important; color: {TEXT} !important; }}

.ai-summary {{
    background: linear-gradient(135deg, {CARD}, {SURFACE});
    border: 1px solid {BORDER}; border-radius: 16px;
    padding: 2rem 2.25rem; position: relative; margin-bottom: 1rem;
}}
.ai-summary::before {{
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, {GOLD}, rgba(212,168,67,0.2));
    border-radius: 16px 0 0 16px;
}}
.ai-summary h3 {{ font-family: 'DM Serif Display', serif; font-size: 1.1rem; font-weight: 400; color: {TEXT}; margin: 0 0 0.75rem; }}
.ai-summary p {{ font-size: 0.9rem; color: {MUTED}; line-height: 1.8; margin: 0; }}
.ai-summary strong {{ color: {TEXT}; font-weight: 500; }}
</style>
""", unsafe_allow_html=True)

# =========================================
# PLOTLY TEMPLATE
# =========================================

DC_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="DM Sans", color=TEXT),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=CARD,
        colorway=[GOLD, "#c49030", "#a87828", "#8c6020", "#704808"],
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor=BORDER,
                   tickfont=dict(color=MUTED, size=12), title_font=dict(color=MUTED)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor=BORDER,
                   tickfont=dict(color=MUTED, size=12), title_font=dict(color=MUTED)),
        title=dict(font=dict(family="DM Serif Display", size=17, color=TEXT), x=0, pad=dict(l=4)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED), bordercolor=BORDER, borderwidth=1),
        margin=dict(t=52, b=36, l=48, r=24),
        hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font=dict(family="DM Sans", color=TEXT)),
    )
)

# =========================================
# SIDEBAR — PERSONALIZACIÓN
# =========================================

with st.sidebar:
    st.markdown(f"""
    <div style="padding:1rem 0 1.5rem">
      <div style="font-family:'DM Serif Display',serif;color:{GOLD};font-size:1.05rem;
                  letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.25rem">
        DC · Dato Claro
      </div>
      <div style="font-size:11px;color:{MUTED};letter-spacing:0.1em;text-transform:uppercase">
        Configuración del reporte
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:{GOLD};margin-bottom:0.5rem'>Empresa</div>", unsafe_allow_html=True)
    empresa  = st.text_input("Nombre", value="Mi Empresa", label_visibility="collapsed")
    sector   = st.selectbox("Sector", [
        "Retail / E-commerce", "Manufactura", "Finanzas / Contabilidad",
        "Salud", "Logística", "Servicios", "Tecnología", "Educación", "Otro"
    ])
    moneda = st.selectbox("Moneda", ["MXN $", "USD $", "EUR €", "Otro"])

    st.markdown("<hr style='border-color:rgba(212,168,67,0.15);margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:{GOLD};margin-bottom:0.5rem'>Umbrales de alerta</div>", unsafe_allow_html=True)
    umbral_anomalia = st.slider("Anomalía si supera el promedio en (×)", 1.2, 4.0, 2.0, 0.1)
    umbral_alerta   = st.slider("Alerta ejecutiva si supera (×)", 1.1, 2.0, 1.5, 0.1)
    top_n           = st.slider("Top N categorías a mostrar", 3, 15, 7)

    st.markdown("<hr style='border-color:rgba(212,168,67,0.15);margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:{GOLD};margin-bottom:0.5rem'>Análisis avanzado</div>", unsafe_allow_html=True)
    mostrar_correlacion  = st.checkbox("Matriz de correlación", value=True)
    mostrar_outliers     = st.checkbox("Detección de outliers (IQR)", value=True)
    mostrar_tendencia    = st.checkbox("Línea de tendencia", value=True)
    mostrar_estadisticas = st.checkbox("Estadísticas completas", value=True)

    st.markdown("<hr style='border-color:rgba(212,168,67,0.15);margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:{GOLD};margin-bottom:0.5rem'>API OpenAI</div>", unsafe_allow_html=True)
    openai_key = st.text_input("API Key", type="password", placeholder="sk-...", label_visibility="collapsed")
    usar_ia    = st.checkbox("Generar insights con IA", value=bool(openai_key))

# =========================================
# HERO
# =========================================

st.markdown(f"""
<div class="dc-hero">
  <div class="dc-logo"><span>DC</span> Dato Claro</div>
  <div class="dc-tag">AI Insights · Beta</div>
  <h1>Tus datos,<br>tu <em>ventaja.</em></h1>
  <p>Análisis ejecutivo inteligente para <strong style="color:{TEXT}">{empresa}</strong> — {sector}.
  Sube tu archivo y obtén insights accionables en segundos.</p>
</div>
<div class="dc-body">
""", unsafe_allow_html=True)

# =========================================
# UPLOAD + CONTEXTO
# =========================================

col_up, col_ctx = st.columns([1, 1], gap="large")

with col_up:
    st.markdown('<div class="dc-label">Datos</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-title">Carga tu archivo</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-sub">Excel (.xlsx) o CSV — hasta 200 MB</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["xlsx", "csv"], label_visibility="collapsed")

with col_ctx:
    st.markdown('<div class="dc-label">Contexto</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-title">Describe tu negocio</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-sub">Ayuda al análisis con contexto específico del archivo</div>', unsafe_allow_html=True)
    contexto_usuario = st.text_area(
        "",
        placeholder=f"Ej: Reporte de ventas mensuales de {empresa}. La columna 'Ventas' son ingresos netos en {moneda}. Objetivo mensual: $500,000.",
        height=148,
        label_visibility="collapsed"
    )

st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

# =========================================
# FUNCIONES
# =========================================

def analisis_estadistico(df, col):
    s = df[col].dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    outliers_low  = s[s < q1 - 1.5 * iqr]
    outliers_high = s[s > q3 + 1.5 * iqr]
    return {
        "count": len(s), "total": s.sum(), "mean": s.mean(),
        "median": s.median(), "std": s.std(),
        "cv": (s.std() / s.mean() * 100) if s.mean() != 0 else 0,
        "min": s.min(), "max": s.max(), "q1": q1, "q3": q3, "iqr": iqr,
        "skewness": s.skew(), "kurtosis": s.kurtosis(),
        "outliers_high": outliers_high, "outliers_low": outliers_low,
        "outlier_count": len(outliers_low) + len(outliers_high),
    }


def generar_insight_cards(df, col, dim_col, est, empresa, sector, moneda, umbral_anomalia, umbral_alerta):
    cards = []
    sym = moneda.split()[1] if len(moneda.split()) > 1 else moneda
    variabilidad = "alta" if est["cv"] > 40 else "moderada" if est["cv"] > 20 else "baja"

    # 1 — Resumen ejecutivo
    sesgo_txt = "simétrica" if abs(est["skewness"]) < 0.5 else \
                "sesgada hacia valores altos" if est["skewness"] > 0 else "sesgada hacia valores bajos"
    cards.append({"type": "gold", "badge": "Resumen ejecutivo",
        "title": f"Panorama de {col} — {empresa}",
        "body": (f"El total acumulado es <strong>{sym}{est['total']:,.0f}</strong>, con un promedio de "
                 f"<strong>{sym}{est['mean']:,.0f}</strong> por registro. La mediana se ubica en "
                 f"<strong>{sym}{est['median']:,.0f}</strong>, indicando una distribución <strong>{sesgo_txt}</strong>. "
                 f"La variabilidad es <strong>{variabilidad}</strong> (CV: {est['cv']:.1f}%), "
                 f"{'lo que sugiere comportamientos muy dispares entre registros — conviene segmentar.' if variabilidad == 'alta' else 'lo que indica consistencia operativa saludable.'}")
    })

    # 2 — Outliers
    if est["outlier_count"] > 0:
        pct = est["outlier_count"] / est["count"] * 100
        rec_outlier = {
            "Retail / E-commerce": "pueden representar campañas promocionales o devoluciones masivas",
            "Manufactura": "pueden indicar paros de línea o sobreproducción puntual",
            "Finanzas / Contabilidad": "requieren revisión para confirmar que no son errores de captura",
        }.get(sector, "merecen revisión individual antes de excluirlos del análisis")
        cards.append({"type": "warn", "badge": "Anomalías detectadas",
            "title": f"{est['outlier_count']} registros atípicos ({pct:.1f}% del total)",
            "body": (f"Se identificaron <strong>{len(est['outliers_high'])} valores superiores</strong> "
                     f"al límite IQR (>{sym}{est['q3'] + 1.5*est['iqr']:,.0f}) y "
                     f"<strong>{len(est['outliers_low'])} valores inferiores</strong> "
                     f"(<{sym}{est['q1'] - 1.5*est['iqr']:,.0f}). "
                     f"En <strong>{sector}</strong>, estos registros {rec_outlier}.")
        })
    else:
        cards.append({"type": "green", "badge": "Sin anomalías críticas",
            "title": f"Distribución limpia en {col}",
            "body": f"No se detectaron outliers bajo el método IQR. Los datos de <strong>{col}</strong> presentan una distribución consistente, sin valores extremos que distorsionen el análisis."
        })

    # 3 — Concentración por dimensión
    if dim_col and dim_col in df.columns:
        try:
            top = df.groupby(dim_col)[col].sum().sort_values(ascending=False)
            top1_pct = top.iloc[0] / top.sum() * 100
            top3_pct = top.iloc[:3].sum() / top.sum() * 100 if len(top) >= 3 else top1_pct
            tipo = "alta" if top3_pct > 70 else "moderada" if top3_pct > 50 else "baja"
            color = "warn" if tipo == "alta" else "green" if tipo == "baja" else "gold"
            cards.append({"type": color, "badge": f"Concentración {tipo}",
                "title": f"Distribución de {col} por {dim_col}",
                "body": (f"<strong>{top.index[0]}</strong> representa el <strong>{top1_pct:.1f}%</strong> del total. "
                         f"Las 3 categorías principales concentran el <strong>{top3_pct:.1f}%</strong>. "
                         f"{'Alta dependencia en pocas categorías — diversificar es prioritario.' if tipo == 'alta' else 'Distribución equilibrada — reduce riesgo operativo y de mercado.' if tipo == 'baja' else 'Concentración moderada — monitorear evolución trimestral.'}")
            })
        except Exception:
            pass

    # 4 — Umbral personalizado
    umbral_val = est["mean"] * umbral_alerta
    registros_sobre = int((df[col] > umbral_val).sum())
    pct_sobre = registros_sobre / est["count"] * 100
    cards.append({"type": "red" if pct_sobre > 25 else "gold",
        "badge": "Umbral de alerta personalizado",
        "title": f"{registros_sobre} registros superan {sym}{umbral_val:,.0f} ({umbral_alerta}× promedio)",
        "body": (f"El <strong>{pct_sobre:.1f}%</strong> de los registros supera el umbral configurado. "
                 f"{'Porcentaje significativo — revisa si los objetivos están bien calibrados.' if pct_sobre > 25 else 'Porcentaje manejable — estos registros merecen atención prioritaria.'} "
                 f"Ajusta el multiplicador en el panel lateral según tus objetivos de {empresa}.")
    })

    # 5 — Recomendación por sector
    recs = {
        "Retail / E-commerce": f"Implementa segmentación RFM para identificar clientes de alto valor. Correlaciona {col} con campañas de marketing para medir ROI real.",
        "Manufactura": f"Cruza {col} con turnos y líneas de producción para calcular OEE y detectar ineficiencias por equipo o proceso.",
        "Finanzas / Contabilidad": f"Compara {col} contra el presupuesto aprobado mensualmente. Establece alertas automáticas cuando la varianza supere el 10%.",
        "Salud": f"Monitorea {col} por unidad o servicio para detectar sobrecargas y optimizar la asignación de personal y recursos.",
        "Logística": f"Analiza {col} por ruta y almacén para identificar cuellos de botella y oportunidades de consolidación de envíos.",
        "Tecnología": f"Establece dashboards de {col} en tiempo real con alertas por umbral para el equipo de operaciones.",
    }
    rec = recs.get(sector, f"Establece KPIs específicos para {col} alineados con los objetivos de {empresa} y revísalos mensualmente con el equipo directivo.")
    cards.append({"type": "gold", "badge": "Recomendación ejecutiva",
        "title": f"Próximos pasos para {empresa}",
        "body": rec
    })

    return cards


def generar_con_openai(df, col, est, empresa, sector, moneda, contexto, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        sym = moneda.split()[1] if len(moneda.split()) > 1 else moneda
        prompt = f"""Eres consultor senior de Business Intelligence especializado en {sector}.
Analiza los datos de {empresa} y genera un Executive Summary profesional en español.

MÉTRICA: {col} | SECTOR: {sector} | MONEDA: {moneda}

ESTADÍSTICAS:
- Total: {sym}{est['total']:,.2f} | Promedio: {sym}{est['mean']:,.2f} | Mediana: {sym}{est['median']:,.2f}
- Desv. estándar: {sym}{est['std']:,.2f} | CV: {est['cv']:.1f}% | Sesgo: {est['skewness']:.2f}
- Mín: {sym}{est['min']:,.2f} | Máx: {sym}{est['max']:,.2f}
- Outliers: {est['outlier_count']} ({est['outlier_count']/est['count']*100:.1f}%)

CONTEXTO: {contexto if contexto else 'No especificado'}

Genera:
1. Diagnóstico en 2-3 oraciones sobre el estado actual
2. 2 oportunidades específicas para {sector}
3. 1 riesgo prioritario a mitigar
4. Una recomendación concreta y accionable

Sé específico, usa los números reales. Habla a un director o gerente. Máximo 200 palabras."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=450, temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al conectar con OpenAI: {str(e)}"


# =========================================
# MAIN APP
# =========================================

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error leyendo archivo: {e}")
        st.stop()

    st.markdown(f'<div class="dc-label">Vista previa</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dc-title">{uploaded_file.name}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dc-sub">{len(df):,} registros · {len(df.columns)} columnas · {empresa} · {sector}</div>', unsafe_allow_html=True)
    st.dataframe(df.head(8), use_container_width=True, hide_index=True)
    st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_columns  = df.columns.tolist()

    if not numeric_cols:
        st.warning("⚠️ No se encontraron columnas numéricas en el archivo.")
        st.stop()

    # ── Configuración ────────────────────
    st.markdown('<div class="dc-label">Configuración</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-title">Parámetros del análisis</div>', unsafe_allow_html=True)

    cfg1, cfg2, cfg3 = st.columns(3, gap="medium")
    with cfg1:
        metric_col     = st.selectbox("Métrica principal", numeric_cols)
        metricas_extra = st.multiselect("Métricas adicionales", [c for c in numeric_cols if c != metric_col])
    with cfg2:
        dimension_col  = st.selectbox("Dimensión / categoría", ["— Ninguna —"] + all_columns)
        date_col       = st.selectbox("Columna de fecha (opcional)", ["— Ninguna —"] + all_columns)
    with cfg3:
        chart_type     = st.radio("Tipo de gráfica", ["Barras", "Línea", "Pie", "Scatter"], horizontal=False)

    dimension_col = None if dimension_col == "— Ninguna —" else dimension_col
    date_col      = None if date_col      == "— Ninguna —" else date_col

    st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

    est = analisis_estadistico(df, metric_col)
    sym = moneda.split()[1] if len(moneda.split()) > 1 else moneda

    # ── KPIs ─────────────────────────────
    st.markdown('<div class="dc-label">KPIs</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dc-title">Indicadores principales — {metric_col}</div>', unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.metric("Total",    f"{sym}{est['total']:,.0f}")
    with k2: st.metric("Promedio", f"{sym}{est['mean']:,.0f}")
    with k3: st.metric("Mediana",  f"{sym}{est['median']:,.0f}")
    with k4: st.metric("Máximo",   f"{sym}{est['max']:,.0f}")
    with k5: st.metric("Outliers", f"{est['outlier_count']}",
                        delta=f"{est['outlier_count']/est['count']*100:.1f}% del total",
                        delta_color="inverse")

    st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

    # ── Estadísticas completas ────────────
    if mostrar_estadisticas:
        st.markdown('<div class="dc-label">Estadística</div>', unsafe_allow_html=True)
        st.markdown('<div class="dc-title">Análisis estadístico completo</div>', unsafe_allow_html=True)
        s1, s2 = st.columns(2, gap="large")
        with s1:
            st.markdown(f"""
<table class="stat-table">
  <tr><td>Registros totales</td><td>{est['count']:,}</td></tr>
  <tr><td>Total acumulado</td><td>{sym}{est['total']:,.2f}</td></tr>
  <tr><td>Media aritmética</td><td>{sym}{est['mean']:,.2f}</td></tr>
  <tr><td>Mediana</td><td>{sym}{est['median']:,.2f}</td></tr>
  <tr><td>Desviación estándar</td><td>{sym}{est['std']:,.2f}</td></tr>
  <tr><td>Coef. de variación</td><td>{est['cv']:.1f}%</td></tr>
</table>""", unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
<table class="stat-table">
  <tr><td>Mínimo</td><td>{sym}{est['min']:,.2f}</td></tr>
  <tr><td>Q1 (25%)</td><td>{sym}{est['q1']:,.2f}</td></tr>
  <tr><td>Q3 (75%)</td><td>{sym}{est['q3']:,.2f}</td></tr>
  <tr><td>Máximo</td><td>{sym}{est['max']:,.2f}</td></tr>
  <tr><td>Sesgo (skewness)</td><td>{est['skewness']:,.3f}</td></tr>
  <tr><td>Curtosis</td><td>{est['kurtosis']:,.3f}</td></tr>
</table>""", unsafe_allow_html=True)
        st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

    # ── Preparar datos ────────────────────
    chart_df = df.copy()
    if date_col:
        try:
            chart_df[date_col] = pd.to_datetime(chart_df[date_col])
        except:
            st.warning("⚠️ No fue posible convertir la columna a fecha.")

    # ── Visualización ─────────────────────
    st.markdown('<div class="dc-label">Visualización</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dc-title">{metric_col} — análisis visual</div>', unsafe_allow_html=True)

    chart = None
    if chart_type == "Línea":
        if date_col:
            gdf   = chart_df.groupby(date_col)[metric_col].sum().reset_index()
            chart = px.line(gdf, x=date_col, y=metric_col, markers=True,
                            title=f"{metric_col} a través del tiempo", template=DC_TEMPLATE)
            if mostrar_tendencia:
                z = np.polyfit(range(len(gdf)), gdf[metric_col], 1)
                chart.add_trace(go.Scatter(x=gdf[date_col], y=np.poly1d(z)(range(len(gdf))),
                    mode="lines", line=dict(color=MUTED, width=1.5, dash="dot"), name="Tendencia"))
        else:
            chart = px.line(chart_df, y=metric_col, title=f"Análisis de {metric_col}", template=DC_TEMPLATE)
        chart.update_traces(line_color=GOLD, line_width=2, marker=dict(color=GOLD, size=5),
                            selector=dict(name=metric_col))

    elif chart_type == "Barras":
        if dimension_col:
            gdf = chart_df.groupby(dimension_col)[metric_col].sum().nlargest(top_n).reset_index()
            chart = px.bar(gdf, x=dimension_col, y=metric_col,
                           title=f"Top {top_n} — {metric_col} por {dimension_col}", template=DC_TEMPLATE)
            chart.update_traces(marker_color=GOLD, marker_line_width=0)
            chart.add_hline(y=est["mean"], line_dash="dot", line_color=MUTED,
                            annotation_text=f"Promedio: {sym}{est['mean']:,.0f}",
                            annotation_font_color=MUTED)
        else:
            chart = px.histogram(chart_df, x=metric_col, nbins=20,
                                 title=f"Distribución de {metric_col}", template=DC_TEMPLATE)
            chart.update_traces(marker_color=GOLD, marker_line_width=0, opacity=0.85)

    elif chart_type == "Pie":
        if dimension_col:
            gdf   = chart_df.groupby(dimension_col)[metric_col].sum().nlargest(top_n).reset_index()
            chart = px.pie(gdf, names=dimension_col, values=metric_col,
                           title=f"Distribución de {metric_col} por {dimension_col}",
                           template=DC_TEMPLATE,
                           color_discrete_sequence=[GOLD,"#c49030","#a87828","#8c6020","#704808","#543000","#382000"])
            chart.update_traces(textfont_color=TEXT)
        else:
            st.info("Selecciona una dimensión para usar el gráfico de Pie.")

    elif chart_type == "Scatter":
        if metricas_extra:
            chart = px.scatter(chart_df, x=metric_col, y=metricas_extra[0],
                               color=dimension_col if dimension_col else None,
                               title=f"{metric_col} vs {metricas_extra[0]}", template=DC_TEMPLATE,
                               trendline="ols" if mostrar_tendencia else None)
            chart.update_traces(marker=dict(color=GOLD, size=7, opacity=0.75),
                                selector=dict(mode="markers"))
        else:
            st.info("Selecciona al menos una métrica adicional para el gráfico Scatter.")

    if chart is not None:
        chart.update_layout(height=500)
        st.plotly_chart(chart, use_container_width=True)

    # ── Histograma + Box plot ─────────────
    h_col, b_col = st.columns([2, 1], gap="large")
    with h_col:
        st.markdown('<div class="dc-label">Distribución</div>', unsafe_allow_html=True)
        hist = px.histogram(chart_df, x=metric_col, nbins=25,
                            title=f"Histograma — {metric_col}", template=DC_TEMPLATE)
        hist.update_traces(marker_color=GOLD, marker_line_width=0, opacity=0.85)
        hist.add_vline(x=est["mean"],   line_dash="dot",  line_color=TEXT,
                       annotation_text="Media",   annotation_font_color=MUTED)
        hist.add_vline(x=est["median"], line_dash="dash", line_color=MUTED,
                       annotation_text="Mediana", annotation_font_color=MUTED)
        hist.update_layout(height=320)
        st.plotly_chart(hist, use_container_width=True)

    with b_col:
        if mostrar_outliers:
            st.markdown('<div class="dc-label">Outliers IQR</div>', unsafe_allow_html=True)
            box = px.box(chart_df, y=metric_col,
                         title=f"Box plot — {metric_col}", template=DC_TEMPLATE)
            box.update_traces(marker_color=GOLD, line_color=GOLD, fillcolor=CARD)
            box.update_layout(height=320)
            st.plotly_chart(box, use_container_width=True)

    # ── Correlación ───────────────────────
    if mostrar_correlacion and len(numeric_cols) > 1:
        st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)
        st.markdown('<div class="dc-label">Correlación</div>', unsafe_allow_html=True)
        st.markdown('<div class="dc-title">Matriz de correlación entre variables numéricas</div>', unsafe_allow_html=True)
        corr    = df[numeric_cols].corr()
        fig_corr = px.imshow(corr, text_auto=".2f", template=DC_TEMPLATE,
                             color_continuous_scale=[[0, CARD],[0.5, SURFACE],[1, GOLD]],
                             title="Correlación de Pearson")
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)

    # ── Insight cards ─────────────────────
    st.markdown('<div class="dc-label">Inteligencia</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dc-title">Executive Business Summary — {empresa}</div>', unsafe_allow_html=True)
    st.markdown('<div class="dc-sub">Análisis automático basado en estadísticas reales de tu archivo</div>', unsafe_allow_html=True)

    cards = generar_insight_cards(
        chart_df, metric_col, dimension_col, est,
        empresa, sector, moneda, umbral_anomalia, umbral_alerta
    )
    for card in cards:
        st.markdown(f"""
<div class="insight-card {card['type']}">
  <div class="ic-badge {card['type']}">{card['badge']}</div>
  <h4>{card['title']}</h4>
  <p>{card['body']}</p>
</div>""", unsafe_allow_html=True)

    # ── IA OpenAI ─────────────────────────
    if usar_ia and openai_key:
        st.markdown('<hr class="dc-divider">', unsafe_allow_html=True)
        st.markdown('<div class="dc-label">IA Generativa</div>', unsafe_allow_html=True)
        st.markdown('<div class="dc-title">Análisis ejecutivo con IA</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dc-sub">Generado por OpenAI GPT para {empresa} · {sector}</div>', unsafe_allow_html=True)
        with st.spinner("Generando análisis con IA..."):
            ai_text = generar_con_openai(
                chart_df, metric_col, est, empresa, sector,
                moneda, contexto_usuario, openai_key
            )
        st.markdown(f"""
<div class="ai-summary">
  <h3>🤖 Diagnóstico ejecutivo — {empresa}</h3>
  <p>{ai_text.replace(chr(10), '<br>')}</p>
</div>""", unsafe_allow_html=True)

    elif usar_ia and not openai_key:
        st.info("Ingresa tu API Key de OpenAI en el panel lateral para activar los insights con IA.")

else:
    st.markdown(f"""
<div style="text-align:center;padding:4rem 2rem;color:{MUTED}">
  <div style="font-size:2.5rem;margin-bottom:1rem;opacity:0.4">◈</div>
  <div style="font-family:'DM Serif Display',serif;font-size:1.25rem;color:{TEXT};margin-bottom:0.5rem">
    Carga un archivo para comenzar
  </div>
  <div style="font-size:0.875rem">
    Excel (.xlsx) o CSV · Análisis ejecutivo automático en segundos
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
  border-top: 1px solid {BORDER}; padding: 1.5rem 3rem;
  display:flex; justify-content:space-between; align-items:center;
  font-size:12px; color:{MUTED}; margin-top:3rem;
">
  <div style="font-family:'DM Serif Display',serif;color:{GOLD};font-size:14px">DC · Dato Claro</div>
  <div>Tus datos, tu ventaja. &nbsp;·&nbsp; Ciudad de México</div>
  <div><a href="https://dato-claro-ai.streamlit.app" style="color:{GOLD};text-decoration:none">dato-claro-ai.streamlit.app ↗</a></div>
</div>
""", unsafe_allow_html=True)