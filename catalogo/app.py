import re
import html
import streamlit as st
import pandas as pd
import openpyxl
import io
from PIL import Image
import base64
from pathlib import Path

st.set_page_config(page_title="Catálogo", layout="wide", page_icon="🛍️")

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #f0ebe4 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #1c1c1e !important;
}
[data-testid="stSidebar"] * { color: #e8e0d5 !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: #2c2c2e !important;
    border: 1px solid #3a3a3c !important;
    color: #e8e0d5 !important;
    border-radius: 6px;
}
[data-testid="stSidebar"] .stMultiSelect > div { background: #2c2c2e !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] label { color: #e8e0d5 !important; }
[data-testid="stSidebar"] hr { border-color: #3a3a3c !important; }
[data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #c9a96e !important; }

h1 { font-family: 'Playfair Display', serif !important; color: #1c1c1e !important; }

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    color: #1c1c1e;
    margin: 36px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #c9a96e;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}
.section-count {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: #999;
    font-weight: 400;
}
.card {
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 8px;
    transition: box-shadow 0.2s;
}
.card:hover { box-shadow: 0 6px 24px rgba(0,0,0,0.12); }
.card-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
}
.card-no-img {
    width: 100%;
    height: 200px;
    background: #f5f0ea;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 42px;
}
.card-body { padding: 12px 14px 14px; }
.card-sku {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #c9a96e;
    margin-bottom: 4px;
}
.card-name {
    font-size: 13px;
    font-weight: 600;
    color: #1c1c1e;
    line-height: 1.4;
    margin-bottom: 8px;
    min-height: 36px;
}
.card-price {
    font-size: 17px;
    font-weight: 700;
    color: #2e7d32;
    margin-bottom: 4px;
}
.card-meta {
    font-size: 11px;
    color: #888;
    line-height: 1.6;
}
.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 8px;
}
.detail-item {
    background: #f9f6f2;
    border-radius: 8px;
    padding: 8px 10px;
}
.detail-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #aaa;
    font-weight: 600;
}
.detail-value {
    font-size: 13px;
    color: #1c1c1e;
    font-weight: 500;
    margin-top: 2px;
}
.stExpander { background: #fff !important; border-radius: 8px !important; }
div[data-testid="stExpanderDetails"] { background: #faf7f3 !important; }
</style>
""", unsafe_allow_html=True)

# ── Column aliases ─────────────────────────────────────────────────────────────
FIELD_ALIASES = {
    "nombre": [
        "nombre", "name", "producto", "product", "产品", "品名", "品名描述",
        "descripcion", "description", "product description", "item description",
        "denominacion", "detalle", "detail",
    ],
    "modelo": [
        "modelo", "model", "型号", "item no", "item no.", "item number",
        "货号", "sku", "codigo", "code", "ref", "referencia", "art", "articulo",
    ],
    "precio": [
        "precio", "price", "单价", "unit price", "unit price/¥", "precio unitario",
        "costo", "cost", "价格", "p.u.", "p.unit",
    ],
    "talla": [
        "talla", "size", "talle", "尺寸", "medida", "medidas", "medida de cama",
        "dimension", "dimensiones", "bed size", "bed.size",
    ],
    "cantidad": [
        "cantidad", "quantity", "qty", "数量", "number", "ctns", "qty/pcs",
        "tt.qty", "t.t.qty", "total qty", "pcs",
    ],
    "material": ["material", "材质", "materiales", "mat"],
    "total": [
        "total", "amount", "总价", "precio total", "total price", "total amount",
        "total amount/¥", "importe", "monto",
    ],
    "cbm": ["cbm", "volumen", "体积", "total cbm", "t.cbm", "cbm total"],
    "peso": ["peso", "weight", "重量", "total kg", "kg", "t.g.w", "g.w"],
    "observaciones": ["observaciones", "remarks", "备注", "notas", "notes", "obs"],
}
IMAGE_KEYWORDS = ["imagen", "image", "picture", "foto", "图片", "pics", "photo", "product picture"]

# Known sub-header values to skip (second-row bilingual headers)
SUBHEADER_VALUES = {
    "货号", "图片", "品名描述", "装量", "件数", "总数", "单价", "金额",
    "品名", "型号", "尺寸", "数量", "价格", "材质",
}

DISPLAY_LABELS = {
    "nombre": "Nombre",
    "modelo": "Código / SKU",
    "precio": "Precio unitario",
    "talla": "Medida / Talle",
    "cantidad": "Cantidad",
    "material": "Material",
    "total": "Total",
    "cbm": "Volumen CBM",
    "peso": "Peso KG",
    "observaciones": "Observaciones",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def pil_to_b64(img: Image.Image) -> str | None:
    try:
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None


def extract_excel_images(file_bytes: bytes) -> dict:
    result = {}
    try:
        wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
        ws = wb.active
        for img in ws._images:
            try:
                anchor = img.anchor
                if hasattr(anchor, "_from"):
                    row = anchor._from.row + 1
                elif hasattr(anchor, "row"):
                    row = anchor.row + 1
                else:
                    continue
                pil = Image.open(io.BytesIO(img._data()))
                result[row] = pil
            except Exception:
                pass
    except Exception:
        pass
    return result


def find_header_row(df_raw: pd.DataFrame) -> int:
    keywords = [
        "model", "name", "price", "qty", "size", "型号", "数量", "价格",
        "nombre", "precio", "cantidad", "picture", "image", "material",
        "item no", "product", "descripcion", "sku", "codigo",
    ]
    best, best_score = 0, 0
    for i in range(min(15, len(df_raw))):
        row_str = " ".join(str(v).lower() for v in df_raw.iloc[i] if pd.notna(v))
        score = sum(1 for kw in keywords if kw in row_str)
        if score > best_score:
            best_score, best = score, i
    return best


def normalize_col(col: str) -> str:
    c = str(col).lower().strip()
    for norm, aliases in FIELD_ALIASES.items():
        if c in aliases or any(a in c for a in aliases):
            return norm
    return c


def is_image_col(col: str) -> bool:
    c = str(col).lower().strip()
    return any(kw in c for kw in IMAGE_KEYWORDS)


def is_subheader_row(row: pd.Series) -> bool:
    """Detect bilingual second-header rows (e.g. 货号 / 图片 / 品名描述)."""
    vals = set()
    for v in row:
        if pd.notna(v):
            vals.add(str(v).strip())
    overlap = vals & SUBHEADER_VALUES
    return len(overlap) >= 2


def get_display_name(row: pd.Series) -> str:
    """Best-effort product name with fallbacks."""
    for col in ["nombre", "modelo"]:
        if col in row.index:
            v = row[col]
            if pd.notna(v) and str(v).strip() not in ("", "nan"):
                return str(v).strip()
    # Fallback: first non-private, non-numeric, non-tiny text column
    for col in row.index:
        if col.startswith("_"):
            continue
        v = row[col]
        if pd.notna(v):
            s = str(v).strip()
            if s in ("", "nan"):
                continue
            try:
                float(s)
                continue
            except ValueError:
                if len(s) > 1:
                    return s
    return "—"


@st.cache_data(show_spinner=False)
def process_excel(file_bytes: bytes, filename: str) -> pd.DataFrame:
    category = Path(filename).stem

    images = extract_excel_images(file_bytes)

    df_raw = pd.read_excel(io.BytesIO(file_bytes), header=None)
    hdr = find_header_row(df_raw)

    df = pd.read_excel(io.BytesIO(file_bytes), header=hdr)
    df.columns = [str(c).strip() for c in df.columns]

    # Track Excel row numbers BEFORE dropping anything
    df["_excel_row"] = range(hdr + 2, hdr + 2 + len(df))

    # Drop fully empty rows
    data_cols = [c for c in df.columns if c != "_excel_row"]
    df = df.dropna(subset=data_cols, how="all").reset_index(drop=True)

    # Drop bilingual sub-header rows (second header row in Chinese/English combos)
    mask_subhdr = df[data_cols].apply(is_subheader_row, axis=1)
    df = df[~mask_subhdr].reset_index(drop=True)

    # Remove image-only columns
    df = df[[c for c in df.columns if not is_image_col(c) or c == "_excel_row"]]

    # Normalize column names; keep the most-populated when duplicates arise
    rename = {c: normalize_col(c) for c in df.columns if not c.startswith("_")}
    df = df.rename(columns=rename)

    # If duplicate normalized columns exist, keep the one with most non-null values
    seen = {}
    cols_to_keep = []
    for c in df.columns:
        if c in seen:
            existing_count = df[seen[c]].notna().sum()
            new_count = df[c].notna().sum()
            if new_count > existing_count:
                cols_to_keep = [col if col != seen[c] else c for col in cols_to_keep]
                seen[c] = c
            # else: skip this duplicate
        else:
            seen[c] = c
            cols_to_keep.append(c)
    df = df[cols_to_keep]

    # Attach images by Excel row
    df["_image"] = df["_excel_row"].map(images.get)

    # Add category
    df["_category"] = category

    # Remove rows that have no code, no name AND no image (truly empty/footer rows)
    def is_valid(row):
        def scalar(v):
            # Guard against a cell returning a Series when columns are still duped
            if isinstance(v, pd.Series):
                v = v.iloc[0] if len(v) else None
            return v

        has_img = scalar(row.get("_image")) is not None
        for col in ["modelo", "nombre"]:
            v = scalar(row.get(col))
            try:
                if pd.notna(v) and str(v).strip() not in ("", "nan"):
                    return True
            except (TypeError, ValueError):
                pass
        for c in row.index:
            if c.startswith("_"):
                continue
            v = scalar(row[c])
            try:
                if pd.notna(v) and str(v).strip() not in ("", "nan"):
                    return True
            except (TypeError, ValueError):
                pass
        return has_img

    df = df[df.apply(is_valid, axis=1)].reset_index(drop=True)

    return df


def match_png_files(df: pd.DataFrame, png_files) -> pd.DataFrame:
    if not png_files:
        return df
    pngs = {}
    for f in png_files:
        stem = re.sub(r"[\s\-_]", "", Path(f.name).stem.lower())
        pngs[stem] = Image.open(f)

    def find(row):
        if row["_image"] is not None:
            return row["_image"]
        for col in ["modelo", "nombre"]:
            if col in row.index and pd.notna(row.get(col)):
                key = re.sub(r"[\s\-_]", "", str(row[col]).lower())
                if key in pngs:
                    return pngs[key]
                for stem, img in pngs.items():
                    if stem in key or key in stem:
                        return img
        return None

    df["_image"] = df.apply(find, axis=1)
    return df


# ── Card renderer ─────────────────────────────────────────────────────────────

def _safe_str(val) -> str:
    """Safely convert a cell value (possibly a Series) to a clean string."""
    if isinstance(val, pd.Series):
        val = val.iloc[0] if len(val) else None
    try:
        if pd.isna(val):
            return ""
    except (TypeError, ValueError):
        pass
    s = str(val).strip()
    return "" if s == "nan" else s


def _esc(val) -> str:
    """Safe string + HTML-escape for inserting into HTML templates."""
    return html.escape(_safe_str(val))


def _build_card_html(img_html: str, modelo: str, nombre: str,
                     precio: str, meta: str) -> str:
    """Build card HTML as a plain string to avoid f-string / markdown conflicts."""
    parts = ['<div class="card">', img_html, '<div class="card-body">']
    if modelo:
        parts.append(f'<div class="card-sku">{modelo}</div>')
    parts.append(f'<div class="card-name">{nombre}</div>')
    if precio:
        parts.append(f'<div class="card-price">{precio}</div>')
    if meta:
        parts.append(f'<div class="card-meta">{meta}</div>')
    parts += ['</div>', '</div>']
    return "".join(parts)


def render_card(product: pd.Series, col, product_id: str):
    with col:
        img = product.get("_image")
        nombre   = _esc(get_display_name(product))
        modelo   = _esc(product.get("modelo", ""))
        precio_v = product.get("precio")
        try:
            precio = f"¥ {float(precio_v):,.0f}" if pd.notna(precio_v) and precio_v != "" else ""
        except (TypeError, ValueError):
            precio = ""
        talla    = _esc(product.get("talla", ""))
        material = _esc(product.get("material", ""))

        if img is not None:
            b64 = pil_to_b64(img)
            img_html = (f'<img class="card-img" src="data:image/jpeg;base64,{b64}">'
                        if b64 else '<div class="card-no-img">📦</div>')
        else:
            img_html = '<div class="card-no-img">📦</div>'

        meta = " · ".join(p for p in [talla, material] if p)
        st.markdown(_build_card_html(img_html, modelo, nombre, precio, meta),
                    unsafe_allow_html=True)

        is_open = st.session_state.get("selected_product") == product_id
        btn_label = "✕ Cerrar" if is_open else "Ver detalles"
        if st.button(btn_label, key=f"btn_{product_id}", use_container_width=True):
            st.session_state["selected_product"] = None if is_open else product_id
            st.rerun()


def render_detail_panel(product: pd.Series):
    img    = product.get("_image")
    nombre = _safe_str(get_display_name(product))

    left, right = st.columns([1, 2])
    with left:
        if img is not None:
            b64 = pil_to_b64(img)
            if b64:
                st.markdown(
                    f'<img src="data:image/jpeg;base64,{b64}" '
                    f'style="width:100%;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,0.1);">',
                    unsafe_allow_html=True,
                )
    with right:
        st.markdown(f"### {nombre}")
        items = []
        for dc in [c for c in product.index if not c.startswith("_")]:
            val = _safe_str(product[dc])
            if val:
                label = DISPLAY_LABELS.get(dc, dc.replace("_", " ").capitalize())
                items.append(
                    f'<div class="detail-item">'
                    f'<div class="detail-label">{html.escape(label)}</div>'
                    f'<div class="detail-value">{html.escape(val)}</div>'
                    f'</div>'
                )
        if items:
            st.markdown(
                '<div class="detail-grid">' + "".join(items) + "</div>",
                unsafe_allow_html=True,
            )


# ── Password ──────────────────────────────────────────────────────────────────

def check_password() -> bool:
    correct = st.secrets.get("PASSWORD", "")
    if not correct:
        return True
    if st.session_state.get("authenticated"):
        return True
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
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

    with st.sidebar:
        st.markdown("## Catálogo")
        st.markdown("---")
        excel_files = st.file_uploader(
            "Packing lists (Excel)",
            type=["xlsx", "xls"],
            accept_multiple_files=True,
        )
        png_files = st.file_uploader(
            "Imágenes adicionales",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
        )
        st.markdown("---")
        st.markdown("### Filtros")
        search = st.text_input("Buscar", placeholder="nombre, código, material…")

    st.markdown("# Catálogo de Productos")

    if not excel_files:
        st.markdown("""
> Subí tus archivos Excel desde el panel izquierdo para comenzar.

**Cómo usar:**
- Subí uno o más packing lists en Excel — cada archivo es una categoría
- Opcionalmente subí imágenes sueltas en PNG/JPG
- Usá los filtros para navegar; **Editar** para corregir datos manualmente
        """)
        return

    dfs = []
    progress = st.sidebar.empty()
    for f in excel_files:
        try:
            fb = f.read()
            df = process_excel(fb, f.name)
            dfs.append(df)
            progress.success(f"✅ {f.name}  ({len(df)} productos)")
        except Exception as e:
            st.sidebar.error(f"❌ {f.name}: {e}")

    if not dfs:
        st.error("No se pudo procesar ningún archivo.")
        return

    all_products = pd.concat(dfs, ignore_index=True)

    if png_files:
        all_products = match_png_files(all_products, png_files)

    # Store editable copy in session state so edits persist across reruns
    if "edited_products" not in st.session_state or st.session_state.get("_source_hash") != id(excel_files):
        st.session_state["edited_products"] = all_products.copy()
        st.session_state["_source_hash"] = id(excel_files)

    all_products = st.session_state["edited_products"]
    categories = sorted(all_products["_category"].unique().tolist())

    with st.sidebar:
        sel_cats = st.multiselect("Categorías", options=categories, default=categories)

        price_range = None
        if "precio" in all_products.columns:
            valid = pd.to_numeric(all_products["precio"], errors="coerce").dropna()
            if len(valid) and valid.max() > valid.min():
                mn, mx = float(valid.min()), float(valid.max())
                price_range = st.slider("Precio", mn, mx, (mn, mx), format="¥%.0f")

        st.markdown("---")
        st.metric("Total productos", len(all_products))
        st.metric("Categorías", len(categories))

    tab_catalog, tab_edit = st.tabs(["Catálogo", "✏️ Editar datos"])

    # ── Edit tab ──────────────────────────────────────────────────────────────
    with tab_edit:
        st.markdown("Editá directamente en la tabla. Los cambios se reflejan en el catálogo.")
        edit_cols = [c for c in all_products.columns if not c.startswith("_")]
        edited = st.data_editor(
            all_products[edit_cols].copy(),
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "nombre":       st.column_config.TextColumn("Nombre"),
                "modelo":       st.column_config.TextColumn("Código / SKU"),
                "precio":       st.column_config.NumberColumn("Precio", format="¥%.0f"),
                "talla":        st.column_config.TextColumn("Medida"),
                "material":     st.column_config.TextColumn("Material"),
                "cantidad":     st.column_config.NumberColumn("Cantidad"),
                "total":        st.column_config.NumberColumn("Total", format="¥%.0f"),
                "observaciones":st.column_config.TextColumn("Observaciones"),
                "_category":    st.column_config.TextColumn("Categoría"),
            },
            key="data_editor",
        )
        if st.button("💾 Guardar cambios", type="primary"):
            # Merge edited text columns back, keeping private cols (_image etc.)
            for c in edit_cols:
                if c in all_products.columns:
                    st.session_state["edited_products"][c] = edited[c].values
            st.success("Cambios guardados.")
            st.rerun()

    # ── Catalog tab ───────────────────────────────────────────────────────────
    with tab_catalog:
        # Apply filters
        filtered = all_products.copy()
        if sel_cats:
            filtered = filtered[filtered["_category"].isin(sel_cats)]

        if search:
            mask = pd.Series(False, index=filtered.index)
            for col in ["nombre", "modelo", "material"]:
                if col in filtered.columns:
                    mask |= filtered[col].astype(str).str.lower().str.contains(
                        search.lower(), na=False
                    )
            filtered = filtered[mask]

        if price_range and "precio" in filtered.columns:
            num_precio = pd.to_numeric(filtered["precio"], errors="coerce")
            filtered = filtered[num_precio.isna() | num_precio.between(*price_range)]

        if filtered.empty:
            st.warning("No hay productos que coincidan con los filtros.")
            return

        COLS = 4
        selected_id = st.session_state.get("selected_product")
        for cat in (sel_cats if sel_cats else categories):
            cat_df = filtered[filtered["_category"] == cat]
            if cat_df.empty:
                continue

            st.markdown(
                f'<div class="section-title">{html.escape(cat)}'
                f'<span class="section-count">{len(cat_df)} productos</span></div>',
                unsafe_allow_html=True,
            )

            rows = [cat_df.iloc[i : i + COLS] for i in range(0, len(cat_df), COLS)]
            for row_group in rows:
                cols = st.columns(COLS)
                selected_in_row = None
                for j, (idx, product) in enumerate(row_group.iterrows()):
                    pid = f"{cat}_{idx}"
                    render_card(product, cols[j], pid)
                    if selected_id == pid:
                        selected_in_row = product

                if selected_in_row is not None:
                    render_detail_panel(selected_in_row)


if __name__ == "__main__":
    main()
