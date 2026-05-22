import base64
import html
import io
import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Catálogo · Casa Mater", layout="wide", page_icon="🛍️")

FOTOS_DIR    = Path(__file__).parent / "fotos"
PACKINGS_DIR = Path(__file__).parent.parent / "Packings Formateados"
IMG_EXTS     = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
COLS         = 4

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #f5f0ea !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #1c1c1e !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #e8e0d5 !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: #2c2c2e !important; border: 1px solid #3a3a3c !important;
    color: #e8e0d5 !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] hr { border-color: #3a3a3c !important; }
[data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #c9a96e !important; font-size: 28px !important; }
[data-testid="stSidebar"] [data-testid="stMetricLabel"] { color: #888 !important; font-size: 11px !important; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

h1 {
    font-family: 'Playfair Display', serif !important;
    color: #1c1c1e !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}

/* ── Section header ── */
.section-header {
    display: flex; justify-content: space-between; align-items: baseline;
    margin: 40px 0 16px 0; padding-bottom: 10px;
    border-bottom: 2px solid #c9a96e;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px; color: #1c1c1e; font-weight: 600;
}
.section-count {
    font-size: 12px; color: #aaa; font-weight: 400;
    font-family: 'Inter', sans-serif;
}

/* ── Cards ── */
.card {
    background: #fff; border-radius: 14px; overflow: hidden;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    transition: box-shadow 0.25s, transform 0.25s;
    margin-bottom: 4px;
    cursor: pointer;
}
.card:hover {
    box-shadow: 0 8px 28px rgba(0,0,0,0.13);
    transform: translateY(-2px);
}
.card-img {
    width: 100%; height: 210px;
    object-fit: cover; display: block;
    background: #f0ebe3;
}
.card-no-img {
    width: 100%; height: 210px;
    background: linear-gradient(135deg, #f0ebe3 0%, #e8e0d5 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 40px; color: #c9a96e;
}
.card-body { padding: 14px 16px 16px; }
.card-sku {
    font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #c9a96e; margin-bottom: 5px;
}
.card-name {
    font-size: 13px; font-weight: 600; color: #1c1c1e;
    line-height: 1.4; margin-bottom: 8px; min-height: 36px;
    font-family: 'Inter', sans-serif;
}
.card-footer {
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 4px;
}
.card-price {
    font-size: 14px; font-weight: 700; color: #1c1c1e;
}
.card-cat {
    font-size: 10px; color: #bbb; font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.5px;
}

/* ── Detail panel ── */
.detail-wrap {
    background: #fff; border-radius: 16px;
    padding: 28px 32px; margin: 4px 0 28px 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.09);
    border-top: 3px solid #c9a96e;
}
.detail-nombre {
    font-family: 'Playfair Display', serif;
    font-size: 24px; color: #1c1c1e; margin-bottom: 4px; font-weight: 700;
}
.detail-sku {
    font-size: 11px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #c9a96e; margin-bottom: 20px;
}
.detail-desc {
    font-size: 13px; color: #666; line-height: 1.8;
    margin-bottom: 20px; border-left: 3px solid #f0ebe3;
    padding-left: 14px;
}
.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 10px; margin-top: 4px;
}
.detail-item {
    background: #f9f6f2; border-radius: 10px;
    padding: 12px 14px;
}
.detail-item.highlight {
    background: #1c1c1e;
}
.detail-item.highlight .detail-label { color: #888 !important; }
.detail-item.highlight .detail-value { color: #c9a96e !important; font-size: 20px !important; }
.detail-label {
    font-size: 9px; text-transform: uppercase;
    letter-spacing: 0.8px; color: #aaa; font-weight: 700;
}
.detail-value {
    font-size: 15px; color: #1c1c1e;
    font-weight: 700; margin-top: 4px;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    background: #f5f0ea !important; border: 1.5px solid #e0d8cf !important;
    color: #1c1c1e !important; border-radius: 8px !important;
    font-size: 12px !important; font-weight: 600 !important;
    letter-spacing: 0.3px !important; padding: 8px !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    background: #1c1c1e !important; color: #fff !important;
    border-color: #1c1c1e !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: #c9a96e !important; border-color: #c9a96e !important;
    color: #fff !important;
}

/* ── Password screen ── */
.login-box {
    background: #fff; border-radius: 20px; padding: 48px 40px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.1); text-align: center;
    max-width: 400px; margin: 80px auto;
}
.login-logo {
    font-family: 'Playfair Display', serif;
    font-size: 28px; color: #1c1c1e; font-weight: 700;
    letter-spacing: -0.5px; margin-bottom: 8px;
}
.login-sub {
    font-size: 12px; color: #aaa; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 32px;
}
</style>
""", unsafe_allow_html=True)

# ── Column map ────────────────────────────────────────────────────────────────
COL_MAP = {
    "sku":     ["SKU"],
    "nombre":  ["Nombre del Producto"],
    "desc":    ["Descripción", "Descripcion"],
    "costo":   ["Costo (ARS)", "Costo (¥)", "Costo"],
    "precio":  ["Precio Venta (ARS)", "Precio Venta "],
    "stock":   ["Stock", "Stock (unid.)"],
    "peso":    ["Peso (kg)"],
    "alto":    ["Alto (cm)", "Alto Armado"],
    "ancho":   ["Ancho (cm)"],
    "prof":    ["Profundidad (cm)"],
    "cat":     ["Categoría", "Categoria"],
    "subcat":  ["Subcategoría", "Subcategoria"],
    "imagen1": ["Imagen URL 1"],
    "imagen2": ["Imagen URL 2"],
    "imagen3": ["Imagen URL 3"],
}


def find_col(df: pd.DataFrame, key: str) -> str | None:
    for c in COL_MAP.get(key, []):
        if c in df.columns:
            return c
    return None


def cell(row: pd.Series, key: str) -> str:
    for c in COL_MAP.get(key, []):
        if c in row.index:
            v = row[c]
            if isinstance(v, pd.Series):
                v = v.iloc[0] if len(v) else None
            if v is None or (isinstance(v, float) and pd.isna(v)):
                continue
            s = str(v).strip()
            if s and s != "nan":
                return s
    return ""


def fmt_ars(val: str) -> str:
    try:
        return f"$ {float(val):,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return val


# ── Image helpers ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def build_sku_image_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    if not FOTOS_DIR.exists():
        return mapping
    for p in FOTOS_DIR.rglob("*"):
        if p.suffix.lower() in IMG_EXTS and not p.name.startswith("."):
            mapping[p.stem.upper()] = str(p)
    return mapping


def find_image_path(sku: str, img_map: dict) -> str | None:
    if not sku:
        return None
    key = sku.upper()
    if key in img_map:
        return img_map[key]
    parts = key.rsplit("-", 1)
    if len(parts) == 2:
        return img_map.get(parts[0])
    return None


@st.cache_data(show_spinner=False)
def thumbnail_b64(path_str: str, w: int = 600, h: int = 480) -> str:
    img = Image.open(path_str).convert("RGB")
    img.thumbnail((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ── Loaders ───────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def parse_file(data: bytes, name: str) -> pd.DataFrame:
    df = pd.read_excel(io.BytesIO(data), sheet_name="Packing List")
    df = df.dropna(how="all").reset_index(drop=True)
    sku_col = find_col(df, "sku")
    nom_col = find_col(df, "nombre")
    if sku_col or nom_col:
        check = [c for c in [sku_col, nom_col] if c]
        df = df.dropna(subset=check, how="all").reset_index(drop=True)
    df["_archivo"] = Path(name).stem
    return df


def load_from_folder() -> list[pd.DataFrame]:
    frames = []
    if not PACKINGS_DIR.exists():
        return frames
    for path in sorted(PACKINGS_DIR.glob("*.xlsx")):
        try:
            frames.append(parse_file(path.read_bytes(), path.name))
        except Exception as e:
            st.sidebar.warning(f"⚠️ {path.name}: {e}")
    return frames


def load_from_upload(files) -> list[pd.DataFrame]:
    frames = []
    for f in files:
        try:
            frames.append(parse_file(f.read(), f.name))
        except Exception as e:
            st.sidebar.error(f"❌ {f.name}: {e}")
    return frames


# ── Card ──────────────────────────────────────────────────────────────────────
def render_card(row: pd.Series, col, pid: str, img_map: dict):
    sku    = cell(row, "sku")
    nombre = cell(row, "nombre") or sku or "—"
    subcat = cell(row, "subcat") or cell(row, "cat")
    precio = fmt_ars(cell(row, "precio"))
    img_path = find_image_path(sku, img_map)

    if img_path:
        try:
            img_src = thumbnail_b64(img_path)
            img_html = f'<img class="card-img" src="{img_src}">'
        except Exception:
            img_html = '<div class="card-no-img">📦</div>'
    else:
        img_html = '<div class="card-no-img">📦</div>'

    precio_html = f'<span class="card-price">{html.escape(precio)}</span>' if precio else ""

    with col:
        st.markdown(
            f'<div class="card">{img_html}'
            f'<div class="card-body">'
            f'<div class="card-sku">{html.escape(sku)}</div>'
            f'<div class="card-name">{html.escape(nombre)}</div>'
            f'<div class="card-footer">{precio_html}'
            f'<span class="card-cat">{html.escape(subcat)}</span>'
            f'</div></div></div>',
            unsafe_allow_html=True,
        )
        is_open = st.session_state.get("sel") == pid
        if st.button("✕ Cerrar" if is_open else "Ver detalles",
                     key=f"btn_{pid}", use_container_width=True):
            st.session_state["sel"] = None if is_open else pid
            st.rerun()


# ── Detail panel ──────────────────────────────────────────────────────────────
def render_detail(row: pd.Series, img_map: dict):
    sku    = cell(row, "sku")
    nombre = cell(row, "nombre") or sku or "—"
    desc   = cell(row, "desc")
    costo  = fmt_ars(cell(row, "costo"))
    precio = fmt_ars(cell(row, "precio"))
    alto   = cell(row, "alto")
    ancho  = cell(row, "ancho")
    prof   = cell(row, "prof")
    peso   = cell(row, "peso")
    stock  = cell(row, "stock")
    img_path = find_image_path(sku, img_map)

    left, right = st.columns([1, 2])

    with left:
        if img_path:
            try:
                data_url = thumbnail_b64(img_path, 800, 800)
                st.markdown(
                    f'<img src="{data_url}" style="width:100%;border-radius:12px;'
                    f'object-fit:cover;max-height:380px;">',
                    unsafe_allow_html=True,
                )
            except Exception:
                st.image(img_path, use_container_width=True)
        else:
            st.markdown(
                '<div style="height:260px;background:linear-gradient(135deg,#f0ebe3,#e8e0d5);'
                'border-radius:12px;display:flex;align-items:center;'
                'justify-content:center;font-size:52px;">📦</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(
            f'<div class="detail-nombre">{html.escape(nombre)}</div>'
            f'<div class="detail-sku">{html.escape(sku)}</div>',
            unsafe_allow_html=True,
        )
        if desc:
            st.markdown(
                f'<div class="detail-desc">{html.escape(desc)}</div>',
                unsafe_allow_html=True,
            )

        items = []
        if precio:
            items.append(
                f'<div class="detail-item highlight">'
                f'<div class="detail-label">Precio venta</div>'
                f'<div class="detail-value">{html.escape(precio)}</div></div>'
            )
        if costo:
            items.append(
                f'<div class="detail-item">'
                f'<div class="detail-label">Costo</div>'
                f'<div class="detail-value">{html.escape(costo)}</div></div>'
            )
        for label, val in [
            ("Alto (cm)", alto), ("Ancho (cm)", ancho),
            ("Prof. (cm)", prof), ("Peso (kg)", peso), ("Stock", stock),
        ]:
            if val:
                items.append(
                    f'<div class="detail-item">'
                    f'<div class="detail-label">{label}</div>'
                    f'<div class="detail-value">{html.escape(val)}</div></div>'
                )
        if items:
            st.markdown(
                '<div class="detail-grid">' + "".join(items) + "</div>",
                unsafe_allow_html=True,
            )


# ── Password ──────────────────────────────────────────────────────────────────
def check_password() -> bool:
    correct = st.secrets.get("PASSWORD", "")
    if not correct or st.session_state.get("authenticated"):
        return True
    _, c, _ = st.columns([1, 1.4, 1])
    with c:
        st.markdown(
            '<div class="login-box">'
            '<div class="login-logo">Casa Mater</div>'
            '<div class="login-sub">Catálogo interno</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        pwd = st.text_input("Contraseña", type="password", label_visibility="collapsed",
                            placeholder="Contraseña")
        if st.button("Entrar", use_container_width=True, type="primary"):
            if pwd == correct:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    return False


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not check_password():
        st.stop()

    img_map = build_sku_image_map()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## Casa Mater")
        st.markdown("<p style='font-size:11px;color:#666;letter-spacing:1px;text-transform:uppercase;margin-top:-12px;'>Catálogo interno</p>", unsafe_allow_html=True)
        st.markdown("---")

        local_frames = load_from_folder()
        if local_frames:
            st.success(f"✅ {len(local_frames)} archivo(s) cargados")
            frames = local_frames
            if st.button("🔄 Recargar"):
                st.cache_data.clear()
                st.rerun()
        else:
            uploaded = st.file_uploader(
                "Packing lists (Excel)", type=["xlsx", "xls"],
                accept_multiple_files=True,
            )
            frames = load_from_upload(uploaded) if uploaded else []

        if not frames:
            st.info("Subí los archivos de packing para comenzar.")
            st.stop()

        df = pd.concat(frames, ignore_index=True)

        st.markdown("---")
        cat_col  = find_col(df, "cat")
        cats     = sorted(df[cat_col].dropna().unique()) if cat_col else []
        sel_cats = st.multiselect("Categoría", cats, default=list(cats))
        search   = st.text_input("Buscar", placeholder="SKU, nombre…")
        st.markdown("---")

        total = len(df)
        con_img = sum(1 for _, r in df.iterrows() if find_image_path(cell(r, "sku"), img_map))
        col1, col2 = st.columns(2)
        col1.metric("Productos", total)
        col2.metric("Con foto", con_img)
        if cat_col:
            st.metric("Categorías", df[cat_col].nunique())

    st.markdown("# Catálogo de Productos")

    # ── Filters ───────────────────────────────────────────────────────────────
    filtered = df.copy()
    if sel_cats and cat_col:
        filtered = filtered[filtered[cat_col].isin(sel_cats)]
    if search:
        s = search.lower()
        mask = pd.Series(False, index=filtered.index)
        for key in ["sku", "nombre", "desc"]:
            c = find_col(filtered, key)
            if c:
                mask |= filtered[c].astype(str).str.lower().str.contains(s, na=False)
        filtered = filtered[mask]

    if filtered.empty:
        st.warning("No hay productos que coincidan.")
        return

    # ── Grid by file ──────────────────────────────────────────────────────────
    selected = st.session_state.get("sel")

    for archivo in filtered["_archivo"].unique():
        grp = filtered[filtered["_archivo"] == archivo]
        titulo = (archivo.replace("-Format", "").replace("_completo", "")
                         .replace("_v2", "").replace("_", " ").replace("-", " ").title())

        st.markdown(
            f'<div class="section-header">'
            f'<span class="section-title">{html.escape(titulo)}</span>'
            f'<span class="section-count">{len(grp)} productos</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        for i in range(0, len(grp), COLS):
            chunk = grp.iloc[i: i + COLS]
            cols  = st.columns(COLS)
            detail_row = None

            for j, (idx, product) in enumerate(chunk.iterrows()):
                pid = f"{archivo}_{idx}"
                render_card(product, cols[j], pid, img_map)
                if selected == pid:
                    detail_row = product

            if detail_row is not None:
                st.markdown('<div class="detail-wrap">', unsafe_allow_html=True)
                render_detail(detail_row, img_map)
                st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
