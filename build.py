#!/usr/bin/env python3
"""
Generador del sitio judasaca.art

Todo el contenido vive aqui arriba, en OBRAS, EXPOS y PRENSA. Se corre
`python3 build.py` y se reescriben los seis HTML. La ventaja de tenerlo asi
es que la barra, el pie y las etiquetas de Google quedan identicas en todas
las paginas: no hay forma de que una quede desactualizada.

Para marcar una obra como vendida: pon vendida=True. Toda obra que no este
vendida lleva boton de compra; el precio lo decide el Worker, no esta pagina.
"""
import os, re, html

RUTA = os.path.dirname(os.path.abspath(__file__))
SITIO = 'https://judasaca.art'
CORREO = 'contact@judasaca.art'
IG = 'https://www.instagram.com/judasaca'

# ── pagos con Bold ───────────────────────────────────────────────────────
# La llave de IDENTIDAD es publica y va en el HTML: solo dice a que comercio
# pertenece el cobro. La llave SECRETA no esta aqui ni en este repositorio,
# vive como secreto del Worker de Cloudflare.
LLAVE_IDENTIDAD = '2heS56eZeRZj1n1B8NDPF9_LA2aDpNbyNBJOoG65qWI'
FIRMADOR = 'https://judasaca-bold.judasaca-art.workers.dev'

# Tope de tarjeta de Bold: 5.000.000 COP. A la TRM que usa el dossier (3.361,62)
# son unos 1.487 dolares.
#
# YA NO ESCONDE NINGUN BOTON. Por decision de Juan, toda obra que no este
# vendida se puede comprar de una.
#
# Comprobado el 25/08/2026: pasarse del tope NO da el error BTN-002. Bold
# muestra una pantalla distinta que dice "monto maximo excedido". Asi que el
# tope no era la causa de la falla que vimos, y este numero queda solo como
# dato: subirlo se pide a soporte.online@bold.co.
TOPE_TARJETA_USD = 1487

# ── formulario de contacto ───────────────────────────────────────────────
# Un sitio estatico no puede mandar correo por si solo: no hay servidor detras.
# Web3Forms recibe el envio y lo reenvia a CORREO. Se saca la llave en
# web3forms.com poniendo contact@judasaca.art, llega por correo, y se pega aqui.
# Mientras diga PEGA-AQUI, el formulario no envia nada.
LLAVE_FORM = '511aafa4-63bd-453c-a671-8825c5104c7a'
REEL = 'https://www.instagram.com/reel/DXqQrk9l-U-/'

# ── las obras ────────────────────────────────────────────────────────────
# El campo 'buy' quedo de la epoca de Stripe y ya no se usa: hoy el cobro lo
# arma el Worker a partir del slug. vendida=True es lo unico que apaga la venta.
OBRAS = [
 dict(slug='oil-city-woodstock',   titulo='Oil City Woodstock',
      tec='Acrylics and oil stick on canvas', med='100 × 100 cm', usd=1950, buy='', vendida=False),
 dict(slug='sunday-snoops',        titulo='Sunday, Snoops',
      tec='Acrylics and spray on canvas',     med='100 × 100 cm', usd=1950, buy='', vendida=False),
 dict(slug='pop-art-rat',          titulo='Pop Art Rat',
      tec='Acrylics and oil stick on canvas', med='100 × 100 cm', usd=1950, buy='', vendida=True),
 dict(slug='mango-og',             titulo='Mango OG',
      tec='Acrylics and oil stick on canvas', med='100 × 100 cm', usd=1950, buy='', vendida=False),
 dict(slug='original-pastel-disney', titulo='Original Pastel Disney',
      tec='Acrylics and spray on canvas',     med='100 × 100 cm', usd=1950, buy='', vendida=False),
 dict(slug='nothing-stays-the-same', titulo='Nothing Stays the Same',
      tec='Oil on canvas',                    med='100 × 120 cm', usd=1950, buy='', vendida=True),
 # recorte=True: la obra es redonda y su foto no es cuadrada, asi que dentro del
 # marco cuadrado quedaba flotando con franjas arriba y abajo. Con recorte llena
 # el marco y se le quita lo que sobra por arriba y por abajo.
 dict(slug='blue-thoughts-rat',    titulo='Blue Thoughts Rat',
      tec='Acrylics and spray on canvas',     med='80 cm diameter', usd=1235, buy='',
      vendida=False, recorte=True),
 dict(slug='smiling-ratsquiat-blue-crown', titulo='Smiling Ratsquiat, Blue Crown',
      tec='Acrylics and spray on canvas',     med='50 × 50 cm', usd=975, buy='', vendida=False),
 dict(slug='smiling-ratsquiat-yellow-crown', titulo='Smiling Ratsquiat, Yellow Crown',
      tec='Acrylics and spray on canvas',     med='50 × 50 cm', usd=975, buy='', vendida=False),
 dict(slug='oil-woodstock',        titulo='Oil Woodstock',
      tec='Acrylics and oil on canvas',       med='50 × 50 cm', usd=975, buy='', vendida=False),
 dict(slug='here-love',            titulo='Here, Love',
      tec='Acrylics and spray on canvas',     med='50 × 50 cm', usd=975, buy='', vendida=True),
 dict(slug='cloud-city-snoops',    titulo='Cloud City Snoops',
      tec='Oil on canvas',                    med='50 × 50 cm', usd=1000, buy='', vendida=False),
 dict(slug='new-york-street-snoops', titulo='New York Street Snoops',
      tec='Acrylics and spray on canvas',     med='50 × 50 cm', usd=975, buy='', vendida=False),
 dict(slug='city-rounds-icon',     titulo='City Rounds Icon',
      tec='Oil on canvas',                    med='50 × 50 cm', usd=1000, buy='', vendida=False),
]

# ── exposiciones ─────────────────────────────────────────────────────────
EXPOS = [
 ('2026', [('OKUPA Art Expo', 'Museo Casa Lleras, Universidad Jorge Tadeo Lozano · Bogotá', ''),
           ('NFT NYC · Speaker', 'New York City, USA', '')]),
 ('2025', [('JUTTA Gallery', 'New York City, USA', ''),
           ('BRANDALISM · Solo exhibition', 'Bogotá, Colombia', ''),
           ('NFT NYC · Speaker', 'New York City, USA', '')]),
 ('2024', [('NFT NYC · Featured Artist', 'New York City, USA', ''),
           ('NFT NYC · Speaker', 'New York City, USA', ''),
           ('Miami Art Week · Public murals and exhibitions', 'Miami, USA', ''),
           ('Oculus Center Fall Exhibition', 'New York City, USA', ''),
           ('Street Art Expo', 'OBJKT digital exhibition', ''),
           ('Ordinals Meet Up', 'Mexico City, Mexico', ''),
           ('SoyArte PLAY', 'Bogotá, Colombia', '')]),
 ('2023', [('5th Colombian Art Salon', 'Tokyo, Japan', ''),
           ('UNGA78 Latine Art Exhibition', 'New York City, USA', ''),
           ('NFT NYC', 'New York City, USA', ''),
           ('BlockDown Festival', 'Algarve, Portugal', ''),
           ('Blockchain Jungle · ChromaVerse Jungle', 'Costa Rica', ''),
           ('One Love Art Festival · Miami Art Week', 'Miami, USA', ''),
           ('Chromaflora · Hybrid Art Exhibition', 'Lisbon, Portugal', ''),
           ('BlockchainCon', 'Lima, Peru', 'Dynamic Artwork Award'),
           ('Artsies Collective Digital Exhibition', 'Barcelona, Spain', ''),
           ('Artsies Collective Digital Exhibition', 'Portugal', '')]),
 ('2022', [('Bogotá NFT Art Expo', 'Bogotá, Colombia', ''),
           ('LG Electronics × Zientte NFT Exhibition', 'Bogotá, Colombia', ''),
           ('Blockchain Summit Latam', 'Bogotá, Colombia', ''),
           ('Arte y Tecnología', 'Centro Comercial Avenida Chile · Bogotá', ''),
           ('ARTRADE × KARE', 'Bogotá, Colombia', '')]),
 ('2021', [('We Art Colombia', 'Bogotá, Colombia', ''),
           ('We Art Colombia', 'Miami, USA', ''),
           ('Art PRBLMS 2', 'Bogotá, Colombia', ''),
           ('Open San Felipe', 'Bogotá, Colombia', '')]),
]

PRENSA = [
 ('El Espectador', 'Judasaca presenta ‘Brandalism’, arte que cuestiona el poder de las marcas',
  'https://www.elespectador.com/especiales/judasaca-presenta-brandalism-arte-que-cuestiona-el-poder-de-las-marcas/'),
 ('ColombiaOne', 'Judasaca: Colombian Artist Reimagines Pop Culture with Tech, Color, and NFTs',
  'https://colombiaone.com/2025/10/18/judasaca-colombian-artist-nfts/'),
 ('Universidad Jorge Tadeo Lozano', 'Street art y realidad aumentada se toman el Museo Biblioteca Carlos Lleras Restrepo',
  'https://www.utadeo.edu.co/es/eventos/street-art-y-realidad-aumentada-se-toman-el-museo-biblioteca-carlos-lleras-restrepo-con-la'),
 ('Plaza Capital', 'El arte digital, una apuesta por la innovación',
  'https://plazacapital.co/innovacion/7273-el-arte-digital-una-apuesta-por-la-innovacion'),
]

PAISES = {'Colombia':'Colombia', 'USA':'United States', 'Japan':'Japan',
          'Portugal':'Portugal', 'Costa Rica':'Costa Rica', 'Peru':'Peru',
          'Spain':'Spain', 'Mexico':'Mexico'}

def cuenta():
    n = sum(len(i) for _, i in EXPOS)
    paises = set()
    for _, items in EXPOS:
        for _, lugar, _ in items:
            for clave in PAISES:
                if clave in lugar:
                    paises.add(clave)
    # Bogota y Miami aparecen sin pais en algunas lineas
    if any('Bogotá' in l for _, its in EXPOS for _, l, _ in its): paises.add('Colombia')
    if any('Miami' in l for _, its in EXPOS for _, l, _ in its): paises.add('USA')
    anios = [int(a) for a, _ in EXPOS]
    return n, len(paises), min(anios)

N_EXPOS, N_PAISES, ANIO_0 = cuenta()

PAGINAS = [('index.html', 'Home'), ('about.html', 'About'), ('art.html', 'Art'),
           ('shop.html', 'Shop'), ('cv.html', 'CV'), ('contact.html', 'Contact')]


def nav(activa):
    ls = []
    for arch, nom in PAGINAS:
        if nom == 'Home':
            continue
        on = ' class="on"' if arch == activa else ''
        ls.append(f'<a href="{arch}"{on}>{nom}</a>')
    return '\n      '.join(ls)


def cabeza(titulo, desc, activa, og='img/oil-city-woodstock-sm.webp'):
    canon = SITIO + ('/' if activa == 'index.html' else '/' + activa)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="JUDASACA">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITIO}/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/judasaca-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<header>
  <div class="barra">
    <button class="trazo" id="abrir-menu" aria-label="Menu" aria-expanded="false">
      <svg viewBox="0 0 30 22" aria-hidden="true" width="21" height="15">
        <path d="M2.4 4.1c6.1-1.2 15.7-1.5 25.2.3"/>
        <path d="M3.1 11c7.6-.9 14.9-.7 23.8.4"/>
        <path d="M2.7 17.9c5.3-1.3 14.4-1.4 24.6.2"/>
      </svg>
    </button>
    <a class="marca" href="index.html" aria-label="JUDASACA, home">
      <img src="img/judasaca-logo.png" alt="JUDASACA" width="900" height="673">
    </a>
    <button class="carro" id="carro" aria-label="Cart">
      <svg viewBox="0 0 24 24" aria-hidden="true" width="16" height="16"><circle cx="9" cy="20" r="1.3"/><circle cx="18" cy="20" r="1.3"/><path d="M1 2h3.4l2.6 12.4h11.6L22 6H6"/></svg>
      <span class="n" id="carro-n">0</span>
    </button>
  </div>
</header>

<aside class="menu-panel" id="menu-panel" aria-label="Menu" aria-hidden="true">
  <button class="x" id="cerrar-menu" aria-label="Close">&times;</button>
  <nav id="nav">
      {nav(activa)}
  </nav>
  <div class="abajo">
    Bogotá, Colombia<br>
    <a href="mailto:{CORREO}">{CORREO}</a><br>
    <a href="{IG}" rel="noopener">@judasaca</a>
  </div>
</aside>
'''


import json
# Las vendidas quedan fuera del catalogo del carrito. Asi, si alguien tenia una
# guardada en su navegador de antes, desaparece sola la proxima vez que entre.
CATALOGO = json.dumps({o['slug']: {'t': o['titulo'], 'm': o['med'], 'usd': o['usd']}
                       for o in OBRAS if not o['vendida']}, ensure_ascii=False)

DISPONIBLES = sum(1 for o in OBRAS if not o['vendida'])

PIE = f'''
<footer>
  <div class="wrap pie">
    <div class="col"><b>Artwork</b>
      <a href="art.html">Original works</a>
      <a href="shop.html">Shop</a>
      <a href="cv.html">CV</a>
    </div>
    <div class="col"><b>Studio</b>
      <a href="about.html">About the artist</a>
      <a href="contact.html">Contact</a>
      <a href="mailto:{CORREO}">{CORREO}</a>
    </div>
    <div class="col"><b>Follow</b>
      <a href="{IG}" rel="noopener">Instagram · @judasaca</a>
    </div>
    <div class="col fin">JUDASACA · Juan Salazar<br>Bogotá, Colombia<br>
      <span style="opacity:.7">nothing stays the same</span>
      <!-- Dice solo lo que es verdad. El pago ocurre dentro de la pasarela de
           Bold, no en esta pagina, asi que el numero de la tarjeta no pasa por
           aqui ni queda en ningun sitio nuestro. No se reclama ninguna
           certificacion que no tengamos. -->
      <span class="seguro">Payments are processed by Bold.<br>
        Card details are entered on Bold's gateway and never pass through this site.<br>
        <a href="privacy.html">Privacy</a></span></div>
  </div>
</footer>

<div class="velo" id="velo"></div>
<aside class="panel" id="panel" aria-label="Cart" aria-hidden="true">
  <div class="alto"><h2>Selected works</h2><button class="x" id="cerrar-carro" aria-label="Close">&times;</button></div>
  <div class="lista" id="carro-lista"></div>
  <div class="bajo">
    <div class="total"><span>Total</span><span id="carro-total">USD 0</span></div>
    <div class="pagar-carro" id="carro-pagar"></div>
    <button class="btn lleno" id="carro-pedir" type="button">Checkout</button>
    <p class="nota" id="carro-nota">Payment opens on Bold's gateway. Card details are
      entered there and never pass through this site. We ask where to ship afterwards.</p>
  </div>
</aside>

<div class="lupa" id="lupa" role="dialog" aria-modal="true" aria-label="Artwork">
  <button class="cerrar" aria-label="Close">&times;</button>
  <button class="pasar ant" aria-label="Previous">&#8249;</button>
  <button class="pasar sig" aria-label="Next">&#8250;</button>
  <figure><img id="lupa-img" alt=""><figcaption id="lupa-pie"></figcaption></figure>
</div>

<script>
/* Menu de celular y lupa de obras. Si el JavaScript falla, los enlaces de las
   obras siguen abriendo la imagen grande por su cuenta. */
(function(){{
  var b=document.getElementById('abrir-menu'), p=document.getElementById('menu-panel'),
      v=document.getElementById('velo'), x=document.getElementById('cerrar-menu');
  if(!b||!p) return;
  function abrir(){{ p.classList.add('abierto'); v.classList.add('abierto');
    p.setAttribute('aria-hidden','false'); b.setAttribute('aria-expanded','true');
    document.body.style.overflow='hidden'; x.focus(); }}
  function cerrar(){{ p.classList.remove('abierto'); v.classList.remove('abierto');
    p.setAttribute('aria-hidden','true'); b.setAttribute('aria-expanded','false');
    document.body.style.overflow=''; b.focus(); }}
  b.addEventListener('click', abrir);
  x.addEventListener('click', cerrar);
  v.addEventListener('click', cerrar);
  document.addEventListener('keydown', function(e){{
    if(e.key==='Escape' && p.classList.contains('abierto')) cerrar(); }});
}})();

(function(){{
  var enlaces=[].slice.call(document.querySelectorAll('[data-lupa]'));
  if(!enlaces.length) return;
  var caja=document.getElementById('lupa'), img=document.getElementById('lupa-img'),
      pie=document.getElementById('lupa-pie'), i=0, antes=null;

  function mostrar(n){{
    i=(n+enlaces.length)%enlaces.length;
    var a=enlaces[i];
    img.src=a.getAttribute('href');
    img.alt=a.getAttribute('data-tit');
    pie.textContent=a.getAttribute('data-tit')+' · '+a.getAttribute('data-fic');
  }}
  function abrir(n,orig){{
    antes=orig; mostrar(n);
    caja.classList.add('viendo');
    document.body.style.overflow='hidden';
    caja.querySelector('.cerrar').focus();
  }}
  function cerrar(){{
    caja.classList.remove('viendo');
    document.body.style.overflow='';
    if(antes) antes.focus();
  }}
  enlaces.forEach(function(a,n){{
    a.addEventListener('click',function(e){{ e.preventDefault(); abrir(n,a); }});
  }});
  caja.querySelector('.cerrar').addEventListener('click',cerrar);
  caja.querySelector('.ant').addEventListener('click',function(){{ mostrar(i-1); }});
  caja.querySelector('.sig').addEventListener('click',function(){{ mostrar(i+1); }});
  caja.addEventListener('click',function(e){{ if(e.target===caja) cerrar(); }});
  document.addEventListener('keydown',function(e){{
    if(!caja.classList.contains('viendo')) return;
    if(e.key==='Escape') cerrar();
    if(e.key==='ArrowLeft') mostrar(i-1);
    if(e.key==='ArrowRight') mostrar(i+1);
  }});
}})();

/* ── Carrito ──────────────────────────────────────────────────────────
   Guarda lo elegido en el propio navegador y arma un correo con la lista.
   No cobra nada todavia: cuando existan los enlaces de pago de Stripe,
   este mismo carrito puede mandar al checkout. */
(function(){{
  var CAT = {CATALOGO};
  var LLAVE='judasaca-carro';
  var carro=[];
  try{{ carro=JSON.parse(localStorage.getItem(LLAVE)||'[]'); }}catch(e){{ carro=[]; }}
  carro = carro.filter(function(s){{ return CAT[s]; }});

  var bot=document.getElementById('carro'), num=document.getElementById('carro-n'),
      panel=document.getElementById('panel'), velo=document.getElementById('velo'),
      lista=document.getElementById('carro-lista'), total=document.getElementById('carro-total'),
      pedir=document.getElementById('carro-pedir'), nota=document.getElementById('carro-nota');
  if(!bot||!panel) return;

  function guardar(){{ try{{ localStorage.setItem(LLAVE, JSON.stringify(carro)); }}catch(e){{}} }}
  function dinero(n){{ return 'USD ' + n.toLocaleString('en-US'); }}

  function pintar(){{
    num.textContent = carro.length;
    if(!carro.length){{
      lista.innerHTML = '<p class="vacio">Nothing selected yet.</p>';
      total.textContent = dinero(0);
      pedir.disabled = true;
      return;
    }}
    pedir.disabled = false;
    var suma = 0, h = '';
    carro.forEach(function(sl){{
      var o = CAT[sl]; suma += o.usd;
      h += '<div class="item"><img src="img/'+sl+'-sm.webp" alt="">'
        +  '<div class="d"><div class="t">'+o.t+'</div>'
        +  '<div class="f">'+o.m+'</div>'
        +  '<div class="p">'+dinero(o.usd)+'</div>'
        +  '<button class="quitar" data-q="'+sl+'">Remove</button></div></div>';
    }});
    lista.innerHTML = h;
    total.textContent = dinero(suma);
  }}

  /* Checkout de verdad: el carrito cobra, no manda un correo. Se firma la
     lista contra el Worker (que suma el total y decide el precio) y se abre
     Bold por el total, en una sola orden. */
  function cobrar(){{
    if (!carro.length || !window.fetch || !window.JUDPAGO) return;
    pedir.disabled = true;
    pedir.textContent = 'One moment…';

    fetch('{FIRMADOR}/firma', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ modo: 'carro', slugs: carro }})
    }})
    .then(function(r){{ return r.json(); }})
    .then(function(d){{
      if (!d || !d.carro) throw new Error('sin-orden');

      // Si algo se vendio mientras el comprador miraba, el Worker lo deja
      // fuera de la firma. Se le dice, se le quita del carrito y se cobra lo
      // que si esta: nadie paga por un cuadro que ya no existe.
      var firmadas = d.carro.slugs || [];
      var caidas = carro.filter(function(s){{ return firmadas.indexOf(s) < 0; }});
      if (caidas.length) {{
        carro = firmadas.slice();
        guardar(); pintar();
        nota.textContent = caidas.length === 1
          ? CAT[caidas[0]].t + ' was just sold and has been removed. Paying for the rest.'
          : caidas.length + ' works were just sold and have been removed. Paying for the rest.';
        nota.className = 'nota aviso';
      }}

      pedir.style.display = 'none';
      window.JUDPAGO.abrir(document.getElementById('carro-pagar'), d.carro, location.href);
    }})
    .catch(function(){{
      pedir.disabled = false;
      pedir.textContent = 'Checkout';
      nota.className = 'nota aviso';
      nota.innerHTML = 'Checkout is not responding. Write to '
        + '<a href="mailto:{CORREO}">{CORREO}</a> and Juan will take it from there.';
    }});
  }}

  function abrir(){{ panel.classList.add('abierto'); velo.classList.add('abierto');
    panel.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }}
  function cerrar(){{ panel.classList.remove('abierto'); velo.classList.remove('abierto');
    panel.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }}

  bot.addEventListener('click', function(){{ pintar(); abrir(); }});
  pedir.addEventListener('click', cobrar);
  velo.addEventListener('click', cerrar);
  document.getElementById('cerrar-carro').addEventListener('click', cerrar);
  document.addEventListener('keydown', function(e){{
    if(e.key==='Escape' && panel.classList.contains('abierto')) cerrar(); }});

  lista.addEventListener('click', function(e){{
    var q=e.target.getAttribute && e.target.getAttribute('data-q');
    if(!q) return;
    carro = carro.filter(function(s){{ return s!==q; }});
    guardar(); pintar();
  }});

  document.querySelectorAll('.add').forEach(function(b){{
    b.addEventListener('click', function(){{
      var sl=b.getAttribute('data-slug');
      if(carro.indexOf(sl)<0) carro.push(sl);
      guardar(); pintar(); abrir();
    }});
  }});

  pintar();
}})();

/* ── Pago ───────────────────────────────────────────────────────────────
   Un solo motor de pago para toda la pagina: lo usan los botones Buy de cada
   obra y tambien el carrito.

   Flujo, corto a proposito: clic en Buy -> la pasarela de Bold se abre encima
   del sitio -> paga. Nada de formularios antes. La direccion de envio se pide
   DESPUES, en la pagina de gracias, cuando la plata ya entro y el comprador
   no puede arrepentirse a mitad de camino por tener que teclear.

   El navegador NUNCA manda el precio: manda slugs, y el Worker decide cuanto
   se cobra y lo firma. Un precio que mande el atacante no vale nada aunque
   venga firmado, porque estaria firmando su propia mentira. */
window.JUDPAGO = (function(){{
  var libreria = null, abriendo = false;

  /* Devuelve una promesa que solo se cumple cuando la libreria esta lista de
     verdad. Se guarda para que dos clics no la carguen dos veces. */
  function cargarLibreria(){{
    if (libreria) return libreria;
    libreria = new Promise(function(ok, mal){{
      if (window.BoldCheckout) return ok();
      var s = document.createElement('script');
      s.src = 'https://checkout.bold.co/library/boldPaymentButton.js';
      s.onload = function(){{ window.BoldCheckout ? ok() : mal(); }};
      s.onerror = mal;
      document.head.appendChild(s);
    }});
    return libreria;
  }}

  /* Se recuerda la orden para que la pagina de gracias sepa que se acaba de
     pagar: ahi se le pide la direccion y se marcan las obras como vendidas. */
  function recordar(orden){{
    try {{
      localStorage.setItem('judasaca-orden', JSON.stringify({{
        id: orden.orderId,
        slugs: orden.slugs || [],
        amount: orden.amount,
        description: orden.description,
        t: Date.now()
      }}));
    }} catch(e) {{}}
  }}

  /* Abre la pasarela directamente, sin dibujar ningun boton de Bold.

     Antes esto inyectaba un <script data-bold-button> y luego le hacia clic
     solo. Eso era una carrera perdida: la libreria de Bold busca esos scripts
     cuando ELLA carga, asi que segun quien llegara primero unas veces salia el
     boton y otras veces no salia nada. Con la API (new BoldCheckout().open())
     no hay nada que esperar ni nada que adivinar: se abre y ya. */
  function abrir(destino, orden, origen){{
    if (abriendo) return;
    abriendo = true;
    recordar(orden);

    cargarLibreria().then(function(){{
      new window.BoldCheckout({{
        orderId: orden.orderId,
        currency: orden.currency,
        amount: orden.amount,
        apiKey: '{LLAVE_IDENTIDAD}',
        integritySignature: orden.signature,
        description: orden.description,
        redirectionUrl: '{SITIO}/thanks.html',
        originUrl: origen || '{SITIO}/art.html',
        // Embedded: la pasarela abre encima del sitio y el comprador no se va.
        renderMode: 'embedded'
      }}).open();
      abriendo = false;
    }}).catch(function(){{
      abriendo = false;
      if (destino) {{
        destino.innerHTML = '<span class="fallo">Checkout could not open. '
          + 'Write to <a href="mailto:{CORREO}">{CORREO}</a>.</span>';
      }}
    }});
  }}

  /* Una obra vendida se apaga entera: sello, ficha tachada y sin botones. */
  function marcarVendidas(lista){{
    (lista || []).forEach(function(slug){{
      var hueco = document.querySelector('.pagar[data-obra="' + slug + '"]');
      if (!hueco) return;
      var obra = hueco.closest('.obra');
      if (!obra || obra.classList.contains('agotada')) return;
      obra.classList.add('agotada');
      var marco = obra.querySelector('.marco');
      if (marco && !marco.querySelector('.sello')) {{
        marco.classList.add('vendido');
        var s = document.createElement('span');
        s.className = 'sello';
        s.setAttribute('aria-hidden', 'true');
        s.innerHTML = '<i></i><b>Sold</b><i></i>';
        marco.appendChild(s);
      }}
      var acciones = obra.querySelector('.acciones');
      if (acciones) acciones.innerHTML = '<span class="sello-vendida">Sold</span>';
    }});
  }}

  return {{ abrir: abrir, marcarVendidas: marcarVendidas, firmador: '{FIRMADOR}' }};
}})();

/* ── Buy en cada obra ───────────────────────────────────────────────────
   Solo corre en paginas con huecos .pagar (hoy, la de obras). */
(function(){{
  var huecos = [].slice.call(document.querySelectorAll('.pagar[data-obra]'));
  if (!huecos.length || !window.fetch) return;

  var slugs = huecos.map(function(h){{ return h.getAttribute('data-obra'); }});

  fetch('{FIRMADOR}/firma', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{ slugs: slugs }})
  }})
  .then(function(r){{ return r.json(); }})
  .then(function(d){{
    // El Worker manda la lista real de vendidas. Si una se vendio despues de
    // publicar la pagina, se marca aqui sin tener que reconstruir el sitio.
    if (d && d.vendidas) window.JUDPAGO.marcarVendidas(d.vendidas);
    if (!d || !d.obras) return;

    huecos.forEach(function(hueco){{
      var o = d.obras[hueco.getAttribute('data-obra')];
      if (!o) return;
      o.slugs = [hueco.getAttribute('data-obra')];
      var b = document.createElement('button');
      b.className = 'btn lleno';
      b.textContent = 'Buy';
      b.addEventListener('click', function(){{
        b.disabled = true;
        b.textContent = 'Opening…';
        window.JUDPAGO.abrir(hueco, o, location.href);
      }});
      hueco.appendChild(b);
    }});
  }})
  .catch(function(){{ }});
}})();
</script>
</body>
</html>
'''


def tarjeta_obra(o, mini=True):
    img = f"img/{o['slug']}-sm.webp" if mini else f"img/{o['slug']}.webp"
    # El precio de una obra vendida se sigue mostrando, tachado. Esconderlo
    # obliga a preguntar, y la respuesta ya no le sirve a nadie.
    precio = f'<span class="p">USD {o["usd"]:,}</span>'
    # Hueco donde el JavaScript inserta el boton de Bold una vez el Worker
    # devuelve la firma. Toda obra que no este vendida lo lleva: quien quiere
    # comprar compra, sin pasos de por medio y sin pedir permiso por correo.
    comprar = '' if o['vendida'] else f'<span class="pagar" data-obra="{o["slug"]}"></span>'
    carrito = ('' if o['vendida'] else
               f'<button class="btn add" data-slug="{o["slug"]}">Add to cart</button>')

    # Vendida: se va todo lo que invita a comprar y queda el sello. Dos rayas
    # rojas en diagonal con la palabra en medio, y la ficha en gris tachada.
    if o['vendida']:
        acciones = '<span class="sello-vendida">Sold</span>'
        sello = '<span class="sello" aria-hidden="true"><i></i><b>Sold</b><i></i></span>'
        clase_obra, clase_marco = ' agotada', ' vendido'
    else:
        acciones = f'{comprar}{carrito}'
        sello, clase_obra, clase_marco = '', '', ''

    if o.get('recorte'):
        clase_marco += ' recorte'

    return f'''      <article class="obra{clase_obra}">
        <figure>
          <a class="marco{clase_marco}" href="img/{o['slug']}.webp"
             data-lupa data-tit="{html.escape(o['titulo'])}"
             data-fic="{html.escape(o['tec'])} · {o['med']}">
            <img src="{img}" alt="{html.escape(o['titulo'])}, {html.escape(o['tec'].lower())}, {o['med']}" loading="lazy">{sello}
          </a>
          <figcaption>
            <div class="linea"><span class="t">{html.escape(o['titulo'])}</span>
              <span class="f">· {o['med']} ·</span> {precio}</div>
            <div class="acciones">{acciones}</div>
          </figcaption>
        </figure>
      </article>
'''


def escribir(nombre, cuerpo):
    with open(os.path.join(RUTA, nombre), 'w', encoding='utf-8') as f:
        f.write(cuerpo)
    return len(cuerpo)


# ══════════════════════════════════════════════════════════════════════════
# 1 · HOME
# ══════════════════════════════════════════════════════════════════════════
destacadas = [o for o in OBRAS if o['slug'] in
              ('sunday-snoops', 'nothing-stays-the-same', 'blue-thoughts-rat')]

home = cabeza(
  'JUDASACA · Juan Salazar · Hybrid artist, Bogotá',
  'Colombian hybrid artist working between painting and augmented reality. '
  'Original works, exhibitions and contact.',
  'index.html') + f'''
<main>
  <div class="wrap">
    <div class="hero">
      <h1>nothing stays the same</h1>
    </div>

    <div class="portada-obra">
      <img src="intro_photo.webp"
           alt="Juan Salazar, JUDASACA">
      <div class="pie-obra">Juan Salazar</div>
    </div>

    <div class="entrada-home">
      <p>Juan Salazar paints the characters that raised us, then lets technology pull them
        out of shape. Traditional canvas, augmented reality, and the question of what a
        brand really owns once it has lived inside your childhood.</p>
      <a class="btn" href="art.html">See the work</a>
    </div>
  </div>
</main>
''' + PIE

# ══════════════════════════════════════════════════════════════════════════
# 2 · ABOUT
# ══════════════════════════════════════════════════════════════════════════
prensa_html = '\n'.join(
  f'''        <a href="{u}" rel="noopener">
          <div class="medio">{html.escape(m)}</div>
          <div class="titular">{html.escape(t)}</div>
        </a>''' for m, t, u in PRENSA)

about = cabeza(
  'About · JUDASACA · Juan Salazar',
  'Juan Salazar, known as JUDASACA, is a Colombian hybrid artist working between '
  'traditional painting and augmented reality.',
  'about.html', og='about_photo.webp') + f'''
<main>
  <section>
    <div class="wrap">
      <div class="tit centrado"><div class="eti">About</div><h2>Juan Salazar</h2></div>
      <div class="dos">
        <!-- La foto se queda quieta mientras el texto corre. Es el gesto mas caro
             que se puede hacer sin agregar un solo elemento a la pagina. -->
        <div class="foto">
          <img class="retrato" src="about_photo.webp"
               alt="Juan Salazar painting a mural, Bogotá">
          <figcaption class="pie-foto">Studio, Bogotá</figcaption>
        </div>
        <div class="prosa vida">
          <p class="entrada">JUDASACA is a hybrid artist. He paints on canvas, and then
            <span class="mueve">he lets the painting move.</span></p>

          <p>Juan Salazar spent more than fifteen years in marketing and international
            business before art became the work rather than the thing beside it. His
            artistic career began in 2018, though some collectors trace his earliest
            pieces back to 2014. The turn came during a master's degree in Barcelona,
            where the artists around him made the decision look obvious. He returned to
            Bogotá, found the San Felipe art district, and started showing.</p>

          <p>In 2021 he exhibited internationally for the first time and ran into crypto
            art. His first NFT collection, five editions, sold in under a day. By early
            2023 his work was on the screens of Times Square. Since then it has travelled
            to New York, Miami, Tokyo, Lisbon, Barcelona, Mexico City, Costa Rica and Lima.</p>

          <h3>Brandalism</h3>
          <p>He paints the characters that raised a generation: Snoopy, Woodstock, Mickey.
            He takes them out of the stories they belong to and puts them somewhere less
            comfortable. The work asks what a brand actually owns once it has lived inside
            your childhood, and what is left of you when you notice the icons have aged too.</p>

          <p>The other half is technology. He has spent years building augmented and virtual
            layers over his paintings, so that a fixed canvas becomes something that will not
            hold still. That is the whole argument in one gesture: nothing stays the same. He
            is a member of One Love ArtDAO, co-founder of the
            artist collective The Art Cartel alongside Yuseph Zapata and Lucas Zapata, and
            helped build Chromaverse, a platform for showing work in physical and virtual
            galleries at once.</p>

          <blockquote class="cita">
            “I play with art and technology to create experiences that go beyond the canvas.”
            <cite>Juan Salazar, interviewed by ColombiaOne, October 2025</cite>
          </blockquote>

          <p>He has spoken at NFT NYC in 2024, 2025 and 2026. He lives and works in Bogotá.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="humo">
    <div class="wrap">
      <div class="tit"><div class="eti">Press</div><h2>Written about</h2></div>
      <div class="prensa">
{prensa_html}
      </div>
    </div>
  </section>
</main>
''' + PIE

# ══════════════════════════════════════════════════════════════════════════
# 3 · ART
# ══════════════════════════════════════════════════════════════════════════
art = cabeza(
  'Original works · JUDASACA',
  f'{DISPONIBLES} original paintings by JUDASACA, available now. Acrylics, oil and spray '
  'on canvas. Bogotá, Colombia.',
  'art.html') + f'''
<main>
  <section>
    <div class="wrap">
      <div class="tit">
        <div class="eti">Original works · {DISPONIBLES} available</div>
        <h2>Art</h2>
        <p>Every piece here is a single original, painted by hand and signed. Prices are
          in US dollars. Worldwide shipping and framing is not included.</p>
      </div>
      <div class="obras">
{''.join(tarjeta_obra(o) for o in OBRAS)}      </div>
    </div>
  </section>

  <section class="humo">
    <div class="wrap estrecho prosa">
      <div class="tit"><div class="eti">Buying</div><h2>How it works</h2></div>
      <p>Works ship worldwide from Bogotá. Larger canvases usually travel rolled in a
        tube and are stretched on arrival, which is standard practice and keeps shipping
        sane.</p>

      <!-- Dicho en positivo, pero sin inventar nada. Cada frase de aqui es
           comprobable: el pago ocurre en la pasarela de Bold, el sitio va por
           HTTPS, y el monto se firma antes de salir. No se menciona ninguna
           certificacion que no sea nuestra. -->
      <h3>Paying securely</h3>
      <p>Payments are completed through Bold's payment gateway. We do not keep your card
        details. More on the <a href="privacy.html">privacy page</a>.</p>
    </div>
  </section>
</main>
''' + PIE

# ══════════════════════════════════════════════════════════════════════════
# 4 · SHOP
# ══════════════════════════════════════════════════════════════════════════
shop = cabeza(
  'Shop · JUDASACA',
  'Prints and merchandise by JUDASACA. Coming soon.',
  'shop.html') + f'''
<main>
  <section>
    <div class="wrap">
      <div class="tit">
        <div class="eti">Shop</div>
        <h2>Prints and merch</h2>
        <p>The originals live on the <a href="art.html" style="color:inherit">Art</a> page.
          This is where the affordable end of the work will be.</p>
      </div>
      <div class="pronto">
        <h3>Opening soon</h3>
        <p>Prints, apparel and small editions are being prepared. If you want to know the
          moment it opens, write and you will be told first.</p>
        <p style="margin-top:24px">
          <a class="btn" href="mailto:{CORREO}?subject=Shop%20—%20let%20me%20know%20when%20it%20opens">Tell me when it opens</a>
        </p>
      </div>
    </div>
  </section>
</main>
''' + PIE

# ══════════════════════════════════════════════════════════════════════════
# 5 · CV
# ══════════════════════════════════════════════════════════════════════════
def bloque_anio(anio, items):
    lis = []
    for nombre, lugar, premio in items:
        p = f'<span class="premio">{html.escape(premio)}</span>' if premio else ''
        lis.append(f'          <li><span>{html.escape(nombre)}</span>'
                   f'<span class="lugar">{html.escape(lugar)}</span>{p}</li>')
    return (f'      <div class="anio">\n        <h3>{anio}</h3>\n        <ul>\n'
            + '\n'.join(lis) + '\n        </ul>\n      </div>')

cv = cabeza(
  'CV · JUDASACA · Juan Salazar',
  'Exhibition history of JUDASACA, 2021 to 2026: New York, Miami, Tokyo, Lisbon, '
  'Barcelona, Mexico City, Costa Rica, Lima and Bogotá.',
  'cv.html') + f'''
<main>
  <section>
    <div class="wrap">
      <div class="tit">
        <div class="eti">Curriculum</div>
        <h2>Exhibitions</h2>
        <p>Juan Salazar · JUDASACA · born and based in Bogotá, Colombia.
          Speaker at NFT NYC in 2024, 2025 and 2026.</p>
      </div>
      <div class="cv">
{chr(10).join(bloque_anio(a, its) for a, its in EXPOS)}
      </div>
      <p style="margin-top:34px"><a class="btn" href="contact.html">Request full dossier</a></p>
    </div>
  </section>
</main>
''' + PIE

# ══════════════════════════════════════════════════════════════════════════
# 6 · CONTACT
# ══════════════════════════════════════════════════════════════════════════
contact = cabeza(
  'Contact · JUDASACA',
  'Contact Juan Salazar, JUDASACA. Bogotá, Colombia. Enquiries about original '
  'works, exhibitions and commissions.',
  'contact.html', og='img/nothing-stays-the-same-sm.webp') + f'''
<main>
  <section>
    <div class="wrap estrecho contacto">
      <!-- Una obra y no un retrato: la pagina de contacto es el ultimo sitio donde
           alguien duda, y lo que tiene que ver ahi es el trabajo. -->
      <figure class="obra-contacto">
        <img src="contact_photo.webp" alt="Juan Salazar with a signed print of Smiling Ratsquiat, King Crown">
        <figcaption><span class="t1">Smiling Ratsquiat,</span> <span class="t2">King Crown</span></figcaption>
      </figure>

      <div class="tit">
        <div class="eti">Contact</div>
        <h2>Say something</h2>
        <p>Enquiries about available works, exhibitions, commissions and collaborations
          all reach the same place, and Juan answers them himself.</p>
      </div>

      <form class="forma" id="forma" action="https://api.web3forms.com/submit" method="POST">
        <input type="hidden" name="access_key" value="{LLAVE_FORM}">
        <input type="hidden" name="subject" value="New enquiry from judasaca.art">
        <input type="hidden" name="from_name" value="judasaca.art">
        <!-- Trampa para robots: un humano nunca la ve ni la llena. Si viene
             marcada, Web3Forms descarta el envio sin molestar a nadie. -->
        <input type="checkbox" name="botcheck" class="miel" tabindex="-1" autocomplete="off">

        <div class="dos-campos">
          <div class="campo">
            <label for="nombre">First name</label>
            <input id="nombre" name="First name" type="text" required autocomplete="given-name">
          </div>
          <div class="campo">
            <label for="apellido">Last name</label>
            <input id="apellido" name="Last name" type="text" autocomplete="family-name">
          </div>
        </div>
        <div class="campo">
          <label for="correo">Email</label>
          <input id="correo" name="email" type="email" required autocomplete="email">
        </div>
        <div class="campo">
          <label for="mensaje">Message</label>
          <textarea id="mensaje" name="Message" rows="5" required></textarea>
        </div>
        <button class="btn lleno enviar" type="submit">Send</button>
        <p class="aviso-forma" id="aviso-forma" role="status" aria-live="polite"></p>
      </form>

      <p class="o-bien">Or write directly to
        <a class="correo-linea" href="mailto:{CORREO}">{CORREO}</a></p>

      <div class="enlaces">
        <a href="{IG}" rel="noopener">Instagram · @judasaca</a>
        <a href="art.html">Available works</a>
        <a href="cv.html">CV</a>
      </div>

      <div class="prosa" style="margin-top:48px">
        <h3>Based in Bogotá</h3>
        <p>Works ship worldwide. For exhibitions and press, ask for the full dossier and
          high-resolution images and they will be sent the same day.</p>
      </div>
    </div>
  </section>
</main>

<script>
/* Envia sin recargar la pagina. Si el JavaScript falla o esta apagado, el form
   se manda igual por POST normal: Web3Forms responde con su propia pagina de
   gracias. Nunca queda un formulario que no hace nada. */
(function(){{
  var f=document.getElementById('forma'); if(!f||!window.fetch) return;
  var aviso=document.getElementById('aviso-forma'), boton=f.querySelector('button');
  f.addEventListener('submit', function(e){{
    e.preventDefault();
    aviso.className='aviso-forma'; aviso.textContent='Sending…'; boton.disabled=true;
    fetch(f.action, {{method:'POST', body:new FormData(f), headers:{{'Accept':'application/json'}}}})
      .then(function(r){{ return r.json(); }})
      .then(function(d){{
        if(!d.success) throw new Error(d.message||'error');
        f.reset();
        aviso.className='aviso-forma ok';
        aviso.textContent='Thank you. Juan reads these himself and will reply from {CORREO}.';
      }})
      .catch(function(){{
        aviso.className='aviso-forma mal';
        aviso.textContent='That did not go through. Please write directly to {CORREO}.';
      }})
      .then(function(){{ boton.disabled=false; }});
  }});
}})();
</script>
''' + PIE

# ══════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════
# 7 · PRIVACIDAD
# ══════════════════════════════════════════════════════════════════════════
# No va en el menu principal: nadie entra a una web de arte buscando la
# politica de privacidad. Va en el pie, que es donde se busca cuando se busca.
privacidad = cabeza(
  'Privacy · JUDASACA',
  'How judasaca.art handles personal data: the contact form, payments through '
  'Bold, and your rights under Colombian law.',
  'privacy.html') + f'''
<main>
  <section>
    <div class="wrap estrecho">
      <div class="tit">
        <div class="eti">Privacy</div>
        <h2>What we collect, and what we do not</h2>
        <p>Short version: a name, an email and a message if you write to us. Nothing else,
          and never a card number.</p>
      </div>

      <div class="prosa">
        <h3>Who is responsible</h3>
        <p>Juan Salazar, working as JUDASACA, in Bogotá, Colombia.
          Questions about anything on this page go to
          <a href="mailto:{CORREO}">{CORREO}</a>.</p>

        <h3>What this site collects</h3>
        <p><b>The contact form.</b> Your first name, last name, email address and the
          message you write. We use them to answer you and for nothing else. They are not
          sold, rented or shared, and there is no mailing list to be added to.</p>
        <p><b>The selection of works.</b> When you add a piece to the selection, that list
          is saved in your own browser and never leaves your device. It is not a cookie and
          it is not sent to us. Clearing your browser data erases it.</p>
        <p><b>Payments.</b> Card details are entered inside Bold's payment gateway. They do
          not pass through this site and we never see, receive or store them.</p>

        <h3>Who else touches this information</h3>
        <table class="tabla-privacidad">
          <tr><td><b>Web3Forms</b></td><td>Delivers the contact form to our inbox.</td></tr>
          <tr><td><b>Bold</b></td><td>Processes payments. Colombian payment gateway.</td></tr>
          <tr><td><b>Cloudflare</b></td><td>Signs each sale so its amount cannot be altered.
            It receives only which artwork was chosen, never who you are.</td></tr>
        </table>

        <h3>Your rights</h3>
        <p>Under Ley 1581 de 2012 you may ask us what data we hold about you, correct it,
          update it, or ask us to delete it, and you may withdraw your permission at any
          time. Write to <a href="mailto:{CORREO}">{CORREO}</a> and Juan answers himself.
          Consultations are answered within ten working days and complaints within fifteen.</p>

        <h3>Cookies</h3>
        <p>This site sets no advertising or tracking cookies, and there is nothing here
          following you to other websites.</p>

        <h3>Encryption</h3>
        <p>The whole site is served over HTTPS, so everything travelling between your
          browser and this site is encrypted, including whatever you type into the contact
          form. Payment encryption is handled inside Bold's gateway.</p>

        <p class="chico">Last updated <span class="dato-fecha">August 2026</span>.</p>
      </div>
    </div>
  </section>
</main>
''' + PIE


# ══════════════════════════════════════════════════════════════════════════
# 8 · DESPUES DEL PAGO
# ══════════════════════════════════════════════════════════════════════════
# Bold devuelve al comprador aqui con ?bold-order-id=...&bold-tx-status=...
# El estado que llega en la URL es informativo y puede no ser el definitivo, asi
# que el texto no promete nada que no se pueda sostener: dice lo que Bold dijo y
# remite a Juan, que es quien confirma de verdad.
gracias = cabeza(
  'Thank you · JUDASACA',
  'Payment confirmation for your order at judasaca.art.',
  'thanks.html') + f'''
<main>
  <section>
    <div class="wrap estrecho prosa gracias">
      <div class="tit centrado">
        <div class="eti">Order</div>
        <h2 id="titulo-gracias">Thank you</h2>
      </div>
      <p id="mensaje-gracias" style="text-align:center">Juan will write to you from {CORREO} to
        confirm the work and arrange shipping to your city.</p>
      <p class="chico" id="referencia-gracias" style="color:var(--tenue);text-align:center"></p>

      <!-- La direccion se pide AQUI y no antes de pagar. Antes del pago cada
           campo es una excusa para no comprar; despues del pago el comprador ya
           esta contento y quiere que le llegue el cuadro. -->
      <div id="caja-envio" hidden>
        <h3 style="margin-top:38px">Where should it go?</h3>
        <p>Juan ships worldwide. Leave the address and he confirms the cost and the
          date the same day.</p>
        <form class="forma" id="form-envio">
          <div class="campo">
            <label for="e-nombre">Full name</label>
            <input id="e-nombre" name="nombre" type="text" required autocomplete="name">
          </div>
          <div class="dos-campos">
            <div class="campo">
              <label for="e-email">Email</label>
              <input id="e-email" name="email" type="email" required autocomplete="email">
            </div>
            <div class="campo">
              <label for="e-telefono">Phone</label>
              <input id="e-telefono" name="telefono" type="tel" required autocomplete="tel">
            </div>
          </div>
          <div class="campo">
            <label for="e-direccion">Address</label>
            <input id="e-direccion" name="direccion" type="text" required autocomplete="street-address">
          </div>
          <div class="dos-campos">
            <div class="campo">
              <label for="e-ciudad">City</label>
              <input id="e-ciudad" name="ciudad" type="text" required autocomplete="address-level2">
            </div>
            <div class="campo">
              <label for="e-pais">Country</label>
              <input id="e-pais" name="pais" type="text" required autocomplete="country-name">
            </div>
          </div>
          <div class="campo">
            <label for="e-notas">Anything Juan should know</label>
            <input id="e-notas" name="notas" type="text" autocomplete="off">
          </div>
          <button class="btn lleno enviar" type="submit">Send shipping details</button>
          <p class="aviso-forma" id="aviso-envio" role="status" aria-live="polite"></p>
        </form>
      </div>

      <p style="margin-top:34px;text-align:center"><a class="btn" href="art.html">Back to the works</a></p>
    </div>
  </section>
</main>

<script>
(function(){{
  var p = new URLSearchParams(window.location.search);
  var estado = (p.get('bold-tx-status') || '').toLowerCase();
  var orden = p.get('bold-order-id');
  var t = document.getElementById('titulo-gracias');
  var m = document.getElementById('mensaje-gracias');
  var r = document.getElementById('referencia-gracias');
  var caja = document.getElementById('caja-envio');

  // Respaldo: si Bold no devolviera la referencia en la URL, se recupera la que
  // el sitio guardo justo antes de abrir la pasarela.
  var guardada = null;
  try {{ guardada = JSON.parse(localStorage.getItem('judasaca-orden') || 'null'); }} catch(e) {{}}
  if (!orden && guardada && guardada.id) orden = guardada.id;

  var aprobada = (estado === 'approved');

  if (aprobada) {{
    t.textContent = 'Thank you';
    m.textContent = 'Your payment went through. One last thing and it is done.';
  }} else if (estado === 'rejected' || estado === 'failed') {{
    t.textContent = 'That payment did not go through';
    m.textContent = 'Nothing has been charged. You can try again, or write to {CORREO} '
      + 'and Juan will sort it out with you directly.';
  }} else if (estado) {{
    t.textContent = 'Your payment is being processed';
    m.textContent = 'Bold has not confirmed it yet. As soon as it settles, Juan will write '
      + 'to you from {CORREO}.';
  }}
  if (orden) r.textContent = 'Reference: ' + orden;

  /* El webhook de Bold puede tardar hasta diez minutos. El comprador esta aqui
     ahora. Se le avisa al Worker para que marque la obra enseguida; el Worker
     no se fia de esto y lo verifica contra Bold antes de hacer nada. */
  if (orden && aprobada && window.fetch) {{
    fetch('{FIRMADOR}/confirmar', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ orderId: orden }})
    }}).catch(function(){{ }});

    // Lo pagado sale del carrito. Si no, sigue ahi tentando a pagarlo otra vez.
    try {{
      var comprados = (guardada && guardada.slugs) || [];
      var carro = JSON.parse(localStorage.getItem('judasaca-carro') || '[]');
      localStorage.setItem('judasaca-carro', JSON.stringify(
        carro.filter(function(s){{ return comprados.indexOf(s) < 0; }})));
    }} catch(e) {{}}
  }}

  if (!aprobada || !orden) return;
  caja.hidden = false;

  var f = document.getElementById('form-envio');
  var aviso = document.getElementById('aviso-envio');
  f.addEventListener('submit', function(e){{
    e.preventDefault();
    var boton = f.querySelector('button[type=submit]');
    boton.disabled = true;
    aviso.className = 'aviso-forma';
    aviso.textContent = 'Sending…';

    var datos = {{ orderId: orden }};
    ['nombre','email','telefono','direccion','ciudad','pais','notas']
      .forEach(function(k){{ datos[k] = (f[k] && f[k].value || '').trim(); }});

    fetch('{FIRMADOR}/datos', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(datos)
    }})
    .then(function(rr){{ return rr.json(); }})
    .then(function(d){{
      if (!d || !d.ok) throw new Error('no');
      f.innerHTML = '';
      aviso.className = 'aviso-forma ok';
      aviso.textContent = 'Got it. Juan has your address and will write from {CORREO} '
        + 'with the shipping date.';
      f.appendChild(aviso);
    }})
    .catch(function(){{
      boton.disabled = false;
      aviso.className = 'aviso-forma mal';
      aviso.textContent = 'That did not save. Please send your address to {CORREO} '
        + 'quoting the reference above.';
    }});
  }});
}})();
</script>
''' + PIE


if __name__ == '__main__':
    for nombre, cuerpo in [('index.html', home), ('about.html', about), ('art.html', art),
                           ('shop.html', shop), ('cv.html', cv), ('contact.html', contact),
                           ('privacy.html', privacidad), ('thanks.html', gracias)]:
        n = escribir(nombre, cuerpo)
        print(f'  {nombre:<14} {n/1024:>6.1f} KB')

    # CNAME para GitHub Pages, robots y sitemap
    open(os.path.join(RUTA, 'CNAME'), 'w').write('judasaca.art\n')
    open(os.path.join(RUTA, 'robots.txt'), 'w').write(
        f'User-agent: *\nAllow: /\n\nSitemap: {SITIO}/sitemap.xml\n')
    urls = ''.join(
        f'  <url><loc>{SITIO}/{"" if a == "index.html" else a}</loc>'
        f'<priority>{"1.0" if a == "index.html" else "0.8"}</priority></url>\n'
        # privacy.html no esta en PAGINAS porque no va en el menu, pero si debe
        # poder indexarse: es la pagina que alguien busca cuando desconfia.
        for a, _ in PAGINAS + [('privacy.html', 'Privacy')])
    open(os.path.join(RUTA, 'sitemap.xml'), 'w').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print('\n  CNAME · robots.txt · sitemap.xml')
    print(f'  {len(OBRAS)} obras · {sum(len(i) for _, i in EXPOS)} exposiciones')
