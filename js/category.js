/* ============================================================
   CASA MATER — Category Page JS
   Filtros, ordenar, vista, wishlist
   ============================================================ */

// --- Filter accordion ---
document.querySelectorAll('.filter-group__header').forEach(btn => {
  btn.addEventListener('click', function () {
    const group = this.closest('.filter-group');
    group.classList.toggle('open');
  });
});

// Abrir primer filtro por defecto
document.querySelector('.filter-group')?.classList.add('open');

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
      grid.classList.remove('view-2col', 'view-4col');
      if (cols !== '3') grid.classList.add('view-' + cols + 'col');
    });
  });
});

// --- Wishlist toggle ---
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.cat-product__wish-btn');
  if (!btn) return;
  btn.classList.toggle('active');
  const name = btn.closest('.cat-product')?.querySelector('.cat-product__name')?.textContent || 'Producto';
  const isActive = btn.classList.contains('active');
  showCatToast(isActive ? `"${name}" guardado en favoritos` : `"${name}" eliminado de favoritos`);
});

// --- Add to cart from category ---
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.cat-product__quick[data-price]');
  if (!btn) return;
  const card = btn.closest('.cat-product');
  const name  = card?.querySelector('.cat-product__name')?.textContent || 'Producto';
  const price = btn.dataset.price || '0';
  const img   = card?.querySelector('.cat-product__img')?.src || '';
  showCatToast(`"${name}" agregado al carrito`);
  // Bump cart count
  const countEl = document.getElementById('cartCount');
  if (countEl) {
    countEl.textContent = parseInt(countEl.textContent || 0) + 1;
    countEl.style.display = 'flex';
  }
});

// --- Sort (visual only, no backend) ---
document.querySelector('.sort-select')?.addEventListener('change', function () {
  const sections = document.querySelectorAll('.cat-section');
  sections.forEach(s => {
    const grid  = s.querySelector('.cat-products-grid');
    if (!grid) return;
    const cards = [...grid.querySelectorAll('.cat-product')];
    if (this.value === 'price-asc') {
      cards.sort((a, b) => {
        const pa = parseInt(a.dataset.price || 0);
        const pb = parseInt(b.dataset.price || 0);
        return pa - pb;
      });
    } else if (this.value === 'price-desc') {
      cards.sort((a, b) => {
        const pa = parseInt(a.dataset.price || 0);
        const pb = parseInt(b.dataset.price || 0);
        return pb - pa;
      });
    }
    cards.forEach(c => grid.appendChild(c));
  });
});

// --- Toast ---
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

// --- Scroll reveal ---
const revealEls = document.querySelectorAll('.cat-product, .cat-section__header, .reveal');
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
