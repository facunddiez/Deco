"""Casa Mater — Dashboard de Costos e Importación"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Casa Mater · Costos",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ID del archivo en Google Drive (reemplazar con el tuyo)
# Obtenerlo desde la URL: drive.google.com/file/d/ESTE_ES_EL_ID/view
GDRIVE_FILE_ID = st.secrets.get("gdrive_file_id", "")

# Fallback local para desarrollo
LOCAL_EXCEL = Path(__file__).parent / "Costos_Importacion.xlsx"

# ── PALETTE ───────────────────────────────────────────────────────────────────
DARK   = "#1F2D3D"
GOLD   = "#B8955A"
CREAM  = "#FAFAF7"
GRN    = "#1A6B3C"
RED    = "#A93226"
ORG    = "#BF6900"
NAVY   = "#1B4F72"
TEAL   = "#0E6655"
GRAY   = "#7F8C8D"

CHART_COLORS = [GOLD, NAVY, TEAL, GRN, ORG, RED, GRAY,
                "#8E44AD", "#2980B9", "#E74C3C", "#27AE60"]

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Montserrat:wght@400;500;600&display=swap');

  html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif;
    background-color: {CREAM};
  }}
  .main {{ background-color: {CREAM}; }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{
    background-color: {DARK};
  }}
  section[data-testid="stSidebar"] * {{
    color: #EEEEEE !important;
  }}
  section[data-testid="stSidebar"] .stDateInput label,
  section[data-testid="stSidebar"] .stMultiSelect label,
  section[data-testid="stSidebar"] .stSelectbox label {{
    color: {GOLD} !important;
    font-weight: 600;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }}

  /* KPI cards */
  .kpi-card {{
    background: {DARK};
    border-radius: 10px;
    padding: 18px 20px 14px;
    border-top: 3px solid {GOLD};
    text-align: center;
    height: 100%;
  }}
  .kpi-label {{
    font-size: 0.70rem;
    color: #AAAAAA;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 6px;
  }}
  .kpi-value {{
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    color: {GOLD};
    line-height: 1.1;
  }}
  .kpi-value.green  {{ color: #52BE80; }}
  .kpi-value.red    {{ color: #E74C3C; }}
  .kpi-value.teal   {{ color: #48C9B0; }}
  .kpi-value.navy   {{ color: #85C1E9; }}

  /* Section headers */
  .section-hdr {{
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: {DARK};
    border-bottom: 2px solid {GOLD};
    padding-bottom: 4px;
    margin: 28px 0 14px;
  }}

  /* Page title */
  .page-title {{
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: {DARK};
    letter-spacing: 0.02em;
  }}
  .page-subtitle {{
    font-size: 0.82rem;
    color: {GRAY};
    margin-top: -6px;
    margin-bottom: 20px;
  }}

  /* Tabs */
  button[data-baseweb="tab"] {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }}
  button[data-baseweb="tab"][aria-selected="true"] {{
    color: {GOLD} !important;
    border-bottom-color: {GOLD} !important;
  }}

  /* Alert badges */
  .badge-red    {{ background:#FAECEA; color:{RED}; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; }}
  .badge-orange {{ background:#FDF3E3; color:{ORG}; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; }}
  .badge-green  {{ background:#D4EDDA; color:{GRN}; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; }}
  .badge-navy   {{ background:#D6EAF8; color:{NAVY}; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; }}
</style>
""", unsafe_allow_html=True)

# ── LOGIN ─────────────────────────────────────────────────────────────────────
def login_screen():
    st.markdown(f"""
    <div style='display:flex; flex-direction:column; align-items:center;
                justify-content:center; height:70vh; gap:8px;'>
      <div style='font-family:"Playfair Display",serif; font-size:2.2rem;
                  color:{DARK}; letter-spacing:0.04em;'>Casa Mater</div>
      <div style='font-size:0.75rem; color:{GRAY}; letter-spacing:0.12em;
                  text-transform:uppercase; margin-bottom:28px;'>Panel de Costos</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        pwd = st.text_input("Contraseña", type="password", label_visibility="collapsed",
                            placeholder="Contraseña")
        if st.button("Ingresar", use_container_width=True):
            correct = st.secrets.get("password", "casaMater2025!")
            if pwd == correct:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    st.stop()

if not st.session_state.get("auth"):
    login_screen()

# ── DATA LOADING ──────────────────────────────────────────────────────────────
def get_excel_path():
    if GDRIVE_FILE_ID:
        url  = f"https://docs.google.com/spreadsheets/d/{GDRIVE_FILE_ID}/export?format=xlsx"
        resp = requests.get(url, timeout=30)
        if resp.status_code != 200:
            st.error("No se pudo descargar el archivo. Verificá que el Google Sheet esté compartido como 'Cualquier persona con el enlace'.")
            st.stop()
        dest = "/tmp/Costos_Importacion.xlsx"
        with open(dest, "wb") as f:
            f.write(resp.content)
        return dest
    if LOCAL_EXCEL.exists():
        return str(LOCAL_EXCEL)
    st.error("⚙️ **Configuración pendiente:** agregá el `gdrive_file_id` en los Secrets de Streamlit Cloud.")
    st.info("Ir a: tu app → ⋮ → Settings → Secrets → agregar `gdrive_file_id = \"ID_del_archivo\"`")
    st.stop()

@st.cache_data(ttl=300)
def load_data():
    path = get_excel_path()
    prod = pd.read_excel(path, sheet_name="PRODUCTOS", header=1, dtype=str)
    prod.columns = [c.strip().replace("\n", " ") for c in prod.columns]

    log = pd.read_excel(path, sheet_name="LOGÍSTICA", header=1, dtype=str)
    log.columns = [c.strip().replace("\n", " ") for c in log.columns]

    # Rename to safe keys
    prod_cols = {
        prod.columns[0]:  "codigo",
        prod.columns[1]:  "nombre",
        prod.columns[2]:  "categoria",
        prod.columns[3]:  "proveedor",
        prod.columns[4]:  "pais",
        prod.columns[5]:  "fob_unit",
        prod.columns[6]:  "imp_unit",
        prod.columns[8]:  "tc",
        prod.columns[10]: "pvp",
        prod.columns[13]: "stock_act",
        prod.columns[14]: "stock_min",
        prod.columns[16]: "vendidas_30d",
        prod.columns[19]: "ult_recepcion",
        prod.columns[20]: "prox_orden",
        prod.columns[21]: "estado",
        prod.columns[22]: "id_embarque",
    }
    prod = prod.rename(columns=prod_cols)
    prod = prod[prod["codigo"].notna() & (prod["codigo"] != "")].copy()

    for col in ["fob_unit","imp_unit","tc","pvp","stock_act","stock_min","vendidas_30d"]:
        prod[col] = pd.to_numeric(prod[col], errors="coerce").fillna(0)

    prod["costo_landed"] = prod["fob_unit"] + prod["imp_unit"]
    prod["costo_ars"]    = prod["costo_landed"] * prod["tc"]
    prod["margen"]       = ((prod["pvp"] - prod["costo_ars"]) / prod["pvp"]).clip(-1, 1)
    prod["markup"]       = ((prod["pvp"] - prod["costo_ars"]) / prod["costo_ars"]).clip(-1, 5)
    prod["valor_inv"]    = prod["stock_act"] * prod["costo_ars"]
    prod["ult_recepcion"] = pd.to_datetime(prod["ult_recepcion"], errors="coerce")
    prod["prox_orden"]    = pd.to_datetime(prod["prox_orden"], errors="coerce")

    log_cols = {
        log.columns[0]:  "id",
        log.columns[1]:  "fecha_orden",
        log.columns[2]:  "eta",
        log.columns[3]:  "arribo_real",
        log.columns[5]:  "proveedor",
        log.columns[6]:  "pais",
        log.columns[7]:  "descripcion",
        log.columns[8]:  "incoterm",
        log.columns[9]:  "fob",
        log.columns[10]: "flete",
        log.columns[11]: "seguro",
        log.columns[21]: "despachante",
        log.columns[22]: "almacenaje",
        log.columns[23]: "transporte",
        log.columns[24]: "gastos_bco",
        log.columns[25]: "otros",
        log.columns[31]: "estado",
    }
    log = log.rename(columns=log_cols)
    log = log[log["id"].notna() & (log["id"] != "")].copy()

    for col in ["fob","flete","seguro","despachante","almacenaje","transporte","gastos_bco","otros"]:
        log[col] = pd.to_numeric(log[col], errors="coerce").fillna(0)

    arancel_col = log.columns[13] if len(log.columns) > 13 else None
    te_col      = log.columns[15] if len(log.columns) > 15 else None
    iva_col     = log.columns[17] if len(log.columns) > 17 else None
    percep_col  = log.columns[19] if len(log.columns) > 19 else None
    tc_col      = log.columns[29] if len(log.columns) > 29 else None

    for c in [arancel_col, te_col, iva_col, percep_col, tc_col]:
        if c:
            log[c] = pd.to_numeric(log[c], errors="coerce").fillna(0)

    cif = log["fob"] + log["flete"] + log["seguro"]
    if arancel_col:
        ar  = cif * log[arancel_col]
        te  = (cif + ar) * (log[te_col] if te_col else 0)
        iva = (cif + ar + te) * (log[iva_col] if iva_col else 0)
        per = (cif + ar + te + iva) * (log[percep_col] if percep_col else 0)
    else:
        ar = te = iva = per = 0

    log["cif"]         = cif
    log["arancel"]     = ar
    log["te"]          = te
    log["iva_imp"]     = iva
    log["percep"]      = per
    log["total_costos"] = (log["flete"] + log["seguro"] + ar + te + iva + per +
                           log["despachante"] + log["almacenaje"] +
                           log["transporte"] + log["gastos_bco"] + log["otros"])
    log["total_landed"] = log["fob"] + log["total_costos"]
    log["pct_costos"]   = (log["total_costos"] / log["fob"]).clip(0, 5)
    log["tc"]           = pd.to_numeric(log[tc_col], errors="coerce").fillna(1200) if tc_col else 1200
    log["landed_ars"]   = log["total_landed"] * log["tc"]

    log["fecha_orden"]  = pd.to_datetime(log["fecha_orden"], errors="coerce")
    log["eta"]          = pd.to_datetime(log["eta"],          errors="coerce")
    log["arribo_real"]  = pd.to_datetime(log["arribo_real"],  errors="coerce")

    return prod, log

prod_df, log_df = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 20px 0 10px;'>
      <div style='font-family:"Playfair Display",serif; font-size:1.4rem; color:{GOLD};'>Casa Mater</div>
      <div style='font-size:0.7rem; color:#888; letter-spacing:0.1em; text-transform:uppercase;'>Panel de Costos</div>
    </div>
    <hr style='border-color:#333; margin: 0 0 20px;'>
    """, unsafe_allow_html=True)

    tab_sel = st.radio("Sección", ["Categoría", "Productos", "Proveedores", "Logística"],
                       label_visibility="collapsed")

    st.markdown("<hr style='border-color:#333; margin: 16px 0;'>", unsafe_allow_html=True)

    if tab_sel == "Categoría":
        st.markdown("**Filtros**")

        min_date = prod_df["ult_recepcion"].dropna().min().date()
        max_date = prod_df["ult_recepcion"].dropna().max().date()

        date_desde = st.date_input("Recepción desde", value=min_date,
                                   min_value=min_date, max_value=max_date,
                                   key="p_desde")
        date_hasta = st.date_input("Recepción hasta", value=max_date,
                                   min_value=min_date, max_value=max_date,
                                   key="p_hasta")

        cats = ["Todas"] + sorted(prod_df["categoria"].dropna().unique().tolist())
        cat_sel = st.selectbox("Categoría", cats)

        provs = ["Todos"] + sorted(prod_df["proveedor"].dropna().unique().tolist())
        prov_sel = st.selectbox("Proveedor", provs)

        estados = ["Todos"] + sorted(prod_df["estado"].dropna().unique().tolist())
        est_sel = st.selectbox("Estado", estados)

    elif tab_sel == "Productos":
        st.markdown("**Buscar**")
        search_q = st.text_input("Nombre o SKU", placeholder="Ej: DEC-001 o Mesa...",
                                 label_visibility="collapsed")
        st.markdown("**Filtros**")
        cats_p = ["Todas"] + sorted(prod_df["categoria"].dropna().unique().tolist())
        cat_sel_p = st.selectbox("Categoría", cats_p, key="prd_cat")
        provs_p = ["Todos"] + sorted(prod_df["proveedor"].dropna().unique().tolist())
        prov_sel_p = st.selectbox("Proveedor", provs_p, key="prd_prov")
        est_p = ["Todos"] + sorted(prod_df["estado"].dropna().unique().tolist())
        est_sel_p = st.selectbox("Estado", est_p, key="prd_est")
        st.markdown("**Reorden**")
        dias_critico = st.slider("Días crítico", 5, 30, 15, key="ro_crit")
        dias_revisar = st.slider("Días revisar", 15, 60, 30, key="ro_rev")
        cats_ro = ["Todas"] + sorted(prod_df["categoria"].dropna().unique().tolist())
        cat_sel_ro = cat_sel_p  # usa el mismo filtro de categoría

    elif tab_sel == "Proveedores":
        st.markdown("**Filtros**")
        est_pv = ["Todos"] + sorted(prod_df["estado"].dropna().unique().tolist())
        est_sel_pv = st.selectbox("Estado producto", est_pv, key="pv_est")

    else:
        st.markdown("**Filtros**")

        min_date_l = log_df["fecha_orden"].dropna().min().date()
        max_date_l = log_df["fecha_orden"].dropna().max().date()

        date_desde_l = st.date_input("Orden desde", value=min_date_l,
                                     min_value=min_date_l, max_value=max_date_l,
                                     key="l_desde")
        date_hasta_l = st.date_input("Orden hasta", value=max_date_l,
                                     min_value=min_date_l, max_value=max_date_l,
                                     key="l_hasta")

        prov_l = ["Todos"] + sorted(log_df["proveedor"].dropna().unique().tolist())
        prov_sel_l = st.selectbox("Proveedor", prov_l)

        est_l = ["Todos"] + sorted(log_df["estado"].dropna().unique().tolist())
        est_sel_l = st.selectbox("Estado", est_l)

    st.markdown("""
    <hr style='border-color:#333; margin: 20px 0 12px;'>
    <div style='font-size:0.65rem; color:#555; text-align:center;'>
      Datos desde Costos_Importacion.xlsx<br>
      Actualiza automáticamente al guardar el Excel
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄  Recargar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ── HELPER ────────────────────────────────────────────────────────────────────
def export_button(df, filename, label="⬇  Exportar Excel"):
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    st.download_button(label=label, data=buf.getvalue(),
                       file_name=filename,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def kpi(label, value, color="", suffix="", prefix=""):
    return f"""
    <div class="kpi-card">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value {color}">{prefix}{value}{suffix}</div>
    </div>"""

def section(title):
    st.markdown(f'<div class="section-hdr">{title}</div>', unsafe_allow_html=True)

def chart_layout(fig, height=340):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Montserrat", color=DARK),
        margin=dict(t=48, b=48, l=10, r=10),
        height=height,
        title=dict(font=dict(size=13), x=0, xanchor="left", pad=dict(l=4)),
        legend=dict(orientation="h", yanchor="top", y=-0.12,
                    xanchor="center", x=0.5,
                    font=dict(size=11)),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EEEEEE", zeroline=False)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# TAB — CATEGORÍA
# ══════════════════════════════════════════════════════════════════════════════
if tab_sel == "Categoría":
    st.markdown('<div class="page-title">Análisis por Categoría</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Recepción: {date_desde.strftime("%d/%m/%Y")} → {date_hasta.strftime("%d/%m/%Y")}  ·  {cat_sel}  ·  {prov_sel}</div>', unsafe_allow_html=True)

    # ── Filter ──────────────────────────────────────────────────────────────
    mask = (
        (prod_df["ult_recepcion"].dt.date >= date_desde) &
        (prod_df["ult_recepcion"].dt.date <= date_hasta)
    )
    if cat_sel  != "Todas":  mask &= prod_df["categoria"] == cat_sel
    if prov_sel != "Todos":  mask &= prod_df["proveedor"] == prov_sel
    if est_sel  != "Todos":  mask &= prod_df["estado"]    == est_sel

    df = prod_df[mask].copy()
    df_all = prod_df.copy()  # for stock (always current)

    # ── KPIs ─────────────────────────────────────────────────────────────────
    total_skus    = len(df_all)
    activos       = int((df_all["estado"] == "Activo").sum())
    valor_inv     = df["valor_inv"].sum()
    margen_prom   = df["margen"].mean() if len(df) > 0 else 0
    bajo_stock    = int(((df_all["stock_act"] <= df_all["stock_min"]) & (df_all["stock_act"] > 0)).sum())
    sin_stock     = int((df_all["stock_act"] == 0).sum())
    ventas_30d    = int(df["vendidas_30d"].sum())

    cols = st.columns(7, gap="small")
    cards = [
        (cols[0], "Total SKUs",       f"{total_skus}",                        ""),
        (cols[1], "SKUs Activos",     f"{activos}",                           "green"),
        (cols[2], "Valor Inventario", f"${valor_inv/1_000_000:.1f}M",         ""),
        (cols[3], "Margen Prom.",     f"{margen_prom:.0%}",                   "teal" if margen_prom >= 0.4 else ("" if margen_prom >= 0.3 else "red")),
        (cols[4], "Stock Bajo",       f"{bajo_stock}",                        "orange" if bajo_stock > 0 else "green"),
        (cols[5], "Sin Stock",        f"{sin_stock}",                         "red" if sin_stock > 0 else "green"),
        (cols[6], "Ventas 30d",       f"{ventas_30d} uds",                    "navy"),
    ]
    for col_, label_, val_, color_ in cards:
        with col_:
            st.markdown(kpi(label_, val_, color_), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row 1 ─────────────────────────────────────────────────────────
    section("Rentabilidad y Distribución")
    c1, c2 = st.columns(2, gap="large")

    with c1:
        # Margen bruto por categoría
        cat_mg = (df.groupby("categoria")["margen"]
                  .mean().reset_index()
                  .sort_values("margen", ascending=True))
        cat_mg["margen_pct"] = (cat_mg["margen"] * 100).round(1)
        cat_mg["color"] = cat_mg["margen"].apply(
            lambda x: GRN if x >= 0.5 else (ORG if x >= 0.3 else RED))
        fig1 = px.bar(cat_mg, x="margen_pct", y="categoria", orientation="h",
                      title="Margen Bruto Promedio por Categoría (%)",
                      color="color", color_discrete_map="identity",
                      text="margen_pct")
        fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig1.update_layout(showlegend=False, xaxis_title="Margen %", yaxis_title="")
        st.plotly_chart(chart_layout(fig1), use_container_width=True)

    with c2:
        # Distribución de inventario
        cat_inv = (df.groupby("categoria")["valor_inv"]
                   .sum().reset_index()
                   .sort_values("valor_inv", ascending=False))
        cat_inv = cat_inv[cat_inv["valor_inv"] > 0]
        fig2 = px.pie(cat_inv, values="valor_inv", names="categoria",
                      title="Distribución del Valor de Inventario",
                      color_discrete_sequence=CHART_COLORS, hole=0.4)
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        fig2.update_layout(legend=dict(orientation="v", yanchor="middle", y=0.5,
                                       xanchor="left", x=1.02))
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    # ── Charts row 2 ─────────────────────────────────────────────────────────
    section("Stock y Actividad")
    c3, c4 = st.columns(2, gap="large")

    with c3:
        # Stock actual vs mínimo
        cat_stk = df_all.groupby("categoria").agg(
            act=("stock_act", "sum"),
            min_=("stock_min", "sum")
        ).reset_index().sort_values("act", ascending=False)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name="Stock Actual", x=cat_stk["categoria"],
                               y=cat_stk["act"], marker_color=NAVY))
        fig3.add_trace(go.Bar(name="Stock Mínimo", x=cat_stk["categoria"],
                               y=cat_stk["min_"], marker_color=RED,
                               opacity=0.75))
        fig3.update_layout(title="Stock Actual vs Mínimo por Categoría",
                           barmode="group", xaxis_title="", yaxis_title="Unidades",
                           legend=dict(orientation="h", yanchor="top", y=-0.15,
                                       xanchor="center", x=0.5))
        st.plotly_chart(chart_layout(fig3), use_container_width=True)

    with c4:
        # Ventas 30d por categoría
        cat_v = (df.groupby("categoria")["vendidas_30d"]
                 .sum().reset_index()
                 .sort_values("vendidas_30d", ascending=False))
        cat_v = cat_v[cat_v["vendidas_30d"] > 0]
        fig4 = px.bar(cat_v, x="categoria", y="vendidas_30d",
                      title="Ventas Últimos 30 Días por Categoría",
                      color="vendidas_30d",
                      color_continuous_scale=[[0,GOLD],[1,TEAL]],
                      text="vendidas_30d")
        fig4.update_traces(textposition="outside")
        fig4.update_layout(showlegend=False, coloraxis_showscale=False,
                           xaxis_title="", yaxis_title="Unidades")
        st.plotly_chart(chart_layout(fig4), use_container_width=True)

    # ── Alerts ───────────────────────────────────────────────────────────────
    alertas = df_all[df_all["stock_act"] <= df_all["stock_min"]].copy()
    if len(alertas) > 0:
        section(f"⚠ Alertas de Stock ({len(alertas)} productos)")
        for _, row in alertas.iterrows():
            badge = '<span class="badge-red">SIN STOCK</span>' if row["stock_act"] == 0 \
                    else '<span class="badge-orange">STOCK BAJO</span>'
            st.markdown(
                f"{badge} &nbsp; <b>{row['codigo']}</b> · {row['nombre']} &nbsp;|&nbsp; "
                f"Actual: <b>{int(row['stock_act'])}</b> &nbsp;·&nbsp; Mínimo: {int(row['stock_min'])}",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB — PRODUCTOS
# ══════════════════════════════════════════════════════════════════════════════
elif tab_sel == "Productos":

    # ── Filter ────────────────────────────────────────────────────────────────
    dpf = prod_df.copy()
    if search_q:
        q = search_q.lower()
        dpf = dpf[dpf["codigo"].str.lower().str.contains(q, na=False) |
                  dpf["nombre"].str.lower().str.contains(q, na=False)]
    if cat_sel_p  != "Todas":  dpf = dpf[dpf["categoria"] == cat_sel_p]
    if prov_sel_p != "Todos":  dpf = dpf[dpf["proveedor"] == prov_sel_p]
    if est_sel_p  != "Todos":  dpf = dpf[dpf["estado"]    == est_sel_p]

    n_res = len(dpf)
    subtitle = f"{n_res} producto{'s' if n_res != 1 else ''} encontrado{'s' if n_res != 1 else ''}"
    if search_q: subtitle += f"  ·  Búsqueda: \"{search_q}\""

    st.markdown('<div class="page-title">Detalle por Producto</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

    if n_res == 0:
        st.info("No se encontraron productos con ese criterio.")
    else:
        # ── KPIs ─────────────────────────────────────────────────────────────
        margen_p   = dpf["margen"].mean()
        valor_p    = dpf["valor_inv"].sum()
        ventas_p   = int(dpf["vendidas_30d"].sum())
        bajo_p     = int(((dpf["stock_act"] <= dpf["stock_min"]) & (dpf["stock_act"] > 0)).sum())
        sin_p      = int((dpf["stock_act"] == 0).sum())
        markup_p   = dpf["markup"].mean()

        cols_p = st.columns(6, gap="small")
        cards_p = [
            (cols_p[0], "SKUs",            f"{n_res}",                   ""),
            (cols_p[1], "Valor Inventario", f"${valor_p/1_000_000:.1f}M",""),
            (cols_p[2], "Margen Prom.",    f"{margen_p:.0%}",            "teal" if margen_p >= 0.4 else ("" if margen_p >= 0.3 else "red")),
            (cols_p[3], "Markup Prom.",    f"{markup_p:.0%}",            "navy"),
            (cols_p[4], "Stock Bajo",      f"{bajo_p}",                  "orange" if bajo_p > 0 else "green"),
            (cols_p[5], "Ventas 30d",      f"{ventas_p} uds",            "green"),
        ]
        for col_, label_, val_, color_ in cards_p:
            with col_:
                st.markdown(kpi(label_, val_, color_), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Charts row 1 ─────────────────────────────────────────────────────
        section("Rentabilidad por Producto")
        c1p, c2p = st.columns(2, gap="large")

        with c1p:
            mg_prod = dpf.sort_values("margen", ascending=True).copy()
            mg_prod["color"] = mg_prod["margen"].apply(
                lambda x: GRN if x >= 0.5 else (ORG if x >= 0.3 else RED))
            mg_prod["label"] = mg_prod["codigo"] + "  " + mg_prod["nombre"].str[:22]
            fig_mg = px.bar(mg_prod, x="margen", y="label", orientation="h",
                            title="Margen Bruto por Producto",
                            color="color", color_discrete_map="identity",
                            text=mg_prod["margen"].map(lambda x: f"{x:.1%}"))
            fig_mg.update_traces(textposition="outside")
            fig_mg.update_layout(showlegend=False, xaxis_title="Margen %",
                                 yaxis_title="", xaxis_tickformat=".0%")
            st.plotly_chart(chart_layout(fig_mg, height=max(320, n_res * 32 + 60)),
                            use_container_width=True)

        with c2p:
            fig_sc = px.scatter(dpf,
                                x="vendidas_30d", y="margen",
                                size="valor_inv", color="categoria",
                                hover_name="nombre",
                                hover_data={"codigo": True, "pvp": True,
                                            "valor_inv": True, "vendidas_30d": True},
                                title="Margen vs Ventas 30d  (tamaño = valor inventario)",
                                color_discrete_sequence=CHART_COLORS)
            fig_sc.update_layout(yaxis_tickformat=".0%", xaxis_title="Unidades vendidas 30d",
                                 yaxis_title="Margen %",
                                 legend=dict(orientation="h", yanchor="top", y=-0.18,
                                             xanchor="center", x=0.5, font=dict(size=10)))
            st.plotly_chart(chart_layout(fig_sc), use_container_width=True)

        # ── Charts row 2 ─────────────────────────────────────────────────────
        section("Stock e Inventario")
        c3p, c4p = st.columns(2, gap="large")

        with c3p:
            stk_prod = dpf.sort_values("stock_act", ascending=False).copy()
            stk_prod["label"] = stk_prod["codigo"] + " · " + stk_prod["nombre"].str[:18]
            fig_stk = go.Figure()
            fig_stk.add_trace(go.Bar(name="Stock Actual", y=stk_prod["label"],
                                     x=stk_prod["stock_act"], orientation="h",
                                     marker_color=NAVY))
            fig_stk.add_trace(go.Bar(name="Stock Mínimo", y=stk_prod["label"],
                                     x=stk_prod["stock_min"], orientation="h",
                                     marker_color=RED, opacity=0.7))
            fig_stk.update_layout(title="Stock Actual vs Mínimo",
                                  barmode="overlay", xaxis_title="Unidades", yaxis_title="",
                                  legend=dict(orientation="h", yanchor="top", y=-0.12,
                                              xanchor="center", x=0.5))
            st.plotly_chart(chart_layout(fig_stk, height=max(320, n_res * 32 + 60)),
                            use_container_width=True)

        with c4p:
            inv_prod = dpf.sort_values("valor_inv", ascending=False).copy()
            inv_prod["label"] = inv_prod["codigo"]
            fig_inv = px.bar(inv_prod, x="label", y="valor_inv",
                             title="Valor de Inventario por Producto (ARS)",
                             color="categoria", color_discrete_sequence=CHART_COLORS,
                             text=inv_prod["valor_inv"].map(lambda x: f"${x/1000:.0f}K"))
            fig_inv.update_traces(textposition="outside")
            fig_inv.update_layout(xaxis_title="", yaxis_title="ARS",
                                  yaxis_tickformat=",.0f")
            st.plotly_chart(chart_layout(fig_inv), use_container_width=True)

        # ── Detail table ─────────────────────────────────────────────────────
        section("Ficha de Productos")
        show_cols = ["codigo","nombre","categoria","proveedor","pais",
                     "fob_unit","imp_unit","costo_landed","costo_ars","pvp",
                     "margen","markup","stock_act","stock_min","vendidas_30d",
                     "valor_inv","ult_recepcion","prox_orden","estado","id_embarque"]
        disp = dpf[show_cols].copy()
        disp.columns = ["Código","Nombre","Categoría","Proveedor","País",
                        "FOB USD","Imp. USD","Landed USD","Costo ARS","PVP ARS",
                        "Margen %","Markup %","Stock","Stk. Mín","Ventas 30d",
                        "Valor Inv.","Últ. Recep.","Próx. Orden","Estado","Embarque"]
        disp["Margen %"]   = disp["Margen %"].map(lambda x: f"{x:.1%}")
        disp["Markup %"]   = disp["Markup %"].map(lambda x: f"{x:.1%}")
        disp["FOB USD"]    = disp["FOB USD"].map(lambda x: f"${x:,.2f}")
        disp["Imp. USD"]   = disp["Imp. USD"].map(lambda x: f"${x:,.2f}")
        disp["Landed USD"] = disp["Landed USD"].map(lambda x: f"${x:,.2f}")
        disp["Costo ARS"]  = disp["Costo ARS"].map(lambda x: f"${x:,.0f}")
        disp["PVP ARS"]    = disp["PVP ARS"].map(lambda x: f"${x:,.0f}")
        disp["Valor Inv."] = disp["Valor Inv."].map(lambda x: f"${x:,.0f}")
        disp["Últ. Recep."] = pd.to_datetime(disp["Últ. Recep."]).dt.strftime("%d/%m/%Y")
        disp["Próx. Orden"] = pd.to_datetime(disp["Próx. Orden"]).dt.strftime("%d/%m/%Y")
        st.dataframe(disp, use_container_width=True, hide_index=True,
                     height=min(500, 38 + n_res * 35))
        st.markdown("<br>", unsafe_allow_html=True)
        export_button(dpf[show_cols].rename(columns=dict(zip(show_cols, disp.columns))),
                      "productos_filtrados.xlsx")

        # ── Panel de Reorden ─────────────────────────────────────────────────
        section("Panel de Reorden")
        dro = dpf.copy()
        dro["ventas_dia"] = dro["vendidas_30d"] / 30
        dro["dias_stock"] = dro.apply(
            lambda r: round(r["stock_act"] / r["ventas_dia"]) if r["ventas_dia"] > 0 else 999, axis=1)
        dro["urgencia"] = dro["dias_stock"].apply(
            lambda x: "SIN MOVIMIENTO" if x == 999
            else ("CRÍTICO"  if x < dias_critico
            else ("REVISAR"  if x < dias_revisar
            else  "OK")))
        dro["color_urg"] = dro["urgencia"].map(
            {"CRÍTICO": RED, "REVISAR": ORG, "OK": GRN, "SIN MOVIMIENTO": GRAY})

        criticos = int((dro["urgencia"] == "CRÍTICO").sum())
        revisar  = int((dro["urgencia"] == "REVISAR").sum())
        ok_      = int((dro["urgencia"] == "OK").sum())
        sin_mov  = int((dro["urgencia"] == "SIN MOVIMIENTO").sum())

        cr1, cr2, cr3, cr4 = st.columns(4, gap="small")
        for col_, lbl_, val_, clr_ in [
            (cr1, f"Crítico  (<{dias_critico}d)", str(criticos), "red"    if criticos else "green"),
            (cr2, f"Revisar  (<{dias_revisar}d)", str(revisar),  "orange" if revisar  else "green"),
            (cr3, "OK",                           str(ok_),      "green"),
            (cr4, "Sin movimiento",               str(sin_mov),  ""),
        ]:
            with col_: st.markdown(kpi(lbl_, val_, clr_), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        activos_ro = dro[dro["urgencia"] != "SIN MOVIMIENTO"].sort_values("dias_stock")
        if len(activos_ro) > 0:
            activos_ro = activos_ro.copy()
            activos_ro["label"] = activos_ro["codigo"] + "  " + activos_ro["nombre"].str[:22]
            activos_ro["dias_display"] = activos_ro["dias_stock"].clip(upper=90)
            fig_ro = px.bar(activos_ro, x="dias_display", y="label", orientation="h",
                            title="Días de Stock Restantes",
                            color="color_urg", color_discrete_map="identity",
                            text=activos_ro["dias_stock"].map(lambda x: f"{int(x)}d" if x < 90 else "90d+"))
            fig_ro.update_traces(textposition="outside")
            fig_ro.add_vline(x=dias_critico, line_dash="dash", line_color=RED,
                             annotation_text=f"Crítico", annotation_position="top right")
            fig_ro.add_vline(x=dias_revisar, line_dash="dash", line_color=ORG,
                             annotation_text=f"Revisar", annotation_position="top right")
            fig_ro.update_layout(showlegend=False, xaxis_title="Días de stock", yaxis_title="")
            st.plotly_chart(chart_layout(fig_ro, height=max(300, len(activos_ro)*30+80)),
                            use_container_width=True)

        dro_disp = dro.sort_values("dias_stock")[
            ["codigo","nombre","categoria","proveedor","stock_act","stock_min",
             "vendidas_30d","dias_stock","urgencia","prox_orden"]].copy()
        dro_disp.columns = ["Código","Nombre","Categoría","Proveedor","Stock","Mín.",
                             "Ventas 30d","Días Stock","Urgencia","Próx. Orden"]
        dro_disp["Días Stock"]  = dro_disp["Días Stock"].map(lambda x: "Sin mov." if x==999 else f"{int(x)}d")
        dro_disp["Próx. Orden"] = pd.to_datetime(dro_disp["Próx. Orden"]).dt.strftime("%d/%m/%Y")
        st.dataframe(dro_disp, use_container_width=True, hide_index=True,
                     height=min(400, 38 + len(dro_disp)*35))
        st.markdown("<br>", unsafe_allow_html=True)
        export_button(dro_disp, "panel_reorden.xlsx")

# ══════════════════════════════════════════════════════════════════════════════
# TAB — PROVEEDORES
# ══════════════════════════════════════════════════════════════════════════════
elif tab_sel == "Proveedores":
    st.markdown('<div class="page-title">Análisis de Proveedores</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Comparativa de rentabilidad, stock y actividad por proveedor</div>', unsafe_allow_html=True)

    dpv = prod_df.copy()
    if est_sel_pv != "Todos": dpv = dpv[dpv["estado"] == est_sel_pv]

    dpv["stock_bajo"] = (dpv["stock_act"] <= dpv["stock_min"]).astype(int)

    prov_sum = dpv.groupby("proveedor").agg(
        SKUs          = ("codigo",      "count"),
        margen_prom   = ("margen",      "mean"),
        markup_prom   = ("markup",      "mean"),
        valor_inv     = ("valor_inv",   "sum"),
        ventas_30d    = ("vendidas_30d","sum"),
        stock_bajo    = ("stock_bajo",  "sum"),
        pais          = ("pais",        "first"),
    ).reset_index().sort_values("valor_inv", ascending=False)

    # ── KPIs ─────────────────────────────────────────────────────────────────
    n_prov = len(prov_sum)
    mejor_margen = prov_sum.loc[prov_sum["margen_prom"].idxmax(), "proveedor"]
    mayor_inv    = prov_sum.loc[prov_sum["valor_inv"].idxmax(),   "proveedor"]
    total_alerta = int(prov_sum["stock_bajo"].sum())

    cols_pv = st.columns(4, gap="small")
    for col_, lbl_, val_, clr_ in [
        (cols_pv[0], "Proveedores",       str(n_prov),        ""),
        (cols_pv[1], "Mayor Margen",      mejor_margen[:14],  "teal"),
        (cols_pv[2], "Mayor Inventario",  mayor_inv[:14],     "navy"),
        (cols_pv[3], "SKUs con Alerta",   str(total_alerta),  "red" if total_alerta else "green"),
    ]:
        with col_: st.markdown(kpi(lbl_, val_, clr_), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    section("Rentabilidad")
    c1v, c2v = st.columns(2, gap="large")

    with c1v:
        mg_pv = prov_sum.sort_values("margen_prom", ascending=True)
        mg_pv["color"] = mg_pv["margen_prom"].apply(
            lambda x: GRN if x >= 0.5 else (ORG if x >= 0.3 else RED))
        fig_pv1 = px.bar(mg_pv, x="margen_prom", y="proveedor", orientation="h",
                         title="Margen Bruto Promedio por Proveedor",
                         color="color", color_discrete_map="identity",
                         text=mg_pv["margen_prom"].map(lambda x: f"{x:.1%}"))
        fig_pv1.update_traces(textposition="outside")
        fig_pv1.update_layout(showlegend=False, xaxis_tickformat=".0%",
                              xaxis_title="Margen %", yaxis_title="")
        st.plotly_chart(chart_layout(fig_pv1), use_container_width=True)

    with c2v:
        fig_pv2 = px.scatter(prov_sum, x="ventas_30d", y="margen_prom",
                             size="valor_inv", color="proveedor",
                             hover_name="proveedor",
                             hover_data={"SKUs": True, "valor_inv": True},
                             title="Margen vs Ventas  (tamaño = valor inventario)",
                             color_discrete_sequence=CHART_COLORS)
        fig_pv2.update_layout(yaxis_tickformat=".0%",
                              xaxis_title="Ventas 30d (uds)", yaxis_title="Margen %",
                              legend=dict(orientation="h", yanchor="top", y=-0.18,
                                          xanchor="center", x=0.5, font=dict(size=10)))
        st.plotly_chart(chart_layout(fig_pv2), use_container_width=True)

    section("Inventario y Actividad")
    c3v, c4v = st.columns(2, gap="large")

    with c3v:
        fig_pv3 = px.bar(prov_sum.sort_values("valor_inv", ascending=False),
                         x="proveedor", y="valor_inv",
                         title="Valor de Inventario por Proveedor (ARS)",
                         color="proveedor", color_discrete_sequence=CHART_COLORS,
                         text=prov_sum.sort_values("valor_inv", ascending=False)
                              ["valor_inv"].map(lambda x: f"${x/1_000_000:.1f}M"))
        fig_pv3.update_traces(textposition="outside")
        fig_pv3.update_layout(showlegend=False, xaxis_title="", yaxis_title="ARS")
        st.plotly_chart(chart_layout(fig_pv3), use_container_width=True)

    with c4v:
        fig_pv4 = go.Figure()
        fig_pv4.add_trace(go.Bar(name="SKUs totales", x=prov_sum["proveedor"],
                                  y=prov_sum["SKUs"], marker_color=NAVY))
        fig_pv4.add_trace(go.Bar(name="SKUs con alerta", x=prov_sum["proveedor"],
                                  y=prov_sum["stock_bajo"], marker_color=RED, opacity=0.8))
        fig_pv4.update_layout(title="SKUs totales vs con Alerta de Stock",
                               barmode="overlay", xaxis_title="", yaxis_title="SKUs",
                               legend=dict(orientation="h", yanchor="top", y=-0.15,
                                           xanchor="center", x=0.5))
        st.plotly_chart(chart_layout(fig_pv4), use_container_width=True)

    section("Tabla Resumen")
    disp_pv = prov_sum[["proveedor","pais","SKUs","margen_prom","markup_prom",
                         "valor_inv","ventas_30d","stock_bajo"]].copy()
    disp_pv.columns = ["Proveedor","País","SKUs","Margen %","Markup %",
                        "Valor Inv. ARS","Ventas 30d","Alertas Stock"]
    disp_pv["Margen %"]      = disp_pv["Margen %"].map(lambda x: f"{x:.1%}")
    disp_pv["Markup %"]      = disp_pv["Markup %"].map(lambda x: f"{x:.1%}")
    disp_pv["Valor Inv. ARS"] = disp_pv["Valor Inv. ARS"].map(lambda x: f"${x:,.0f}")
    st.dataframe(disp_pv, use_container_width=True, hide_index=True)
    st.markdown("<br>", unsafe_allow_html=True)
    export_button(disp_pv, "proveedores.xlsx")

# ══════════════════════════════════════════════════════════════════════════════
# TAB — LOGÍSTICA
# ══════════════════════════════════════════════════════════════════════════════
elif tab_sel == "Logística":
    st.markdown('<div class="page-title">Logística &amp; Importación</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Órdenes: {date_desde_l.strftime("%d/%m/%Y")} → {date_hasta_l.strftime("%d/%m/%Y")}  ·  {prov_sel_l}  ·  {est_sel_l}</div>', unsafe_allow_html=True)

    # ── Filter ────────────────────────────────────────────────────────────────
    mask_l = (
        (log_df["fecha_orden"].dt.date >= date_desde_l) &
        (log_df["fecha_orden"].dt.date <= date_hasta_l)
    )
    if prov_sel_l != "Todos": mask_l &= log_df["proveedor"] == prov_sel_l
    if est_sel_l  != "Todos": mask_l &= log_df["estado"]    == est_sel_l

    dl = log_df[mask_l].copy()

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total_fob     = dl["fob"].sum()
    total_landed  = dl["total_landed"].sum()
    total_ars     = dl["landed_ars"].sum()
    pct_costos    = dl["pct_costos"].mean() if len(dl) > 0 else 0
    n_embarques   = len(dl)
    en_transito   = int((dl["estado"] == "En tránsito").sum())

    cols_l = st.columns(6, gap="small")
    cards_l = [
        (cols_l[0], "Embarques",        f"{n_embarques}",                   ""),
        (cols_l[1], "En Tránsito",      f"{en_transito}",                   "navy"),
        (cols_l[2], "Total FOB",        f"USD {total_fob/1000:.1f}K",       ""),
        (cols_l[3], "Total Landed USD", f"USD {total_landed/1000:.1f}K",    ""),
        (cols_l[4], "Total Landed ARS", f"${total_ars/1_000_000:.1f}M",     ""),
        (cols_l[5], "% Costos s/FOB",   f"{pct_costos:.0%}",                "teal"),
    ]
    for col_, label_, val_, color_ in cards_l:
        with col_:
            st.markdown(kpi(label_, val_, color_), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    section("Composición de Costos por Embarque")
    c1l, c2l = st.columns([3, 2], gap="large")

    with c1l:
        # Stacked bar: FOB vs costos
        fig_s = go.Figure()
        fig_s.add_trace(go.Bar(name="FOB", x=dl["id"], y=dl["fob"],
                                marker_color=NAVY))
        fig_s.add_trace(go.Bar(name="Costos Importación",
                                x=dl["id"], y=dl["total_costos"],
                                marker_color=GOLD))
        fig_s.update_layout(title="FOB vs Costos de Importación (USD)",
                             barmode="stack", xaxis_title="", yaxis_title="USD",
                             legend=dict(orientation="h", yanchor="top", y=-0.15,
                                         xanchor="center", x=0.5))
        st.plotly_chart(chart_layout(fig_s), use_container_width=True)

    with c2l:
        # Pie: desglose de costos (promedio)
        cost_names = ["Flete","Seguro","Arancel","Tasa Est.",
                      "IVA Imp.","Percepciones","Despachante",
                      "Almacenaje","Transporte","Gastos Bco.","Otros"]
        cost_cols  = ["flete","seguro","arancel","te","iva_imp","percep",
                      "despachante","almacenaje","transporte","gastos_bco","otros"]
        cost_vals  = [dl[c].sum() for c in cost_cols]
        cost_df    = pd.DataFrame({"Componente": cost_names, "USD": cost_vals})
        cost_df    = cost_df[cost_df["USD"] > 0]

        fig_p = px.pie(cost_df, values="USD", names="Componente",
                       title="Composición de Costos",
                       color_discrete_sequence=CHART_COLORS, hole=0.35)
        fig_p.update_traces(textposition="inside", textinfo="percent+label",
                            textfont_size=10)
        fig_p.update_layout(legend=dict(orientation="v", yanchor="middle", y=0.5,
                                        xanchor="left", x=1.02, font=dict(size=10)))
        st.plotly_chart(chart_layout(fig_p, height=320), use_container_width=True)

    section("Eficiencia por Embarque")
    c3l, c4l = st.columns(2, gap="large")

    with c3l:
        # % costos s/FOB por embarque
        fig_pct = px.bar(dl.sort_values("pct_costos", ascending=False),
                         x="id", y="pct_costos",
                         title="% Costos sobre FOB por Embarque",
                         color="pct_costos",
                         color_continuous_scale=[[0, GRN], [0.5, GOLD], [1, RED]],
                         text=dl.sort_values("pct_costos", ascending=False)
                              ["pct_costos"].map(lambda x: f"{x:.0%}"))
        fig_pct.update_traces(textposition="outside")
        fig_pct.update_layout(showlegend=False, coloraxis_showscale=False,
                              xaxis_title="", yaxis_title="% s/FOB",
                              yaxis_tickformat=".0%")
        st.plotly_chart(chart_layout(fig_pct), use_container_width=True)

    with c4l:
        # Total Landed ARS por embarque
        fig_ars = px.bar(dl.sort_values("landed_ars", ascending=False),
                         x="id", y="landed_ars",
                         title="Total Landed ARS por Embarque",
                         color_discrete_sequence=[TEAL],
                         text=dl.sort_values("landed_ars", ascending=False)
                              ["landed_ars"].map(lambda x: f"${x/1_000_000:.1f}M"))
        fig_ars.update_traces(textposition="outside")
        fig_ars.update_layout(xaxis_title="", yaxis_title="ARS",
                              yaxis_tickformat=",.0f")
        st.plotly_chart(chart_layout(fig_ars), use_container_width=True)

    # ── Data table ────────────────────────────────────────────────────────────
    section("Detalle de Embarques")
    show_l = ["id","fecha_orden","eta","arribo_real","proveedor","pais",
              "incoterm","fob","total_costos","total_landed","pct_costos",
              "landed_ars","estado"]
    disp_l = dl[show_l].copy()
    disp_l.columns = ["ID","Fecha Orden","ETA","Arribo Real","Proveedor","País",
                      "Incoterm","FOB USD","Costos Imp.","Total Landed USD",
                      "% Costos","Landed ARS","Estado"]
    disp_l["Fecha Orden"]    = disp_l["Fecha Orden"].dt.strftime("%d/%m/%Y")
    disp_l["ETA"]            = disp_l["ETA"].dt.strftime("%d/%m/%Y")
    disp_l["Arribo Real"]    = disp_l["Arribo Real"].dt.strftime("%d/%m/%Y")
    disp_l["FOB USD"]        = disp_l["FOB USD"].map(lambda x: f"${x:,.0f}")
    disp_l["Costos Imp."]    = disp_l["Costos Imp."].map(lambda x: f"${x:,.0f}")
    disp_l["Total Landed USD"] = disp_l["Total Landed USD"].map(lambda x: f"${x:,.0f}")
    disp_l["% Costos"]       = disp_l["% Costos"].map(lambda x: f"{x:.1%}")
    disp_l["Landed ARS"]     = disp_l["Landed ARS"].map(lambda x: f"${x:,.0f}")
    st.dataframe(disp_l, use_container_width=True, hide_index=True,
                 height=min(400, 38 + len(disp_l)*35))
    st.markdown("<br>", unsafe_allow_html=True)
    export_button(disp_l, "logistica.xlsx")
