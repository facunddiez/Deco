"""Casa Mater — Dashboard de Costos e Importación"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gdown
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
        dest = "/tmp/Costos_Importacion.xlsx"
        gdown.download(id=GDRIVE_FILE_ID, output=dest, quiet=True)
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

    tab_sel = st.radio("Sección", ["Productos", "Logística"],
                       label_visibility="collapsed")

    st.markdown("<hr style='border-color:#333; margin: 16px 0;'>", unsafe_allow_html=True)

    if tab_sel == "Productos":
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
        margin=dict(t=40, b=20, l=10, r=10),
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EEEEEE", zeroline=False)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# TAB — PRODUCTOS
# ══════════════════════════════════════════════════════════════════════════════
if tab_sel == "Productos":
    st.markdown('<div class="page-title">Productos &amp; Costos</div>', unsafe_allow_html=True)
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
                           barmode="group", xaxis_title="", yaxis_title="Unidades")
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

    # ── Data table ────────────────────────────────────────────────────────────
    section("Detalle de Productos")
    show_cols = ["codigo","nombre","categoria","proveedor",
                 "fob_unit","costo_landed","costo_ars","pvp",
                 "margen","stock_act","vendidas_30d","estado"]
    disp = df[show_cols].copy()
    disp.columns = ["Código","Nombre","Categoría","Proveedor",
                    "FOB USD","Landed USD","Costo ARS","PVP ARS",
                    "Margen %","Stock","Ventas 30d","Estado"]
    disp["Margen %"] = disp["Margen %"].map(lambda x: f"{x:.1%}")
    disp["FOB USD"]  = disp["FOB USD"].map(lambda x: f"${x:,.2f}")
    disp["Landed USD"] = disp["Landed USD"].map(lambda x: f"${x:,.2f}")
    disp["Costo ARS"] = disp["Costo ARS"].map(lambda x: f"${x:,.0f}")
    disp["PVP ARS"]   = disp["PVP ARS"].map(lambda x: f"${x:,.0f}")
    st.dataframe(disp, use_container_width=True, hide_index=True,
                 height=min(400, 38 + len(disp)*35))

# ══════════════════════════════════════════════════════════════════════════════
# TAB — LOGÍSTICA
# ══════════════════════════════════════════════════════════════════════════════
else:
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
                             barmode="stack", xaxis_title="", yaxis_title="USD")
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
        fig_p.update_traces(textposition="inside", textinfo="percent+label")
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
