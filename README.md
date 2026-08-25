# judasaca.art

Sitio de Juan Salazar (JUDASACA). HTML estático, sin dependencias,
publicado con GitHub Pages.

## Cómo cambiar algo

Todo el contenido vive en `build.py`: las obras, las exposiciones y la
prensa. Se edita ahí y se corre:

```
python3 build.py
```

Eso reescribe los seis HTML. No se editan los `.html` a mano, porque el
siguiente `build.py` los sobrescribe.

## Poner un botón de compra

En `build.py`, cada obra tiene un campo `buy` vacío. Al pegar ahí un enlace
de pago de Bold, esa obra muestra un botón **Buy** junto al de **Inquire**.
Si el campo sigue vacío, solo aparece **Inquire**.

```python
dict(slug='here-love', titulo='Here, Love', ..., buy='https://checkout.bold.co/...'),
```

## Marcar una obra como vendida

Cambiar `vendida=False` por `vendida=True`. La obra queda visible, con la
palabra *Sold* en lugar del precio y sin botones.

## Qué es cada archivo

- `build.py` — el contenido y el generador
- `css/style.css` — todo el diseño
- `img/` — obras (`-sm` para la rejilla, grande para la lupa), retrato y logo
- `CNAME` — el dominio, lo lee GitHub Pages
- `sitemap.xml`, `robots.txt` — para Google
