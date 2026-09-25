import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

import streamlit as st
import numpy as np
import pandas as pd

# 1. Configuración de la página (¡Debe ser la primera línea de Streamlit!)
st.set_page_config(
    page_title="Dashboard Ejecutivo",
    page_icon="📊",
    layout="wide",  # Crucial para dashboards con múltiples gráficos
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Opcional, para pulir el diseño) ---
st.markdown("""
    <style>
    /* Estilizar contenedores de métricas como tarjetas individuales */
    [data-testid="stMetricBlock"] {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)


# 2. Barra Lateral (Filtros y Control Global)
with st.sidebar:
    st.logo("https://placeholder.com", icon_image=None) # Cambia por tu logo
    st.title("🎛️ Filtros Globales")
    
    # Contenedor para agrupar filtros de tiempo
    with st.container():
        st.subheader("Período de Tiempo")
        fecha_inicio = st.date_input("Fecha Inicio", pd.to_datetime("2026-01-01"))
        fecha_fin = st.date_input("Fecha Fin", pd.to_datetime("2026-12-31"))
    
    st.divider() # Línea divisoria visual
    
    # Contenedor para filtros de categoría
    with st.container():
        st.subheader("Segmentación")
        categoria = st.selectbox("Categoría Principal", ["Todas", "Tecnología", "Finanzas", "Salud"])
        region = st.multiselect("Región", ["Norte", "Sur", "Este", "Oeste"], default=["Norte", "Sur"])


# 3. Panel Principal (Layout del Dashboard)

# Encabezado Principal (Uso de un contenedor dedicado)
header_container = st.container()
with header_container:
    st.title("📊 Dashboard de Rendimiento de Negocio")
    st.caption(f"Mostrando datos desde {fecha_inicio} hasta {fecha_fin} | Categoría: {categoria}")
    st.divider()

# FILA 1: Métricas Clave (KPIs) - Columnas fluidas
metric_container = st.container()
with metric_container:
    # Creamos 4 columnas para los KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Ingresos Totales", value="$45,230 USD", delta="+12.5%")
    with col2:
        st.metric(label="Usuarios Activos", value="1,240", delta="21 nuevos", delta_color="normal")
    with col3:
        st.metric(label="Tasa de Conversión", value="3.4%", delta="-0.2%", delta_color="inverse")
    with col4:
        st.metric(label="Ticket Promedio", value="$85.50 USD", delta="+4.2%")

st.subheader("") # Espaciador visual rápido

# FILA 2: Gráficos Principales (Distribución 60/40 o 50/50)
charts_container_1 = st.container()
with charts_container_1:
    col_izq, col_der = st.columns([2, 1]) # La columna izquierda es el doble de ancha
    
    with col_izq:
        st.markdown("### 📈 Tendencia de Ventas Mensuales")
        # Simulación de datos para el gráfico
        chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Ventas', 'Objetivo'])
        st.line_chart(chart_data)
        
    with col_der:
        st.markdown("### 🥧 Distribución por Región")
        # Simulación de datos para gráfico de barras/áreas
        pie_data = pd.DataFrame(np.random.rand(4, 1), index=["Norte", "Sur", "Este", "Oeste"], columns=["Participación"])
        st.bar_chart(pie_data)

st.divider()

# FILA 3: Pestañas para Detalles y Tablas de Datos
details_container = st.container()
with details_container:
    st.markdown("### 🔍 Análisis Detallado")
    
    # Las pestañas (Tabs) son excelentes para ahorrar espacio vertical
    tab_tabla, tab_resumen = st.tabs(["📋 Datos Crudos", "🧮 Resumen Estadístico"])
    
    with tab_tabla:
        st.markdown("#### Últimas transacciones registradas")
        df_transacciones = pd.DataFrame(
            np.random.randint(10, 100, size=(10, 3)),
            columns=['ID Cliente', 'Monto ($)', 'Score de Satisfacción']
        )
        st.dataframe(df_transacciones, use_container_width=True) # Se expande al ancho del contenedor
        
    with tab_resumen:
        st.markdown("#### Métricas agrupadas")
        st.json({
            "Metas del Trimestre": "Cumplidas al 85%",
            "Mejor Región": "Norte",
            "Producto Estrella": "Suscripción Premium"
        })
