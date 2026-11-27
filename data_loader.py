import os
from datetime import datetime
import pandas as pd
import openpyxl

EXCEL_CANDIDATES = ["gesop grupo1 corregido.xlsx", "gesop grupo 1 .xlsx"]

def get_excel_path():
    for candidate in EXCEL_CANDIDATES:
        if os.path.exists(candidate):
            return candidate
    for f in os.listdir("."):
        if f.endswith(".xlsx") and not f.startswith("~$"):
            return f
    raise FileNotFoundError("No se encontró ningún archivo Excel (.xlsx) en la carpeta del proyecto.")

def find_sheet(xls_or_names, target_name):
    names = xls_or_names.sheet_names if hasattr(xls_or_names, "sheet_names") else xls_or_names
    for s in names:
        if s.strip().lower() == target_name.strip().lower():
            return s
    raise ValueError(f"Pestaña '{target_name}' no encontrada en el Excel.")

def fmt_mes(val):
    dt = pd.to_datetime(val, errors="coerce")
    if pd.notna(dt):
        meses_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        return f"{meses_es[dt.month - 1]} {dt.year}"
    return str(val).strip()

# ==============================================================================
# MÓDULO 1: INFORMACIÓN Y PRODUCTOS
# ==============================================================================
def load_company_info():
    path = get_excel_path()
    xls = pd.ExcelFile(path)

    df_portada = pd.read_excel(xls, sheet_name=find_sheet(xls, "Portada"), header=None)
    integrantes = [
        str(df_portada.iloc[r, 2]).strip()
        for r in range(17, 21)
        if pd.notna(df_portada.iloc[r, 2])
    ]
    meta_academica = {
        "universidad": str(df_portada.iloc[2, 1]).strip(),
        "facultad": str(df_portada.iloc[4, 1]).strip(),
        "curso": str(df_portada.iloc[10, 1]).strip(),
        "docente": str(df_portada.iloc[12, 1]).strip(),
        "integrantes": integrantes,
        "anio": str(df_portada.iloc[25, 1]).strip(),
        "archivo_activo": os.path.basename(path),
    }

    df_pres = pd.read_excel(xls, sheet_name=find_sheet(xls, "Presentacion"), header=None)
    empresa = {
        "nombre_comercial": str(df_pres.iloc[8, 2]).strip(),
        "ruc": str(df_pres.iloc[11, 2]).strip(),
        "dueno": str(df_pres.iloc[14, 2]).strip(),
        "ubicacion": str(df_pres.iloc[17, 2]).strip(),
        "sector": "Industria Alimentaria — Panadería Artesanal de Masa Madre y Cafetería de Especialidad",
        "historia": str(df_pres.iloc[20, 2]).replace("Historia:", "").strip(),
        "actividades": str(df_pres.iloc[24, 2]).replace("Actividades principales:", "").strip(),
    }
    return meta_academica, empresa

def load_products_and_dap():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df = pd.read_excel(xls, sheet_name=find_sheet(xls, "Definición del Producto"), header=None)

    def parse_ficha(start_row, end_row):
        return {
            str(df.iloc[r, 1]).strip(): str(df.iloc[r, 2]).strip()
            for r in range(start_row, end_row + 1)
        }

    def parse_dap(start_row, end_row, summary_start, summary_end):
        cols = [
            "N°", "Actividad", "Puesto", "Operación", "Transporte",
            "Inspección", "Demora", "Almacenamiento",
            "T. Operario (min)", "T. Máquina (min)", "Tiempo Total (min)", "Distancia (m)"
        ]
        dap_df = df.iloc[start_row:end_row + 1, 1:13].copy()
        dap_df.columns = cols
        dap_df["N°"] = dap_df["N°"].astype(int)
        for c in ["Operación", "Transporte", "Inspección", "Demora", "Almacenamiento"]:
            dap_df[c] = dap_df[c].fillna("—")
        for c in ["T. Operario (min)", "T. Máquina (min)", "Tiempo Total (min)", "Distancia (m)"]:
            dap_df[c] = pd.to_numeric(dap_df[c], errors="coerce").fillna(0)

        sum_df = df.iloc[summary_start:summary_end + 1, 2:6].copy()
        sum_df.columns = ["Tipo de Actividad", "Cantidad", "Tiempo (min)", "Distancia (m)"]
        sum_df["Cantidad"] = pd.to_numeric(sum_df["Cantidad"], errors="coerce").fillna(0).astype(int)
        sum_df["Tiempo (min)"] = pd.to_numeric(sum_df["Tiempo (min)"], errors="coerce").fillna(0)
        sum_df["Distancia (m)"] = pd.to_numeric(sum_df["Distancia (m)"], errors="coerce").fillna(0)
        return dap_df, sum_df

    return {
        "PF-01": {"ficha": parse_ficha(5, 13), "dap": parse_dap(19, 37, 41, 46)[0], "resumen": parse_dap(19, 37, 41, 46)[1]},
        "PF-02": {"ficha": parse_ficha(55, 63), "dap": parse_dap(69, 87, 91, 96)[0], "resumen": parse_dap(69, 87, 91, 96)[1]},
    }

# ==============================================================================
# MÓDULO 2: CRM Y ATENCIÓN AL CLIENTE (NPS)
# ==============================================================================
def load_crm_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df_raw = pd.read_excel(xls, sheet_name=find_sheet(xls, "Clientes"), header=None)

    headers = [str(df_raw.iloc[5, c]).strip() for c in range(11)]
    df_clientes = df_raw.iloc[6:, :11].copy()
    df_clientes.columns = headers
    df_clientes = df_clientes[df_clientes["ID"].notna()].copy()
    df_clientes["ID"] = df_clientes["ID"].astype(str).str.strip()
    df_clientes = df_clientes[df_clientes["ID"].str.startswith("C-")].reset_index(drop=True)

    df_clientes["Nombre Completo"] = (
        df_clientes["Nombre"].fillna("").astype(str).str.strip() + " " +
        df_clientes["Apellido"].fillna("").astype(str).str.strip()
    ).str.strip()
    df_clientes["Fecha de registro"] = pd.to_datetime(df_clientes["Fecha de registro"], errors="coerce").dt.strftime("%Y-%m-%d").fillna("—")
    df_clientes["Celular"] = df_clientes["Celular"].fillna("—").astype(str).str.strip()
    df_clientes["Canal (captación)"] = df_clientes["Canal (captación)"].fillna("—").astype(str).str.strip()
    df_clientes["Canal de venta (DRP)"] = df_clientes["Canal de venta (DRP)"].fillna("—").astype(str).str.strip()
    df_clientes["Producto"] = df_clientes["Producto"].fillna("—").astype(str).str.strip()
    df_clientes["Asesor asignado"] = df_clientes["Asesor asignado"].fillna("—").astype(str).str.strip()
    df_clientes["Estado"] = df_clientes["Estado"].fillna("Pendiente").astype(str).str.strip()
    df_clientes["N° de compras (Atención)"] = pd.to_numeric(df_clientes["N° de compras (Atención)"], errors="coerce").fillna(0).astype(int)

    return df_clientes

def add_new_lead(nombre, apellido, celular, canal_captacion, canal_drp, producto, asesor, estado):
    path = get_excel_path()
    wb = openpyxl.load_workbook(path)
    ws = wb[find_sheet(wb.sheetnames, "Clientes")]

    last_row = 6
    max_num = 0
    for r in range(7, ws.max_row + 1):
        val = ws.cell(row=r, column=1).value
        if val and str(val).strip().startswith("C-"):
            last_row = r
            try:
                num = int(str(val).strip().split("-")[1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass

    new_id = f"C-{max_num + 1:04d}"
    target_row = last_row + 1

    ws.cell(row=target_row, column=1, value=new_id)
    ws.cell(row=target_row, column=2, value=nombre.strip())
    ws.cell(row=target_row, column=3, value=apellido.strip())
    ws.cell(row=target_row, column=4, value=celular.strip())
    ws.cell(row=target_row, column=5, value=datetime.now().strftime("%Y-%m-%d"))
    ws.cell(row=target_row, column=6, value=canal_captacion)
    ws.cell(row=target_row, column=7, value=canal_drp)
    ws.cell(row=target_row, column=8, value=producto)
    ws.cell(row=target_row, column=9, value=asesor)
    ws.cell(row=target_row, column=10, value=estado)
    ws.cell(row=target_row, column=11, value=0)

    wb.save(path)
    return new_id

def update_lead_status(client_id, new_status):
    path = get_excel_path()
    wb = openpyxl.load_workbook(path)
    ws = wb[find_sheet(wb.sheetnames, "Clientes")]

    updated = False
    for r in range(7, ws.max_row + 1):
        val = ws.cell(row=r, column=1).value
        if val and str(val).strip() == client_id.strip():
            ws.cell(row=r, column=10, value=new_status)
            updated = True
            break

    if not updated:
        raise ValueError(f"No se encontró el cliente {client_id} en el Excel.")
    wb.save(path)
    return True

def load_nps_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df_raw = pd.read_excel(xls, sheet_name=find_sheet(xls, "Atención al Cliente"), header=None)

    headers = [str(df_raw.iloc[5, c]).strip() for c in range(12)]
    df_atc = df_raw.iloc[6:, :12].copy()
    df_atc.columns = headers
    df_atc = df_atc[df_atc["ID venta"].notna()].copy()
    df_atc["ID venta"] = df_atc["ID venta"].astype(str).str.strip()
    df_atc = df_atc[df_atc["ID venta"].str.startswith("V-")].reset_index(drop=True)

    df_atc["N°"] = pd.to_numeric(df_atc["N°"], errors="coerce").fillna(0).astype(int)
    df_atc["Fecha"] = pd.to_datetime(df_atc["Fecha"], errors="coerce").dt.strftime("%Y-%m-%d").fillna("—")
    df_atc["Cantidad (und)"] = pd.to_numeric(df_atc["Cantidad (und)"], errors="coerce").fillna(0).astype(int)
    df_atc["Importe (S/)"] = pd.to_numeric(df_atc["Importe (S/)"], errors="coerce").fillna(0.0)
    df_atc["Calificación NPS (0-10)"] = pd.to_numeric(df_atc["Calificación NPS (0-10)"], errors="coerce").fillna(0).astype(int)
    df_atc["Tipo NPS"] = df_atc["Tipo NPS"].fillna("—").astype(str).str.strip()

    total = len(df_atc)
    promotores = int((df_atc["Calificación NPS (0-10)"] >= 9).sum())
    pasivos = int(((df_atc["Calificación NPS (0-10)"] >= 7) & (df_atc["Calificación NPS (0-10)"] <= 8)).sum())
    detractores = int((df_atc["Calificación NPS (0-10)"] <= 6).sum())
    nps_score = ((promotores - detractores) / total * 100) if total > 0 else 0.0

    kpis_nps = {
        "total_encuestas": total,
        "promotores": promotores,
        "pasivos": pasivos,
        "detractores": detractores,
        "nps_score": round(nps_score, 2)
    }
    return df_atc, kpis_nps

# ==============================================================================
# MÓDULO 3: PRODUCCIÓN (PRONÓSTICOS, PAP, PMP, BOM, MRP I/II, DRP)
# ==============================================================================
def load_forecast_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df = pd.read_excel(xls, sheet_name=find_sheet(xls, "Demanda y Pronósticos"), header=None)

    hist_cols = [
        "Mes", "Periodo (t)", "Pan Ciabatta (lotes)", "Pan Integral (lotes)",
        "Total (lotes)", "Pan Ciabatta (und)", "Pan Integral (und)", "Total (und)"
    ]
    df_hist = df.iloc[5:23, 1:9].copy()
    df_hist.columns = hist_cols
    df_hist["Mes Etiqueta"] = df_hist["Mes"].apply(fmt_mes)
    for c in hist_cols[1:]:
        df_hist[c] = pd.to_numeric(df_hist[c], errors="coerce").fillna(0).astype(int)

    pron_cols = [
        "Mes", "Pan Ciabatta (lotes)", "Pan Integral (lotes)",
        "Total (lotes)", "Pan Ciabatta (und)", "Pan Integral (und)", "Total (und)"
    ]
    df_pron = df.iloc[228:240, 1:8].copy()
    df_pron.columns = pron_cols
    df_pron["Mes Etiqueta"] = df_pron["Mes"].apply(fmt_mes)
    for c in pron_cols[1:]:
        df_pron[c] = pd.to_numeric(df_pron[c], errors="coerce").fillna(0).astype(int)

    df_metodos = df.iloc[245:247, 1:6].copy()
    df_metodos.columns = ["Producto", "Método Seleccionado", "DAM (MAD)", "EPAM (MAPE)", "Señal de Rastreo"]
    df_metodos["DAM (MAD)"] = pd.to_numeric(df_metodos["DAM (MAD)"], errors="coerce").round(3)
    df_metodos["EPAM (MAPE)"] = (pd.to_numeric(df_metodos["EPAM (MAPE)"], errors="coerce") * 100).round(2)
    df_metodos["Señal de Rastreo"] = pd.to_numeric(df_metodos["Señal de Rastreo"], errors="coerce").round(3)

    return df_hist, df_pron, df_metodos

def load_pap_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df = pd.read_excel(xls, sheet_name=find_sheet(xls, "Plan Agregado"), header=None)

    df_resumen = df.iloc[100:109, 1:6].copy()
    df_resumen.columns = [
        "Rubro de Costo / Recurso",
        "Plan 1 (Exacta / Fuerza Variada)",
        "Plan 2 (Nivelada / Inventario)",
        "Plan 3 (Nivelada / Subcontratación)",
        "Plan 4 (Nivelada / Tiempo Extra)"
    ]
    for col in df_resumen.columns[1:]:
        df_resumen[col] = pd.to_numeric(df_resumen[col], errors="coerce").fillna(0.0).round(2)

    plan_elegido = str(df.iloc[110, 2]).strip()

    meses_hdr = ["Concepto"] + [fmt_mes(df.iloc[115, c]) for c in range(2, 14)] + ["Total Anual"]
    df_desag = df.iloc[116:121, 1:15].copy()
    df_desag.columns = meses_hdr
    for col in meses_hdr[1:]:
        df_desag[col] = pd.to_numeric(df_desag[col], errors="coerce").round(2)

    return df_resumen, plan_elegido, df_desag

def load_pmp_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df = pd.read_excel(xls, sheet_name=find_sheet(xls, "PMP"), header=None)

    meses_bloque = [
        ("Julio 2026", [1, 2, 3, 4], ["Sem 1", "Sem 2", "Sem 3", "Sem 4"]),
        ("Agosto 2026", [6, 7, 8, 9], ["Sem 5", "Sem 6", "Sem 7", "Sem 8"]),
        ("Septiembre 2026", [11, 12, 13, 14], ["Sem 9", "Sem 10", "Sem 11", "Sem 12"]),
        ("Octubre 2026", [16, 17, 18, 19], ["Sem 13", "Sem 14", "Sem 15", "Sem 16"]),
        ("Noviembre 2026", [21, 22, 23, 24], ["Sem 17", "Sem 18", "Sem 19", "Sem 20"]),
        ("Diciembre 2026", [26, 27, 28, 29], ["Sem 21", "Sem 22", "Sem 23", "Sem 24"]),
    ]

    def parse_pmp_product(row_start):
        registros = []
        for mes_nombre, cols_sem, nombres_sem in meses_bloque:
            for c_idx, sem_lbl in zip(cols_sem, nombres_sem):
                registros.append({
                    "Mes": mes_nombre,
                    "Semana": sem_lbl,
                    "Requerimiento (und)": int(round(float(df.iloc[row_start, c_idx] or 0))),
                    "Inv. Inicial (und)": int(round(float(df.iloc[row_start + 1, c_idx] or 0))),
                    "Stock Seguridad (und)": int(round(float(df.iloc[row_start + 2, c_idx] or 0))),
                    "Necesidad Neta (und)": int(round(float(df.iloc[row_start + 3, c_idx] or 0))),
                    "Producción PMP (und)": int(round(float(df.iloc[row_start + 4, c_idx] or 0))),
                    "Inv. Final (und)": int(round(float(df.iloc[row_start + 5, c_idx] or 0))),
                })
        return pd.DataFrame(registros)

    return parse_pmp_product(8), parse_pmp_product(21)

def load_bom_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df = pd.read_excel(xls, sheet_name=find_sheet(xls, "BOM"), header=None)

    cols = [
        "Código", "Descripción", "Unidad",
        "Tanda Ciabatta (120 und)", "Tanda Integral (120 und)",
        "Por und Ciabatta", "Por und Integral", "Por kg Masa Madre",
        "Stock Disp.", "Lead Time (sem)", "Tamaño Lote", "Inv. Seguridad", "Se usa en"
    ]
    df_bom = df.iloc[7:17, 0:13].copy()
    df_bom.columns = cols
    df_bom["Código"] = df_bom["Código"].astype(str).str.strip()
    for c in cols[3:12]:
        df_bom[c] = df_bom[c].fillna("—")
    return df_bom.reset_index(drop=True)
def to_float_safe(valor, default=0.0):
    if isinstance(valor, pd.Series):
        return pd.to_numeric(valor, errors="coerce").fillna(default)

    try:
        if pd.isna(valor):
            return default
        return float(valor)
    except (ValueError, TypeError):
        return default
    
def load_mrp_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df = pd.read_excel(xls, sheet_name=find_sheet(xls, "MRP 2"), header=None)

    # 1. Tabla de Lanzamiento de Órdenes (TLO)
    tlo_cols = ["Material / Ítem", "Sem 0", "Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6", "Sem 7", "Sem 8", "Total (9 sem)", "Unidad"]
    df_tlo = df.iloc[5:15, 1:13].copy()
    df_tlo.columns = tlo_cols
    for c in tlo_cols[1:11]:
        df_tlo[c] = pd.to_numeric(df_tlo[c], errors="coerce").fillna(0)

    # 2. Tabla de Capacidades (BOC)
    boc_cols = [
        "Producto / Componente",
        "CT-01 Hombre (min)", "CT-01 Equipo (min)",
        "CT-02 Hombre (min)", "CT-02 Equipo (min)",
        "CT-03 Hombre (min)", "CT-03 Equipo (min)",
        "CT-04 Hombre (min)", "CT-04 Equipo (min)"
    ]
    df_boc = df.iloc[5:15, 16:25].copy()
    df_boc.columns = boc_cols
    for c in boc_cols[1:]:
        df_boc[c] = pd.to_numeric(df_boc[c], errors="coerce").fillna(0.0)

    # 3. Lista de puestos de trabajo
    puestos_cols = [
        "Código", "Puesto de Trabajo", "Actividades", "N° Operarios",
        "Equipos / Máquinas", "N° Máquinas", "Capacidad (h/turno)",
        "T. Preparación (min)", "Turnos/día", "Días/sem", "Jornada",
        "Disp. Hombre (h/sem)", "Disp. Equipo (h/sem)"
    ]
    df_puestos = df.iloc[34:38, 1:14].copy()
    df_puestos.columns = puestos_cols

    # 4. Hoja de ruta completa
    ruta_cols = [
        "N°", "Actividad", "Componente", "Estación", "Descripción Estación",
        "Producto", "T. Operario (min/und)", "T. Máquina (min/und)", "Base"
    ]
    df_ruta_fab = df.iloc[50:74, 1:10].copy()
    df_ruta_fab.columns = ruta_cols

    if len(df) >= 91:
        df_ruta_ins = df.iloc[82:91, 1:10].copy()
        df_ruta_ins.columns = ruta_cols
        df_ruta = pd.concat([df_ruta_fab, df_ruta_ins], ignore_index=True)
    else:
        df_ruta = df_ruta_fab.reset_index(drop=True)

    df_ruta["N°"] = pd.to_numeric(df_ruta["N°"], errors="coerce").fillna(0).astype(int)
    df_ruta["T. Operario (min/und)"] = pd.to_numeric(df_ruta["T. Operario (min/und)"], errors="coerce").fillna(0.0)
    df_ruta["T. Máquina (min/und)"] = pd.to_numeric(df_ruta["T. Máquina (min/und)"], errors="coerce").fillna(0.0)

    # 5. CRP Detallado (Necesidades de Capacidad por Estación, Recurso y Semana)
    crp_rows = []
    sem_indices = [
        ("Sem 0", 25), ("Sem 1", 28), ("Sem 2", 31), ("Sem 3", 34),
        ("Sem 4", 37), ("Sem 5", 40), ("Sem 6", 43), ("Sem 7", 46), ("Sem 8", 49)
    ]
    estaciones_map = [
        ("CT-01", "Preparación de masa y división", "Hombre", 18, 48.0),
        ("CT-01", "Preparación de masa y división", "Equipo", 19, 96.0),
        ("CT-02", "Fermentación controlada", "Equipo", 21, 96.0),
        ("CT-03", "Formado y acabado", "Hombre", 22, 48.0),
        ("CT-04", "Horneado y empaque", "Hombre", 24, 48.0),
        ("CT-04", "Horneado y empaque", "Equipo", 25, 48.0),
    ]
    for sem_lbl, r_base in sem_indices:
        for cod_est, nom_est, tipo_rec, col_i, disp_h in estaciones_map:
            req_min = float(df.iloc[r_base, col_i] or 0.0)
            req_h = float(df.iloc[r_base + 1, col_i] or 0.0)
            ok = str(df.iloc[r_base + 2, col_i]).strip()
            holgura_h = disp_h - req_h
            util_pct = (req_h / disp_h * 100) if disp_h > 0 else 0.0
            estado_carga = (
                "🟢 Carga Alta (>75%)" if util_pct >= 75
                else ("🟡 Carga Media (40-75%)" if util_pct >= 40 else "🔵 Carga Baja / Alistamiento")
            )
            crp_rows.append({
                "Semana": sem_lbl,
                "Código": cod_est,
                "Estación": nom_est,
                "Recurso": tipo_rec,
                "Centro / Recurso": f"{cod_est} {nom_est} ({tipo_rec})",
                "Req. Minutos": round(req_min, 2),
                "Horas Requeridas": round(req_h, 2),
                "Horas Disponibles": disp_h,
                "Holgura (h)": round(holgura_h, 2),
                "Utilización (%)": round(util_pct, 1),
                "Nivel de Carga": estado_carga,
                "¿Hay Capacidad?": ok
            })
    df_crp = pd.DataFrame(crp_rows)

    return df_tlo, df_boc, df_puestos, df_ruta, df_crp

def load_drp_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)

    def parse_drp_sheet(sheet_title):
        df = pd.read_excel(xls, sheet_name=find_sheet(xls, sheet_title), header=None)
        mes_plan = fmt_mes(df.iloc[10, 19])
        resumen_envios = pd.DataFrame({
            "Semana": ["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Total Mes"],
            "Café Yayi's (CAF) - Demanda (und)": [
                int(to_float_safe(df.iloc[19, 12], default=0)), int(to_float_safe(df.iloc[19, 13], default=0)), int(to_float_safe(df.iloc[19, 14], default=0)), int(to_float_safe(df.iloc[19, 15], default=0)),
                sum(int(to_float_safe(df.iloc[19, c], default=0)) for c in range(12, 16))
            ],
            "Café Yayi's (CAF) - Envíos Planificados (und)": [
                int(to_float_safe(df.iloc[25, 12], default=0)), int(to_float_safe(df.iloc[25, 13], default=0)), int(to_float_safe(df.iloc[25, 14], default=0)), int(to_float_safe(df.iloc[25, 15], default=0)),
                sum(int(to_float_safe(df.iloc[25, c], default=0)) for c in range(12, 16))
            ],
            "Delivery & Corp (DLV) - Demanda (und)": [
                int(to_float_safe(df.iloc[19, 25], default=0)), int(to_float_safe(df.iloc[19, 26], default=0)), int(to_float_safe(df.iloc[19, 27], default=0)), int(to_float_safe(df.iloc[19, 28], default=0)),
                sum(int(to_float_safe(df.iloc[19, c], default=0)) for c in range(25, 29))
            ],
            "Delivery & Corp (DLV) - Envíos Planificados (und)": [
                int(to_float_safe(df.iloc[25, 25], default=0)), int(to_float_safe(df.iloc[25, 26], default=0)), int(to_float_safe(df.iloc[25, 27], default=0)), int(to_float_safe(df.iloc[25, 28], default=0)),
                sum(int(to_float_safe(df.iloc[25, c], default=0)) for c in range(25, 29))
            ],
        })
        resumen_envios["Total Envíos Planta → CD → Canales (und)"] = (
            resumen_envios["Café Yayi's (CAF) - Envíos Planificados (und)"] +
            resumen_envios["Delivery & Corp (DLV) - Envíos Planificados (und)"]
        )

        conceptos = [str(df.iloc[r, 10]).strip() for r in range(19, 27)]
        df_caf_det = pd.DataFrame({
            "Concepto DRP": conceptos,
            "Sem 0": [int(to_float_safe(df.iloc[r, 11], default=0)) for r in range(19, 27)],
            "Sem 1": [int(to_float_safe(df.iloc[r, 12], default=0)) for r in range(19, 27)],
            "Sem 2": [int(to_float_safe(df.iloc[r, 13], default=0)) for r in range(19, 27)],
            "Sem 3": [int(to_float_safe(df.iloc[r, 14], default=0)) for r in range(19, 27)],
            "Sem 4": [int(to_float_safe(df.iloc[r, 15], default=0)) for r in range(19, 27)],
        })
        df_dlv_det = pd.DataFrame({
            "Concepto DRP": conceptos,
            "Sem 0": [int(to_float_safe(df.iloc[r, 24], default=0)) for r in range(19, 27)],
            "Sem 1": [int(to_float_safe(df.iloc[r, 25], default=0)) for r in range(19, 27)],
            "Sem 2": [int(to_float_safe(df.iloc[r, 26], default=0)) for r in range(19, 27)],
            "Sem 3": [int(to_float_safe(df.iloc[r, 27], default=0)) for r in range(19, 27)],
            "Sem 4": [int(to_float_safe(df.iloc[r, 28], default=0)) for r in range(19, 27)],
        })
        return {"mes": mes_plan, "resumen": resumen_envios, "caf": df_caf_det, "dlv": df_dlv_det}

    return {
        "Pan Ciabatta (PF-01)": parse_drp_sheet("DRP Ciabatta"),
        "Pan Integral Multigrano (PF-02)": parse_drp_sheet("DRP Integral"),
    }

# ==============================================================================
# MÓDULO 4: INVENTARIOS (MAESTRO DE MATERIALES)
# ==============================================================================
def load_inventory_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)
    df_raw = pd.read_excel(xls, sheet_name=find_sheet(xls, "Maestro de Materiales"), header=None)

    headers = [str(df_raw.iloc[5, c]).strip() for c in range(14)]
    df_mat = df_raw.iloc[6:, :14].copy()
    df_mat.columns = headers
    df_mat = df_mat[df_mat["Código"].notna()].copy()
    df_mat["Código"] = df_mat["Código"].astype(str).str.strip()
    df_mat = df_mat[df_mat["Código"] != "Código"].reset_index(drop=True)

    num_cols = ["Nivel (LLC)", "Inventario disponible", "Stock de seguridad", "Lead time (días hábiles)", "Lead time (semanas)", "Tamaño de lote"]
    for c in num_cols:
        df_mat[c] = pd.to_numeric(df_mat[c], errors="coerce").fillna(0)

    df_mat["Costo unitario (S/)"] = pd.to_numeric(df_mat["Costo unitario (S/)"], errors="coerce")
    df_mat["Costo Display"] = df_mat["Costo unitario (S/)"].apply(lambda x: f"S/ {x:.4f}" if pd.notna(x) else "Producto Terminado")
    df_mat["Valorizado (S/)"] = (df_mat["Inventario disponible"] * df_mat["Costo unitario (S/)"].fillna(0)).round(2)

    def estado_stock(row):
        if row["Tipo"] == "Producto terminado":
            return "Producción Diaria"
        if row["Inventario disponible"] <= row["Stock de seguridad"]:
            return "⚠️ Crítico / Reponer"
        elif row["Inventario disponible"] <= row["Stock de seguridad"] * 1.5:
            return "🟡 Alerta Preventiva"
        return "✅ Stock Óptimo"

    df_mat["Estado Stock"] = df_mat.apply(estado_stock, axis=1)
    return df_mat

def add_new_material(codigo, descripcion, tipo, unidad, nivel_llc, inv_disp, stock_seg, lt_dias, lt_sem, tam_lote, presentacion, costo_unit, proveedor, uso):
    path = get_excel_path()
    wb = openpyxl.load_workbook(path)
    ws = wb[find_sheet(wb.sheetnames, "Maestro de Materiales")]

    last_row = 6
    for r in range(7, ws.max_row + 1):
        val = ws.cell(row=r, column=1).value
        if val and str(val).strip() != "":
            if str(val).strip().upper() == codigo.strip().upper():
                raise ValueError(f"El código '{codigo}' ya existe en el Maestro de Materiales.")
            last_row = r

    target_row = last_row + 1
    valores = [
        codigo.strip().upper(),
        descripcion.strip(),
        tipo,
        unidad.strip(),
        int(nivel_llc),
        float(inv_disp),
        float(stock_seg),
        int(lt_dias),
        int(lt_sem),
        float(tam_lote),
        presentacion.strip(),
        float(costo_unit),
        proveedor.strip(),
        uso.strip()
    ]
    for col_idx, val in enumerate(valores, start=1):
        ws.cell(row=target_row, column=col_idx, value=val)

    wb.save(path)
    return codigo.strip().upper()

# ==============================================================================
# MÓDULO 5: COMPRAS Y PROVEEDORES (INCLUYE OC- Y OS-)
# ==============================================================================
def load_purchasing_data():
    path = get_excel_path()
    xls = pd.ExcelFile(path)

    df_oc_raw = pd.read_excel(xls, sheet_name=find_sheet(xls, "Órdenes de Compra"), header=None)
    headers_oc = [str(df_oc_raw.iloc[6, c]).strip() for c in range(14)]
    df_oc = df_oc_raw.iloc[7:, :14].copy()
    df_oc.columns = headers_oc
    df_oc = df_oc[df_oc["N° de orden"].notna()].copy()
    df_oc["N° de orden"] = df_oc["N° de orden"].astype(str).str.strip()
    df_oc = df_oc[df_oc["N° de orden"].str.startswith(("OC-", "OS-"))].reset_index(drop=True)

    df_oc["Fecha de emisión"] = pd.to_datetime(df_oc["Fecha de emisión"], errors="coerce").dt.strftime("%Y-%m-%d").fillna("—")
    df_oc["Cantidad"] = pd.to_numeric(df_oc["Cantidad"], errors="coerce").fillna(0)
    df_oc["Precio unitario (S/)"] = pd.to_numeric(df_oc["Precio unitario (S/)"], errors="coerce").fillna(0.0)
    df_oc["Monto (S/)"] = pd.to_numeric(df_oc["Monto (S/)"], errors="coerce").fillna(0.0)
    df_oc["Estado"] = df_oc["Estado"].fillna("En proceso").astype(str).str.strip()
    df_oc["Tipo"] = df_oc["Tipo"].fillna("Compra").astype(str).str.strip()
    df_oc["Área usuaria"] = df_oc["Área usuaria"].fillna("—").astype(str).str.strip()

    df_pr_raw = pd.read_excel(xls, sheet_name=find_sheet(xls, "Proveedores"), header=None)
    headers_pr = [str(df_pr_raw.iloc[5, c]).strip() for c in range(14)]
    df_pr = df_pr_raw.iloc[6:, :14].copy()
    df_pr.columns = headers_pr
    df_pr = df_pr[df_pr["Código"].notna()].copy()
    df_pr["Código"] = df_pr["Código"].astype(str).str.strip()
    df_pr = df_pr[df_pr["Código"].str.startswith("PR-")].reset_index(drop=True)

    for c in ["Calidad (1-5)", "Puntualidad (1-5)", "Precio (1-5)", "Calificación", "Monto en órdenes (S/)"]:
        df_pr[c] = pd.to_numeric(df_pr[c], errors="coerce").fillna(0.0)
    df_pr["N° de órdenes"] = pd.to_numeric(df_pr["N° de órdenes"], errors="coerce").fillna(0).astype(int)

    return df_oc, df_pr