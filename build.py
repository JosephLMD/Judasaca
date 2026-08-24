#!/usr/bin/env python3
"""
Generador del sitio judasaca.art

Todo el contenido vive aqui arriba, en OBRAS, EXPOS y PRENSA. Se corre
`python3 build.py` y se reescriben los seis HTML. La ventaja de tenerlo asi
es que la barra, el pie y las etiquetas de Google quedan identicas en todas
las paginas: no hay forma de que una quede desactualizada.

Para poner un boton de compra: rellena 'buy' en la obra con el enlace de
pago de Stripe. Si esta vacio, la obra muestra solo 'Inquire'.
"""
import os, re, html

RUTA = os.path.dirname(os.path.abspath(__file__))
SITIO = 'https://judasaca.art'
CORREO = 'contact@judasaca.art'
IG = 'https://www.instagram.com/judasaca'

# ── formulario de contacto ───────────────────────────────────────────────
# Un sitio estatico no puede mandar correo por si solo: no hay servidor detras.
# Web3Forms recibe el envio y lo reenvia a CORREO. Se saca la llave en
# web3forms.com poniendo contact@judasaca.art, llega por correo, y se pega aqui.
# Mientras diga PEGA-AQUI, el formulario no envia nada.
LLAVE_FORM = '511aafa4-63bd-453c-a671-8825c5104c7a'
REEL = 'https://www.instagram.com/reel/DXqQrk9l-U-/'

# ── las obras ────────────────────────────────────────────────────────────
# 'buy' vacio = solo boton Inquire. Al pegar un enlace de Stripe aparece
# tambien el boton Buy, con Apple Pay y Google Pay incluidos.
OBRAS = [
 dict(slug='oil-city-woodstock',   titulo='Oil City Woodstock',
      tec='Acrylics and oil stick on canvas', med='100 × 100 cm', usd=1500, buy='', vendida=False),
 dict(slug='sunday-snoops',        titulo='Sunday, Snoops',
      tec='Acrylics and spray on canvas',     med='100 × 100 cm', usd=1500, buy='', vendida=False),
 dict(slug='pop-art-rat',          titulo='Pop Art Rat',
      tec='Acrylics and oil stick on canvas', med='100 × 100 cm', usd=1500, buy='', vendida=False),
 dict(slug='mango-og',             titulo='Mango OG',
      tec='Acrylics and oil stick on canvas', med='100 × 100 cm', usd=1500, buy='', vendida=False),
 dict(slug='original-pastel-disney', titulo='Original Pastel Disney',
      tec='Acrylics and spray on canvas',     med='100 × 100 cm', usd=1500, buy='', vendida=False),
 dict(slug='nothing-stays-the-same', titulo='Nothing Stays the Same',
      tec='Oil on canvas',                    med='100 × 120 cm', usd=1500, buy='', vendida=False),
 dict(slug='blue-thoughts-rat',    titulo='Blue Thoughts Rat',
      tec='Acrylics and spray on canvas',     med='80 cm diameter', usd=950, buy='', vendida=False),
 dict(slug='smiling-ratsquiat-blue-crown', titulo='Smiling Ratsquiat, Blue Crown',
      tec='Acrylics and spray on canvas',     med='50 × 50 cm', usd=750, buy='', vendida=False),
 dict(slug='smiling-ratsquiat-yellow-crown', titulo='Smiling Ratsquiat, Yellow Crown',
      tec='Acrylics and spray on canvas',     med='50 × 50 cm', usd=750, buy='', vendida=False),
 dict(slug='oil-woodstock',        titulo='Oil Woodstock',
      tec='Acrylics and oil on canvas',       med='50 × 50 cm', usd=750, buy='', vendida=False),
 dict(slug='here-love',            titulo='Here, Love',
      tec='Acrylics and spray on canvas',     med='50 × 50 cm', usd=750, buy='', vendida=False),
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
CATALOGO = json.dumps({o['slug']: {'t': o['titulo'], 'm': o['med'], 'usd': o['usd']}
                       for o in OBRAS}, ensure_ascii=False)

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
      <span style="opacity:.7">nothing stays the same</span></div>
  </div>
</footer>

<div class="velo" id="velo"></div>
<aside class="panel" id="panel" aria-label="Cart" aria-hidden="true">
  <div class="alto"><h2>Selected works</h2><button class="x" id="cerrar-carro" aria-label="Close">&times;</button></div>
  <div class="lista" id="carro-lista"></div>
  <div class="bajo">
    <div class="total"><span>Total</span><span id="carro-total">USD 0</span></div>
    <a class="btn lleno" id="carro-pedir" href="#">Request these works</a>
    <p class="nota">Sending this opens an email to Juan with the pieces you picked.
      He replies himself, confirms availability and quotes shipping to your city.</p>
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
      pedir=document.getElementById('carro-pedir');
  if(!bot||!panel) return;

  function guardar(){{ try{{ localStorage.setItem(LLAVE, JSON.stringify(carro)); }}catch(e){{}} }}
  function dinero(n){{ return 'USD ' + n.toLocaleString('en-US'); }}

  function pintar(){{
    num.textContent = carro.length;
    if(!carro.length){{
      lista.innerHTML = '<p class="vacio">Nothing selected yet.</p>';
      total.textContent = dinero(0);
      pedir.style.opacity = .4; pedir.style.pointerEvents = 'none';
      return;
    }}
    pedir.style.opacity = 1; pedir.style.pointerEvents = '';
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
    var cuerpo = 'Hi Juan, I am interested in these works:%0D%0A%0D%0A'
      + carro.map(function(sl){{ return '- '+CAT[sl].t+' ('+CAT[sl].m+') — '+dinero(CAT[sl].usd); }}).join('%0D%0A')
      + '%0D%0A%0D%0ATotal: '+dinero(suma)+'%0D%0A%0D%0ACould you confirm availability and shipping?';
    pedir.href = 'mailto:{CORREO}?subject=Enquiry%20from%20judasaca.art&body='+cuerpo;
  }}

  function abrir(){{ panel.classList.add('abierto'); velo.classList.add('abierto');
    panel.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }}
  function cerrar(){{ panel.classList.remove('abierto'); velo.classList.remove('abierto');
    panel.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }}

  bot.addEventListener('click', function(){{ pintar(); abrir(); }});
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
</script>
</body>
</html>
'''


def tarjeta_obra(o, mini=True):
    img = f"img/{o['slug']}-sm.webp" if mini else f"img/{o['slug']}.webp"
    precio = ('<span class="vendida">Sold</span>' if o['vendida']
              else f'<span class="p">USD {o["usd"]:,}</span>')
    asunto = f"Inquiry: {o['titulo']}"
    cuerpo = f"Hi Juan, I would like to know more about {o['titulo']} ({o['med']})."
    inquire = (f'<a class="btn" href="mailto:{CORREO}'
               f'?subject={asunto.replace(" ", "%20")}&body={cuerpo.replace(" ", "%20")}">Inquire</a>')
    comprar = (f'<a class="btn lleno" href="{o["buy"]}" rel="noopener">Buy</a>'
               if o['buy'] and not o['vendida'] else '')
    carrito = ('' if o['vendida'] else
               f'<button class="btn add" data-slug="{o["slug"]}">Add to cart</button>')
    return f'''      <article class="obra">
        <figure>
          <a class="marco" href="img/{o['slug']}.webp"
             data-lupa data-tit="{html.escape(o['titulo'])}"
             data-fic="{html.escape(o['tec'])} · {o['med']}">
            <img src="{img}" alt="{html.escape(o['titulo'])}, {html.escape(o['tec'].lower())}, {o['med']}" loading="lazy">
          </a>
          <figcaption>
            <div class="linea"><span class="t">{html.escape(o['titulo'])}</span>
              <span class="f">· {o['med']} ·</span> {precio}</div>
            <div class="acciones">{comprar}{carrito}{inquire}</div>
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
      <img src="intro_photo.jpg"
           alt="Juan Salazar, JUDASACA">
      <div class="pie-obra">Juan Salazar · Bogotá</div>
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
  'about.html', og='img/about_photo.jpeg') + f'''
<main>
  <section>
    <div class="wrap">
      <div class="tit centrado"><div class="eti">About</div><h2>Juan Salazar</h2></div>
      <div class="dos">
        <!-- La foto se queda quieta mientras el texto corre. Es el gesto mas caro
             que se puede hacer sin agregar un solo elemento a la pagina. -->
        <div class="foto">
          <img class="retrato" src="about_photo.jpeg"
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
  'Eleven original paintings by JUDASACA, available now. Acrylics, oil and spray '
  'on canvas. Bogotá, Colombia.',
  'art.html') + f'''
<main>
  <section>
    <div class="wrap">
      <div class="tit">
        <div class="eti">Original works · {len(OBRAS)} available</div>
        <h2>Art</h2>
        <p>Every piece here is a single original, painted by hand and signed. Prices are
          in US dollars and do not include shipping or framing; write and we will work
          out the best way to get it to you.</p>
      </div>
      <div class="obras">
{''.join(tarjeta_obra(o) for o in OBRAS)}      </div>
    </div>
  </section>

  <section class="humo">
    <div class="wrap estrecho prosa">
      <div class="tit"><div class="eti">Buying</div><h2>How it works</h2></div>
      <p>Write using the button on the piece you want. You will get an answer from Juan
        himself, not a form. He will confirm the work is still available, quote shipping
        to your city, and explain how the augmented layer works once the canvas is on
        your wall.</p>
      <p>Works ship worldwide from Bogotá. Larger canvases usually travel rolled in a
        tube and are stretched on arrival, which is standard practice and keeps shipping
        sane.</p>
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
        <img src="contact_photo.jpeg" alt="Juan Salazar with a signed print of Smiling Ratsquiat, King Crown">
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
if __name__ == '__main__':
    for nombre, cuerpo in [('index.html', home), ('about.html', about), ('art.html', art),
                           ('shop.html', shop), ('cv.html', cv), ('contact.html', contact)]:
        n = escribir(nombre, cuerpo)
        print(f'  {nombre:<14} {n/1024:>6.1f} KB')

    # CNAME para GitHub Pages, robots y sitemap
    open(os.path.join(RUTA, 'CNAME'), 'w').write('judasaca.art\n')
    open(os.path.join(RUTA, 'robots.txt'), 'w').write(
        f'User-agent: *\nAllow: /\n\nSitemap: {SITIO}/sitemap.xml\n')
    urls = ''.join(
        f'  <url><loc>{SITIO}/{"" if a == "index.html" else a}</loc>'
        f'<priority>{"1.0" if a == "index.html" else "0.8"}</priority></url>\n'
        for a, _ in PAGINAS)
    open(os.path.join(RUTA, 'sitemap.xml'), 'w').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print('\n  CNAME · robots.txt · sitemap.xml')
    print(f'  {len(OBRAS)} obras · {sum(len(i) for _, i in EXPOS)} exposiciones')
