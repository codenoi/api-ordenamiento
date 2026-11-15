# API REST de Ordenamiento y Búsqueda Binaria

Aplicación web desacoplada para la asignatura **Lenguajes de Programación II (UNEFA)**.

- **Backend:** Flask (Python) con los algoritmos Quicksort y búsqueda binaria.
- **Frontend:** HTML5 + CSS + JavaScript que consume la API con `fetch()` y dibuja los datos sin recargar la página.

## Funcionalidades

- Catálogo de productos ordenado por precio o nombre (ascendente y descendente) usando **Quicksort**.
- Búsqueda de un producto por ID usando **búsqueda binaria** (la lista se ordena por ID antes de buscar).
- **Benchmark** que compara el tiempo en milisegundos de Quicksort contra Burbuja con 1.000 elementos.

## Estructura del proyecto

```
api-ordenamiento/
├── app.py              # Backend Flask: algoritmos y endpoints
├── productos.json      # Catálogo de productos
├── templates/
│   └── index.html      # Página web (frontend)
├── README.md
├── LICENSE
└── .gitignore
```

## Cómo ejecutarlo

1. Clonar el repositorio y entrar a la carpeta.
2. Crear y activar un entorno virtual (Windows):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instalar Flask:
   ```
   pip install flask
   ```
4. Iniciar el servidor:
   ```
   python app.py
   ```
5. Abrir en el navegador: http://127.0.0.1:5000

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/productos?sort_by=precio&order=asc` | Lista ordenada con Quicksort. `sort_by`: `id`, `nombre` o `precio`. `order`: `asc` o `desc`. |
| GET | `/api/productos/buscar?id=9` | Búsqueda binaria por ID. Devuelve el producto y los pasos realizados. |
| GET | `/api/benchmark?n=1000` | Compara Quicksort y Burbuja con `n` elementos aleatorios. |

## Autor

Elianny Coronado — UNEFA, Núcleo Apure

## Licencia

Distribuido bajo la licencia MIT. Ver el archivo `LICENSE`.