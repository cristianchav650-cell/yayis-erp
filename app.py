import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import (
    load_company_info,
    load_products_and_dap,
    load_crm_data,
    add_new_lead,
    update_lead_status,
    load_nps_data,
    load_forecast_data,
    load_pap_data,
    load_pmp_data,
    load_bom_data,
    load_mrp_data,
    load_drp_data,
    load_inventory_data,
    add_new_material,
    load_purchasing_data,
)

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y DESIGN SYSTEM MODERNO
# ==============================================================================
st.set_page_config(
    page_title="YAYI'S ERP · Plataforma de Operaciones",
    page_icon="🥖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #261C1A;
    }
    h1, h2, h3, h4, .jakarta {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em;
    }

    .stApp {
        background-color: #F7F3EC;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1420px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #231715 0%, #2F201D 100%);
        border-right: 1px solid rgba(212, 154, 66, 0.22);
    }
    section[data-testid="stSidebar"] * {
        color: #F5EFE6 !important;
    }
    div[role="radiogroup"] > label {
        background-color: rgba(255, 255, 255, 0.03);
        padding: 0.55rem 0.85rem;
        border-radius: 10px;
        margin-bottom: 0.3rem;
        border: 1px solid transparent;
        transition: all 0.18s ease;
    }
    div[role="radiogroup"] > label:hover {
        background-color: rgba(212, 154, 66, 0.14);
        border-color: rgba(212, 154, 66, 0.35);
    }

    .hero-modern {
        background: linear-gradient(125deg, #261917 0%, #3E2723 55%, #5C3D34 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        color: #FFFFFF;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 30px rgba(38, 25, 23, 0.16);
        border: 1px solid rgba(212, 154, 66, 0.3);
        margin-bottom: 1.6rem;
    }
    .hero-pill {
        display: inline-block;
        background: rgba(212, 154, 66, 0.18);
        border: 1px solid rgba(245, 194, 107, 0.45);
        color: #F6C873 !important;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 0.32rem 0.85rem;
        border-radius: 999px;
        margin-bottom: 0.85rem;
    }
    .hero-modern h1 {
        color: #FFFDF9 !important;
        font-size: 2.15rem;
        font-weight: 800;
        margin: 0 0 0.45rem 0;
    }
    .hero-modern p {
        color: #E7D8C9 !important;
        font-size: 1.02rem;
        margin: 0;
        max-width: 780px;
    }

    .saas-kpi {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        border: 1px solid #EAE0D2;
        box-shadow: 0 4px 14px rgba(44, 30, 27, 0.04);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        height: 100%;
    }
    .saas-kpi:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(44, 30, 27, 0.08);
    }
    .saas-kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.55rem;
    }
    .saas-kpi-title {
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #7D645B;
    }
    .saas-kpi-badge {
        background: #FBF4E9;
        color: #B87924;
        padding: 0.22rem 0.6rem;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        border: 1px solid #F0DFC2;
    }
    .saas-kpi-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.65rem;
        font-weight: 800;
        color: #261917;
        line-height: 1.2;
    }
    .saas-kpi-sub {
        font-size: 0.82rem;
        color: #6E574F;
        margin-top: 0.35rem;
    }

    .mod-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.35rem 1.4rem 0.6rem 1.4rem;
        border: 1px solid #EAE0D2;
        box-shadow: 0 4px 14px rgba(44, 30, 27, 0.04);
        margin-bottom: 0.5rem;
    }
    .mod-tag {
        display: inline-block;
        background: #F5EDE1;
        color: #6D4C41;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #EAE0D2;
        padding: 1rem 1.15rem;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(44, 30, 27, 0.03);
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #7D645B !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        color: #261917 !important;
    }

    button[data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 0.92rem;
        border-radius: 10px 10px 0 0;
        padding: 0.65rem 1.1rem;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3E2723 0%, #5D4037 100%);
        border: 1px solid #C88A36;
        color: #FFFDF9;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #C88A36 0%, #B37728 100%);
        color: #FFFFFF;
        border-color: #C88A36;
    }

    .topbar-box {
        background: #FFFFFF;
        border: 1px solid #EAE0D2;
        border-radius: 16px;
        padding: 1.15rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 3px 12px rgba(44, 30, 27, 0.04);
    }
    .status-dot {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #EBF7EE;
        color: #1E7E34;
        font-size: 0.76rem;
        font-weight: 700;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        border: 1px solid #C3E6CB;
    }
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

def ir_a(destino):
    st.session_state.pagina = destino

def style_fig(fig, height=340):
    fig.update_layout(
        font=dict(family="Inter, sans-serif", color="#261C1A", size=12),
        title_font=dict(family="Plus Jakarta Sans, sans-serif", size=15, color="#261917"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        height=height,
        margin=dict(t=48, l=24, r=24, b=28),
        hovermode="x unified" if len(fig.data) > 1 else "closest",
    )
    fig.update_xaxes(showgrid=False, linecolor="#E6DCD0")
    fig.update_yaxes(gridcolor="#F3ECE1", zerolinecolor="#E6DCD0")
    return fig

def render_header_modulo(titulo, subtitulo="", badge="Base Excel Sincronizada"):
    st.markdown('<div class="topbar-box">', unsafe_allow_html=True)
    c1, c2 = st.columns([5.2, 1.1])
    with c1:
        st.markdown(f'<span class="status-dot">● {badge}</span>', unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin:0.35rem 0 0.15rem 0; color:#261917;'>{titulo}</h2>", unsafe_allow_html=True)
        if subtitulo:
            st.markdown(f"<p style='margin:0; color:#7D645B; font-size:0.93rem;'>{subtitulo}</p>", unsafe_allow_html=True)
    with c2:
        st.write("")
        if st.button("← Inicio", key=f"btn_home_{titulo}", use_container_width=True):
            ir_a("Inicio")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

try:
    meta_acad, empresa = load_company_info()
    productos_data = load_products_and_dap()
except Exception as e:
    st.error(f"Error al conectar con el archivo Excel: {e}")
    st.stop()

# ==============================================================================
# SIDEBAR DE NAVEGACIÓN
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.4rem 0.2rem 0.6rem 0.2rem;">
        <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.14em; color:#D49A42 !important; font-weight:700;">
            Enterprise Suite
        </div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.55rem; font-weight:800; color:#FFFDF9 !important; margin-top:2px;">
            🥖 YAYI'S ERP
        </div>
        <div style="font-size:0.82rem; color:#C9B8AE !important;">
            Masa Madre & Café · Cajamarca
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    opciones_menu = [
        "Inicio",
        "1. Información General",
        "2. CRM y Atención al Cliente",
        "3. Producción (PAP, PMP, MRP, DRP)",
        "4. Inventarios",
        "5. Compras y Proveedores",
        "6. Dashboard Ejecutivo"
    ]
    seleccion = st.radio(
        "NAVEGACIÓN PRINCIPAL",
        opciones_menu,
        index=opciones_menu.index(st.session_state.pagina)
    )
    if seleccion != st.session_state.pagina:
        st.session_state.pagina = seleccion
        st.rerun()

    st.divider()
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05); padding:0.85rem; border-radius:12px; border:1px solid rgba(212,154,66,0.25); font-size:0.8rem;">
        <div style="color:#F5C26B !important; font-weight:700; margin-bottom:4px;">🎓 Proyecto Académico</div>
        <div><b>Curso:</b> {meta_acad['curso']}</div>
        <div><b>Docente:</b> {meta_acad['docente']}</div>
        <div style="margin-top:4px; color:#B8A69C !important;">{meta_acad['universidad']} · {meta_acad['anio']}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PANTALLA DE INICIO
# ==============================================================================
if st.session_state.pagina == "Inicio":
    st.markdown(f"""
    <div class="hero-modern">
        <div class="hero-pill">● Sistema Integrado de Gestión · {meta_acad.get('archivo_activo', 'Archivo no identificado')}</div>
        <h1>YAYI'S ERP — {empresa['nombre_comercial'].upper()}</h1>
        <p>Plataforma centralizada para la gestión comercial (CRM/NPS), planificación maestra de la producción (PAP, PMP, MRP I/II, DRP), control de inventarios y abastecimiento.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="saas-kpi">
            <div class="saas-kpi-top"><span class="saas-kpi-title">Empresa</span><span class="saas-kpi-badge">🏪 Activa</span></div>
            <div class="saas-kpi-num">{empresa["nombre_comercial"].title()}</div>
            <div class="saas-kpi-sub">Panadería Masa Madre & Café</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="saas-kpi">
            <div class="saas-kpi-top"><span class="saas-kpi-title">RUC Activo</span><span class="saas-kpi-badge">🪪 SUNAT</span></div>
            <div class="saas-kpi-num">{empresa["ruc"]}</div>
            <div class="saas-kpi-sub">Contribuyente Habido</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="saas-kpi">
            <div class="saas-kpi-top"><span class="saas-kpi-title">Portafolio Core</span><span class="saas-kpi-badge">🥖 2 Líneas</span></div>
            <div class="saas-kpi-num">PF-01 · PF-02</div>
            <div class="saas-kpi-sub">Ciabatta & Integral Multigrano</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="saas-kpi">
            <div class="saas-kpi-top"><span class="saas-kpi-title">Planta & Sede</span><span class="saas-kpi-badge">📍 Perú</span></div>
            <div class="saas-kpi-num">Cajamarca</div>
            <div class="saas-kpi-sub">Jr. José Sabogal · Barrio San José</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:1.6rem; margin-bottom:0.8rem;'>Arquitectura Modular del Sistema</h3>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown('<div class="mod-card"><span class="mod-tag">MÓDULO 01</span><h4>🏢 Información General</h4><p style="color:#6E574F; font-size:0.9rem;">Perfil institucional, fichas técnicas de productos y Diagrama de Análisis del Proceso (DAP).</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Módulo 1 →", key="home_m1", use_container_width=True, type="primary"):
            ir_a("1. Información General")
            st.rerun()

        st.write("")
        st.markdown('<div class="mod-card"><span class="mod-tag">MÓDULO 04</span><h4>📦 Gestión de Inventarios</h4><p style="color:#6E574F; font-size:0.9rem;">Consulta de stock valorizado, alertas de stock de seguridad y alta de nuevos materiales.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Módulo 4 →", key="home_m4", use_container_width=True, type="primary"):
            ir_a("4. Inventarios")
            st.rerun()

    with col_b:
        st.markdown('<div class="mod-card"><span class="mod-tag">MÓDULO 02</span><h4>🤝 CRM y Atención (ATC)</h4><p style="color:#6E574F; font-size:0.9rem;">Embudo comercial, registro/actualización de leads y cálculo real de lealtad NPS.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Módulo 2 →", key="home_m2", use_container_width=True, type="primary"):
            ir_a("2. CRM y Atención al Cliente")
            st.rerun()

        st.write("")
        st.markdown('<div class="mod-card"><span class="mod-tag">MÓDULO 05</span><h4>🛒 Compras y Proveedores</h4><p style="color:#6E574F; font-size:0.9rem;">Trazabilidad de 50 órdenes de compra (OC) + 7 servicios (OS) y ranking de 13 proveedores.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Módulo 5 →", key="home_m5", use_container_width=True, type="primary"):
            ir_a("5. Compras y Proveedores")
            st.rerun()

    with col_c:
        st.markdown('<div class="mod-card"><span class="mod-tag">MÓDULO 03</span><h4>⚙️ Planificación Producción</h4><p style="color:#6E574F; font-size:0.9rem;">Pronósticos, PAP, PMP semanal, BOM con árbol estructural, MRP I/II (CRP/Ruta) y DRP.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Módulo 3 →", key="home_m3", use_container_width=True, type="primary"):
            ir_a("3. Producción (PAP, PMP, MRP, DRP)")
            st.rerun()

        st.write("")
        st.markdown('<div class="mod-card"><span class="mod-tag">MÓDULO 06</span><h4>📊 Dashboard Ejecutivo</h4><p style="color:#6E574F; font-size:0.9rem;">4 indicadores estratégicos clave integrando Comercial (M2), Producción/CRP (M3) y Abastecimiento (M4/M5).</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Módulo 6 →", key="home_m6", use_container_width=True, type="primary"):
            ir_a("6. Dashboard Ejecutivo")
            st.rerun()

    st.write("")
    with st.expander("🎓 Créditos Académicos del Equipo — Universidad Privada del Norte"):
        st.write(f"**Docente:** {meta_acad['docente']}")
        st.write("**Integrantes del Grupo 1:** " + " · ".join(meta_acad["integrantes"]))

# ==============================================================================
# MÓDULO 1: INFORMACIÓN
# ==============================================================================
elif st.session_state.pagina == "1. Información General":
    render_header_modulo(
        "🏢 Información Institucional y Productos",
        "Identidad corporativa, fichas técnicas de panificación artesanal y Diagrama de Análisis del Proceso (DAP)"
    )

    tab_emp, tab_p1, tab_p2 = st.tabs([
        "📋 Perfil de la Empresa",
        "🥖 Pan Ciabatta (PF-01)",
        "🌾 Pan Integral Multigrano (PF-02)"
    ])

    with tab_emp:
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Nombre Comercial:** {empresa['nombre_comercial']}")
                st.markdown(f"**RUC:** {empresa['ruc']}")
                st.markdown(f"**Propietaria / Gerente:** {empresa['dueno']}")
            with col2:
                st.markdown(f"**Sector Económico:** {empresa['sector']}")
                st.markdown(f"**Ubicación:** {empresa['ubicacion']}")
            st.divider()
            st.subheader("Reseña Histórica")
            st.write(empresa["historia"])
            st.subheader("Actividades Principales")
            st.write(empresa["actividades"])

    def render_producto(codigo):
        info = productos_data[codigo]
        ficha = info["ficha"]
        dap = info["dap"]
        resumen = info["resumen"]

        st.subheader(f"Ficha Técnica: {ficha.get('Nombre del producto', codigo)} ({ficha.get('Código', codigo)})")

        lote_raw = str(ficha.get("Lote de producción", "120 und")).strip()
        partes_lote = [p.strip() for p in lote_raw.split("·") if p.strip()]
        lote_val = partes_lote[0] if len(partes_lote) >= 1 else lote_raw
        frec_val = partes_lote[1] if len(partes_lote) >= 2 else "Según demanda diaria"

        precio_raw = str(ficha.get("Precio de venta (datos de la carta)", "0")).replace("S/", "").strip()
        try:
            precio_fmt = f"S/ {float(precio_raw):.2f} / und"
        except ValueError:
            precio_fmt = precio_raw

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Precio de Venta", precio_fmt)
        m2.metric("Lote de Producción", lote_val)
        m3.metric("Frecuencia Diaria", frec_val)
        m4.metric("Vida Útil", "1 día (Fresco del día)")

        with st.container(border=True):
            c_left, c_right = st.columns(2)
            with c_left:
                st.markdown(f"**Descripción:** {ficha.get('Descripción', '—')}")
                st.markdown(f"**Presentación:** {ficha.get('Presentación', '—')}")
            with c_right:
                st.markdown(f"**Uso / Aplicación en Carta:** {ficha.get('Uso / aplicación', '—')}")
                st.markdown(f"**Insumos Principales:** {ficha.get('Insumos principales', '—')}")

        st.subheader("Proceso de Fabricación — Diagrama de Análisis del Proceso (DAP)")
        g1, g2 = st.columns([1.15, 1])

        resumen_sin_total = resumen[resumen["Tipo de Actividad"] != "TOTAL"]
        with g1:
            fig_t = px.bar(
                resumen_sin_total,
                x="Tipo de Actividad",
                y="Tiempo (min)",
                color="Tipo de Actividad",
                text="Tiempo (min)",
                title=f"Distribución de Tiempo por Actividad — {codigo}",
                color_discrete_sequence=["#3E2723", "#C88A36", "#795548", "#A1887F", "#261917"]
            )
            fig_t.update_traces(texttemplate="%{text:.2f} min", textposition="outside")
            fig_t.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig_t, 340), use_container_width=True, key=f"chart_dap_{codigo}")

        with g2:
            st.markdown("**Resumen Ejecutivo del Proceso**")
            st.dataframe(resumen, use_container_width=True, hide_index=True)

        st.markdown("**Detalle Secuencial de Actividades (19 Operaciones)**")
        st.dataframe(dap, use_container_width=True, hide_index=True)

    with tab_p1:
        render_producto("PF-01")

    with tab_p2:
        render_producto("PF-02")

# ==============================================================================
# MÓDULO 2: CRM Y ATENCIÓN AL CLIENTE (NPS)
# ==============================================================================
elif st.session_state.pagina == "2. CRM y Atención al Cliente":
    render_header_modulo(
        "🤝 CRM y Atención al Cliente (ATC)",
        "Gestión de embudo comercial (Leads) y monitoreo de lealtad del cliente (Net Promoter Score)"
    )

    df_clientes = load_crm_data()
    df_atc, kpis_nps = load_nps_data()

    tab_estado, tab_registro, tab_nps = st.tabs([
        "📊 Estado de Clientes (Embudo CRM)",
        "➕ Gestión de Lead (Registrar / Actualizar)",
        "⭐ ATC — Indicador NPS"
    ])

    with tab_estado:
        total_leads = len(df_clientes)
        ventas_cerradas = int((df_clientes["Estado"] == "Venta").sum())
        en_proceso = int(df_clientes["Estado"].isin(["Pendiente", "Contactado", "Cotizado"]).sum())
        tasa_conv = (ventas_cerradas / total_leads * 100) if total_leads > 0 else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Leads Registrados", f"{total_leads} clientes")
        k2.metric("Clientes en Venta", f"{ventas_cerradas} clientes")
        k3.metric("Leads Activos en Gestión", f"{en_proceso} leads")
        k4.metric("Tasa de Conversión", f"{tasa_conv:.1f}%")

        g_col1, g_col2 = st.columns([1.15, 1])
        with g_col1:
            resumen_est = df_clientes["Estado"].value_counts().reset_index()
            resumen_est.columns = ["Estado", "Cantidad"]
            fig_est = px.bar(
                resumen_est,
                x="Estado",
                y="Cantidad",
                color="Estado",
                text="Cantidad",
                title="Distribución de Clientes por Estado Comercial",
                color_discrete_map={
                    "Venta": "#2E7D32",
                    "Cotizado": "#C88A36",
                    "Contactado": "#1565C0",
                    "Pendiente": "#795548",
                    "Descartado": "#C62828"
                }
            )
            fig_est.update_traces(textposition="outside")
            fig_est.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig_est, 330), use_container_width=True)

        with g_col2:
            resumen_asesor = df_clientes.groupby(["Asesor asignado", "Estado"]).size().reset_index(name="Clientes")
            fig_as = px.bar(
                resumen_asesor,
                x="Asesor asignado",
                y="Clientes",
                color="Estado",
                title="Cartera Asignada por Asesor Comercial",
                barmode="stack",
                color_discrete_sequence=["#2E7D32", "#C88A36", "#1565C0", "#795548", "#C62828"]
            )
            st.plotly_chart(style_fig(fig_as, 330), use_container_width=True)

        st.subheader("Listado de Atención de Leads")
        f1, f2, f3 = st.columns(3)
        sel_est = f1.selectbox("Filtrar por Estado", ["Todos"] + sorted(df_clientes["Estado"].unique().tolist()))
        sel_ase = f2.selectbox("Filtrar por Asesor", ["Todos"] + sorted(df_clientes["Asesor asignado"].unique().tolist()))
        sel_prd = f3.selectbox("Filtrar por Producto", ["Todos"] + sorted(df_clientes["Producto"].unique().tolist()))

        df_view = df_clientes.copy()
        if sel_est != "Todos":
            df_view = df_view[df_view["Estado"] == sel_est]
        if sel_ase != "Todos":
            df_view = df_view[df_view["Asesor asignado"] == sel_ase]
        if sel_prd != "Todos":
            df_view = df_view[df_view["Producto"] == sel_prd]

        cols_mostrar = [
            "ID", "Nombre Completo", "Asesor asignado", "Producto",
            "Estado", "Canal de venta (DRP)", "Celular", "Fecha de registro"
        ]
        st.dataframe(df_view[cols_mostrar], use_container_width=True, hide_index=True)

    with tab_registro:
        col_form1, col_form2 = st.columns([1.3, 1])

        with col_form1:
            st.subheader("Registrar Nuevo Cliente Potencial (Lead)")
            with st.form("form_nuevo_lead", clear_on_submit=True):
                r1, r2 = st.columns(2)
                nombre = r1.text_input("Nombres *", placeholder="Ej. Carlos Alberto")
                apellido = r2.text_input("Apellidos *", placeholder="Ej. Mendoza Ruiz")

                r3, r4 = st.columns(2)
                celular = r3.text_input("Celular *", placeholder="Ej. 976 123 456")
                canal_cap = r4.selectbox(
                    "Canal de Captación",
                    ["Presencial en el café", "WhatsApp", "Instagram", "Facebook", "Referido"]
                )

                r5, r6 = st.columns(2)
                canal_drp = r5.selectbox(
                    "Canal de Venta (DRP)",
                    ["Café Yayi's (CAF)", "Delivery y corporativos (DLV)"]
                )
                producto_int = r6.selectbox(
                    "Producto de Interés",
                    ["Pan Ciabatta", "Pan Integral Multigrano"]
                )

                r7, r8 = st.columns(2)
                asesores_lista = sorted(df_clientes["Asesor asignado"].unique().tolist())
                asesor_sel = r7.selectbox("Asesor Asignado", asesores_lista)
                estado_ini = r8.selectbox(
                    "Estado Inicial",
                    ["Pendiente", "Contactado", "Cotizado", "Venta", "Descartado"]
                )

                submitted = st.form_submit_button("💾 Guardar Lead en Excel", type="primary", use_container_width=True)
                if submitted:
                    if not nombre.strip() or not apellido.strip() or not celular.strip():
                        st.warning("Por favor complete Nombres, Apellidos y Celular antes de guardar.")
                    else:
                        try:
                            nuevo_codigo = add_new_lead(
                                nombre, apellido, celular, canal_cap, canal_drp, producto_int, asesor_sel, estado_ini
                            )
                            st.success(f"✅ Lead registrado exitosamente con el código **{nuevo_codigo}**.")
                            st.rerun()
                        except PermissionError:
                            st.error("⚠️ Cierra el archivo Excel antes de guardar un registro.")
                        except Exception as err:
                            st.error(f"Error al guardar: {err}")

        with col_form2:
            st.subheader("Actualizar Estado de Lead Existente")
            with st.form("form_actualizar_estado"):
                opciones_clientes = [
                    f"{row['ID']} | {row['Nombre Completo']} ({row['Estado']})"
                    for _, row in df_clientes.iterrows()
                ]
                cliente_sel = st.selectbox("Seleccionar Cliente", opciones_clientes)
                nuevo_estado = st.selectbox(
                    "Nuevo Estado Comercial",
                    ["Pendiente", "Contactado", "Cotizado", "Venta", "Descartado"]
                )
                btn_upd = st.form_submit_button("🔄 Actualizar Estado en Excel", use_container_width=True)
                if btn_upd:
                    cid = cliente_sel.split("|")[0].strip()
                    try:
                        update_lead_status(cid, nuevo_estado)
                        st.success(f"✅ Estado de **{cid}** actualizado a **{nuevo_estado}**.")
                        st.rerun()
                    except PermissionError:
                        st.error("⚠️ Cierra el archivo Excel para poder actualizar el estado.")
                    except Exception as err:
                        st.error(f"Error al actualizar: {err}")

    with tab_nps:
        n1, n2, n3, n4 = st.columns(4)
        n1.metric("Puntaje NPS Global", f"{kpis_nps['nps_score']:.2f} pts", delta="Excelente (> 50)")
        n2.metric("Promotores (9-10)", f"{kpis_nps['promotores']} ({kpis_nps['promotores']/kpis_nps['total_encuestas']*100:.1f}%)")
        n3.metric("Pasivos (7-8)", f"{kpis_nps['pasivos']} ({kpis_nps['pasivos']/kpis_nps['total_encuestas']*100:.1f}%)")
        n4.metric("Detractores (0-6)", f"{kpis_nps['detractores']} ({kpis_nps['detractores']/kpis_nps['total_encuestas']*100:.1f}%)")

        c_nps1, c_nps2 = st.columns([1, 1.4])
        with c_nps1:
            df_pie = pd.DataFrame({
                "Segmento": ["Promotores (9-10)", "Pasivos (7-8)", "Detractores (0-6)"],
                "Cantidad": [kpis_nps["promotores"], kpis_nps["pasivos"], kpis_nps["detractores"]]
            })
            fig_nps = px.pie(
                df_pie,
                names="Segmento",
                values="Cantidad",
                hole=0.52,
                title="Composición NPS (2,721 Atenciones)",
                color="Segmento",
                color_discrete_map={
                    "Promotores (9-10)": "#2E7D32",
                    "Pasivos (7-8)": "#E09F3E",
                    "Detractores (0-6)": "#C62828"
                }
            )
            st.plotly_chart(style_fig(fig_nps, 340), use_container_width=True)

        with c_nps2:
            st.subheader("Registro de Calificaciones NPS por Venta")
            f_nps1, f_nps2 = st.columns(2)
            filtro_tipo_nps = f_nps1.selectbox("Segmento NPS", ["Todos", "Promotor", "Pasivo", "Detractor"])
            filtro_asesor_nps = f_nps2.selectbox("Asesor de Venta", ["Todos"] + sorted(df_atc["Asesor"].unique().tolist()))

            df_nps_view = df_atc.copy()
            if filtro_tipo_nps != "Todos":
                df_nps_view = df_nps_view[df_nps_view["Tipo NPS"] == filtro_tipo_nps]
            if filtro_asesor_nps != "Todos":
                df_nps_view = df_nps_view[df_nps_view["Asesor"] == filtro_asesor_nps]

            cols_nps = ["ID venta", "Nombre del cliente", "Fecha", "Producto", "Asesor", "Calificación NPS (0-10)", "Tipo NPS"]
            st.dataframe(df_nps_view[cols_nps], use_container_width=True, hide_index=True, height=270)

# ==============================================================================
# MÓDULO 3: PRODUCCIÓN (PRONÓSTICOS, PAP, PMP, BOM, MRP, DRP)
# ==============================================================================
elif st.session_state.pagina == "3. Producción (PAP, PMP, MRP, DRP)":
    render_header_modulo(
        "⚙️ Planificación y Control de la Producción",
        "Pronósticos · Plan Agregado (PAP) · Plan Maestro (PMP) · BOM · MRP I/II · DRP"
    )

    tab_pron, tab_pap, tab_pmp, tab_bom, tab_mrp, tab_drp = st.tabs([
        "📈 Pronósticos",
        "🧮 Plan Agregado (PAP)",
        "📅 PMP Semanal",
        "🧬 BOM y Árbol",
        "🏭 MRP (Materiales y Capacidades)",
        "🚚 DRP Distribución"
    ])

    with tab_pron:
        df_hist, df_pron, df_metodos = load_forecast_data()

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Demanda Histórica (18m)", f"{df_hist['Total (und)'].sum():,} und")
        p2.metric("Demanda Proyectada (12m)", f"{df_pron['Total (und)'].sum():,} und")
        p3.metric("Ciabatta Proyectado (12m)", f"{df_pron['Pan Ciabatta (und)'].sum():,} und")
        p4.metric("Integral Proyectado (12m)", f"{df_pron['Pan Integral (und)'].sum():,} und")

        st.subheader("Evaluación de Métodos y Selección Estadística")
        st.dataframe(df_metodos, use_container_width=True, hide_index=True)

        df_h_plot = df_hist[["Mes Etiqueta", "Pan Ciabatta (und)", "Pan Integral (und)"]].copy()
        df_p_plot = df_pron[["Mes Etiqueta", "Pan Ciabatta (und)", "Pan Integral (und)"]].copy()

        fig_pron = go.Figure()
        fig_pron.add_trace(go.Scatter(
            x=df_h_plot["Mes Etiqueta"], y=df_h_plot["Pan Ciabatta (und)"],
            mode="lines+markers", name="Ciabatta — Histórico", line=dict(color="#3E2723", width=2.8)
        ))
        fig_pron.add_trace(go.Scatter(
            x=df_p_plot["Mes Etiqueta"], y=df_p_plot["Pan Ciabatta (und)"],
            mode="lines+markers", name="Ciabatta — Pronóstico", line=dict(color="#3E2723", width=2.8, dash="dash")
        ))
        fig_pron.add_trace(go.Scatter(
            x=df_h_plot["Mes Etiqueta"], y=df_h_plot["Pan Integral (und)"],
            mode="lines+markers", name="Integral — Histórico", line=dict(color="#C88A36", width=2.8)
        ))
        fig_pron.add_trace(go.Scatter(
            x=df_p_plot["Mes Etiqueta"], y=df_p_plot["Pan Integral (und)"],
            mode="lines+markers", name="Integral — Pronóstico", line=dict(color="#C88A36", width=2.8, dash="dash")
        ))
        fig_pron.update_layout(title="Evolución Histórica (18m) y Proyección de Ventas (12m)", xaxis_tickangle=-45, yaxis_title="Unidades")
        st.plotly_chart(style_fig(fig_pron, 370), use_container_width=True)

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("**Tabla 1: Histórico de Ventas (18 periodos)**")
            st.dataframe(
                df_hist[["Mes Etiqueta", "Periodo (t)", "Pan Ciabatta (lotes)", "Pan Integral (lotes)", "Pan Ciabatta (und)", "Pan Integral (und)", "Total (und)"]],
                use_container_width=True, hide_index=True, height=300
            )
        with col_t2:
            st.markdown("**Tabla 2: Pronóstico de Ventas (12 periodos)**")
            st.dataframe(
                df_pron[["Mes Etiqueta", "Pan Ciabatta (lotes)", "Pan Integral (lotes)", "Pan Ciabatta (und)", "Pan Integral (und)", "Total (und)"]],
                use_container_width=True, hide_index=True, height=300
            )

    with tab_pap:
        df_pap_res, plan_elegido, df_pap_desag = load_pap_data()
        st.success(f"🏆 **Estrategia Óptima Seleccionada:** {plan_elegido}")

        totales_row = df_pap_res[df_pap_res["Rubro de Costo / Recurso"].str.contains("Costo Total", case=False)].iloc[0]
        c_p1, c_p2, c_p3, c_p4 = st.columns(4)
        c_p1.metric("Plan 1 (Seleccionado)", f"S/ {totales_row.iloc[1]:,.2f}", delta="Menor Costo")
        c_p2.metric("Plan 2 (Inventario)", f"S/ {totales_row.iloc[2]:,.2f}")
        c_p3.metric("Plan 3 (Subcontratación)", f"S/ {totales_row.iloc[3]:,.2f}")
        c_p4.metric("Plan 4 (Tiempo Extra)", f"S/ {totales_row.iloc[4]:,.2f}")

        g_pap, t_pap = st.columns([1, 1.3])
        with g_pap:
            df_costos_plot = pd.DataFrame({
                "Plan": ["Plan 1 (Exacta)", "Plan 2 (Inventario)", "Plan 3 (Subcontrat.)", "Plan 4 (T. Extra)"],
                "Costo Total (S/)": [totales_row.iloc[1], totales_row.iloc[2], totales_row.iloc[3], totales_row.iloc[4]]
            })
            fig_pap = px.bar(
                df_costos_plot, x="Plan", y="Costo Total (S/)", text="Costo Total (S/)",
                color="Plan", title="Comparativa de Costos Totales por Plan (12 meses)",
                color_discrete_sequence=["#2E7D32", "#8D6E63", "#C88A36", "#5D4037"]
            )
            fig_pap.update_traces(texttemplate="S/ %{text:,.0f}", textposition="outside")
            fig_pap.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig_pap, 350), use_container_width=True)

        with t_pap:
            st.markdown("**Resumen Comparativo de Costos Totales por Estrategia (S/)**")
            st.dataframe(df_pap_res, use_container_width=True, hide_index=True)

        st.subheader("Desagregación Mensual del Plan Seleccionado (Base para PMP)")
        st.dataframe(df_pap_desag, use_container_width=True, hide_index=True)

    with tab_pmp:
        df_pmp_c, df_pmp_i = load_pmp_data()

        f_pmp1, f_pmp2 = st.columns(2)
        prod_pmp_sel = f_pmp1.selectbox(
            "Seleccionar Producto",
            ["Pan Ciabatta (PF-01)", "Pan Integral Multigrano (PF-02)", "Ambos Productos (Consolidado)"]
        )
        meses_pmp_lista = ["Todos los meses (24 semanas)"] + df_pmp_c["Mes"].unique().tolist()
        mes_pmp_sel = f_pmp2.selectbox("Filtrar por Mes", meses_pmp_lista)

        if prod_pmp_sel == "Pan Ciabatta (PF-01)":
            df_pmp_show = df_pmp_c.copy()
            df_pmp_show.insert(0, "Producto", "Pan Ciabatta")
        elif prod_pmp_sel == "Pan Integral Multigrano (PF-02)":
            df_pmp_show = df_pmp_i.copy()
            df_pmp_show.insert(0, "Producto", "Pan Integral Multigrano")
        else:
            c_tmp = df_pmp_c.copy()
            c_tmp.insert(0, "Producto", "Pan Ciabatta")
            i_tmp = df_pmp_i.copy()
            i_tmp.insert(0, "Producto", "Pan Integral Multigrano")
            df_pmp_show = pd.concat([c_tmp, i_tmp], ignore_index=True)

        if mes_pmp_sel != "Todos los meses (24 semanas)":
            df_pmp_show = df_pmp_show[df_pmp_show["Mes"] == mes_pmp_sel]

        m_pmp1, m_pmp2, m_pmp3 = st.columns(3)
        m_pmp1.metric("Requerimiento Total Filtrado", f"{df_pmp_show['Requerimiento (und)'].sum():,} und")
        m_pmp2.metric("Producción Programada PMP", f"{df_pmp_show['Producción PMP (und)'].sum():,} und")
        m_pmp3.metric("Lotes Programados (120 und)", f"{int(df_pmp_show['Producción PMP (und)'].sum() // 120):,} lotes")

        fig_pmp = px.bar(
            df_pmp_show,
            x="Semana",
            y="Producción PMP (und)",
            color="Producto",
            barmode="group",
            title=f"Programa Maestro de Producción (PMP) — {prod_pmp_sel}",
            color_discrete_map={"Pan Ciabatta": "#3E2723", "Pan Integral Multigrano": "#C88A36"}
        )
        st.plotly_chart(style_fig(fig_pmp, 330), use_container_width=True)
        st.dataframe(df_pmp_show, use_container_width=True, hide_index=True)

    with tab_bom:
        df_bom = load_bom_data()
        bom_prod_sel = st.radio(
            "Seleccione el Producto Terminado para desplegar su BOM y Árbol Estructural:",
            ["Pan Ciabatta (PF-01)", "Pan Integral Multigrano (PF-02)"],
            horizontal=True
        )

        if bom_prod_sel == "Pan Ciabatta (PF-01)":
            cods_pf01 = ["SE-01", "MP-01", "MP-03", "MP-04", "MP-05", "EM-01"]
            df_bom_f = df_bom[df_bom["Código"].isin(cods_pf01)][
                ["Código", "Descripción", "Unidad", "Por und Ciabatta", "Tanda Ciabatta (120 und)", "Stock Disp.", "Lead Time (sem)", "Se usa en"]
            ].copy()

            tree_data = [
                {"Nodo": "PF-01 Pan Ciabatta (1 und)", "Padre": "", "Detalle": "Nivel 0 · Producto Terminado", "Valor": 100},
                {"Nodo": "SE-01 Masa Madre (0.01 kg)", "Padre": "PF-01 Pan Ciabatta (1 und)", "Detalle": "Nivel 1 · Semielaborado", "Valor": 22},
                {"Nodo": "MP-01 Harina Trigo (0.04 kg)", "Padre": "PF-01 Pan Ciabatta (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 28},
                {"Nodo": "MP-03 Levadura (0.001 kg)", "Padre": "PF-01 Pan Ciabatta (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 12},
                {"Nodo": "MP-04 Sal de Mesa (0.001 kg)", "Padre": "PF-01 Pan Ciabatta (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 10},
                {"Nodo": "MP-05 Aceite Oliva (0.001 L)", "Padre": "PF-01 Pan Ciabatta (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 13},
                {"Nodo": "EM-01 Bolsa Kraft x6 (0.167 und)", "Padre": "PF-01 Pan Ciabatta (1 und)", "Detalle": "Nivel 1 · Empaque", "Valor": 15},
                {"Nodo": "MP-01 Harina p/ Masa Madre (0.333 kg/kg)", "Padre": "SE-01 Masa Madre (0.01 kg)", "Detalle": "Nivel 2 · Insumo Semielaborado", "Valor": 14},
                {"Nodo": "Agua Filtrada (0.667 L/kg)", "Padre": "SE-01 Masa Madre (0.01 kg)", "Detalle": "Nivel 2 · Insumo Base", "Valor": 8},
            ]
        else:
            cods_pf02 = ["SE-01", "MP-01", "MP-02", "MP-03", "MP-04", "MP-05", "MP-06", "EM-01"]
            df_bom_f = df_bom[df_bom["Código"].isin(cods_pf02)][
                ["Código", "Descripción", "Unidad", "Por und Integral", "Tanda Integral (120 und)", "Stock Disp.", "Lead Time (sem)", "Se usa en"]
            ].copy()

            tree_data = [
                {"Nodo": "PF-02 Pan Integral (1 und)", "Padre": "", "Detalle": "Nivel 0 · Producto Terminado", "Valor": 100},
                {"Nodo": "SE-01 Masa Madre (0.013 kg)", "Padre": "PF-02 Pan Integral (1 und)", "Detalle": "Nivel 1 · Semielaborado", "Valor": 18},
                {"Nodo": "MP-01 Harina Trigo (0.023 kg)", "Padre": "PF-02 Pan Integral (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 16},
                {"Nodo": "MP-02 Harina Integral (0.023 kg)", "Padre": "PF-02 Pan Integral (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 18},
                {"Nodo": "MP-06 Mezcla Linaza (0.003 kg)", "Padre": "PF-02 Pan Integral (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 12},
                {"Nodo": "MP-03 Levadura (0.001 kg)", "Padre": "PF-02 Pan Integral (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 9},
                {"Nodo": "MP-04 Sal de Mesa (0.001 kg)", "Padre": "PF-02 Pan Integral (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 8},
                {"Nodo": "MP-05 Aceite Oliva (0.001 L)", "Padre": "PF-02 Pan Integral (1 und)", "Detalle": "Nivel 1 · Materia Prima", "Valor": 9},
                {"Nodo": "EM-01 Bolsa Kraft x6 (0.167 und)", "Padre": "PF-02 Pan Integral (1 und)", "Detalle": "Nivel 1 · Empaque", "Valor": 10},
                {"Nodo": "MP-01 Harina p/ Masa Madre (0.333 kg/kg)", "Padre": "SE-01 Masa Madre (0.013 kg)", "Detalle": "Nivel 2 · Insumo Semielaborado", "Valor": 11},
                {"Nodo": "Agua Filtrada (0.667 L/kg)", "Padre": "SE-01 Masa Madre (0.013 kg)", "Detalle": "Nivel 2 · Insumo Base", "Valor": 7},
            ]

        b_col1, b_col2 = st.columns([1.15, 1])
        with b_col1:
            st.subheader(f"Lista de Materiales (BOM) — {bom_prod_sel}")
            st.dataframe(df_bom_f, use_container_width=True, hide_index=True)

        with b_col2:
            st.subheader("Árbol Estructural del Producto (Niveles 0, 1 y 2)")
            df_tree = pd.DataFrame(tree_data)
            fig_tree = px.sunburst(
                df_tree,
                names="Nodo",
                parents="Padre",
                values="Valor",
                hover_data=["Detalle"],
                color="Detalle",
                color_discrete_sequence=["#3E2723", "#C88A36", "#6D4C41", "#A1887F", "#D7CCC8"]
            )
            fig_tree.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=380)
            st.plotly_chart(fig_tree, use_container_width=True, key=f"sunburst_{bom_prod_sel}")

    with tab_mrp:
        df_tlo, df_boc, df_puestos, df_ruta, df_crp = load_mrp_data()

        sub_mat, sub_cap = st.tabs([
            "📦 Submódulo Materiales — Tabla de Lanzamiento de Órdenes (TLO)",
            "⚡ Submódulo Capacidades — CRP Detallado, BOC, Puestos y Ruta"
        ])

        with sub_mat:
            st.subheader("Tabla de Lanzamiento de Órdenes (TLO) — Horizonte Semanas 0 a 8")
            st.caption("Cantidades a liberar por semana en la unidad de medida de cada material (enlazado a Órdenes de Compra).")
            st.dataframe(df_tlo, use_container_width=True, hide_index=True)

        with sub_cap:
            crp_prod = df_crp[df_crp["Semana"] != "Sem 0"]
            pico_row = crp_prod.loc[crp_prod["Utilización (%)"].idxmax()]
            total_req_h = crp_prod["Horas Requeridas"].sum()
            total_disp_h = crp_prod["Horas Disponibles"].sum()
            util_prom_planta = (total_req_h / total_disp_h * 100) if total_disp_h > 0 else 0
            holgura_min_h = crp_prod["Holgura (h)"].min()

            c_k1, c_k2, c_k3, c_k4 = st.columns(4)
            c_k1.metric(
                "Cuello de Botella (Pico CRP)",
                f"{pico_row['Utilización (%)']:.1f}%",
                delta=f"{pico_row['Código']} {pico_row['Recurso']} ({pico_row['Semana']})"
            )
            c_k2.metric(
                "Utilización Media Planta (S1–S8)",
                f"{util_prom_planta:.1f}%",
                delta=f"{total_req_h:,.1f} h req / {total_disp_h:,.0f} h disp"
            )
            c_k3.metric(
                "Holgura Mínima Disponible",
                f"{holgura_min_h:.2f} h/sem",
                delta="Margen libre sin horas extra"
            )
            c_k4.metric(
                "Validación Factibilidad CRP",
                "100% VIABLE",
                delta="0 estaciones sobrecargadas"
            )

            st.subheader("1. Análisis Detallado de Necesidades de Capacidad (CRP — Semanas 0 a 8)")

            resumen_est_crp = crp_prod.groupby(["Código", "Estación", "Recurso", "Horas Disponibles"], as_index=False).agg(
                **{
                    "Prom. Req. (min/sem)": ("Req. Minutos", "mean"),
                    "Prom. Req. (h/sem)": ("Horas Requeridas", "mean"),
                    "Pico Máx. (h/sem)": ("Horas Requeridas", "max"),
                    "Holgura Mín. (h/sem)": ("Holgura (h)", "min"),
                    "Utilización Prom. (%)": ("Utilización (%)", "mean"),
                    "Utilización Pico (%)": ("Utilización (%)", "max"),
                }
            )
            for col_r in ["Prom. Req. (min/sem)", "Prom. Req. (h/sem)", "Pico Máx. (h/sem)", "Holgura Mín. (h/sem)"]:
                resumen_est_crp[col_r] = resumen_est_crp[col_r].round(2)
            resumen_est_crp["Utilización Prom. (%)"] = resumen_est_crp["Utilización Prom. (%)"].round(1)
            resumen_est_crp["Utilización Pico (%)"] = resumen_est_crp["Utilización Pico (%)"].round(1)
            resumen_est_crp["Diagnóstico Operativo"] = resumen_est_crp["Utilización Pico (%)"].apply(
                lambda u: "⚠️ Estación Crítica (Monitorear)" if u >= 80 else ("✅ Carga Balanceada" if u >= 40 else "🟢 Amplia Holgura")
            )

            st.markdown("**Resumen Ejecutivo de Carga y Holgura por Estación de Trabajo (Semanas Productivas 1–8)**")
            st.dataframe(resumen_est_crp, use_container_width=True, hide_index=True)

            f_crp1, f_crp2 = st.columns(2)
            sem_crp_sel = f_crp1.selectbox(
                "Filtrar detalle semanal CRP:",
                ["Todas las semanas (Sem 0 – Sem 8)"] + df_crp["Semana"].unique().tolist()
            )
            est_crp_sel = f_crp2.selectbox(
                "Filtrar por Centro / Recurso:",
                ["Todos los centros"] + df_crp["Centro / Recurso"].unique().tolist()
            )

            df_crp_view = df_crp.copy()
            if not sem_crp_sel.startswith("Todas"):
                df_crp_view = df_crp_view[df_crp_view["Semana"] == sem_crp_sel]
            if est_crp_sel != "Todos los centros":
                df_crp_view = df_crp_view[df_crp_view["Centro / Recurso"] == est_crp_sel]

            g_crp1, g_crp2 = st.columns(2)
            with g_crp1:
                fig_crp = px.line(
                    df_crp,
                    x="Semana",
                    y="Utilización (%)",
                    color="Centro / Recurso",
                    markers=True,
                    title="Evolución Semanal de Utilización de Capacidad (%)"
                )
                fig_crp.add_hline(y=100, line_dash="dot", line_color="red", annotation_text="Límite Capacidad (100%)")
                fig_crp.update_layout(yaxis_range=[0, 110])
                st.plotly_chart(style_fig(fig_crp, 350), use_container_width=True)

            with g_crp2:
                fig_crp_bar = go.Figure()
                fig_crp_bar.add_trace(go.Bar(
                    name="Horas Disponibles / sem",
                    x=resumen_est_crp["Código"] + " (" + resumen_est_crp["Recurso"] + ")",
                    y=resumen_est_crp["Horas Disponibles"],
                    marker_color="#D7CCC8"
                ))
                fig_crp_bar.add_trace(go.Bar(
                    name="Pico Horas Requeridas / sem",
                    x=resumen_est_crp["Código"] + " (" + resumen_est_crp["Recurso"] + ")",
                    y=resumen_est_crp["Pico Máx. (h/sem)"],
                    marker_color="#3E2723"
                ))
                fig_crp_bar.update_layout(
                    barmode="overlay",
                    title="Capacidad Disponible vs. Pico Requerido por Recurso (h/sem)",
                    yaxis_title="Horas / semana"
                )
                st.plotly_chart(style_fig(fig_crp_bar, 350), use_container_width=True)

            st.markdown("**Tabla Detallada de Carga CRP (Minutos, Horas Requeridas, Disponibles, Holgura y Estado)**")
            cols_crp_show = [
                "Semana", "Código", "Estación", "Recurso", "Req. Minutos",
                "Horas Requeridas", "Horas Disponibles", "Holgura (h)",
                "Utilización (%)", "Nivel de Carga", "¿Hay Capacidad?"
            ]
            st.dataframe(df_crp_view[cols_crp_show], use_container_width=True, hide_index=True, height=270)

            c_mrp1, c_mrp2 = st.columns(2)
            with c_mrp1:
                st.subheader("2. Tabla de Capacidades (BOC — min/und)")
                st.dataframe(df_boc[df_boc.iloc[:, 1:].sum(axis=1) > 0], use_container_width=True, hide_index=True)
            with c_mrp2:
                st.subheader("3. Lista de Puestos de Trabajo")
                st.dataframe(
                    df_puestos[["Código", "Puesto de Trabajo", "N° Operarios", "N° Máquinas", "Disp. Hombre (h/sem)", "Disp. Equipo (h/sem)"]],
                    use_container_width=True, hide_index=True
                )

            st.subheader("4. Hoja de Ruta Completa (Productos, Semielaborados e Insumos)")
            cods_ruta = ["Todos"] + sorted(df_ruta["Producto"].dropna().unique().tolist())
            filtro_ruta = st.radio("Filtrar Hoja de Ruta por Código:", cods_ruta, horizontal=True)
            df_ruta_view = df_ruta if filtro_ruta == "Todos" else df_ruta[df_ruta["Producto"] == filtro_ruta]
            st.dataframe(df_ruta_view, use_container_width=True, hide_index=True)

    with tab_drp:
        drp_dict = load_drp_data()
        drp_prod_sel = st.selectbox("Seleccionar Producto para Plan de Distribución (DRP):", list(drp_dict.keys()))
        info_drp = drp_dict[drp_prod_sel]

        st.subheader(f"Resumen Semanal de Envíos — {drp_prod_sel} (Mes: {info_drp['mes']})")
        st.dataframe(info_drp["resumen"], use_container_width=True, hide_index=True)

        df_drp_plot = info_drp["resumen"][info_drp["resumen"]["Semana"] != "Total Mes"]
        fig_drp = px.bar(
            df_drp_plot,
            x="Semana",
            y=["Café Yayi's (CAF) - Envíos Planificados (und)", "Delivery & Corp (DLV) - Envíos Planificados (und)"],
            barmode="group",
            title=f"Envíos Planificados Semanales por Canal de Distribución — {drp_prod_sel}",
            color_discrete_sequence=["#3E2723", "#C88A36"]
        )
        fig_drp.update_layout(yaxis_title="Unidades a Enviar")
        st.plotly_chart(style_fig(fig_drp, 330), use_container_width=True)

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.markdown("**Detalle DRP — Canal Café Yayi's (CAF)**")
            st.dataframe(info_drp["caf"], use_container_width=True, hide_index=True)
        with d_col2:
            st.markdown("**Detalle DRP — Canal Delivery y Corporativos (DLV)**")
            st.dataframe(info_drp["dlv"], use_container_width=True, hide_index=True)

# ==============================================================================
# MÓDULO 4: INVENTARIOS
# ==============================================================================
elif st.session_state.pagina == "4. Inventarios":
    render_header_modulo(
        "📦 Gestión de Inventarios",
        "Control del Maestro de Materiales, niveles de stock valorizado y alta de nuevos insumos"
    )

    df_inv = load_inventory_data()

    tab_stock, tab_alta_mat = st.tabs([
        "🔍 Consultar Stock y Valorización",
        "➕ Registrar Nuevos Materiales"
    ])

    with tab_stock:
        insumos_df = df_inv[df_inv["Tipo"] != "Producto terminado"]
        valor_total = insumos_df["Valorizado (S/)"].sum()
        alertas_count = int((insumos_df["Inventario disponible"] <= insumos_df["Stock de seguridad"]).sum())

        i1, i2, i3, i4 = st.columns(4)
        i1.metric("Ítems en Maestro", f"{len(df_inv)} materiales")
        i2.metric("Materias Primas / Empaques", f"{len(insumos_df)} ítems")
        i3.metric("Valorización de Inventario", f"S/ {valor_total:,.2f}")
        i4.metric("Alertas de Reposición", f"{alertas_count} ítems")

        col_f1, col_f2 = st.columns(2)
        sel_tipo_mat = col_f1.selectbox("Filtrar por Tipo de Material", ["Todos"] + sorted(df_inv["Tipo"].unique().tolist()))
        busqueda_mat = col_f2.text_input("Buscar por Código o Descripción", placeholder="Ej. MP-01 o Harina...")

        df_inv_view = df_inv.copy()
        if sel_tipo_mat != "Todos":
            df_inv_view = df_inv_view[df_inv_view["Tipo"] == sel_tipo_mat]
        if busqueda_mat.strip():
            q = busqueda_mat.strip().lower()
            df_inv_view = df_inv_view[
                df_inv_view["Código"].str.lower().str.contains(q) |
                df_inv_view["Descripción"].str.lower().str.contains(q)
            ]

        cols_inv = [
            "Código", "Descripción", "Tipo", "Unidad de medida",
            "Inventario disponible", "Stock de seguridad", "Estado Stock",
            "Lead time (semanas)", "Tamaño de lote", "Costo Display",
            "Valorizado (S/)", "Proveedor / Origen"
        ]
        st.dataframe(df_inv_view[cols_inv], use_container_width=True, hide_index=True)

        fig_inv = px.bar(
            insumos_df,
            x="Descripción",
            y=["Inventario disponible", "Stock de seguridad"],
            barmode="group",
            title="Comparativa: Stock Disponible vs. Stock de Seguridad por Insumo",
            color_discrete_sequence=["#3E2723", "#D49A42"]
        )
        fig_inv.update_layout(xaxis_title="", yaxis_title="Cantidad")
        st.plotly_chart(style_fig(fig_inv, 350), use_container_width=True)

    with tab_alta_mat:
        st.subheader("Alta de Nuevo Material en Maestro de Materiales")
        with st.form("form_nuevo_material", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            cod_mat = c1.text_input("Código del Material *", placeholder="Ej. MP-07")
            desc_mat = c2.text_input("Descripción *", placeholder="Ej. Semillas de ajonjolí")
            tipo_mat = c3.selectbox("Tipo *", ["Materia prima", "Semielaborado", "Empaque", "Producto terminado"])

            c4, c5, c6 = st.columns(3)
            unidad_mat = c4.selectbox("Unidad de Medida *", ["kg", "L", "und", "g", "mL"])
            nivel_llc = c5.number_input("Nivel (LLC)", min_value=0, max_value=5, value=1)
            costo_u = c6.number_input("Costo Unitario (S/) *", min_value=0.0, value=10.0, step=0.1)

            c7, c8, c9 = st.columns(3)
            inv_ini = c7.number_input("Inventario Disponible Inicial *", min_value=0.0, value=20.0, step=1.0)
            stock_s = c8.number_input("Stock de Seguridad *", min_value=0.0, value=5.0, step=1.0)
            tam_lote = c9.number_input("Tamaño de Lote *", min_value=0.1, value=10.0, step=1.0)

            c10, c11, c12 = st.columns(3)
            lt_dias = c10.number_input("Lead Time (días hábiles)", min_value=0, max_value=30, value=2)
            lt_sem = c11.number_input("Lead Time (semanas)", min_value=0, max_value=8, value=1)
            pres_lote = c12.text_input("Presentación / Lote", placeholder="Ej. Bolsa 10 kg")

            c13, c14 = st.columns(2)
            prov_mat = c13.text_input("Proveedor / Origen *", placeholder="Ej. Harinas & Granos del Norte")
            uso_mat = c14.text_input("Se utiliza en *", placeholder="Ej. PF-02")

            btn_mat = st.form_submit_button("💾 Registrar Material en Excel", type="primary", use_container_width=True)
            if btn_mat:
                if not cod_mat.strip() or not desc_mat.strip() or not prov_mat.strip():
                    st.warning("Complete los campos obligatorios marcados con *.")
                else:
                    try:
                        cod_creado = add_new_material(
                            cod_mat, desc_mat, tipo_mat, unidad_mat, nivel_llc,
                            inv_ini, stock_s, lt_dias, lt_sem, tam_lote,
                            pres_lote or f"Lote {tam_lote} {unidad_mat}", costo_u, prov_mat, uso_mat or "General"
                        )
                        st.success(f"✅ Material **{cod_creado} — {desc_mat}** registrado correctamente.")
                        st.rerun()
                    except PermissionError:
                        st.error("⚠️ Cierra el archivo Excel antes de registrar un nuevo material.")
                    except Exception as err:
                        st.error(f"No se pudo guardar: {err}")

# ==============================================================================
# MÓDULO 5: COMPRAS Y PROVEEDORES
# ==============================================================================
elif st.session_state.pagina == "5. Compras y Proveedores":
    render_header_modulo(
        "🛒 Compras y Evaluación de Proveedores",
        "Trazabilidad de órdenes de compra (OC) y servicio (OS) vinculadas al MRP y directorio homologado"
    )

    df_oc, df_pr = load_purchasing_data()

    tab_oc, tab_pr = st.tabs([
        "📄 Órdenes de Compra y Servicio",
        "🏭 Directorio y Calificación de Proveedores"
    ])

    with tab_oc:
        total_oc = len(df_oc)
        cant_compra = int((df_oc["Tipo"] == "Compra").sum())
        cant_servicio = int((df_oc["Tipo"] == "Servicio").sum())
        monto_valido = df_oc[df_oc["Estado"] != "Rechazado"]["Monto (S/)"].sum()
        oc_aprob_ejec = int(df_oc["Estado"].isin(["Aprobado", "Ejecutado"]).sum())

        o1, o2, o3, o4 = st.columns(4)
        o1.metric("Total Órdenes (OC + OS)", f"{total_oc} órdenes", delta=f"{cant_compra} Compras · {cant_servicio} Servicios")
        o2.metric("Monto Comprometido Activo", f"S/ {monto_valido:,.2f}")
        o3.metric("Aprobadas / Ejecutadas", f"{oc_aprob_ejec} órdenes")
        o4.metric("Órdenes de Servicio (OS)", f"{cant_servicio} servicios", delta=f"S/ {df_oc[df_oc['Tipo']=='Servicio']['Monto (S/)'].sum():,.2f}")

        f_oc1, f_oc2, f_oc3 = st.columns(3)
        sel_est_oc = f_oc1.selectbox("Estado de Orden", ["Todos", "En proceso", "Aprobado", "Ejecutado", "Rechazado"])
        sel_tipo_oc = f_oc2.selectbox("Tipo de Orden", ["Todos", "Compra", "Servicio"])
        sel_area_oc = f_oc3.selectbox("Área Usuaria", ["Todos"] + sorted(df_oc["Área usuaria"].unique().tolist()))

        df_oc_view = df_oc.copy()
        if sel_est_oc != "Todos":
            df_oc_view = df_oc_view[df_oc_view["Estado"] == sel_est_oc]
        if sel_tipo_oc != "Todos":
            df_oc_view = df_oc_view[df_oc_view["Tipo"] == sel_tipo_oc]
        if sel_area_oc != "Todos":
            df_oc_view = df_oc_view[df_oc_view["Área usuaria"] == sel_area_oc]

        cols_oc = [
            "N° de orden", "Fecha de emisión", "Proveedor", "Tipo",
            "Producto o servicio", "Cantidad", "Unidad", "Monto (S/)",
            "Área usuaria", "Estado"
        ]
        st.dataframe(df_oc_view[cols_oc], use_container_width=True, hide_index=True)

        g_oc1, g_oc2 = st.columns(2)
        with g_oc1:
            res_est_oc = df_oc.groupby("Estado")["Monto (S/)"].sum().reset_index()
            fig_oc1 = px.bar(
                res_est_oc, x="Estado", y="Monto (S/)", color="Estado", text="Monto (S/)",
                title="Monto Total por Estado de Orden (S/)",
                color_discrete_map={
                    "Ejecutado": "#2E7D32",
                    "Aprobado": "#1565C0",
                    "En proceso": "#C88A36",
                    "Rechazado": "#C62828"
                }
            )
            fig_oc1.update_traces(texttemplate="S/ %{text:,.0f}", textposition="outside")
            fig_oc1.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig_oc1, 320), use_container_width=True)

        with g_oc2:
            res_tipo_oc = df_oc.groupby("Tipo")["Monto (S/)"].sum().reset_index()
            fig_oc2 = px.pie(
                res_tipo_oc, names="Tipo", values="Monto (S/)", hole=0.5,
                title="Distribución Presupuestal: Compra (OC) vs. Servicio (OS)",
                color="Tipo",
                color_discrete_map={"Compra": "#3E2723", "Servicio": "#C88A36"}
            )
            st.plotly_chart(style_fig(fig_oc2, 320), use_container_width=True)

    with tab_pr:
        p1, p2, p3 = st.columns(3)
        p1.metric("Proveedores Homologados", f"{len(df_pr)} proveedores")
        p2.metric("Calificación Promedio", f"{df_pr['Calificación'].mean():.2f} / 5.00")
        p3.metric("Clase A (Preferentes ≥ 4.3)", f"{int((df_pr['Clasificación'] == 'A').sum())} proveedores")

        f_pr1, f_pr2 = st.columns(2)
        sel_clas = f_pr1.selectbox("Filtrar por Clasificación", ["Todos", "A", "B", "C"])
        sel_tipo_pr = f_pr2.selectbox("Tipo de Provisión", ["Todos", "Producto", "Servicio"])

        df_pr_view = df_pr.copy()
        if sel_clas != "Todos":
            df_pr_view = df_pr_view[df_pr_view["Clasificación"] == sel_clas]
        if sel_tipo_pr != "Todos":
            df_pr_view = df_pr_view[df_pr_view["Tipo"] == sel_tipo_pr]

        cols_pr = [
            "Código", "Nombre del proveedor", "Tipo", "Producto o servicio que provee",
            "Celular", "Correo", "Nombre del contacto", "Calificación", "Clasificación"
        ]
        st.dataframe(df_pr_view[cols_pr], use_container_width=True, hide_index=True)

        fig_pr = px.bar(
            df_pr.sort_values("Calificación", ascending=True),
            x="Calificación",
            y="Nombre del proveedor",
            orientation="h",
            color="Clasificación",
            text="Calificación",
            title="Ranking de Evaluación de Proveedores (Escala 1 a 5)",
            color_discrete_map={"A": "#2E7D32", "B": "#E09F3E", "C": "#C62828"}
        )
        fig_pr.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_pr.update_layout(xaxis_range=[0, 5.5])
        st.plotly_chart(style_fig(fig_pr, 420), use_container_width=True)

# ==============================================================================
# MÓDULO 6: DASHBOARD EJECUTIVO (4 INDICADORES ESTRATÉGICOS POR MÓDULO)
# ==============================================================================
elif st.session_state.pagina == "6. Dashboard Ejecutivo":
    render_header_modulo(
        "📊 Dashboard Ejecutivo de Control Gerencial",
        "4 Indicadores Clave de Desempeño (KPIs) integrados: Módulo 2 (Comercial), Módulo 3 (Producción & CRP) y Módulos 4–5 (Abastecimiento)"
    )

    df_clientes = load_crm_data()
    df_atc, kpis_nps = load_nps_data()
    df_hist, df_pron, _ = load_forecast_data()
    df_pap_res, _, _ = load_pap_data()
    _, _, _, _, df_crp = load_mrp_data()
    df_inv = load_inventory_data()
    df_oc, df_pr = load_purchasing_data()

    ventas_crm = int((df_clientes["Estado"] == "Venta").sum())
    tasa_conv = (ventas_crm / len(df_clientes) * 100) if len(df_clientes) > 0 else 0
    ingresos_atc = df_atc["Importe (S/)"].sum()

    demanda_anual_pron = int(df_pron["Total (und)"].sum())
    costo_pap_optimo = float(df_pap_res[df_pap_res["Rubro de Costo / Recurso"].str.contains("Costo Total", case=False)].iloc[0, 1])

    crp_prod = df_crp[df_crp["Semana"] != "Sem 0"]
    pico_crp_row = crp_prod.loc[crp_prod["Utilización (%)"].idxmax()]
    util_media_crp = (crp_prod["Horas Requeridas"].sum() / crp_prod["Horas Disponibles"].sum() * 100)

    insumos_df = df_inv[df_inv["Tipo"] != "Producto terminado"]
    val_inventario = insumos_df["Valorizado (S/)"].sum()
    oc_activas = int(df_oc["Estado"].isin(["Aprobado", "Ejecutado"]).sum())
    tasa_cumpl_oc = (oc_activas / len(df_oc) * 100) if len(df_oc) > 0 else 0

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="saas-kpi">
            <div class="saas-kpi-top">
                <span class="saas-kpi-title">Indicador 1 · Lealtad NPS</span>
                <span class="saas-kpi-badge">Módulo 2 · CRM/ATC</span>
            </div>
            <div class="saas-kpi-num">{kpis_nps['nps_score']:.2f} pts</div>
            <div class="saas-kpi-sub"><b>Conversión CRM:</b> {tasa_conv:.1f}% ({ventas_crm}/{len(df_clientes)} leads) · <b>Ventas ATC:</b> S/ {ingresos_atc:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="saas-kpi">
            <div class="saas-kpi-top">
                <span class="saas-kpi-title">Indicador 2 · Plan Maestro (12m)</span>
                <span class="saas-kpi-badge">Módulo 3 · PAP/PMP</span>
            </div>
            <div class="saas-kpi-num">{demanda_anual_pron:,} und</div>
            <div class="saas-kpi-sub"><b>Costo PAP Óptimo:</b> S/ {costo_pap_optimo:,.2f} (Plan 1 Fuerza Exacta · 976 lotes)</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="saas-kpi">
            <div class="saas-kpi-top">
                <span class="saas-kpi-title">Indicador 3 · Capacidad CRP</span>
                <span class="saas-kpi-badge">Módulo 3 · MRP II</span>
            </div>
            <div class="saas-kpi-num">{pico_crp_row['Utilización (%)']:.1f}% Pico</div>
            <div class="saas-kpi-sub"><b>Cuello Botella:</b> {pico_crp_row['Código']} {pico_crp_row['Recurso']} · <b>Media Planta:</b> {util_media_crp:.1f}% (0% sobrecarga)</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="saas-kpi">
            <div class="saas-kpi-top">
                <span class="saas-kpi-title">Indicador 4 · Abastecimiento</span>
                <span class="saas-kpi-badge">Módulos 4 y 5</span>
            </div>
            <div class="saas-kpi-num">{tasa_cumpl_oc:.1f}% OC/OS</div>
            <div class="saas-kpi-sub"><b>Órdenes Activas:</b> {oc_activas}/{len(df_oc)} · <b>Stock Valorizado:</b> S/ {val_inventario:,.2f} (0 quiebres)</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    g1, g2 = st.columns(2)
    with g1:
        df_nps_seg = pd.DataFrame({
            "Segmento": ["Promotores (9-10)", "Pasivos (7-8)", "Detractores (0-6)"],
            "Encuestas": [kpis_nps["promotores"], kpis_nps["pasivos"], kpis_nps["detractores"]]
        })
        fig_d1 = px.bar(
            df_nps_seg,
            x="Segmento",
            y="Encuestas",
            color="Segmento",
            text="Encuestas",
            title="Indicador 1 (Módulo 2): Composición de Lealtad NPS y Satisfacción",
            color_discrete_map={
                "Promotores (9-10)": "#2E7D32",
                "Pasivos (7-8)": "#C88A36",
                "Detractores (0-6)": "#C62828"
            }
        )
        fig_d1.update_traces(textposition="outside")
        fig_d1.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig_d1, 340), use_container_width=True)

    with g2:
        df_pron_melt = df_pron.melt(
            id_vars=["Mes Etiqueta"],
            value_vars=["Pan Ciabatta (und)", "Pan Integral (und)"],
            var_name="Producto",
            value_name="Unidades"
        )
        fig_d2 = px.area(
            df_pron_melt,
            x="Mes Etiqueta",
            y="Unidades",
            color="Producto",
            title="Indicador 2 (Módulo 3): Proyección de Producción Mensual (12m)",
            color_discrete_map={"Pan Ciabatta (und)": "#3E2723", "Pan Integral (und)": "#C88A36"}
        )
        fig_d2.update_layout(xaxis_tickangle=-45, xaxis_title="")
        st.plotly_chart(style_fig(fig_d2, 340), use_container_width=True)

    g3, g4 = st.columns(2)
    with g3:
        df_crp_max = crp_prod.groupby("Centro / Recurso")["Utilización (%)"].max().reset_index()
        fig_d3 = px.bar(
            df_crp_max.sort_values("Utilización (%)", ascending=True),
            x="Utilización (%)",
            y="Centro / Recurso",
            orientation="h",
            text="Utilización (%)",
            title="Indicador 3 (Módulo 3): Utilización Pico de Capacidad CRP por Estación (%)",
            color_discrete_sequence=["#5D4037"]
        )
        fig_d3.add_vline(x=100, line_dash="dot", line_color="red", annotation_text="Capacidad Máx.")
        fig_d3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_d3.update_layout(xaxis_range=[0, 112], yaxis_title="")
        st.plotly_chart(style_fig(fig_d3, 340), use_container_width=True)

    with g4:
        df_oc_tipo = df_oc.groupby(["Tipo", "Estado"])["Monto (S/)"].sum().reset_index()
        fig_d4 = px.bar(
            df_oc_tipo,
            x="Tipo",
            y="Monto (S/)",
            color="Estado",
            text="Monto (S/)",
            barmode="stack",
            title="Indicador 4 (Módulo 5): Presupuesto de Compras (OC) vs. Servicios (OS)",
            color_discrete_map={
                "Ejecutado": "#2E7D32",
                "Aprobado": "#1565C0",
                "En proceso": "#C88A36",
                "Rechazado": "#C62828"
            }
        )
        fig_d4.update_traces(texttemplate="S/ %{text:,.0f}", textposition="inside")
        st.plotly_chart(style_fig(fig_d4, 340), use_container_width=True)