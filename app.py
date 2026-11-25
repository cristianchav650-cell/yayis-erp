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

# Configuración de página
st.set_page_config(
    page_title="YAYI'S ERP | Gestión Integral de Operaciones",
    page_icon="🥖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS corporativos
st.markdown("""
<style>
    .stApp {
        background-color: #FAF6F0;
    }
    section[data-testid="stSidebar"] {
        background-color: #2C1E1B;
    }
    section[data-testid="stSidebar"] * {
        color: #FAF6F0 !important;
    }
    .hero-banner {
        background: linear-gradient(135deg, #3E2723 0%, #5D4037 65%, #8D6E63 100%);
        padding: 2.2rem;
        border-radius: 14px;
        color: #FFFFFF;
        border-left: 8px solid #D49A42;
        box-shadow: 0 6px 18px rgba(62, 39, 35, 0.18);
        margin-bottom: 1.5rem;
    }
    .hero-banner h1 {
        color: #FFF8E7 !important;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
    }
    .hero-banner p {
        color: #EBDCCB !important;
        font-size: 1.05rem;
        margin-top: 0.4rem;
    }
    .kpi-card {
        background-color: #FFFFFF;
        padding: 1.2rem 1.4rem;
        border-radius: 12px;
        border-top: 4px solid #C88A36;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        height: 100%;
    }
    .kpi-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #795548;
        font-weight: 700;
    }
    .kpi-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #3E2723;
        margin-top: 0.25rem;
    }
    .section-box {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E6DCD0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

def ir_a(destino):
    st.session_state.pagina = destino

def render_header_modulo(titulo, subtitulo=""):
    top_col1, top_col2 = st.columns([5, 1])
    with top_col1:
        st.title(titulo)
        if subtitulo:
            st.caption(subtitulo)
    with top_col2:
        st.write("")
        if st.button("🏠 Menú Principal", key=f"btn_home_{titulo}", use_container_width=True):
            ir_a("Inicio")
            st.rerun()

# Carga base
try:
    meta_acad, empresa = load_company_info()
    productos_data = load_products_and_dap()
except Exception as e:
    st.error(f"Error al conectar con el archivo Excel: {e}")
    st.stop()

# Barra lateral
with st.sidebar:
    st.markdown("## 🥖 YAYI'S ERP")
    st.caption("Masa Madre & Café · Cajamarca")
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
        "Módulos del Sistema",
        opciones_menu,
        index=opciones_menu.index(st.session_state.pagina)
    )
    if seleccion != st.session_state.pagina:
        st.session_state.pagina = seleccion
        st.rerun()

    st.divider()
    st.markdown(f"**Curso:** {meta_acad['curso']}")
    st.markdown(f"**Docente:** {meta_acad['docente']}")
    st.caption(f"{meta_acad['universidad']} · {meta_acad['anio']}")

# ==============================================================================
# PANTALLA DE INICIO
# ==============================================================================
if st.session_state.pagina == "Inicio":
    st.markdown(f"""
    <div class="hero-banner">
        <div style="font-size:0.85rem; letter-spacing:0.12em; text-transform:uppercase; color:#F5C26B; font-weight:700;">
            Sistema de Planificación de Recursos Empresariales
        </div>
        <h1>YAYI'S ERP — {empresa['nombre_comercial'].upper()}</h1>
        <p>Plataforma integrada de gestión comercial, planificación de la producción, inventarios y abastecimiento.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Nombre Comercial</div><div class="kpi-value">{empresa["nombre_comercial"].title()}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">RUC Activo</div><div class="kpi-value">{empresa["ruc"]}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="kpi-card"><div class="kpi-label">Línea Principal</div><div class="kpi-value">2 Panes Masa Madre</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="kpi-card"><div class="kpi-label">Sede Operativa</div><div class="kpi-value">San José, Cajamarca</div></div>', unsafe_allow_html=True)

    st.markdown("### Acceso Rápido a Módulos")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        with st.container(border=True):
            st.markdown("#### 🏢 Módulo 1: Información")
            st.write("Identidad corporativa, ubicación, fichas técnicas y Diagrama de Análisis del Proceso (DAP).")
            if st.button("Ingresar a Información →", use_container_width=True, type="primary"):
                ir_a("1. Información General")
                st.rerun()

        with st.container(border=True):
            st.markdown("#### 📦 Módulo 4: Inventarios")
            st.write("Maestro de materiales, consulta de stock disponible, stock de seguridad y registro de insumos.")
            if st.button("Ingresar a Inventarios →", use_container_width=True, type="primary"):
                ir_a("4. Inventarios")
                st.rerun()

    with col_b:
        with st.container(border=True):
            st.markdown("#### 🤝 Módulo 2: CRM y ATC")
            st.write("Gestión de leads, registro de prospectos, seguimiento de ventas y medición de satisfacción NPS.")
            if st.button("Ingresar a CRM →", use_container_width=True, type="primary"):
                ir_a("2. CRM y Atención al Cliente")
                st.rerun()

        with st.container(border=True):
            st.markdown("#### 🛒 Módulo 5: Compras y Proveedores")
            st.write("Control de órdenes de compra/servicio (OC), estados de aprobación y evaluación de proveedores.")
            if st.button("Ingresar a Compras →", use_container_width=True, type="primary"):
                ir_a("5. Compras y Proveedores")
                st.rerun()

    with col_c:
        with st.container(border=True):
            st.markdown("#### ⚙️ Módulo 3: Producción")
            st.write("Pronósticos, PAP, PMP semanal, BOM, MRP I/II (capacidades y ruta) y DRP por canal.")
            if st.button("Ingresar a Producción →", use_container_width=True, type="primary"):
                ir_a("3. Producción (PAP, PMP, MRP, DRP)")
                st.rerun()

        with st.container(border=True):
            st.markdown("#### 📊 Módulo 6: Dashboard")
            st.write("Tablero gerencial con indicadores clave (KPIs) consolidados de CRM, Producción y Logística.")
            if st.button("Ingresar a Dashboard →", use_container_width=True, type="primary"):
                ir_a("6. Dashboard Ejecutivo")
                st.rerun()

    with st.expander("🎓 Créditos Académicos del Equipo — Universidad Privada del Norte"):
        st.write(f"**Docente:** {meta_acad['docente']}")
        st.write("**Integrantes del Grupo 1:** " + " · ".join(meta_acad["integrantes"]))

# ==============================================================================
# MÓDULO 1: INFORMACIÓN
# ==============================================================================
elif st.session_state.pagina == "1. Información General":
    render_header_modulo("🏢 Módulo 1: Información Institucional y Productos")

    tab_emp, tab_p1, tab_p2 = st.tabs([
        "📋 Perfil de la Empresa",
        "🥖 Producto 1: Pan Ciabatta (PF-01)",
        "🌾 Producto 2: Pan Integral Multigrano (PF-02)"
    ])

    with tab_emp:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)

    def render_producto(codigo):
        info = productos_data[codigo]
        ficha = info["ficha"]
        dap = info["dap"]
        resumen = info["resumen"]

        st.subheader(f"Ficha Técnica: {ficha['Nombre del producto']} ({ficha['Código']})")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Precio de Venta", f"S/ {float(ficha['Precio de venta (datos de la carta)']):.2f} / und")
        m2.metric("Lote de Producción", ficha["Lote de producción"].split("·")[0].strip())
        m3.metric("Frecuencia Diaria", ficha["Lote de producción"].split("·")[1].strip())
        m4.metric("Vida Útil", "1 día (Fresco del día)")

        with st.container(border=True):
            c_left, c_right = st.columns(2)
            with c_left:
                st.markdown(f"**Descripción:** {ficha['Descripción']}")
                st.markdown(f"**Presentación:** {ficha['Presentación']}")
            with c_right:
                st.markdown(f"**Uso / Aplicación en Carta:** {ficha['Uso / aplicación']}")
                st.markdown(f"**Insumos Principales:** {ficha['Insumos principales']}")

        st.subheader("Proceso de Fabricación — Diagrama de Análisis del Proceso (DAP)")
        g1, g2 = st.columns([1.1, 1])

        resumen_sin_total = resumen[resumen["Tipo de Actividad"] != "TOTAL"]
        with g1:
            fig_t = px.bar(
                resumen_sin_total,
                x="Tipo de Actividad",
                y="Tiempo (min)",
                color="Tipo de Actividad",
                text="Tiempo (min)",
                title="Tiempo por Tipo de Actividad (min / tanda 120 und)",
                color_discrete_sequence=["#5D4037", "#C88A36", "#8D6E63", "#BCAAA4", "#3E2723"]
            )
            fig_t.update_traces(texttemplate="%{text:.2f} min", textposition="outside")
            fig_t.update_layout(showlegend=False, plot_bgcolor="white", height=340)
            st.plotly_chart(fig_t, use_container_width=True)

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
        "🤝 Módulo 2: CRM y Atención al Cliente (ATC)",
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

        g_col1, g_col2 = st.columns([1.2, 1])
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
                    "Pendiente": "#8D6E63",
                    "Descartado": "#B71C1C"
                }
            )
            fig_est.update_traces(textposition="outside")
            fig_est.update_layout(showlegend=False, plot_bgcolor="white", height=320)
            st.plotly_chart(fig_est, use_container_width=True)

        with g_col2:
            resumen_asesor = df_clientes.groupby(["Asesor asignado", "Estado"]).size().reset_index(name="Clientes")
            fig_as = px.bar(
                resumen_asesor,
                x="Asesor asignado",
                y="Clientes",
                color="Estado",
                title="Cartera Asignada por Asesor Comercial",
                barmode="stack"
            )
            fig_as.update_layout(plot_bgcolor="white", height=320)
            st.plotly_chart(fig_as, use_container_width=True)

        st.subheader("Listado de Atención de Leads")
        f1, f2, f3 = st.columns(3)
        estados_disp = ["Todos"] + sorted(df_clientes["Estado"].unique().tolist())
        asesores_disp = ["Todos"] + sorted(df_clientes["Asesor asignado"].unique().tolist())
        prods_disp = ["Todos"] + sorted(df_clientes["Producto"].unique().tolist())

        sel_est = f1.selectbox("Filtrar por Estado", estados_disp)
        sel_ase = f2.selectbox("Filtrar por Asesor", asesores_disp)
        sel_prd = f3.selectbox("Filtrar por Producto", prods_disp)

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
                            st.success(f"✅ Lead registrado exitosamente en Excel con el código **{nuevo_codigo}**.")
                            st.rerun()
                        except PermissionError:
                            st.error("⚠️ Cierra el archivo Excel antes de guardar un registro para permitir la escritura.")
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
                hole=0.45,
                title="Composición NPS (2,721 Atenciones)",
                color="Segmento",
                color_discrete_map={
                    "Promotores (9-10)": "#2E7D32",
                    "Pasivos (7-8)": "#F9A825",
                    "Detractores (0-6)": "#C62828"
                }
            )
            fig_nps.update_layout(height=330)
            st.plotly_chart(fig_nps, use_container_width=True)

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
        "⚙️ Módulo 3: Planificación y Control de la Producción",
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
            mode="lines+markers", name="Ciabatta — Histórico", line=dict(color="#3E2723", width=2.5)
        ))
        fig_pron.add_trace(go.Scatter(
            x=df_p_plot["Mes Etiqueta"], y=df_p_plot["Pan Ciabatta (und)"],
            mode="lines+markers", name="Ciabatta — Pronóstico", line=dict(color="#3E2723", width=2.5, dash="dash")
        ))
        fig_pron.add_trace(go.Scatter(
            x=df_h_plot["Mes Etiqueta"], y=df_h_plot["Pan Integral (und)"],
            mode="lines+markers", name="Integral — Histórico", line=dict(color="#C88A36", width=2.5)
        ))
        fig_pron.add_trace(go.Scatter(
            x=df_p_plot["Mes Etiqueta"], y=df_p_plot["Pan Integral (und)"],
            mode="lines+markers", name="Integral — Pronóstico", line=dict(color="#C88A36", width=2.5, dash="dash")
        ))
        fig_pron.update_layout(
            title="Evolución Histórica (18 meses) y Proyección de Ventas (12 meses) en Unidades",
            plot_bgcolor="white", height=370, xaxis_tickangle=-45, yaxis_title="Unidades"
        )
        st.plotly_chart(fig_pron, use_container_width=True)

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
            fig_pap.update_layout(showlegend=False, plot_bgcolor="white", height=350)
            st.plotly_chart(fig_pap, use_container_width=True)

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
        fig_pmp.update_layout(plot_bgcolor="white", height=330)
        st.plotly_chart(fig_pmp, use_container_width=True)

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
            st.plotly_chart(fig_tree, use_container_width=True)

    with tab_mrp:
        df_tlo, df_boc, df_puestos, df_ruta, df_crp = load_mrp_data()

        sub_mat, sub_cap = st.tabs([
            "📦 Submódulo Materiales — Tabla de Lanzamiento de Órdenes (TLO)",
            "⚡ Submódulo Capacidades — BOC, CRP, Puestos y Hoja de Ruta"
        ])

        with sub_mat:
            st.subheader("Tabla de Lanzamiento de Órdenes (TLO) — Horizonte Semanas 0 a 8")
            st.caption("Cantidades a liberar por semana en la unidad de medida de cada material (enlazado a Órdenes de Compra).")
            st.dataframe(df_tlo, use_container_width=True, hide_index=True)

        with sub_cap:
            st.success("✅ **Validación CRP (Semanas 0 a 8):** Todas las estaciones cuentan con capacidad disponible suficiente (Utilización máx. 83.8% en CT-01 Hombre).")

            st.subheader("1. Requerimientos de Capacidad (CRP) por Centro de Trabajo")
            sem_crp_sel = st.selectbox(
                "Seleccionar Semana MRP para detalle de carga:",
                ["Todas las semanas (Sem 0 – Sem 8)"] + df_crp["Semana"].unique().tolist()
            )
            df_crp_view = df_crp if sem_crp_sel.startswith("Todas") else df_crp[df_crp["Semana"] == sem_crp_sel]

            fig_crp = px.line(
                df_crp,
                x="Semana",
                y="Utilización (%)",
                color="Centro / Recurso",
                markers=True,
                title="Porcentaje de Utilización Semanal de Capacidad por Estación (%)"
            )
            fig_crp.add_hline(y=100, line_dash="dot", line_color="red", annotation_text="Límite Capacidad (100%)")
            fig_crp.update_layout(plot_bgcolor="white", height=340, yaxis_range=[0, 110])
            st.plotly_chart(fig_crp, use_container_width=True)
            st.dataframe(df_crp_view, use_container_width=True, hide_index=True, height=240)

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

            st.subheader("4. Hoja de Ruta por Producto")
            filtro_ruta = st.radio("Filtrar Hoja de Ruta:", ["Todos", "PF-01", "PF-02", "SE-01"], horizontal=True)
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
        fig_drp.update_layout(plot_bgcolor="white", height=330, yaxis_title="Unidades a Enviar")
        st.plotly_chart(fig_drp, use_container_width=True)

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
        "📦 Módulo 4: Gestión de Inventarios",
        "Control del Maestro de Materiales, niveles de stock y alta de nuevos insumos"
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
        tipos_mat = ["Todos"] + sorted(df_inv["Tipo"].unique().tolist())
        sel_tipo_mat = col_f1.selectbox("Filtrar por Tipo de Material", tipos_mat)
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
        fig_inv.update_layout(plot_bgcolor="white", height=350, xaxis_title="", yaxis_title="Cantidad")
        st.plotly_chart(fig_inv, use_container_width=True)

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
                        st.success(f"✅ Material **{cod_creado} — {desc_mat}** registrado correctamente en el Excel.")
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
        "🛒 Módulo 5: Compras y Evaluación de Proveedores",
        "Trazabilidad de órdenes de compra/servicio vinculadas al MRP y directorio homologado de proveedores"
    )

    df_oc, df_pr = load_purchasing_data()

    tab_oc, tab_pr = st.tabs([
        "📄 Órdenes de Compra y Servicio",
        "🏭 Directorio y Calificación de Proveedores"
    ])

    with tab_oc:
        total_oc = len(df_oc)
        monto_valido = df_oc[df_oc["Estado"] != "Rechazado"]["Monto (S/)"].sum()
        oc_aprob_ejec = int(df_oc["Estado"].isin(["Aprobado", "Ejecutado"]).sum())
        oc_proceso = int((df_oc["Estado"] == "En proceso").sum())

        o1, o2, o3, o4 = st.columns(4)
        o1.metric("Total Órdenes Emitidas", f"{total_oc} órdenes")
        o2.metric("Monto Comprometido Activo", f"S/ {monto_valido:,.2f}")
        o3.metric("Aprobadas / Ejecutadas", f"{oc_aprob_ejec} órdenes")
        o4.metric("En Proceso", f"{oc_proceso} órdenes")

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
            fig_oc1.update_layout(showlegend=False, plot_bgcolor="white", height=320)
            st.plotly_chart(fig_oc1, use_container_width=True)

        with g_oc2:
            res_tipo_oc = df_oc.groupby("Tipo")["Monto (S/)"].sum().reset_index()
            fig_oc2 = px.pie(
                res_tipo_oc, names="Tipo", values="Monto (S/)", hole=0.45,
                title="Distribución Presupuestal: Compra vs. Servicio",
                color_discrete_sequence=["#3E2723", "#C88A36"]
            )
            fig_oc2.update_layout(height=320)
            st.plotly_chart(fig_oc2, use_container_width=True)

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
            color_discrete_map={"A": "#2E7D32", "B": "#F9A825", "C": "#C62828"}
        )
        fig_pr.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_pr.update_layout(plot_bgcolor="white", height=420, xaxis_range=[0, 5.5])
        st.plotly_chart(fig_pr, use_container_width=True)

# ==============================================================================
# MÓDULO 6: DASHBOARD EJECUTIVO (KPIs CONSOLIDADOS)
# ==============================================================================
elif st.session_state.pagina == "6. Dashboard Ejecutivo":
    render_header_modulo(
        "📊 Módulo 6: Dashboard Gerencial Consolidado",
        "Indicadores Clave de Desempeño (KPIs) integrados de Comercial, Producción, Inventarios y Abastecimiento"
    )

    df_clientes = load_crm_data()
    df_atc, kpis_nps = load_nps_data()
    df_hist, df_pron, _ = load_forecast_data()
    df_pap_res, _, _ = load_pap_data()
    _, _, _, _, df_crp = load_mrp_data()
    df_inv = load_inventory_data()
    df_oc, df_pr = load_purchasing_data()

    # Cálculo de los 6 KPIs ejecutivos clave
    ventas_crm = int((df_clientes["Estado"] == "Venta").sum())
    tasa_conv = (ventas_crm / len(df_clientes) * 100) if len(df_clientes) > 0 else 0
    ingresos_atc = df_atc["Importe (S/)"].sum()
    demanda_anual_pron = int(df_pron["Total (und)"].sum())
    costo_pap_optimo = float(df_pap_res[df_pap_res["Rubro de Costo / Recurso"].str.contains("Costo Total", case=False)].iloc[0, 1])
    util_max_crp = df_crp["Utilización (%)"].max()
    insumos_df = df_inv[df_inv["Tipo"] != "Producto terminado"]
    val_inventario = insumos_df["Valorizado (S/)"].sum()
    otif_compras = (int(df_oc["Estado"].isin(["Aprobado", "Ejecutado"]).sum()) / len(df_oc) * 100) if len(df_oc) > 0 else 0

    st.markdown("### 1. Tarjetas Ejecutivas de Desempeño (KPIs)")
    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric(
            "KPI 1 · Índice de Lealtad (NPS)",
            f"{kpis_nps['nps_score']:.2f} pts",
            delta=f"{kpis_nps['promotores']} promotores de {kpis_nps['total_encuestas']} encuestas"
        )
        st.metric(
            "KPI 4 · Producción Proyectada (12m)",
            f"{demanda_anual_pron:,} unidades",
            delta=f"Costo PAP Óptimo: S/ {costo_pap_optimo:,.2f}"
        )
    with k2:
        st.metric(
            "KPI 2 · Conversión Comercial CRM",
            f"{tasa_conv:.1f}%",
            delta=f"{ventas_crm} ventas cerradas / {len(df_clientes)} leads"
        )
        st.metric(
            "KPI 5 · Pico de Carga en Planta (CRP)",
            f"{util_max_crp:.1f}%",
            delta="Capacidad instalada suficiente (< 100%)"
        )
    with k3:
        st.metric(
            "KPI 3 · Ingresos Registrados ATC",
            f"S/ {ingresos_atc:,.2f}",
            delta=f"Ticket promedio: S/ {ingresos_atc / len(df_atc):.2f}"
        )
        st.metric(
            "KPI 6 · Cumplimiento Compras & Stock",
            f"{otif_compras:.1f}% OC Activas",
            delta=f"Inventario valorizado: S/ {val_inventario:,.2f}"
        )

    st.divider()

    # Fila 1 de gráficos gerenciales
    g1, g2 = st.columns(2)
    with g1:
        df_atc_prod = df_atc.groupby("Producto")["Importe (S/)"].sum().reset_index()
        fig_d1 = px.bar(
            df_atc_prod,
            x="Producto",
            y="Importe (S/)",
            color="Producto",
            text="Importe (S/)",
            title="Ingresos Históricos por Línea de Producto (S/)",
            color_discrete_sequence=["#3E2723", "#C88A36"]
        )
        fig_d1.update_traces(texttemplate="S/ %{text:,.0f}", textposition="outside")
        fig_d1.update_layout(showlegend=False, plot_bgcolor="white", height=340)
        st.plotly_chart(fig_d1, use_container_width=True)

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
            title="Proyección Mensual de Demanda Agregada (Jul 2026 – Jun 2027)",
            color_discrete_map={"Pan Ciabatta (und)": "#3E2723", "Pan Integral (und)": "#C88A36"}
        )
        fig_d2.update_layout(plot_bgcolor="white", height=340, xaxis_tickangle=-45, xaxis_title="")
        st.plotly_chart(fig_d2, use_container_width=True)

    # Fila 2 de gráficos gerenciales
    g3, g4 = st.columns(2)
    with g3:
        df_oc_area = df_oc[df_oc["Estado"] != "Rechazado"].groupby("Área usuaria")["Monto (S/)"].sum().reset_index()
        fig_d3 = px.pie(
            df_oc_area,
            names="Área usuaria",
            values="Monto (S/)",
            hole=0.45,
            title="Distribución del Gasto de Abastecimiento por Área Usuaria",
            color_discrete_sequence=["#3E2723", "#C88A36", "#8D6E63", "#D7CCC8"]
        )
        fig_d3.update_layout(height=340)
        st.plotly_chart(fig_d3, use_container_width=True)

    with g4:
        df_crp_max = df_crp.groupby("Centro / Recurso")["Utilización (%)"].max().reset_index()
        fig_d4 = px.bar(
            df_crp_max.sort_values("Utilización (%)", ascending=True),
            x="Utilización (%)",
            y="Centro / Recurso",
            orientation="h",
            text="Utilización (%)",
            title="Utilización Máxima de Capacidad por Estación de Trabajo (%)",
            color_discrete_sequence=["#5D4037"]
        )
        fig_d4.add_vline(x=100, line_dash="dot", line_color="red")
        fig_d4.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_d4.update_layout(plot_bgcolor="white", height=340, xaxis_range=[0, 110], yaxis_title="")
        st.plotly_chart(fig_d4, use_container_width=True)