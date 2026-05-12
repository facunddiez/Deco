import streamlit as st
import pandas as pd
import openpyxl
import io
from PIL import Image
import base64
from pathlib import Path

st.set_page_config(page_title="Catálogo de Productos", layout="wide", page_icon="🛍️")

st.markdown("""
<style>
    .stApp { background-color: #f5f5f5; }
    .section-header {
        background: linear-gradient(135deg, #1a1a2e, #2d3561);
        color: white;
        padding: 14px 20px;
        border-radius: 10px;
        margin: 28px 0 16px 0;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .product-wrapper {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        margin-bottom: 4px;
    }
    .card-body {
        padding: 10px 12px 8px 12px;
    }
    .card-name {
        font-weight: 600;
        font-size: 13px;
        line-height: 1.4;
        margin-bottom: 3px;
        color: #1a1a2e;
    }
    .card-model {
        color: #999;
        font-size: 11px;
        margin-bottom: 6px;
    }
    .card-price {
        color: #2e7d32;
        font-size: 15px;
        font-weight: 700;
    }
    .card-size {
        color: #666;
        font-size: 11px;
        margin-top: 2px;
    }
    .no-image {
        width: 100%;
        height: 180px;
        background: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        color: #ccc;
    }
    .detail-row {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        border-bottom: 1px solid #f0f0f0;
        font-size: 13px;
    }
    .detail-label { color: #888; font-weight: 500; }
    .detail-value { color: #1a1a2e; font-weight: 400; text-align: right; max-width: 60%; }
</style>
""", unsafe_allow_html=True)

# ── Column normalization map ──────────────────────────────────────────────────
FIELD_ALIASES = {
    "nombre":       ["nombre", "name", "producto", "product", "产品", "品名",
                     "descripcion", "description", "item", "n.°", "no."],
    "modelo":       ["modelo", "model", "型号", "item no", "item no.", "货号",
                     "sku", "codigo", "code", "ref", "referencia"],
    "precio":       ["precio", "price", "单价", "unit price", "precio unitario",
                     "costo", "cost", "价格"],
    "talla":        ["talla", "size", "talle", "尺寸", "medida", "medidas",
                     "medida de cama", "dimension", "dimensiones"],
    "cantidad":     ["cantidad", "quantity", "qty", "数量", "number", "ctns"],
    "material":     ["material", "材质", "materiales"],
    "total":        ["total", "amount", "总价", "precio total", "total price",
                     "importe", "monto"],
    "cbm":          ["cbm", "volumen", "体积", "total cbm", "volumen cbm"],
    "peso":         ["peso", "weight", "重量", "total kg", "kg"],
    "observaciones":["observaciones", "remarks", "备注", "notas", "notes"],
}
IMAGE_KEYWORDS = ["imagen", "image", "picture", "foto", "图片", "pics", "photo"]

DISPLAY_LABELS = {
    "nombre": "Nombre",
    "modelo": "Modelo / SKU",
    "precio": "Precio unitario",
    "talla": "Medida / Talle",
    "cantidad": "Cantidad",
    "material": "Material",
    "total": "Precio total",
    "cbm": "Volumen (CBM)",
    "peso": "Peso (KG)",
    "observaciones": "Observaciones",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def pil_to_b64(img: Image.Image) -> str | None:
    try:
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=82)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None


def extract_excel_images(file_bytes: bytes) -> dict[int, Image.Image]:
    """Return {excel_row_1based: PIL.Image} for all embedded images."""
    result = {}
    try:
        wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
        ws = wb.active
        for img in ws._images:
            try:
                anchor = img.anchor
                row = (anchor._from.row if hasattr(anchor, "_from") else anchor.row) + 1
                pil = Image.open(io.BytesIO(img._data()))
                result[row] = pil
            except Exception:
                pass
    except Exception:
        pass
    return result


def find_header_row(df_raw: pd.DataFrame) -> int:
    keywords = ["model", "name", "price", "qty", "size", "型号", "数量", "价格",
                "nombre", "precio", "cantidad", "picture", "image", "material", "item"]
    best, best_score = 0, 0
    for i in range(min(12, len(df_raw))):
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


@st.cache_data(show_spinner=False)
def process_excel(file_bytes: bytes, filename: str) -> pd.DataFrame:
    category = Path(filename).stem

    images = extract_excel_images(file_bytes)

    df_raw = pd.read_excel(io.BytesIO(file_bytes), header=None)
    hdr = find_header_row(df_raw)

    df = pd.read_excel(io.BytesIO(file_bytes), header=hdr)
    df.columns = [str(c).strip() for c in df.columns]

    # Track original Excel rows before dropping empties
    df["_excel_row"] = range(hdr + 2, hdr + 2 + len(df))

    # Drop totally empty data rows
    data_cols = [c for c in df.columns if c != "_excel_row"]
    df = df.dropna(subset=data_cols, how="all").reset_index(drop=True)

    # Remove image-only columns
    df = df[[c for c in df.columns if not is_image_col(c) or c == "_excel_row"]]

    # Normalize column names
    rename = {c: normalize_col(c) for c in df.columns if not c.startswith("_")}
    df = df.rename(columns=rename)
    df = df.loc[:, ~df.columns.duplicated()]

    # Attach embedded images
    df["_image"] = df["_excel_row"].map(images.get)

    # Fallback name column
    if "nombre" not in df.columns:
        first = next((c for c in df.columns if not c.startswith("_")), None)
        if first:
            df["nombre"] = df[first]

    df["_category"] = category
    return df


def match_png_files(df: pd.DataFrame, png_files) -> pd.DataFrame:
    if not png_files:
        return df
    pngs = {}
    for f in png_files:
        stem = Path(f.name).stem.lower().replace(" ", "").replace("-", "").replace("_", "")
        pngs[stem] = Image.open(f)

    def find(row):
        if row["_image"] is not None:
            return row["_image"]
        for col in ["modelo", "nombre"]:
            if col in row.index and pd.notna(row[col]):
                key = str(row[col]).lower().replace(" ", "").replace("-", "").replace("_", "")
                if key in pngs:
                    return pngs[key]
                for stem, img in pngs.items():
                    if stem in key or key in stem:
                        return img
        return None

    df["_image"] = df.apply(find, axis=1)
    return df


# ── Card renderer ─────────────────────────────────────────────────────────────

def render_card(product: pd.Series, col):
    with col:
        with st.container():
            st.markdown('<div class="product-wrapper">', unsafe_allow_html=True)

            img = product.get("_image")
            if img is not None:
                b64 = pil_to_b64(img)
                if b64:
                    st.markdown(
                        f'<img src="data:image/jpeg;base64,{b64}" '
                        f'style="width:100%;height:180px;object-fit:cover;">',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown('<div class="no-image">📦</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="no-image">📦</div>', unsafe_allow_html=True)

            nombre = str(product.get("nombre", "—"))[:60]
            modelo = str(product.get("modelo", "")) if pd.notna(product.get("modelo", "")) else ""
            precio = product.get("precio")
            talla  = product.get("talla")

            precio_str = f"¥ {float(precio):,.0f}" if pd.notna(precio) and precio != "" else ""
            talla_str  = str(talla) if pd.notna(talla) and talla != "" else ""

            st.markdown(f"""
            <div class="card-body">
                <div class="card-name">{nombre}</div>
                <div class="card-model">{modelo}</div>
                <div class="card-price">{precio_str}</div>
                {'<div class="card-size">' + talla_str + '</div>' if talla_str else ''}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("Ver detalles"):
                detail_cols = [c for c in product.index if not c.startswith("_")]
                for dc in detail_cols:
                    val = product[dc]
                    if pd.notna(val) and str(val).strip() not in ("", "nan"):
                        label = DISPLAY_LABELS.get(dc, dc.capitalize())
                        st.markdown(
                            f'<div class="detail-row">'
                            f'<span class="detail-label">{label}</span>'
                            f'<span class="detail-value">{val}</span>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                # Show full image in detail view
                if img is not None:
                    b64 = pil_to_b64(img)
                    if b64:
                        st.markdown(
                            f'<br><img src="data:image/jpeg;base64,{b64}" '
                            f'style="width:100%;border-radius:6px;">',
                            unsafe_allow_html=True,
                        )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    st.title("🛍️ Catálogo de Productos")

    with st.sidebar:
        st.header("📁 Cargar archivos")
        excel_files = st.file_uploader(
            "Packing lists (Excel)",
            type=["xlsx", "xls"],
            accept_multiple_files=True,
        )
        png_files = st.file_uploader(
            "Imágenes adicionales (PNG/JPG)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
        )
        st.divider()
        st.header("🔍 Filtros")
        search = st.text_input("Buscar", placeholder="nombre, modelo, material…")

    if not excel_files:
        st.info("👆 Subí tus archivos Excel desde el panel izquierdo para comenzar.")
        st.markdown("""
**Cómo usar:**
1. Subí uno o más packing lists en Excel
2. Opcionalmente subí imágenes sueltas en PNG/JPG
3. La app extrae datos e imágenes automáticamente
4. Navegá por categoría, buscá o filtrá productos
5. Clickeá **Ver detalles** para ver todas las características
        """)
        return

    # Load & process
    dfs = []
    with st.spinner("Procesando archivos…"):
        for f in excel_files:
            try:
                fb = f.read()
                df = process_excel(fb, f.name)
                dfs.append(df)
                st.sidebar.success(f"✅ {f.name}  ({len(df)} productos)")
            except Exception as e:
                st.sidebar.error(f"❌ {f.name}: {e}")

    if not dfs:
        st.error("No se pudo procesar ningún archivo.")
        return

    all_products = pd.concat(dfs, ignore_index=True)

    if png_files:
        all_products = match_png_files(all_products, png_files)

    # Sidebar: category + price filters
    categories = sorted(all_products["_category"].unique().tolist())

    with st.sidebar:
        sel_cats = st.multiselect("Categorías", options=categories, default=categories)

        price_range = None
        if "precio" in all_products.columns:
            valid = all_products["precio"].dropna()
            if len(valid):
                mn, mx = float(valid.min()), float(valid.max())
                if mn < mx:
                    price_range = st.slider(
                        "Rango de precio", mn, mx, (mn, mx), format="¥%.0f"
                    )

        st.divider()
        st.metric("Productos totales", len(all_products))
        st.metric("Categorías", len(categories))

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
        filtered = filtered[
            filtered["precio"].isna()
            | (filtered["precio"].between(price_range[0], price_range[1]))
        ]

    if len(filtered) == 0:
        st.warning("No hay productos que coincidan con los filtros.")
        return

    # Render by category
    COLS = 4
    for cat in (sel_cats if sel_cats else categories):
        cat_df = filtered[filtered["_category"] == cat]
        if cat_df.empty:
            continue

        st.markdown(
            f'<div class="section-header">📦 {cat}'
            f'<span style="font-size:13px;opacity:.65;margin-left:10px;">'
            f'{len(cat_df)} productos</span></div>',
            unsafe_allow_html=True,
        )

        rows = [cat_df.iloc[i : i + COLS] for i in range(0, len(cat_df), COLS)]
        for row_group in rows:
            cols = st.columns(COLS)
            for j, (_, product) in enumerate(row_group.iterrows()):
                render_card(product, cols[j])


if __name__ == "__main__":
    main()
