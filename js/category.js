/* ============================================================
   CASA MATER — Category Page JS
   ============================================================ */

// --- Filter accordion (open/close groups) ---
document.querySelectorAll('.filter-group__header').forEach(btn => {
  btn.addEventListener('click', function () {
    const group = this.closest('.filter-group');
    const icon  = this.querySelector('.filter-group__icon');
    const isOpen = group.classList.toggle('open');
    if (icon) icon.textContent = isOpen ? '×' : '+';
  });
});
// Open first filter by default
const firstGroup = document.querySelector('.filter-group');
if (firstGroup) {
  firstGroup.classList.add('open');
  const icon = firstGroup.querySelector('.filter-group__icon');
  if (icon) icon.textContent = '×';
}

// --- Toggle sidebar ---
const toggleBtn  = document.getElementById('toggleFilters');
const catLayout  = document.querySelector('.cat-layout');
const catFilters = document.querySelector('.cat-filters');

toggleBtn?.addEventListener('click', function () {
  const hidden = catFilters.classList.toggle('hidden');
  catLayout.classList.toggle('filters-hidden', hidden);
  this.classList.toggle('filters-hidden', hidden);
  this.querySelector('.toggle-label').textContent = hidden ? 'Mostrar Filtros' : 'Ocultar Filtros';
});

// --- View toggle ---
document.querySelectorAll('.view-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const cols = this.dataset.view;
    document.querySelectorAll('.cat-products-grid').forEach(grid => {
      grid.classList.remove('view-4col', 'view-2col');
      if (cols === '4') grid.classList.add('view-4col');
      if (cols === '2') grid.classList.add('view-2col');
    });
  });
});

// ── Filter engine ─────────────────────────────────────────────────────────────

let priceMin = 0;
let priceMax = Infinity;
const totalProducts = document.querySelectorAll('.cat-product').length;

function getCheckedByGroup() {
  const result = {};
  document.querySelectorAll('.filter-group').forEach(group => {
    const header = group.querySelector('.filter-group__header');
    if (!header) return;
    const groupName = header.textContent.replace(/[+×]/g, '').trim();
    // skip price group
    if (group.querySelector('#priceFrom')) return;
    const checked = [...group.querySelectorAll('input[type=checkbox]:checked')]
      .map(cb => cb.closest('label').textContent.trim().toLowerCase());
    if (checked.length) result[groupName] = checked;
  });
  return result;
}

function applyFilters() {
  const byGroup = getCheckedByGroup();
  const hasChecked = Object.keys(byGroup).length > 0;

  document.querySelectorAll('.cat-product').forEach(card => {
    const price = parseInt(card.dataset.price || 0);
    const cardText = card.textContent.toLowerCase();

    // Price check
    let show = price >= priceMin && price <= priceMax;

    // Checkbox check: ALL groups must have at least one match
    if (show && hasChecked) {
      for (const [, values] of Object.entries(byGroup)) {
        const groupMatch = values.some(v => cardText.includes(v));
        if (!groupMatch) { show = false; break; }
      }
    }

    card.style.display = show ? '' : 'none';
  });

  // Update section visibility + count labels
  let visibleTotal = 0;
  document.querySelectorAll('.cat-section').forEach(section => {
    const visibleCards = [...section.querySelectorAll('.cat-product')]
      .filter(c => c.style.display !== 'none');
    section.style.display = visibleCards.length ? '' : 'none';
    const countEl = section.querySelector('.cat-section__count');
    if (countEl) countEl.textContent = `${visibleCards.length} producto${visibleCards.length !== 1 ? 's' : ''}`;
    visibleTotal += visibleCards.length;
  });

  // Update toolbar count
  const toolbarCount = document.querySelector('.cat-toolbar__count');
  if (toolbarCount) {
    toolbarCount.innerHTML = `Mostrando <strong>${visibleTotal}</strong> de <strong>${totalProducts}</strong> resultados.`;
  }
}

// Checkbox change → filter
document.querySelectorAll('.cat-filters input[type=checkbox]').forEach(cb => {
  cb.addEventListener('change', applyFilters);
});

// Price filter
document.getElementById('applyPrice')?.addEventListener('click', () => {
  const fromVal = document.getElementById('priceFrom')?.value;
  const toVal   = document.getElementById('priceTo')?.value;
  priceMin = fromVal ? parseInt(fromVal) : 0;
  priceMax = toVal   ? parseInt(toVal)   : Infinity;
  applyFilters();
});

// Enter key on price inputs
['priceFrom', 'priceTo'].forEach(id => {
  document.getElementById(id)?.addEventListener('keydown', e => {
    if (e.key === 'Enter') document.getElementById('applyPrice')?.click();
  });
});

// ── Sort ──────────────────────────────────────────────────────────────────────
// Save original order on load so "Más Nuevo" can restore it
const originalOrder = new Map();
document.querySelectorAll('.cat-products-grid').forEach(grid => {
  originalOrder.set(grid, [...grid.querySelectorAll('.cat-product')]);
});

document.querySelector('.sort-select')?.addEventListener('change', function () {
  document.querySelectorAll('.cat-products-grid').forEach(grid => {
    const cards = [...grid.querySelectorAll('.cat-product')];
    if (this.value === 'price-asc') {
      cards.sort((a, b) => parseInt(a.dataset.price || 0) - parseInt(b.dataset.price || 0));
    } else if (this.value === 'price-desc') {
      cards.sort((a, b) => parseInt(b.dataset.price || 0) - parseInt(a.dataset.price || 0));
    } else {
      // newest: restore original DOM order
      const orig = originalOrder.get(grid) || cards;
      orig.forEach(c => grid.appendChild(c));
      return;
    }
    cards.forEach(c => grid.appendChild(c));
  });
});

// ── Wishlist ──────────────────────────────────────────────────────────────────
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.cat-product__wish-btn');
  if (!btn) return;
  btn.classList.toggle('active');
  const name = btn.closest('.cat-product')?.querySelector('.cat-product__name')?.textContent || 'Producto';
  showCatToast(btn.classList.contains('active')
    ? `"${name}" guardado en favoritos`
    : `"${name}" eliminado de favoritos`);
});

// ── Add to cart ───────────────────────────────────────────────────────────────
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.cat-product__quick[data-price]');
  if (!btn) return;
  const card  = btn.closest('.cat-product');
  const name  = card?.querySelector('.cat-product__name')?.textContent || 'Producto';
  showCatToast(`"${name}" agregado al carrito`);
  const countEl = document.getElementById('cartCount');
  if (countEl) {
    countEl.textContent = parseInt(countEl.textContent || 0) + 1;
    countEl.style.display = 'flex';
  }
});

// ── Toast ─────────────────────────────────────────────────────────────────────
function showCatToast(msg) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast';
    toast.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg><span id="toastMsg"></span>`;
    document.body.appendChild(toast);
  }
  toast.querySelector('#toastMsg').textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => toast.classList.remove('show'), 2800);
}

// ── Scroll reveal ─────────────────────────────────────────────────────────────
const revealEls = document.querySelectorAll('.cat-product, .cat-section__header');
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
      io.unobserve(e.target);
    }
  });
}, { threshold: .08, rootMargin: '0px 0px -20px 0px' });

revealEls.forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = `opacity .55s ease ${(i % 8) * 0.06}s, transform .55s ease ${(i % 8) * 0.06}s`;
  io.observe(el);
});
