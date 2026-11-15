from flask import Flask, jsonify, request, render_template
import json
import time
import random
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def quicksort(items, clave, reverse=False):
    # Caso base: una lista de 0 o 1 elementos 
    if len(items) <= 1:
        return items

    # 1. Elegimos el pivote (el elemento del medio)
    pivote = items[len(items) // 2][clave]
 
    # 2. Repartimos en tres grupos
    if reverse:
        izq = [x for x in items if x[clave] > pivote]
        der = [x for x in items if x[clave] < pivote]
    else:
        izq = [x for x in items if x[clave] < pivote]
        der = [x for x in items if x[clave] > pivote]
    centro = [x for x in items if x[clave] == pivote]

    # 3. Ordenamos cada lado y unimos
    return quicksort(izq, clave, reverse) + centro + quicksort(der, clave, reverse)

 #                  BÚSQUEDA BINARIA 
def busqueda_binaria(items, clave, objetivo):
    # items DEBE venir ordenada por 'clave'
    izq = 0
    der = len(items) - 1
    pasos = 0

    while izq <= der:
        pasos += 1
        medio = (izq + der) // 2
        valor = items[medio][clave]

        if valor == objetivo:
            return medio, pasos      # lo encontramos
        elif valor < objetivo:
            izq = medio + 1          # descartamos la mitad izquierda
        else:
            der = medio - 1          # descartamos la mitad derecha

    return -1, pasos                 # no existe

#  ORDENAMIENTO BURBUJA (para el benchmark) 
def burbuja(items, clave):
    items = list(items)  # trabajamos sobre una copia
    n = len(items)

    for i in range(n):
        hubo_cambio = False
        # En cada pasada, los últimos i elementos ya quedaron en su lugar
        for j in range(n - i - 1):
            if items[j][clave] > items[j + 1][clave]:
                items[j], items[j + 1] = items[j + 1], items[j]
                hubo_cambio = True
        if not hubo_cambio:   # si no cambió nada, ya está ordenada
            break

    return items

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/productos')
def get_productos():
    with open(os.path.join(BASE_DIR, 'productos.json'), encoding='utf-8') as f:
        productos = json.load(f)

    sort_by = request.args.get('sort_by', 'precio')
    order = request.args.get('order', 'asc') == 'desc'

   
    if sort_by not in ('id', 'nombre', 'precio'):
        sort_by = 'precio'

    ordenados = quicksort(productos, sort_by, reverse=order)
    return jsonify(ordenados)

@app.route('/api/productos/buscar')
def buscar_producto():
    # Lee el id que viene en la dirección (?id=9)
    try:
        id_buscado = int(request.args.get('id'))
    except (TypeError, ValueError):
        return jsonify({"error": "Debes indicar un id numérico, por ejemplo ?id=5"}), 400

    with open(os.path.join(BASE_DIR, 'productos.json'), encoding='utf-8') as f:
        productos = json.load(f)

    # Precondición: la lista debe estar ordenada por id
    ordenados = quicksort(productos, 'id')

    posicion, pasos = busqueda_binaria(ordenados, 'id', id_buscado)

    if posicion == -1:
        return jsonify({"error": f"No existe un producto con id {id_buscado}"}), 404

    return jsonify({"producto": ordenados[posicion], "pasos": pasos})

@app.route('/api/benchmark')
def benchmark():
    # Cantidad de elementos (por defecto 1000, máximo 5000 para no trabar el servidor)
    try:
        n = int(request.args.get('n', 1000))
    except ValueError:
        n = 1000
    n = max(10, min(n, 5000))

  
    datos = [
        {"id": i, "nombre": f"Producto {i}", "precio": round(random.uniform(1, 1000), 2)}
        for i in range(1, n + 1)
    ]


    inicio = time.perf_counter()
    res_quick = quicksort(datos, 'precio')
    ms_quick = (time.perf_counter() - inicio) * 1000

    # Medimos Burbuja (con los mismos datos)
    inicio = time.perf_counter()
    res_burbuja = burbuja(datos, 'precio')
    ms_burbuja = (time.perf_counter() - inicio) * 1000

    return jsonify({
        "elementos": n,
        "quicksort_ms": round(ms_quick, 3),
        "burbuja_ms": round(ms_burbuja, 3),
        "veces_mas_rapido": round(ms_burbuja / ms_quick, 1) if ms_quick > 0 else None,
        "mismo_resultado": [p['precio'] for p in res_quick] == [p['precio'] for p in res_burbuja]
    })

if __name__ == '__main__':
    app.run(debug=True)
