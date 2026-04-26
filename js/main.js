/* ============================================================
   CASA MATER — Main JS
   Módulos: Nav, Cart, Filters, Scroll Reveal, Wishlist
   ============================================================ */

// --- ANNOUNCE BAR close ---
(function () {
  const bar   = document.getElementById('announceBar');
  const close = document.getElementById('announceClose');
  if (!bar || !close) return;
  close.addEventListener('click', () => {
    bar.classList.add('hidden');
    sessionStorage.setItem('announceHidden', '1');
  });
  if (sessionStorage.getItem('announceHidden')) bar.classList.add('hidden');
})();

// --- NAV: Transparente → sólida al scroll ---
(function () {
  const nav     = document.getElementById('mainNav');
  const announce = document.getElementById('announceBar');
  if (!nav) return;

  // On non-home pages always start solid/dark
  if (document.body.dataset.page !== 'home') {
    nav.classList.add('scrolled');
    nav.classList.remove('nav--hero');
  }

  let lastY = 0;

  function onScroll() {
    const y = window.scrollY;
    const announceH = announce && !announce.classList.contains('hidden') ? announce.offsetHeight : 0;
    const threshold = announceH + 40;
    const isScrolled = y > threshold;

    nav.classList.toggle('scrolled', isScrolled);
    const isHome = document.body.dataset.page === 'home';
    nav.classList.toggle('nav--hero', isHome && !isScrolled);

    if (y > 200) {
      nav.style.transform = y > lastY + 4 ? 'translateY(-100%)' : 'translateY(0)';
    } else {
      nav.style.transform = 'translateY(0)';
    }
    lastY = y;
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

// --- NAV MOBILE: Burger + Drawer ---
(function () {
  const burger  = document.getElementById('menuToggle');
  const drawer  = document.getElementById('navDrawer');
  const overlay = document.getElementById('navOverlay');
  if (!burger) return;

  function toggle(open) {
    burger.classList.toggle('open', open);
    drawer.classList.toggle('open', open);
    overlay.classList.toggle('visible', open);
    document.body.style.overflow = open ? 'hidden' : '';
  }

  burger.addEventListener('click', () => toggle(!drawer.classList.contains('open')));
  overlay.addEventListener('click', () => toggle(false));

  drawer.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => toggle(false));
  });
})();

// --- CART ---
const cart = (function () {
  const items    = {};
  const sidebar  = document.getElementById('cartSidebar');
  const overlay  = document.getElementById('cartOverlay');
  const body     = document.getElementById('cartBody');
  const footer   = document.getElementById('cartFooter');
  const empty    = document.getElementById('cartEmpty');
  const countEl  = document.getElementById('cartCount');
  const totalEl  = document.getElementById('cartTotal');
  const cartBtn  = document.querySelector('.cart-btn');

  function fmt(n) {
    return '$' + n.toLocaleString('es-AR');
  }

  function totalItems() {
    return Object.values(items).reduce((s, i) => s + i.qty, 0);
  }

  function totalPrice() {
    return Object.values(items).reduce((s, i) => s + i.price * i.qty, 0);
  }

  function render() {
    const total = totalItems();
    countEl.textContent = total;
    countEl.style.display = total > 0 ? 'flex' : 'none';

    const keys = Object.keys(items);
    empty.style.display = keys.length ? 'none' : 'flex';
    footer.style.display = keys.length ? 'block' : 'none';
    totalEl.textContent = fmt(totalPrice());

    // Re-render items
    body.querySelectorAll('.cart-item').forEach(el => el.remove());

    keys.forEach(id => {
      const item = items[id];
      const el = document.createElement('div');
      el.className = 'cart-item';
      el.dataset.id = id;
      el.innerHTML = `
        <img class="cart-item__img" src="${item.img}" alt="${item.name}" />
        <div>
          <p class="cart-item__name">${item.name}</p>
          <p class="cart-item__option">${item.option || 'Color natural'}</p>
          <div class="cart-item__qty">
            <button class="qty-btn qty-minus" data-id="${id}">−</button>
            <span class="qty-val">${item.qty}</span>
            <button class="qty-btn qty-plus"  data-id="${id}">+</button>
          </div>
          <button class="cart-item__remove" data-id="${id}">Eliminar</button>
        </div>
        <span class="cart-item__price">${fmt(item.price * item.qty)}</span>
      `;
      body.appendChild(el);
    });

    // Attach qty & remove listeners
    body.querySelectorAll('.qty-minus').forEach(btn =>
      btn.addEventListener('click', () => changeQty(btn.dataset.id, -1))
    );
    body.querySelectorAll('.qty-plus').forEach(btn =>
      btn.addEventListener('click', () => changeQty(btn.dataset.id, 1))
    );
    body.querySelectorAll('.cart-item__remove').forEach(btn =>
      btn.addEventListener('click', () => remove(btn.dataset.id))
    );
  }

  function changeQty(id, delta) {
    if (!items[id]) return;
    items[id].qty = Math.max(1, items[id].qty + delta);
    render();
  }

  function remove(id) {
    delete items[id];
    render();
  }

  function add(id, name, price, img) {
    if (items[id]) {
      items[id].qty++;
    } else {
      items[id] = { id, name, price: parseInt(price), img: img || '', qty: 1 };
    }
    render();
    // Bump animation on cart icon
    if (cartBtn) {
      cartBtn.classList.remove('bump');
      void cartBtn.offsetWidth;
      cartBtn.classList.add('bump');
    }
  }

  function open()  {
    sidebar.classList.add('open');
    overlay.classList.add('visible');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    sidebar.classList.remove('open');
    overlay.classList.remove('visible');
    document.body.style.overflow = '';
  }

  // Toggle on cart icon click
  document.getElementById('cartToggle')?.addEventListener('click', () => {
    sidebar.classList.contains('open') ? close() : open();
  });
  document.getElementById('cartClose')?.addEventListener('click', close);
  overlay?.addEventListener('click', close);

  return { add, open, close };
})();

// --- TOAST ---
function showToast(msg) {
  const toast = document.getElementById('toast');
  const msgEl = document.getElementById('toastMsg');
  if (!toast) return;
  msgEl.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => toast.classList.remove('show'), 2800);
}

// --- ADD TO CART: Event delegation on product grid ---
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.product-card__cta');
  if (!btn) return;

  const { id, name, price } = btn.dataset;
  const card = btn.closest('.product-card');
  const img  = card?.querySelector('.product-card__img')?.src || '';

  cart.add(id, name, price, img);
  showToast(`"${name}" fue agregado al carrito`);

  // Open cart after short delay
  setTimeout(() => cart.open(), 320);
});

// --- FILTER BUTTONS ---
(function () {
  const buttons = document.querySelectorAll('.filter-btn');
  const cards   = document.querySelectorAll('.product-card');
  if (!buttons.length) return;

  buttons.forEach(btn => {
    btn.addEventListener('click', function () {
      buttons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');

      const filter = this.dataset.filter;
      let delay = 0;

      cards.forEach(card => {
        const match = filter === 'all' || card.dataset.category === filter;
        card.style.transition = 'opacity .3s ease, transform .3s ease';
        card.style.animationDelay = delay + 's';

        if (match) {
          card.style.display = 'flex';
          requestAnimationFrame(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          });
          delay += 0.06;
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(12px)';
          setTimeout(() => {
            if (card.style.opacity === '0') card.style.display = 'none';
          }, 300);
        }
      });
    });
  });
})();

// --- WISHLIST (toggle heart) ---
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.product-card__wish');
  if (!btn) return;
  e.preventDefault();
  const isActive = btn.classList.toggle('active');
  const card = btn.closest('.product-card');
  const name = card?.querySelector('.product-card__name')?.textContent || 'Producto';
  showToast(isActive ? `"${name}" guardado en favoritos` : `"${name}" eliminado de favoritos`);
});

// --- SCROLL REVEAL ---
(function () {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;

  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: .12, rootMargin: '0px 0px -40px 0px' });

  els.forEach(el => io.observe(el));
})();

// --- NEWSLETTER form ---
(function () {
  const form = document.getElementById('newsletterForm');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const input = form.querySelector('input');
    showToast('¡Gracias! Ya estás suscrito a Casa Mater.');
    input.value = '';
  });
})();

// --- NAV smooth scroll for anchor links ---
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const offset = 90;
    const top = target.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});

// --- Parallax on hero bg (desktop only) ---
(function () {
  const heroBg = document.querySelector('.hero__bg');
  if (!heroBg || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function onScroll() {
    const y = window.scrollY;
    if (y < window.innerHeight) {
      heroBg.style.transform = `translateY(${y * 0.28}px)`;
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
})();
