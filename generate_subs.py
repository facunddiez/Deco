#!/usr/bin/env python3
"""Generate subcategory and sub-subcategory pages for Casa Mater."""

import os, re

DEST = "/Users/facu/Desktop/Claude/Deco"

# ── product image pools per theme ────────────────────────────────────────────
IMGS = {
    "sofas":     ["1555041469-a586c61ea9bc","1493663284031-b7e3aaa4cab3","1540574163026-43ab29c09c85","1549497538-303791108f90","1586023492125-27b2c045efd7"],
    "sillones":  ["1567538096630-e0c55bd6374c","1555041469-a586c61ea9bc","1484101403633-562f891dc89a","1616046229478-9901c5536a45"],
    "sillas":    ["1549187774-b4e9b0445b41","1533090161767-e6ffed986c88","1567538096630-e0c55bd6374c","1540574163026-43ab29c09c85"],
    "mesas":     ["1530018607912-eff2daa1bac4","1555041469-a586c61ea9bc","1567538096630-e0c55bd6374c","1616046229478-9901c5536a45"],
    "storage":   ["1555041469-a586c61ea9bc","1530018607912-eff2daa1bac4","1484101403633-562f891dc89a","1493663284031-b7e3aaa4cab3"],
    "outdoor":   ["1600210492493-0946911123ea","1555399801-e27a37af4eb8","1506905925346-21bda4d32df4","1558618666-fcd25c85cd64"],
    "lighting":  ["1524484485831-a92ffc0de03f","1565814329452-e1efa11c5b89","1507003211169-0a1dd7228f2d","1519710164239-da123dc03ef4"],
    "textiles":  ["1616046229478-9901c5536a45","1555041469-a586c61ea9bc","1540574163026-43ab29c09c85","1549187774-b4e9b0445b41"],
    "deco":      ["1567538096630-e0c55bd6374c","1524484485831-a92ffc0de03f","1506905925346-21bda4d32df4","1484101403633-562f891dc89a"],
}

def img_url(pool, idx, w=600, q=85):
    imgs = IMGS[pool]
    p = imgs[idx % len(imgs)]
    return f"https://images.unsplash.com/photo-{p}?w={w}&q={q}&auto=format&fit=crop"

def hero_url(pool, w=1600):
    return img_url(pool, 0, w=w, q=80)

# ── page structure definition ─────────────────────────────────────────────────
STRUCTURE = {
    "indoor": {
        "label": "Indoor", "page": "indoor", "hero_pool": "sofas",
        "subs": {
            "asientos": {
                "label": "Asientos", "pool": "sofas",
                "subsubs": {
                    "sofas-2-cuerpos":   {"label": "Sofás 2 cuerpos",    "products": [("Bergamo","Sofá 2 cuerpos","$218.000"),("Oslo","Sofá 2 cuerpos","$196.000"),("Bremen","Sofá 2 cuerpos","$235.000"),("Atenas","Sofá 2 cuerpos","$189.000")]},
                    "sofas-3-cuerpos":   {"label": "Sofás 3 cuerpos",    "products": [("Osaka","Sofá 3 cuerpos","$285.000"),("Nórdica","Sofá 3 cuerpos","$310.000"),("Milán","Sofá 3 cuerpos","$265.000"),("Praga","Sofá 3 cuerpos","$298.000")]},
                    "sofas-chaise":      {"label": "Sofás con chaise",   "products": [("Nápoles","Sofá chaise izq.","$345.000"),("Florencia","Sofá chaise der.","$362.000"),("Lyon","Sofá chaise","$378.000"),("Porto","Sofá chaise","$325.000")]},
                    "sillones":          {"label": "Sillones",           "products": [("Lund","Sillón bouclé","$142.000"),("Viena","Sillón relax","$168.000"),("Berlín","Sillón lectura","$155.000"),("Kyoto","Sillón tapizado","$178.000")]},
                    "poltronas":         {"label": "Poltronas",          "products": [("Havana","Poltrona giratoria","$195.000"),("Padova","Poltrona fija","$178.000"),("Rimini","Poltrona lounge","$210.000"),("Lecce","Poltrona accent","$162.000")]},
                    "sillas-comedor":    {"label": "Sillas de comedor",  "products": [("Arco","Silla tapizada","$52.000"),("Bolonia","Silla rattan","$48.500"),("Copal","Silla madera","$44.000"),("Dover","Silla metal","$38.000")]},
                }
            },
            "mesas": {
                "label": "Mesas", "pool": "mesas",
                "subsubs": {
                    "mesas-comedor":     {"label": "Mesas de comedor",   "products": [("Alpes","Mesa 180cm teca","$285.000"),("Domo","Mesa 160cm roble","$245.000"),("Fenix","Mesa 200cm marmol","$420.000"),("Goya","Mesa 140cm nogal","$198.000")]},
                    "mesas-centro":      {"label": "Mesas de centro",    "products": [("Pebble","Mesa ratán","$82.000"),("Slate","Mesa piedra","$95.000"),("Drift","Mesa madera","$74.000"),("Stone","Mesa marmol","$112.000")]},
                    "mesas-auxiliares":  {"label": "Mesas auxiliares",   "products": [("Nido","Set x2 madera","$56.000"),("Trío","Set x3 metal","$48.000"),("Duo","Set x2 ratán","$42.000"),("Solo","Mesa lateral","$38.000")]},
                    "escritorios":       {"label": "Escritorios",        "products": [("Studi","Escritorio roble 140cm","$195.000"),("Work","Escritorio metal","$178.000"),("Home","Escritorio compacto","$145.000"),("Loft","Escritorio L","$225.000")]},
                    "consolas":          {"label": "Consolas",           "products": [("Arc","Consola hierro","$98.000"),("Bow","Consola ratán","$85.000"),("Curva","Consola madera","$92.000"),("Fina","Consola metal","$78.000")]},
                }
            },
            "almacenamiento": {
                "label": "Almacenamiento", "pool": "storage",
                "subsubs": {
                    "bibliotecas":       {"label": "Bibliotecas",        "products": [("Tomo","Biblioteca 180cm","$285.000"),("Lomo","Biblioteca modular","$345.000"),("Canto","Biblioteca abierta","$265.000"),("Hoja","Biblioteca con puertas","$298.000")]},
                    "aparadores":        {"label": "Aparadores",         "products": [("Sideboard","Aparador 180cm","$385.000"),("Buffet","Aparador 160cm","$345.000"),("Credenza","Aparador nogal","$415.000"),("Base","Aparador bajo","$295.000")]},
                    "comodas":           {"label": "Cómodas",            "products": [("Dama","Cómoda 5 cajones","$245.000"),("Reina","Cómoda 3 cajones","$185.000"),("Alta","Cómoda alta","$265.000"),("Baja","Cómoda baja","$198.000")]},
                    "rack-tv":           {"label": "Rack TV",            "products": [("Screen","Rack 160cm","$195.000"),("Media","Rack 180cm","$215.000"),("Float","Rack flotante","$175.000"),("Low","Rack bajo","$148.000")]},
                    "estantes":          {"label": "Estantes",           "products": [("Shelf","Estante flotante","$48.000"),("Wall","Estante pared","$42.000"),("Cube","Estante cúbico","$38.000"),("Long","Estante largo","$55.000")]},
                }
            },
        }
    },
    "outdoor": {
        "label": "Outdoor", "page": "outdoor", "hero_pool": "outdoor",
        "subs": {
            "asientos-ext": {
                "label": "Asientos", "pool": "outdoor",
                "subsubs": {
                    "sofas-jardin":      {"label": "Sofás de jardín",    "products": [("Caribe","Set sofá jardín","$385.000"),("Trópico","Sofá 3 plazas ext.","$342.000"),("Cala","Sofá modular ext.","$415.000"),("Mar","Sofá 2 plazas ext.","$298.000")]},
                    "sillas-exterior":   {"label": "Sillas de exterior", "products": [("Brisa","Silla apilable","$45.000"),("Costa","Silla con brazo","$58.000"),("Arena","Silla hierro","$52.000"),("Viento","Silla ratán sint.","$48.000")]},
                    "reposeras":         {"label": "Reposeras",          "products": [("Sun","Reposera aluminio","$125.000"),("Bay","Reposera madera","$145.000"),("Pool","Reposera flotante","$98.000"),("Relax","Reposera ajustable","$138.000")]},
                    "hamacas":           {"label": "Hamacas",            "products": [("Rio","Hamaca algodón","$68.000"),("Palma","Hamaca con soporte","$125.000"),("Swing","Hamaca silla","$85.000"),("Bali","Hamaca tejida","$75.000")]},
                    "puffs-exterior":    {"label": "Puffs exterior",     "products": [("Cube","Puff cúbico ext.","$58.000"),("Round","Puff redondo ext.","$52.000"),("Big","Puff grande ext.","$75.000"),("Mini","Puff pequeño ext.","$38.000")]},
                }
            },
            "mesas-ext": {
                "label": "Mesas & Accesorios", "pool": "outdoor",
                "subsubs": {
                    "mesas-jardin":      {"label": "Mesas de jardín",    "products": [("Teak","Mesa teca 180cm","$285.000"),("Ferro","Mesa hierro 160cm","$245.000"),("Cemento","Mesa cemento","$198.000"),("Mix","Mesa aluminio","$215.000")]},
                    "mesas-terraza":     {"label": "Mesas de terraza",   "products": [("Bistró","Mesa bistró","$95.000"),("Café","Mesa café ext.","$85.000"),("Alto","Mesa alta ext.","$115.000"),("Bajo","Mesa baja ext.","$78.000")]},
                    "sombrillas":        {"label": "Sombrillas",         "products": [("Giant","Sombrilla 3m","$145.000"),("Classic","Sombrilla 2.5m","$98.000"),("Tilt","Sombrilla articulada","$125.000"),("Wall","Sombrilla pared","$115.000")]},
                    "parasoles":         {"label": "Parasoles",          "products": [("Vela","Parasol vela triag.","$168.000"),("Rect","Parasol rect. 4x3m","$245.000"),("Cuad","Parasol cuad. 3x3m","$195.000"),("Mini","Parasol pequeño","$85.000")]},
                }
            },
            "ambientacion-ext": {
                "label": "Ambientación", "pool": "outdoor",
                "subsubs": {
                    "macetas-grandes":   {"label": "Macetas grandes",    "products": [("Barrel","Maceta barril","$45.000"),("Tower","Maceta alta","$52.000"),("Bowl","Maceta cuenco","$38.000"),("Cube","Maceta cúbica","$42.000")]},
                    "faroles-exterior":  {"label": "Faroles exterior",   "products": [("Lantern","Farol marroquí","$32.000"),("Pillar","Farol pilar","$45.000"),("Hang","Farol colgante","$38.000"),("Floor","Farol de suelo","$52.000")]},
                    "alfombras-exterior":{"label": "Alfombras exterior", "products": [("Sisal","Alfombra sisal 200x300","$145.000"),("Jute","Alfombra yute","$125.000"),("Poly","Alfombra poliprop.","$95.000"),("Flat","Alfombra plana","$85.000")]},
                    "calefactores":      {"label": "Calefactores",       "products": [("Fire","Calefactor gas","$285.000"),("Eco","Calefactor eléctrico","$195.000"),("Bio","Calefactor bioetanol","$245.000"),("Wall","Calefactor pared","$168.000")]},
                }
            },
        }
    },
    "iluminacion": {
        "label": "Iluminación", "page": "iluminacion", "hero_pool": "lighting",
        "subs": {
            "interior-ilum": {
                "label": "Interior", "pool": "lighting",
                "subsubs": {
                    "colgantes-arana":   {"label": "Colgantes & Araña",  "products": [("Jute","Colgante ratán","$31.500"),("Boule","Araña 5 luces","$85.000"),("Drop","Colgante vidrio","$45.000"),("Nest","Colgante nido","$52.000")]},
                    "lamparas-pie":      {"label": "Lámparas de pie",    "products": [("Arc","Lámpara arco","$98.000"),("Tripod","Lámpara trípode","$85.000"),("Slim","Lámpara lineal","$75.000"),("Drum","Lámpara pantalla","$68.000")]},
                    "lamparas-mesa":     {"label": "Lámparas de mesa",   "products": [("Ceramic","Lámpara cerámica","$42.000"),("Brass","Lámpara latón","$55.000"),("Linen","Lámpara lino","$38.000"),("Stone","Lámpara piedra","$65.000")]},
                    "apliques-pared":    {"label": "Apliques de pared",  "products": [("Wall A","Aplique latón","$28.000"),("Wall B","Aplique negro","$24.000"),("Wall C","Aplique mármol","$38.000"),("Wall D","Aplique madera","$22.000")]},
                    "plafones":          {"label": "Plafones",           "products": [("Round","Plafón redondo","$32.000"),("Square","Plafón cuadrado","$28.000"),("Oval","Plafón oval","$35.000"),("Ring","Plafón aro","$42.000")]},
                }
            },
            "material-ilum": {
                "label": "Por material", "pool": "lighting",
                "subsubs": {
                    "rattan-jute":       {"label": "Rattan & Jute",      "products": [("Boho","Colgante ratán","$38.000"),("Jute L","Colgante yute L","$32.000"),("Basket","Lámpara canasto","$45.000"),("Woven","Aplique tejido","$28.000")]},
                    "metal-hierro":      {"label": "Metal & Hierro",     "products": [("Iron A","Colgante hierro","$52.000"),("Brass B","Colgante latón","$65.000"),("Steel","Lámpara acero","$48.000"),("Copper","Lámpara cobre","$58.000")]},
                    "vidrio-cristal":    {"label": "Vidrio & Cristal",   "products": [("Globe","Colgante globo","$45.000"),("Bell","Colgante campana","$38.000"),("Tube","Colgante tubo","$52.000"),("Dome","Colgante domo","$65.000")]},
                    "ceramica-ilum":     {"label": "Cerámica",           "products": [("Terr","Lámpara terracota","$42.000"),("White","Lámpara cerámica blanca","$38.000"),("Speck","Lámpara salpicada","$48.000"),("Matte","Lámpara mate","$35.000")]},
                    "madera-ilum":       {"label": "Madera",             "products": [("Oak","Colgante roble","$55.000"),("Walnut","Colgante nogal","$68.000"),("Bamboo","Colgante bambú","$45.000"),("Pine","Colgante pino","$38.000")]},
                }
            },
            "exterior-ilum": {
                "label": "Exterior", "pool": "lighting",
                "subsubs": {
                    "faroles-jardin":    {"label": "Faroles jardín",     "products": [("Post","Farol poste","$48.000"),("Solar A","Farol solar A","$32.000"),("Spike","Farol estaca","$28.000"),("Ground","Farol suelo","$38.000")]},
                    "apliques-exterior": {"label": "Apliques exterior",  "products": [("Out A","Aplique IP65","$35.000"),("Out B","Aplique moderno","$42.000"),("Out C","Aplique clásico","$38.000"),("Out D","Aplique minima","$28.000")]},
                    "guirnaldas":        {"label": "Guirnaldas",         "products": [("String","Guirnalda 10m","$28.000"),("Globe","Guirnalda globos","$35.000"),("Edison","Guirnalda Edison","$32.000"),("Solar","Guirnalda solar","$25.000")]},
                    "solar":             {"label": "Solar",              "products": [("Panel","Kit solar jardín","$45.000"),("Spot","Foco solar","$28.000"),("Path","Luz camino solar","$22.000"),("Float","Luz flotante solar","$32.000")]},
                }
            },
        }
    },
    "textiles": {
        "label": "Textiles", "page": "textiles", "hero_pool": "textiles",
        "subs": {
            "alfombras-text": {
                "label": "Alfombras", "pool": "textiles",
                "subsubs": {
                    "shaggy":            {"label": "Shaggy",             "products": [("Shaggy Arena","Alfombra 160x230","$62.400"),("Shaggy Moca","Alfombra 200x300","$98.000"),("Shaggy Crema","Alfombra 80x150","$38.000"),("Shaggy Gris","Alfombra 240x340","$125.000")]},
                    "kilim":             {"label": "Kilim",              "products": [("Kilim Anatolia","200x300","$145.000"),("Kilim Tribal","160x230","$112.000"),("Kilim Mini","80x150","$68.000"),("Kilim Runner","80x250","$75.000")]},
                    "lana-natural":      {"label": "Lana natural",       "products": [("Wool Natural","200x300","$168.000"),("Wool Gris","160x230","$125.000"),("Wool Marfil","240x340","$215.000"),("Wool Camel","80x150","$72.000")]},
                    "yute-sisal":        {"label": "Yute & Sisal",       "products": [("Sisal Natural","200x300","$95.000"),("Yute Herringbone","160x230","$78.000"),("Sisal Borde","200x300","$105.000"),("Yute Natural","80x150","$42.000")]},
                    "alfombras-ext":     {"label": "Exterior",           "products": [("Poly Azul","200x300","$85.000"),("Flat Verde","160x230","$72.000"),("Sisal Ext","200x300","$95.000"),("Geo Gris","120x180","$48.000")]},
                }
            },
            "cama-bano": {
                "label": "Cama & Baño", "pool": "textiles",
                "subsubs": {
                    "ropa-cama":         {"label": "Ropa de cama",       "products": [("Linen Set","Set cama matrimonial","$125.000"),("Cotton Soft","Set cama 2 plazas","$95.000"),("Percal 300","Set cama queen","$145.000"),("Jersey","Sábana ajustable","$42.000")]},
                    "toallas-albornoces":{"label": "Toallas & Albornoces","products": [("Bambú Set","Set toallas x4","$68.000"),("Terry Plus","Toallón","$38.000"),("Robe Linen","Albornoz lino","$95.000"),("Robe Terry","Albornoz felpa","$85.000")]},
                    "almohadones":       {"label": "Almohadones",        "products": [("Linen A","Almohadón 50x50","$18.000"),("Velvet B","Almohadón terciopelo","$22.000"),("Bouclé C","Almohadón bouclé","$25.000"),("Cotton D","Almohadón estampado","$16.000")]},
                    "mantas-throws":     {"label": "Mantas & Throws",    "products": [("Chunky","Manta punto grueso","$68.000"),("Alpaca","Manta alpaca","$125.000"),("Fringed","Manta con flecos","$55.000"),("Sherpa","Manta sherpa","$48.000")]},
                }
            },
            "ventanas": {
                "label": "Ventanas", "pool": "textiles",
                "subsubs": {
                    "cortinas-lino":     {"label": "Cortinas lino",      "products": [("Lino Natural","Par 140x250","$85.000"),("Lino Blanco","Par 140x280","$92.000"),("Lino Gris","Par 160x260","$98.000"),("Lino Crudo","Par 120x240","$75.000")]},
                    "cortinas-blackout": {"label": "Cortinas blackout",  "products": [("Black Natural","Par 140x250","$95.000"),("Black Gris","Par 160x260","$105.000"),("Black Blanco","Par 140x280","$98.000"),("Black Beige","Par 120x240","$85.000")]},
                    "visillos":          {"label": "Visillos",           "products": [("Voile Blanco","Par 140x250","$48.000"),("Voile Crema","Par 160x260","$52.000"),("Organza","Par 140x250","$58.000"),("Lino Fino","Par 120x240","$42.000")]},
                    "estores":           {"label": "Estores",            "products": [("Roller Lino","120cm","$42.000"),("Roller Black","160cm","$52.000"),("Roman Lino","140cm","$75.000"),("Bamboo","90cm","$38.000")]},
                }
            },
        }
    },
    "decoracion": {
        "label": "Decoración", "page": "decoracion", "hero_pool": "deco",
        "subs": {
            "objetos-deco": {
                "label": "Objetos", "pool": "deco",
                "subsubs": {
                    "jarrones-floreros": {"label": "Jarrones & Floreros","products": [("Travertino","Jarrón cerámica","$22.500"),("Ónix","Jarrón mármol","$38.000"),("Soba","Jarrón ratán","$18.000"),("Agata","Florero vidrio","$28.000")]},
                    "espejos":           {"label": "Espejos",            "products": [("Arc Mirror","Espejo arco 80x180","$125.000"),("Round","Espejo redondo 90cm","$98.000"),("Leaner","Espejo recostado","$145.000"),("Wall","Espejo pared 60x90","$75.000")]},
                    "esculturas":        {"label": "Esculturas",         "products": [("Figura A","Escultura cerámica","$28.000"),("Figura B","Escultura mármol","$45.000"),("Figura C","Escultura bronce","$65.000"),("Figura D","Escultura madera","$38.000")]},
                    "relojes":           {"label": "Relojes",            "products": [("Wall Clock","Reloj pared 50cm","$42.000"),("Mantel","Reloj repisa","$38.000"),("Mid Century","Reloj vintage","$55.000"),("Minimal","Reloj minimalista","$35.000")]},
                    "objetos-autor":     {"label": "Objetos de autor",   "products": [("Autor A","Pieza cerámica","$55.000"),("Autor B","Objeto diseño","$75.000"),("Autor C","Pieza bronce","$95.000"),("Autor D","Escultura autor","$125.000")]},
                }
            },
            "arte-pared": {
                "label": "Arte & Pared", "pool": "deco",
                "subsubs": {
                    "cuadros-prints":    {"label": "Cuadros & Prints",   "products": [("Print A","60x80 enmarcado","$38.000"),("Print B","40x50 enmarcado","$25.000"),("Print C","80x100 enmarcado","$55.000"),("Print D","50x70 enmarcado","$32.000")]},
                    "fotografias":       {"label": "Fotografías",        "products": [("Photo A","Foto 60x80","$35.000"),("Photo B","Foto 40x60","$22.000"),("Photo C","Foto 80x100","$48.000"),("Photo D","Foto díptico","$42.000")]},
                    "marcos":            {"label": "Marcos",             "products": [("Marco Oro","Set x3","$28.000"),("Marco Negro","Set x3","$22.000"),("Marco Natural","Set x3","$25.000"),("Marco Mármol","Set x2","$32.000")]},
                    "tapices":           {"label": "Tapices",            "products": [("Tapiz A","120x160 lana","$85.000"),("Tapiz B","100x140 algodón","$65.000"),("Tapiz C","80x120 macramé","$75.000"),("Tapiz D","150x200 tejido","$125.000")]},
                }
            },
            "ambiente-deco": {
                "label": "Ambiente", "pool": "deco",
                "subsubs": {
                    "velas-difusores":   {"label": "Velas & Difusores",  "products": [("Vela Soja","Set x3 velas","$22.000"),("Difusor Lino","200ml","$28.000"),("Palo Santo","Set incienso","$18.000"),("Room Spray","Ambiental","$24.000")]},
                    "plantas-macetas":   {"label": "Plantas & Macetas",  "products": [("Terr Small","Maceta terracota S","$12.000"),("Terr Large","Maceta terracota L","$22.000"),("Cactus Set","Set suculentas","$18.000"),("Ceramic Pot","Maceta cerámica","$25.000")]},
                    "cestos-organiz":    {"label": "Cestos & Organizadores","products": [("Seagrass L","Cesto L","$32.000"),("Seagrass M","Cesto M","$24.000"),("Storage","Set organizadores","$28.000"),("Tray","Bandeja madera","$18.000")]},
                    "libros-diseno":     {"label": "Libros de diseño",   "products": [("Arch Book","Libro arquitectura","$38.000"),("Deco Book","Libro interiorismo","$32.000"),("Art Book","Libro arte","$28.000"),("Photo Book","Libro fotografía","$35.000")]},
                }
            },
        }
    },
}

# ── HTML helpers ──────────────────────────────────────────────────────────────

NAV_JS_INCLUDE = '<script src="js/nav.js"></script>'

def head(title, page):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Casa Mater</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/main.css" /><link rel="stylesheet" href="css/category.css" />
</head>
<body data-page="{page}">"""

def announce_nav(page_label):
    return f"""<div class="announce-bar" id="announceBar"><div class="announce-bar__inner"><span>Nuevo en <a href="#">{page_label}</a></span><span class="announce-bar__sep">|</span><span>🚚 Envío gratis en compras +$80.000</span></div><button class="announce-bar__close" id="announceClose">✕</button></div>
<nav class="nav scrolled" id="mainNav"><div class="container"><div class="nav__inner">
  <a href="index.html" class="nav__logo">Casa Mater<span>Design &amp; Interiors</span></a>
  <ul class="nav__menu"></ul>
  <div class="nav__actions">
    <button class="btn-icon" aria-label="Buscar"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="btn-icon cart-btn" id="cartToggle" aria-label="Carrito"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg><span class="cart-count" id="cartCount" style="display:none">0</span></button>
    <button class="nav__burger" id="menuToggle" aria-label="Menú"><span></span><span></span><span></span></button>
  </div>
</div></div></nav>
<div class="nav__overlay" id="navOverlay"></div>
<nav class="nav__drawer" id="navDrawer"></nav>"""

def cat_hero(title, hero_img):
    return f"""<div class="cat-hero">
  <img class="cat-hero__bg" src="{hero_img}" alt="{title}" />
  <div class="cat-hero__overlay"></div>
  <h1 class="cat-hero__title">{title}</h1>
</div>"""

def breadcrumb(crumbs):
    parts = []
    for i, (label, href) in enumerate(crumbs):
        if href and i < len(crumbs) - 1:
            parts.append(f"<a href='{href}'>{label}</a><span class='breadcrumb__sep'>/</span>")
        else:
            parts.append(f"<span>{label}</span>")
    return f"<nav class='breadcrumb'>{''.join(parts)}</nav>"

def product_card(name, sub, price, img_url, badge=""):
    badge_html = f'<span class="cat-product__badge badge-new">{badge}</span>' if badge else ""
    price_int = int(price.replace("$","").replace(".","").replace(",",""))
    return f"""<article class="cat-product" data-price="{price_int}">
  <div class="cat-product__media">
    <img class="cat-product__img" src="{img_url}" alt="{name}" loading="lazy" />
    {badge_html}
    <div class="cat-product__actions"><button class="cat-product__quick" data-price="{price_int}">Agregar al carrito</button><button class="cat-product__wish-btn" aria-label="Favorito"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg></button></div>
  </div>
  <div class="cat-product__body">
    <p class="cat-product__name">{name}</p>
    <p class="cat-product__sub">{sub}</p>
    <p class="cat-product__price">{price}</p>
  </div>
</article>"""

def filter_sidebar(cat_key):
    filters = {
        "indoor":      [("Estilo","Escandinavo,Moderno,Industrial,Clásico"),("Material","Tela,Cuero,Madera,Metal"),("Color","Beige,Gris,Negro,Blanco,Terracota"),("Precio","")],
        "outdoor":     [("Material","Aluminio,Ratán,Teca,Hierro,Cemento"),("Tipo","Sofás,Sillas,Mesas,Accesorios"),("Color","Negro,Gris,Blanco,Natural"),("Precio","")],
        "iluminacion": [("Tipo","Colgante,De pie,De mesa,Aplique"),("Material","Ratán,Metal,Vidrio,Cerámica"),("Color","Negro,Dorado,Blanco,Natural"),("Precio","")],
        "textiles":    [("Tipo","Alfombras,Almohadones,Mantas,Cortinas"),("Material","Lana,Algodón,Lino,Yute"),("Color","Natural,Gris,Azul,Terracota"),("Precio","")],
        "decoracion":  [("Categoría","Jarrones,Espejos,Cuadros,Velas"),("Material","Cerámica,Vidrio,Metal,Madera"),("Estilo","Minimalista,Orgánico,Industrial"),("Precio","")],
    }
    groups = filters.get(cat_key, filters["indoor"])
    html = '<aside class="cat-filters">'
    for (title, opts) in groups:
        opts_html = ""
        if opts:
            for o in opts.split(","):
                opts_html += f'<label class="filter-option"><input type="checkbox"> {o}</label>'
        html += f'<div class="filter-group"><button class="filter-group__header">{title} <span class="filter-group__icon">+</span></button><div class="filter-group__body">{opts_html}</div></div>'
    html += '</aside>'
    return html

def toolbar(count):
    return f"""<div class="cat-toolbar">
  <button class="cat-toolbar__left" id="toggleFilters"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="4" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="11" y1="18" x2="13" y2="18"/></svg><span class="toggle-label">Ocultar Filtros</span></button>
  <div class="cat-toolbar__right">
    <span class="cat-toolbar__count">Mostrando <strong>{count}</strong> de <strong>{count}</strong> resultados.</span>
    <div class="cat-toolbar__views"><span style="font-size:.68rem;color:var(--text-muted)">Vista:</span><button class="view-btn active" data-view="3"><svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><rect x="0" y="0" width="4" height="4"/><rect x="6" y="0" width="4" height="4"/><rect x="12" y="0" width="4" height="4"/><rect x="0" y="6" width="4" height="4"/><rect x="6" y="6" width="4" height="4"/><rect x="12" y="6" width="4" height="4"/></svg></button><button class="view-btn" data-view="4"><svg width="14" height="14" viewBox="0 0 18 18" fill="currentColor"><rect x="0" y="0" width="3" height="3"/><rect x="5" y="0" width="3" height="3"/><rect x="10" y="0" width="3" height="3"/><rect x="15" y="0" width="3" height="3"/><rect x="0" y="5" width="3" height="3"/><rect x="5" y="5" width="3" height="3"/><rect x="10" y="5" width="3" height="3"/><rect x="15" y="5" width="3" height="3"/></svg></button></div>
    <div class="cat-toolbar__sort"><span>Ordenar por:</span><select class="sort-select"><option>Más Nuevo</option><option>Precio: menor a mayor</option><option>Precio: mayor a menor</option></select></div>
  </div>
</div>"""

def scripts():
    return """<a href="https://wa.me/5491100000000?text=Hola%20Casa%20Mater!" class="whatsapp-btn" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg><span class="whatsapp-btn__tooltip">¿Necesitás ayuda?</span></a>
<aside class="cart-sidebar" id="cartSidebar"><div class="cart-sidebar__header"><h4>Tu Carrito</h4><button class="btn-icon" id="cartClose"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button></div><div class="cart-sidebar__body" id="cartBody"><div class="cart-empty" id="cartEmpty"><p>Tu carrito está vacío.</p></div></div><div class="cart-sidebar__footer" id="cartFooter" style="display:none"><div class="cart-sidebar__subtotal"><span>Subtotal</span><span class="amount" id="cartTotal">$0</span></div><a href="#" class="btn btn-primary" style="width:100%;justify-content:center;padding:16px;">Finalizar compra</a></div></aside>
<div class="nav__overlay" id="cartOverlay" style="z-index:1099"></div>
<div class="toast" id="toast"><span id="toastMsg">Producto agregado al carrito</span></div>
<script src="js/nav.js"></script><script src="js/main.js"></script><script src="js/category.js"></script>
</body></html>"""

# ── page generators ───────────────────────────────────────────────────────────

def gen_subcategory_page(cat_key, cat, sub_key, sub):
    """Category-group page: e.g. outdoor-asientos.html showing all subsub links + products."""
    page_slug = f"{cat_key}-{sub_key}"
    filename = f"{page_slug}.html"
    page_id = cat["page"]
    label = sub["label"]
    cat_label = cat["label"]
    pool = sub["pool"]

    crumbs = [("Home","index.html"),(cat_label, f"{cat_key}.html"),(label, None)]

    # Build sections: one per subsub
    sections_html = ""
    for ss_key, ss in sub["subsubs"].items():
        ss_label = ss["label"]
        ss_href = f"{cat_key}-{ss_key}.html"
        products_html = ""
        for i, (name, subname, price) in enumerate(ss["products"]):
            products_html += product_card(name, subname, price, img_url(pool, i), "Nuevo" if i == 0 else "")
        sections_html += f"""<section class="cat-section">
  <div class="cat-section__header"><h2 class="cat-section__title"><a href="{ss_href}" style="color:inherit;text-decoration:none">{ss_label}</a></h2><span class="cat-section__count">{len(ss["products"])} productos</span></div>
  <div class="cat-products-grid">{products_html}</div>
</section>"""

    total = sum(len(ss["products"]) for ss in sub["subsubs"].values())

    html = head(f"{label} {cat_label}", page_id)
    html += announce_nav(label)
    html += cat_hero(f"{label} — {cat_label}", hero_url(pool))
    html += f"""<div class="cat-page"><div class="container">
  <div class="cat-breadcrumb-bar">{breadcrumb(crumbs)}</div>
  {toolbar(total)}
  <div class="cat-layout">
    {filter_sidebar(cat_key)}
    <main class="cat-main">{sections_html}</main>
  </div>
</div></div>"""
    html += scripts()
    return filename, html


def gen_subsubcategory_page(cat_key, cat, sub_key, sub, ss_key, ss):
    """Specific product type page: e.g. outdoor-sofas-jardin.html"""
    page_slug = f"{cat_key}-{ss_key}"
    filename = f"{page_slug}.html"
    page_id = cat["page"]
    label = ss["label"]
    cat_label = cat["label"]
    sub_label = sub["label"]
    pool = sub["pool"]

    crumbs = [
        ("Home","index.html"),
        (cat_label, f"{cat_key}.html"),
        (sub_label, f"{cat_key}-{sub_key}.html"),
        (label, None)
    ]

    products_html = ""
    for i, (name, subname, price) in enumerate(ss["products"]):
        products_html += product_card(name, subname, price, img_url(pool, i), "Nuevo" if i == 0 else "")

    sections_html = f"""<section class="cat-section">
  <div class="cat-section__header"><h2 class="cat-section__title">{label}</h2><span class="cat-section__count">{len(ss["products"])} productos</span></div>
  <div class="cat-products-grid">{products_html}</div>
</section>"""

    html = head(f"{label} — {cat_label}", page_id)
    html += announce_nav(label)
    html += cat_hero(label, hero_url(pool))
    html += f"""<div class="cat-page"><div class="container">
  <div class="cat-breadcrumb-bar">{breadcrumb(crumbs)}</div>
  {toolbar(len(ss["products"]))}
  <div class="cat-layout">
    {filter_sidebar(cat_key)}
    <main class="cat-main">{sections_html}</main>
  </div>
</div></div>"""
    html += scripts()
    return filename, html


# ── main ─────────────────────────────────────────────────────────────────────

pages_created = []

for cat_key, cat in STRUCTURE.items():
    for sub_key, sub in cat["subs"].items():
        # subcategory page
        fname, html = gen_subcategory_page(cat_key, cat, sub_key, sub)
        with open(os.path.join(DEST, fname), "w", encoding="utf-8") as f:
            f.write(html)
        pages_created.append(fname)

        # sub-subcategory pages
        for ss_key, ss in sub["subsubs"].items():
            fname, html = gen_subsubcategory_page(cat_key, cat, sub_key, sub, ss_key, ss)
            with open(os.path.join(DEST, fname), "w", encoding="utf-8") as f:
                f.write(html)
            pages_created.append(fname)

print(f"Created {len(pages_created)} pages:")
for p in sorted(pages_created):
    print(f"  {p}")
