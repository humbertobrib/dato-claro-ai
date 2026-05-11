import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# CONFIGURACIÓN GENERAL
# =========================================

st.set_page_config(
    page_title="Dato Claro AI",
    page_icon="📊",
    layout="wide"
)

# =========================================
# ESTILOS CSS
# =========================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #1f2937;
}

.insight-box {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    border-left: 6px solid #2563eb;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# TÍTULO
# =========================================

st.title("📊 Dato Claro AI Insights")

st.markdown("""
### Transforma archivos Excel en insights ejecutivos automáticos

Sube un archivo y obtén:
- KPIs automáticos
- Visualizaciones inteligentes
- Insights ejecutivos
- Detección de comportamientos atípicos
""")

# =========================================
# UPLOADER
# =========================================

uploaded_file = st.file_uploader(
    "📂 Sube tu archivo Excel o CSV",
    type=["xlsx", "csv"]
)

# =========================================
# CONTEXTO DEL NEGOCIO
# =========================================

contexto_usuario = st.text_area(
    "📄 Describe el contexto del archivo",
    placeholder="""
Ejemplo:

Ventas mensuales por sucursal.
La columna 'Ventas' representa ingresos netos.
La columna 'Clientes' representa tickets atendidos.
La empresa pertenece al sector retail.
""",
    height=180
)

# =========================================
# FUNCIÓN DE INSIGHTS
# =========================================

def generar_insights(df, contexto, metric_col):

    insights = []

    promedio = df[metric_col].mean()
    maximo = df[metric_col].max()
    minimo = df[metric_col].min()
    total = df[metric_col].sum()

    # CONTEXTO

    if contexto:

        insights.append(f"""
### 🧾 Contexto del Negocio

{contexto}
""")

    # MÉTRICA

    insights.append(
        f"""
### 📌 Análisis Ejecutivo de '{metric_col}'

- Total acumulado: **{total:,.2f}**
- Promedio: **{promedio:,.2f}**
- Máximo registrado: **{maximo:,.2f}**
- Mínimo registrado: **{minimo:,.2f}**
"""
    )

    # ANOMALÍAS

    if maximo > (promedio * 2):

        insights.append(
            f"""
### ⚠️ Comportamiento Atípico Detectado

La métrica **'{metric_col}'** presenta valores significativamente superiores al promedio.

Esto podría indicar:
- campañas exitosas,
- eventos extraordinarios,
- errores operativos,
- o alta concentración de resultados.
"""
        )

    # RECOMENDACIÓN

    insights.append(
        f"""
### 💼 Recomendación Ejecutiva

Se recomienda monitorear continuamente la métrica **'{metric_col}'**
para identificar tendencias relevantes y posibles desviaciones operativas.

Valores superiores a **{(promedio * 1.5):,.2f}**
deberían revisarse con mayor detalle.
"""
    )

    return "\n\n".join(insights)

# =========================================
# MAIN APP
# =========================================

if uploaded_file:

    # =====================================
    # LEER ARCHIVO
    # =====================================

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:

        st.error(f"❌ Error leyendo archivo: {e}")
        st.stop()

    # =====================================
    # PREVIEW
    # =====================================

    st.subheader("📄 Vista previa de datos")

    st.dataframe(df.head())

    # =====================================
    # COLUMNAS
    # =====================================

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_columns = df.columns.tolist()

    if len(numeric_cols) > 0:

        # =================================
        # CONFIGURACIÓN DEL ANÁLISIS
        # =================================

        st.subheader("⚙️ Configuración del Análisis")

        col1, col2 = st.columns(2)

        with col1:

            metric_col = st.selectbox(
                "📈 Selecciona la métrica principal",
                numeric_cols
            )

            dimension_col = st.selectbox(
                "📊 Selecciona una categoría",
                all_columns
            )

        with col2:

            date_col = st.selectbox(
                "📅 Selecciona columna de fecha (opcional)",
                ["Ninguna"] + all_columns
            )

            chart_type = st.radio(
                "📉 Tipo de visualización",
                ["Línea", "Barras", "Pie"],
                horizontal=True
            )

        # =================================
        # KPIs
        # =================================

        st.subheader("📈 KPIs Principales")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.metric(
                "Registros",
                f"{len(df):,}"
            )

        with kpi2:
            st.metric(
                "Variables Numéricas",
                len(numeric_cols)
            )

        with kpi3:
            st.metric(
                "Total",
                f"{df[metric_col].sum():,.2f}"
            )

        with kpi4:
            st.metric(
                "Promedio",
                f"{df[metric_col].mean():,.2f}"
            )

        # =================================
        # PREPARAR DATOS
        # =================================

        chart_df = df.copy()

        # FECHAS

        if date_col != "Ninguna":

            try:
                chart_df[date_col] = pd.to_datetime(
                    chart_df[date_col]
                )

            except:
                st.warning(
                    "⚠️ No fue posible convertir la columna a fecha."
                )

        # =================================
        # VISUALIZACIÓN
        # =================================

        st.subheader("📊 Visualización Inteligente")

        if chart_type == "Línea":

            if date_col != "Ninguna":

                grouped_df = chart_df.groupby(
                    date_col
                )[metric_col].sum().reset_index()

                chart = px.line(
                    grouped_df,
                    x=date_col,
                    y=metric_col,
                    markers=True,
                    title=f"{metric_col} a través del tiempo"
                )

            else:

                chart = px.line(
                    chart_df,
                    y=metric_col,
                    title=f"Análisis de {metric_col}"
                )

        elif chart_type == "Barras":

            grouped_df = chart_df.groupby(
                dimension_col
            )[metric_col].sum().reset_index()

            chart = px.bar(
                grouped_df,
                x=dimension_col,
                y=metric_col,
                title=f"{metric_col} por {dimension_col}"
            )

        elif chart_type == "Pie":

            grouped_df = chart_df.groupby(
                dimension_col
            )[metric_col].sum().reset_index()

            chart = px.pie(
                grouped_df,
                names=dimension_col,
                values=metric_col,
                title=f"Distribución de {metric_col}"
            )

        # =================================
        # ESTILO
        # =================================

        chart.update_layout(
            template="plotly_white",
            height=550
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

        # =================================
        # HISTOGRAMA
        # =================================

        st.subheader("📉 Distribución de Datos")

        hist = px.histogram(
            chart_df,
            x=metric_col,
            nbins=20,
            title=f"Distribución de {metric_col}"
        )

        hist.update_layout(
            template="plotly_white",
            height=400
        )

        st.plotly_chart(
            hist,
            use_container_width=True
        )

        # =================================
        # INSIGHTS
        # =================================

        st.subheader("🧠 Executive Business Summary")

        with st.spinner("Analizando información..."):

            insights = generar_insights(
                chart_df,
                contexto_usuario,
                metric_col
            )

        st.markdown(
            f"""
<div class="insight-box">

{insights}

</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "⚠️ No se encontraron columnas numéricas en el archivo."
        )

else:

    st.info(
        "📂 Carga un archivo Excel o CSV para comenzar el análisis."
    )