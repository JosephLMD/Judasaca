# -*- coding: utf-8 -*-
"""Recorta cada foto hasta la obra.

Las fotos son cuadros colgados en una pared: la obra ocupa la mitad del
encuadre y queda descentrada. Con 'contain' se centra la FOTO, no la OBRA, y
por eso se veia chueca y pequena. Aqui se busca donde termina la pared y se
recorta ahi, para que la imagen del sitio sea la obra y nada mas.

Metodo: se toma el color de la pared del anillo exterior, se marca todo pixel
que se aleje de ese color, y se corta en el primer punto donde una fila o
columna deja de ser pared. Se trabaja sobre los JPEG originales de Shop/, asi
que se puede volver a correr cuantas veces haga falta.
"""
import numpy as np
from PIL import Image
import os, json

def recorte(ruta, tol=26, minfrac=0.012, margen=0.012):
    im = Image.open(ruta).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    n = max(3, min(h, w) // 90)
    borde = np.concatenate([a[:n].reshape(-1,3), a[-n:].reshape(-1,3),
                            a[:,:n].reshape(-1,3), a[:,-n:].reshape(-1,3)])
    pared = np.median(borde, axis=0)
    dif = np.abs(a - pared).sum(axis=2)
    obra = dif > tol * 3

    filas = obra.mean(axis=1); cols = obra.mean(axis=0)
    def rango(v):
        act = np.where(v > minfrac)[0]
        return (int(act[0]), int(act[-1])) if len(act) else (0, len(v)-1)
    y1, y2 = rango(filas); x1, x2 = rango(cols)

    mx, my = int((x2-x1)*margen), int((y2-y1)*margen)
    caja = (max(0,x1-mx), max(0,y1-my), min(w,x2+mx+1), min(h,y2+my+1))
    area = ((caja[2]-caja[0])*(caja[3]-caja[1])) / float(w*h)
    return im, caja, area, tuple(int(c) for c in pared)

if __name__ == '__main__':
    import sys
    for f in sorted(os.listdir('Shop')):
        if not f.lower().endswith(('.jpeg','.jpg')): continue
        im, caja, area, pared = recorte(os.path.join('Shop', f))
        ar = (caja[2]-caja[0]) / float(caja[3]-caja[1])
        print(f'  {f[:38]:<40} queda {area:>5.0%} de la foto · proporcion {ar:.2f} · pared {pared}')


def cuadrar(ruta, aire=1.20):
    """Cuadrado centrado en la obra, conservando la moldura y algo de pared.

    Nunca corta la obra: si el cuadrado no cabe dentro de la foto, se agranda
    el lienzo con el color de la pared en lugar de recortar. Asi todas las
    fichas quedan del mismo tamano y centradas, y ninguna pierde un pedazo.
    """
    from PIL import Image
    im, caja, _, pared = recorte(ruta)
    x1, y1, x2, y2 = caja
    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    l = max(x2 - x1, y2 - y1) * aire / 2.0
    izq, arr, der, aba = int(cx - l), int(cy - l), int(cx + l), int(cy + l)
    lienzo = Image.new('RGB', (der - izq, aba - arr), pared)
    rx1, ry1 = max(0, izq), max(0, arr)
    rx2, ry2 = min(im.width, der), min(im.height, aba)
    lienzo.paste(im.crop((rx1, ry1, rx2, ry2)), (rx1 - izq, ry1 - arr))
    return lienzo
