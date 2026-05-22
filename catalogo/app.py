import html
import io
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Catálogo", layout="wide", page_icon="🛍️")

FOTOS_DIR = Path(__file__).parent / "fotos"
IMG_EXTS   = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


@st.cache_data(show_spinner=False)
def build_sku_image_map() -> dict[str, Path]:
    """Scan FOTOS_DIR recursively, return {sku_stem: path}."""
    mapping: dict[str, Path] = {}
    if not FOTOS_DIR.exists():
        return mapping
    for p in FOTOS_DIR.rglob("*"):
        if p.suffix.lower() in IMG_EXTS and not p.name.startswith("."):
            mapping[p.stem.upper()] = p
    return mapping


def find_image(sku: str, img_map: dict[str, Path]) -> Path | None:
    if not sku:
        return None
    key = sku.upper()
    if key in img_map:
        return img_map[key]
    # Fallback: SKU variant suffix (e.g. EST-ARB-002-180 → EST-ARB-002)
    parts = key.rsplit("-", 1)
    if len(parts) == 2 and img_map.get(parts[0]):
        return img_map[parts[0]]
    return None

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #f0ebe4 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] { background-color: #1c1c1e !important; }
[data-testid="stSidebar"] * { color: #e8e0d5 !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: #2c2c2e !important; border: 1px solid #3a3a3c !important;
    color: #e8e0d5 !important; border-radius: 6px;
}
[data-testid="stSidebar"] hr { border-color: #3a3a3c !important; }
[data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #c9a96e !important; }
h1 { font-family: 'Playfair Display', serif !important; color: #1c1c1e !important; }

.section-title {
    font-family: 'Playfair Display', serif; font-size: 22px; color: #1c1c1e;
    margin: 36px 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid #c9a96e;
    display: flex; justify-content: space-between; align-items: baseline;
}
.section-count { font-size: 13px; color: #999; font-weight: 400; font-family: 'Inter', sans-serif; }

.card {
    background: #fff; border-radius: 12px; overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom: 8px;
}
.card:hover { box-shadow: 0 6px 24px rgba(0,0,0,0.12); }
.card-img { width:100%; height:200px; object-fit:cover; display:block; }
.card-no-img {
    width:100%; height:200px; background:#f5f0ea;
    display:flex; align-items:center; justify-content:center;
    font-size:42px; color:#ccc;
}
.card-body { padding: 12px 14px 14px; }
.card-sku { font-size:10px; font-weight:600; letter-spacing:1px; text-transform:uppercase; color:#c9a96e; margin-bottom:4px; }
.card-name { font-size:13px; font-weight:600; color:#1c1c1e; line-height:1.4; margin-bottom:6px; min-height:36px; }
.card-cat { font-size:11px; color:#aaa; }

.detail-wrap {
    background:#fff; border-radius:12px; padding:24px 28px;
    margin: 8px 0 24px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.detail-nombre { font-family:'Playfair Display',serif; font-size:22px; color:#1c1c1e; margin-bottom:4px; }
.detail-sku { font-size:11px; font-weight:600; letter-spacing:1px; text-transform:uppercase; color:#c9a96e; margin-bottom:20px; }
.detail-desc { font-size:13px; color:#555; line-height:1.75; margin-bottom:20px; }
.detail-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:10px; margin-top:4px; }
.detail-item { background:#f9f6f2; border-radius:8px; padding:10px 12px; }
.detail-label { font-size:10px; text-transform:uppercase; letter-spacing:0.5px; color:#aaa; font-weight:600; }
.detail-value { font-size:14px; color:#1c1c1e; font-weight:600; margin-top:3px; }
.detail-costo { font-size:22px; font-weight:700; color:#2e7d32; }
</style>
""", unsafe_allow_html=True)

# ── Column map ────────────────────────────────────────────────────────────────
COL_MAP = {
    "sku":      ["SKU"],
    "nombre":   ["Nombre del Producto"],
    "desc":     ["Descripción", "Descripcion"],
    "costo":    ["Costo (ARS)", "Costo"],
    "precio":   ["Precio Venta (ARS)", "Precio Venta "],
    "stock":    ["Stock"],
    "peso":     ["Peso (kg)"],
    "alto":     ["Alto (cm)", "Alto Armado"],
    "ancho":    ["Ancho (cm)"],
    "prof":     ["Profundidad (cm)"],
    "cat":      ["Categoría", "Categoria"],
    "subcat":   ["Subcategoría", "Subcategoria"],
    "imagen1":  ["Imagen URL 1"],
    "imagen2":  ["Imagen URL 2"],
    "imagen3":  ["Imagen URL 3"],
}

PACKINGS_DIR = Path(__file__).parent.parent / "Packings Formateados"


def find_col(df: pd.DataFrame, key: str) -> str | None:
    for c in COL_MAP.get(key, []):
        if c in df.columns:
            return c
    return None


def cell(row: pd.Series, key: str) -> str:
    """Get scalar string value from a row using a COL_MAP key."""
    for c in COL_MAP.get(key, []):
        if c in row.index:
            v = row[c]
            # Guard: if somehow a Series slipped in (duplicate cols), take first
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


# ── Loaders ───────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def parse_file(data: bytes, name: str) -> pd.DataFrame:
    """Parse one packing list Excel, return clean DataFrame."""
    df = pd.read_excel(io.BytesIO(data), sheet_name="Packing List")
    # Drop completely empty rows
    df = df.dropna(how="all").reset_index(drop=True)
    # Drop rows with no SKU and no name
    sku_col  = find_col(df, "sku")
    nom_col  = find_col(df, "nombre")
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
            df = parse_file(path.read_bytes(), path.name)
            frames.append(df)
        except Exception as e:
            st.sidebar.warning(f"⚠️ {path.name}: {e}")
    return frames


def load_from_upload(files) -> list[pd.DataFrame]:
    frames = []
    for f in files:
        try:
            df = parse_file(f.read(), f.name)
            frames.append(df)
        except Exception as e:
            st.sidebar.error(f"❌ {f.name}: {e}")
    return frames


# ── Card ──────────────────────────────────────────────────────────────────────
def render_card(row: pd.Series, col, pid: str, img_map: dict):
    sku    = cell(row, "sku")
    nombre = cell(row, "nombre") or sku or "—"
    subcat = cell(row, "subcat") or cell(row, "cat")
    img_path = find_image(sku, img_map)

    with col:
        if img_path:
            st.image(str(img_path), use_container_width=True)
        else:
            st.markdown('<div class="card-no-img">📦</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="card-body">'
            f'<div class="card-sku">{html.escape(sku)}</div>'
            f'<div class="card-name">{html.escape(nombre)}</div>'
            f'<div class="card-cat">{html.escape(subcat)}</div>'
            f'</div>',
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
    alto   = cell(row, "alto")
    ancho  = cell(row, "ancho")
    prof   = cell(row, "prof")
    peso   = cell(row, "peso")
    stock  = cell(row, "stock")
    img_path = find_image(sku, img_map)

    left, right = st.columns([1, 2])

    with left:
        if img_path:
            st.image(str(img_path), use_container_width=True)
        else:
            st.markdown(
                '<div style="height:220px;background:#f5f0ea;border-radius:10px;'
                'display:flex;align-items:center;justify-content:center;font-size:48px;">📦</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(
            f'<div class="detail-nombre">{html.escape(nombre)}</div>'
            f'<div class="detail-sku">{html.escape(sku)}</div>',
            unsafe_allow_html=True,
        )
        if desc:
            st.markdown(f'<div class="detail-desc">{html.escape(desc)}</div>',
                        unsafe_allow_html=True)

        items = []
        if costo:
            items.append(
                f'<div class="detail-item"><div class="detail-label">Costo</div>'
                f'<div class="detail-value detail-costo">{html.escape(costo)}</div></div>'
            )
        for label, val in [("Alto (cm)", alto), ("Ancho (cm)", ancho),
                            ("Prof. (cm)", prof), ("Peso (kg)", peso), ("Stock", stock)]:
            if val:
                items.append(
                    f'<div class="detail-item"><div class="detail-label">{label}</div>'
                    f'<div class="detail-value">{html.escape(val)}</div></div>'
                )
        if items:
            st.markdown('<div class="detail-grid">' + "".join(items) + "</div>",
                        unsafe_allow_html=True)


# ── Password ──────────────────────────────────────────────────────────────────
def check_password() -> bool:
    correct = st.secrets.get("PASSWORD", "")
    if not correct or st.session_state.get("authenticated"):
        return True
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🔒 Acceso al Catálogo")
        pwd = st.text_input("Contraseña", type="password")
        if st.button("Entrar", use_container_width=True):
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

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## Catálogo")
        st.markdown("---")

        # Intentar carga automática desde carpeta local
        local_frames = load_from_folder()
        if local_frames:
            st.success(f"✅ {len(local_frames)} archivo(s) cargados automáticamente")
            frames = local_frames
            if st.button("🔄 Recargar"):
                st.cache_data.clear()
                st.rerun()
        else:
            # Fallback: uploader (para Streamlit Cloud)
            uploaded = st.file_uploader(
                "Packing lists (Excel)",
                type=["xlsx", "xls"],
                accept_multiple_files=True,
            )
            frames = load_from_upload(uploaded) if uploaded else []

        if not frames:
            st.info("Subí los archivos de packing para comenzar.")
            st.stop()

        df = pd.concat(frames, ignore_index=True)

        # Filtros
        st.markdown("---")
        cat_col = find_col(df, "cat")
        cats    = sorted(df[cat_col].dropna().unique()) if cat_col else []
        sel_cats = st.multiselect("Categoría", cats, default=list(cats))
        search   = st.text_input("Buscar", placeholder="SKU, nombre…")
        st.markdown("---")
        st.metric("Total productos", len(df))
        if cat_col:
            st.metric("Categorías", df[cat_col].nunique())

    img_map = build_sku_image_map()

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
    COLS     = 4
    selected = st.session_state.get("sel")

    for archivo in filtered["_archivo"].unique():
        grp = filtered[filtered["_archivo"] == archivo]
        titulo = (archivo.replace("-Format", "").replace("_completo", "")
                         .replace("_", " ").replace("-", " ").title())

        st.markdown(
            f'<div class="section-title">{html.escape(titulo)}'
            f'<span class="section-count">{len(grp)} productos</span></div>',
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
