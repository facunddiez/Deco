/* ============================================================
   AURA HOME — Shared Nav (mega menus completos + hover estable)
   Incluir ANTES de main.js en cada página.
   Agregar data-page="indoor|outdoor|iluminacion|textiles|decoracion|sale"
   al <body> para marcar el ítem activo.
   ============================================================ */

const MEGA = {
  indoor: {
    href: 'indoor.html',
    label: 'Indoor',
    img: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Colección Osaka',
    cols: [
      { title: 'New In',  links: ['Novedades','Best Sellers','Outlet'] },
      { title: 'Asientos', links: ['Sofás 2 cuerpos','Sofás 3 cuerpos','Sofás con chaise','Sillones','Poltronas','Sillas de comedor'] },
      { title: 'Mesas',   links: ['Mesas de comedor','Mesas de centro','Mesas auxiliares','Escritorios','Consolas'] },
      { title: 'Almacenamiento', links: ['Bibliotecas','Aparadores','Cómodas','Rack TV','Estantes'] },
    ],
  },
  outdoor: {
    href: 'outdoor.html',
    label: 'Outdoor',
    img: 'https://images.unsplash.com/photo-1600210492493-0946911123ea?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Colección Jardín',
    cols: [
      { title: 'New In',  links: ['Novedades','Best Sellers'] },
      { title: 'Asientos', links: ['Sofás de jardín','Sillas de exterior','Reposeras','Hamacas','Puffs exterior'] },
      { title: 'Mesas & Accesorios', links: ['Mesas de jardín','Mesas de terraza','Sombrillas','Parasoles'] },
      { title: 'Ambientación', links: ['Macetas grandes','Faroles exterior','Alfombras exterior','Calefactores'] },
    ],
  },
  iluminacion: {
    href: 'iluminacion.html',
    label: 'Iluminación',
    img: 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Nueva colección',
    cols: [
      { title: 'New In',  links: ['Novedades','Best Sellers'] },
      { title: 'Interior', links: ['Colgantes & Araña','Lámparas de pie','Lámparas de mesa','Apliques de pared','Plafones'] },
      { title: 'Por material', links: ['Rattan & Jute','Metal & Hierro','Vidrio & Cristal','Cerámica','Madera'] },
      { title: 'Exterior', links: ['Faroles jardín','Apliques exterior','Guirnaldas','Solar'] },
    ],
  },
  textiles: {
    href: 'textiles.html',
    label: 'Textiles',
    img: 'https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Textiles naturales',
    cols: [
      { title: 'New In',  links: ['Novedades','Best Sellers'] },
      { title: 'Alfombras', links: ['Shaggy','Kilim','Lana natural','Yute & Sisal','Exterior'] },
      { title: 'Cama & Baño', links: ['Ropa de cama','Toallas & Albornoces','Almohadones','Mantas & Throws'] },
      { title: 'Ventanas', links: ['Cortinas lino','Cortinas blackout','Visillos','Estores'] },
    ],
  },
  decoracion: {
    href: 'decoracion.html',
    label: 'Decoración',
    img: 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Objetos de autor',
    cols: [
      { title: 'New In',  links: ['Novedades','Best Sellers'] },
      { title: 'Objetos', links: ['Jarrones & Floreros','Espejos','Esculturas','Relojes','Objetos de autor'] },
      { title: 'Arte & Pared', links: ['Cuadros & Prints','Fotografías','Marcos','Tapices'] },
      { title: 'Ambiente', links: ['Velas & Difusores','Plantas & Macetas','Cestos & Organizadores','Libros de diseño'] },
    ],
  },
};

function buildMegaMenu(key) {
  const m = MEGA[key];
  const cols = m.cols.map(col => `
    <div class="mega-menu__col">
      <p class="mega-menu__heading">${col.title}</p>
      <ul>${col.links.map(l => `<li><a href="#">${l}</a></li>`).join('')}</ul>
    </div>`).join('');
  return `
    <div class="mega-menu">
      <div class="container">
        <div class="mega-menu__grid">
          ${cols}
          <div class="mega-menu__col mega-menu__col--img">
            <a href="${m.href}" class="mega-menu__promo">
              <img src="${m.img}" alt="${m.label}" />
              <span class="mega-menu__promo-label">${m.imgLabel}</span>
            </a>
          </div>
        </div>
      </div>
    </div>`;
}

const chevronSVG = `<svg class="nav__chevron" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>`;

function buildNavMenu(activePage) {
  const megaItems = Object.entries(MEGA).map(([key, m]) => {
    const isActive = activePage === key ? ' active' : '';
    return `
      <li class="nav__item--mega">
        <a href="${m.href}" class="nav__link nav__link--dropdown${isActive}">${m.label} ${chevronSVG}</a>
        ${buildMegaMenu(key)}
      </li>`;
  }).join('');

  const homeActive = activePage === 'home' ? ' active' : '';
  return `
    <li><a href="index.html" class="nav__link${homeActive}">Home</a></li>
    ${megaItems}
    <li><a href="sale.html" class="nav__link nav__link--sale${activePage === 'sale' ? ' active' : ''}">SALE</a></li>`;
}

function buildDrawer(activePage) {
  const items = [
    { key: 'home', href: 'index.html', label: 'Home', sub: null },
    { key: 'indoor', href: 'indoor.html', label: 'Indoor', sub: ['Sofás & Sillones','Sillas de comedor','Mesas de comedor','Mesas de centro','Escritorios','Almacenamiento'] },
    { key: 'outdoor', href: 'outdoor.html', label: 'Outdoor', sub: ['Sofás de jardín','Sillas de exterior','Reposeras','Mesas de terraza','Ambientación'] },
    { key: 'iluminacion', href: 'iluminacion.html', label: 'Iluminación', sub: ['Colgantes & Araña','Lámparas de pie','Lámparas de mesa','Apliques de pared','Exterior'] },
    { key: 'textiles', href: 'textiles.html', label: 'Textiles', sub: ['Alfombras','Almohadones','Mantas & Throws','Ropa de cama','Cortinas'] },
    { key: 'decoracion', href: 'decoracion.html', label: 'Decoración', sub: ['Jarrones & Floreros','Espejos','Cuadros & Arte','Velas & Difusores','Plantas & Macetas'] },
  ];
  return items.map(item => {
    const active = activePage === item.key ? ' active' : '';
    if (!item.sub) return `<a href="${item.href}" class="nav__link${active}">${item.label}</a>`;
    const subLinks = item.sub.map(s => `<a href="#">${s}</a>`).join('');
    return `
      <details class="drawer__details"${activePage === item.key ? ' open' : ''}>
        <summary class="nav__link${active}">${item.label}</summary>
        <div class="drawer__sub">${subLinks}</div>
      </details>`;
  }).join('') + `<a href="sale.html" class="nav__link nav__link--sale${activePage === 'sale' ? ' active' : ''}">SALE</a>`;
}

/* ---- Inject on DOMContentLoaded ---- */
document.addEventListener('DOMContentLoaded', () => {
  const activePage = document.body.dataset.page || 'home';

  // Inject desktop menu
  const menu = document.querySelector('#mainNav .nav__menu');
  if (menu) menu.innerHTML = buildNavMenu(activePage);

  // Inject mobile drawer
  const drawer = document.getElementById('navDrawer');
  if (drawer) drawer.innerHTML = buildDrawer(activePage);

  /* ---- Stable hover: JS timer approach ---- */
  document.querySelectorAll('.nav__item--mega').forEach(item => {
    let closeTimer;

    const openMenu = () => {
      clearTimeout(closeTimer);
      // Close all others first
      document.querySelectorAll('.nav__item--mega.mega-open').forEach(other => {
        if (other !== item) other.classList.remove('mega-open');
      });
      item.classList.add('mega-open');
    };

    const scheduleClose = () => {
      closeTimer = setTimeout(() => item.classList.remove('mega-open'), 120);
    };

    item.addEventListener('mouseenter', openMenu);
    item.addEventListener('mouseleave', scheduleClose);

    const drop = item.querySelector('.mega-menu');
    if (drop) {
      drop.addEventListener('mouseenter', () => clearTimeout(closeTimer));
      drop.addEventListener('mouseleave', scheduleClose);
    }
  });

  // Close mega menus when clicking outside
  document.addEventListener('click', e => {
    if (!e.target.closest('.nav__item--mega')) {
      document.querySelectorAll('.nav__item--mega.mega-open').forEach(item => item.classList.remove('mega-open'));
    }
  });

  // Close mega menus on scroll
  window.addEventListener('scroll', () => {
    document.querySelectorAll('.nav__item--mega.mega-open').forEach(item => item.classList.remove('mega-open'));
  }, { passive: true });
});
