/* ============================================================
   CASA MATER — Shared Nav (mega menus completos + hover estable)
   ============================================================ */

const MEGA = {
  indoor: {
    href: 'indoor.html',
    label: 'Indoor',
    img: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Colección Osaka',
    cols: [
      { title: 'New In', links: [
        { label: 'Novedades',    href: 'indoor.html' },
        { label: 'Best Sellers', href: 'indoor.html' },
        { label: 'Outlet',       href: 'sale.html' },
      ]},
      { title: 'Asientos', href: 'indoor-asientos.html', links: [
        { label: 'Sofás 2 cuerpos',   href: 'indoor-sofas-2-cuerpos.html' },
        { label: 'Sofás 3 cuerpos',   href: 'indoor-sofas-3-cuerpos.html' },
        { label: 'Sofás con chaise',  href: 'indoor-sofas-chaise.html' },
        { label: 'Sillones',          href: 'indoor-sillones.html' },
        { label: 'Poltronas',         href: 'indoor-poltronas.html' },
        { label: 'Sillas de comedor', href: 'indoor-sillas-comedor.html' },
      ]},
      { title: 'Mesas', href: 'indoor-mesas.html', links: [
        { label: 'Mesas de comedor',  href: 'indoor-mesas-comedor.html' },
        { label: 'Mesas de centro',   href: 'indoor-mesas-centro.html' },
        { label: 'Mesas auxiliares',  href: 'indoor-mesas-auxiliares.html' },
        { label: 'Escritorios',       href: 'indoor-escritorios.html' },
        { label: 'Consolas',          href: 'indoor-consolas.html' },
      ]},
      { title: 'Almacenamiento', href: 'indoor-almacenamiento.html', links: [
        { label: 'Bibliotecas', href: 'indoor-bibliotecas.html' },
        { label: 'Aparadores',  href: 'indoor-aparadores.html' },
        { label: 'Cómodas',     href: 'indoor-comodas.html' },
        { label: 'Rack TV',     href: 'indoor-rack-tv.html' },
        { label: 'Estantes',    href: 'indoor-estantes.html' },
      ]},
    ],
  },
  outdoor: {
    href: 'outdoor.html',
    label: 'Outdoor',
    img: 'https://images.unsplash.com/photo-1600210492493-0946911123ea?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Colección Jardín',
    cols: [
      { title: 'New In', links: [
        { label: 'Novedades',    href: 'outdoor.html' },
        { label: 'Best Sellers', href: 'outdoor.html' },
      ]},
      { title: 'Asientos', href: 'outdoor-asientos-ext.html', links: [
        { label: 'Sofás de jardín',    href: 'outdoor-sofas-jardin.html' },
        { label: 'Sillas de exterior', href: 'outdoor-sillas-exterior.html' },
        { label: 'Reposeras',          href: 'outdoor-reposeras.html' },
        { label: 'Hamacas',            href: 'outdoor-hamacas.html' },
        { label: 'Puffs exterior',     href: 'outdoor-puffs-exterior.html' },
      ]},
      { title: 'Mesas & Accesorios', href: 'outdoor-mesas-ext.html', links: [
        { label: 'Mesas de jardín',  href: 'outdoor-mesas-jardin.html' },
        { label: 'Mesas de terraza', href: 'outdoor-mesas-terraza.html' },
        { label: 'Sombrillas',       href: 'outdoor-sombrillas.html' },
        { label: 'Parasoles',        href: 'outdoor-parasoles.html' },
      ]},
      { title: 'Ambientación', href: 'outdoor-ambientacion-ext.html', links: [
        { label: 'Macetas grandes',    href: 'outdoor-macetas-grandes.html' },
        { label: 'Faroles exterior',   href: 'outdoor-faroles-exterior.html' },
        { label: 'Alfombras exterior', href: 'outdoor-alfombras-exterior.html' },
        { label: 'Calefactores',       href: 'outdoor-calefactores.html' },
      ]},
    ],
  },
  iluminacion: {
    href: 'iluminacion.html',
    label: 'Iluminación',
    img: 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Nueva colección',
    cols: [
      { title: 'New In', links: [
        { label: 'Novedades',    href: 'iluminacion.html' },
        { label: 'Best Sellers', href: 'iluminacion.html' },
      ]},
      { title: 'Interior', href: 'iluminacion-interior-ilum.html', links: [
        { label: 'Colgantes & Araña', href: 'iluminacion-colgantes-arana.html' },
        { label: 'Lámparas de pie',   href: 'iluminacion-lamparas-pie.html' },
        { label: 'Lámparas de mesa',  href: 'iluminacion-lamparas-mesa.html' },
        { label: 'Apliques de pared', href: 'iluminacion-apliques-pared.html' },
        { label: 'Plafones',          href: 'iluminacion-plafones.html' },
      ]},
      { title: 'Por material', href: 'iluminacion-material-ilum.html', links: [
        { label: 'Rattan & Jute',  href: 'iluminacion-rattan-jute.html' },
        { label: 'Metal & Hierro', href: 'iluminacion-metal-hierro.html' },
        { label: 'Vidrio & Cristal',href: 'iluminacion-vidrio-cristal.html' },
        { label: 'Cerámica',       href: 'iluminacion-ceramica-ilum.html' },
        { label: 'Madera',         href: 'iluminacion-madera-ilum.html' },
      ]},
      { title: 'Exterior', href: 'iluminacion-exterior-ilum.html', links: [
        { label: 'Faroles jardín',    href: 'iluminacion-faroles-jardin.html' },
        { label: 'Apliques exterior', href: 'iluminacion-apliques-exterior.html' },
        { label: 'Guirnaldas',        href: 'iluminacion-guirnaldas.html' },
        { label: 'Solar',             href: 'iluminacion-solar.html' },
      ]},
    ],
  },
  textiles: {
    href: 'textiles.html',
    label: 'Textiles',
    img: 'https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Textiles naturales',
    cols: [
      { title: 'New In', links: [
        { label: 'Novedades',    href: 'textiles.html' },
        { label: 'Best Sellers', href: 'textiles.html' },
      ]},
      { title: 'Alfombras', href: 'textiles-alfombras-text.html', links: [
        { label: 'Shaggy',       href: 'textiles-shaggy.html' },
        { label: 'Kilim',        href: 'textiles-kilim.html' },
        { label: 'Lana natural', href: 'textiles-lana-natural.html' },
        { label: 'Yute & Sisal', href: 'textiles-yute-sisal.html' },
        { label: 'Exterior',     href: 'textiles-alfombras-ext.html' },
      ]},
      { title: 'Cama & Baño', href: 'textiles-cama-bano.html', links: [
        { label: 'Ropa de cama',         href: 'textiles-ropa-cama.html' },
        { label: 'Toallas & Albornoces', href: 'textiles-toallas-albornoces.html' },
        { label: 'Almohadones',          href: 'textiles-almohadones.html' },
        { label: 'Mantas & Throws',      href: 'textiles-mantas-throws.html' },
      ]},
      { title: 'Ventanas', href: 'textiles-ventanas.html', links: [
        { label: 'Cortinas lino',     href: 'textiles-cortinas-lino.html' },
        { label: 'Cortinas blackout', href: 'textiles-cortinas-blackout.html' },
        { label: 'Visillos',          href: 'textiles-visillos.html' },
        { label: 'Estores',           href: 'textiles-estores.html' },
      ]},
    ],
  },
  decoracion: {
    href: 'decoracion.html',
    label: 'Decoración',
    img: 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=320&q=80&auto=format&fit=crop',
    imgLabel: 'Objetos de autor',
    cols: [
      { title: 'New In', links: [
        { label: 'Novedades',    href: 'decoracion.html' },
        { label: 'Best Sellers', href: 'decoracion.html' },
      ]},
      { title: 'Objetos', href: 'decoracion-objetos-deco.html', links: [
        { label: 'Jarrones & Floreros', href: 'decoracion-jarrones-floreros.html' },
        { label: 'Espejos',             href: 'decoracion-espejos.html' },
        { label: 'Esculturas',          href: 'decoracion-esculturas.html' },
        { label: 'Relojes',             href: 'decoracion-relojes.html' },
        { label: 'Objetos de autor',    href: 'decoracion-objetos-autor.html' },
      ]},
      { title: 'Arte & Pared', href: 'decoracion-arte-pared.html', links: [
        { label: 'Cuadros & Prints', href: 'decoracion-cuadros-prints.html' },
        { label: 'Fotografías',      href: 'decoracion-fotografias.html' },
        { label: 'Marcos',           href: 'decoracion-marcos.html' },
        { label: 'Tapices',          href: 'decoracion-tapices.html' },
      ]},
      { title: 'Ambiente', href: 'decoracion-ambiente-deco.html', links: [
        { label: 'Velas & Difusores',    href: 'decoracion-velas-difusores.html' },
        { label: 'Plantas & Macetas',    href: 'decoracion-plantas-macetas.html' },
        { label: 'Cestos & Organizadores',href:'decoracion-cestos-organiz.html' },
        { label: 'Libros de diseño',     href: 'decoracion-libros-diseno.html' },
      ]},
    ],
  },
};

function buildMegaMenu(key) {
  const m = MEGA[key];
  const cols = m.cols.map(col => {
    const titleHtml = col.href
      ? `<a href="${col.href}" class="mega-menu__heading mega-menu__heading--link">${col.title}</a>`
      : `<p class="mega-menu__heading">${col.title}</p>`;
    const linksHtml = col.links.map(l => `<li><a href="${l.href}">${l.label}</a></li>`).join('');
    return `<div class="mega-menu__col">${titleHtml}<ul>${linksHtml}</ul></div>`;
  }).join('');
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
    { key: 'indoor', href: 'indoor.html', label: 'Indoor', sub: [
      { label: 'Asientos',       href: 'indoor-asientos.html' },
      { label: 'Sofás 2 cuerpos',href: 'indoor-sofas-2-cuerpos.html' },
      { label: 'Sofás 3 cuerpos',href: 'indoor-sofas-3-cuerpos.html' },
      { label: 'Sillones',       href: 'indoor-sillones.html' },
      { label: 'Mesas',          href: 'indoor-mesas.html' },
      { label: 'Almacenamiento', href: 'indoor-almacenamiento.html' },
    ]},
    { key: 'outdoor', href: 'outdoor.html', label: 'Outdoor', sub: [
      { label: 'Asientos',         href: 'outdoor-asientos-ext.html' },
      { label: 'Sofás de jardín',  href: 'outdoor-sofas-jardin.html' },
      { label: 'Sillas exterior',  href: 'outdoor-sillas-exterior.html' },
      { label: 'Mesas & Acc.',     href: 'outdoor-mesas-ext.html' },
      { label: 'Ambientación',     href: 'outdoor-ambientacion-ext.html' },
    ]},
    { key: 'iluminacion', href: 'iluminacion.html', label: 'Iluminación', sub: [
      { label: 'Interior',         href: 'iluminacion-interior-ilum.html' },
      { label: 'Colgantes & Araña',href: 'iluminacion-colgantes-arana.html' },
      { label: 'Lámparas de pie',  href: 'iluminacion-lamparas-pie.html' },
      { label: 'Por material',     href: 'iluminacion-material-ilum.html' },
      { label: 'Exterior',         href: 'iluminacion-exterior-ilum.html' },
    ]},
    { key: 'textiles', href: 'textiles.html', label: 'Textiles', sub: [
      { label: 'Alfombras',        href: 'textiles-alfombras-text.html' },
      { label: 'Shaggy',           href: 'textiles-shaggy.html' },
      { label: 'Cama & Baño',      href: 'textiles-cama-bano.html' },
      { label: 'Almohadones',      href: 'textiles-almohadones.html' },
      { label: 'Ventanas',         href: 'textiles-ventanas.html' },
    ]},
    { key: 'decoracion', href: 'decoracion.html', label: 'Decoración', sub: [
      { label: 'Jarrones & Floreros',href: 'decoracion-jarrones-floreros.html' },
      { label: 'Espejos',            href: 'decoracion-espejos.html' },
      { label: 'Arte & Pared',       href: 'decoracion-arte-pared.html' },
      { label: 'Ambiente',           href: 'decoracion-ambiente-deco.html' },
    ]},
  ];
  return items.map(item => {
    const active = activePage === item.key ? ' active' : '';
    if (!item.sub) return `<a href="${item.href}" class="nav__link${active}">${item.label}</a>`;
    const subLinks = item.sub.map(s => `<a href="${s.href}">${s.label}</a>`).join('');
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

  const menu = document.querySelector('#mainNav .nav__menu');
  if (menu) menu.innerHTML = buildNavMenu(activePage);

  const drawer = document.getElementById('navDrawer');
  if (drawer) drawer.innerHTML = buildDrawer(activePage);

  /* ---- Stable hover: JS timer approach ---- */
  document.querySelectorAll('.nav__item--mega').forEach(item => {
    let closeTimer;

    const openMenu = () => {
      clearTimeout(closeTimer);
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

  document.addEventListener('click', e => {
    if (!e.target.closest('.nav__item--mega')) {
      document.querySelectorAll('.nav__item--mega.mega-open').forEach(item => item.classList.remove('mega-open'));
    }
  });

  window.addEventListener('scroll', () => {
    document.querySelectorAll('.nav__item--mega.mega-open').forEach(item => item.classList.remove('mega-open'));
  }, { passive: true });
});
