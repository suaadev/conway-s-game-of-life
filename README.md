# Conway-s-game-of-life

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-green.svg?style=for-the-badge)](https://www.pygame.org/)

## Tabla de Contenidos

- [Acerca del proyecto](#acerca-del-proyecto)
- [Comportamiento](#comportamiento)
  - [Generaciones](#generaciones)
- [Implementación](#implementación)
- [Optimizaciones](#optimizaciones)
  - [Analizando estados](#analizando-estados)
  - [Subproblemas repetidos](#subproblemas-repetidos)
- [Instalación y Uso](#instalación-y-uso)

## Acerca del proyecto

Hace un año me topé con un juego llamado `game-of-life` del matemático británico John Conway y me resultó muy fascinante cómo, con tan solo 4 simples reglas, se puede llegar a simular un comportamiento tan complejo y extraordinario. Así que, motivado por este concepto, decidí implementar el juego utilizando Python y Pygame para darle representación visual. El resultado fue un simulador interactivo con el que podemos entender el comportamiento de estas células y observar múltiples patrones fascinantes que emergen a partir de una configuración inicial.

<div>
<img style="display: block; margin: 0 auto" src="docs/ezgif-12a5b859dc35bc1b.gif">
</div>

## Comportamiento

El Juego de la Vida se desarrolla en un mundo bidimensional infinito donde cada celda representa una célula que tiene 2 estados posibles: viva o muerta. Para determinar el estado de una célula en la siguiente generación, se aplican 4 reglas fundamentales establecidas por John Conway:

- **Soledad:** Cualquier célula viva con menos de dos vecinas vivas muere (infrapoblación).
- **Supervivencia:** Cualquier célula viva con dos o tres vecinas vivas permanece viva en la siguiente generación.
- **Sobrepoblación:** Toda célula viva con más de tres vecinas vivas muere.
- **Reproducción:** Toda célula muerta que tenga exactamente tres vecinas vivas se convierte en una célula viva.

Estas reglas son apasionantes porque simulan dinámicas de un ecosistema natural: las células mueren por aislamiento o superpoblación, o nacen si las condiciones de su entorno son ideales. De ahí su nombre, pues demuestra cómo reglas sencillas pueden generar comportamientos orgánicos.

#### Generaciones

La evolución del sistema ocurre en "generaciones", donde cada paso representa una iteración del estado actual del mundo. Dependiendo de la configuración inicial, una simulación puede tener dos desenlaces:
1. **Extinción (Estado final):** Se llega a un punto donde todas las células mueren y el juego termina.
2. **Estructuras Cíclicas o Infinitas:** Se forma un patrón recurrente donde las células nacen y mueren de forma periódica, permitiendo que la simulación continúe indefinidamente.

## Implementación

Para llevar esta lógica a un entorno práctico, representamos el mundo como una matriz finita de dimensiones $N \times M$. Cada posición almacena el estado de una célula (`0` para muerta y `1` para viva). En cada iteración, el motor calcula los vecinos adyacentes de cada celda (incluyendo las diagonales) para determinar su estado en la siguiente generación. Toda esta lógica algorítmica fue desarrollada en Python, utilizando Pygame para renderizar la interfaz gráfica de usuario.

## Optimizaciones

### Analizando estados

Al probar tableros de gran tamaño, el enfoque tradicional para calcular cada generación resultaba muy ineficiente. Recorrer una matriz de $10000 \times 10000$ requiere evaluar 100.000.000 de posiciones en cada iteración, con una complejidad de $O(N \times M)$ (o $O(N^2)$ en tableros cuadrados).

<div>
<img style="display: block; margin: 0 auto" src="docs/image-8.png">
<p style="text-align: center">Matriz de 25x25, Células vivas: 5</p>
</div>

##### Solución

Para solucionar esto me planteé la siguiente duda: *¿Realmente es necesario evaluar todo el tablero?* 

Las únicas celdas que pueden cambiar de estado o hacer que sus vecinas cambien son las células vivas y su entorno inmediato. Por lo tanto, en lugar de analizar las $N \times M$ posiciones del tablero, basta con centrarse únicamente en las posiciones donde hay una célula viva y su vecindad de $3 \times 3$. Esto reduce la complejidad computacional de depender del tamaño total del mapa a depender únicamente de $K$, donde $K$ es el número de células vivas en la generación actual ($O(K)$).

<div>
<img style="display: block; margin: 0 auto" src="docs/image-7.png">
<p style="text-align: center">Área delimitada a explorar</p>
</div>

##### Ejemplo práctico

Consideremos la imagen anterior con una matriz de $25 \times 25$ ($625$ celdas) y solo $5$ células vivas:
- **Enfoque ingenuo:** Evalúa las $625$ posiciones de la matriz.
- **Enfoque optimizado:** Solamente explora las $5$ células vivas y sus vecindades inmediatas ($5 \times 9 = 45$ evaluaciones potenciales), reduciendo de $625$ a menos de $45$ operaciones por ciclo.

#### Efectos secundarios

- **Tableros densos:** Si el tablero se llena casi por completo de células vivas, el valor de $K$ se aproxima al tamaño total del tablero, igualando la complejidad del enfoque inicial. No obstante, dada la naturaleza del juego, es muy inusual que la densidad de células vivas cubra la totalidad de la matriz.
- **Vecindades superpuestas:** Si dos células vivas están muy cerca, el área de $3 \times 3$ de cada una evaluará las mismas celdas vecinas múltiples veces.

---

### Subproblemas repetidos

Aunque redujimos la evaluación al entorno de las células vivas, surge un problema cuando las células están agrupadas. Por ejemplo:

<div>
<img style="display: block; margin: 0 auto" src="docs/image-3.png">
<p style="text-align: center;">Matriz de 3x5, Células vivas: 3</p>
</div>

En este mini mundo de $3 \times 5$, tenemos células vivas en las posiciones `(1,1)`, `(1,2)` y `(1,3)`.
Al evaluar la célula `(1,1)`, analizamos las celdas a su alrededor:
`{(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)}`

Al pasar a la siguiente célula viva en `(1,2)`, se generan las celdas:
`{(0,1), (0,2), (0,3), (1,1), (1,2), (1,3), (2,1), (2,2), (2,3)}`

Como se observa, posiciones como `(0,1)`, `(0,2)`, `(1,1)`, `(1,2)`, `(2,1)` y `(2,2)` se evaluarían dos veces en el mismo turno, desperdiciando ciclos de procesamiento.

#### Solución

Para evitar procesar celdas duplicadas, implementamos un control de memoización mediante un conjunto de datos (**`set()`**). A medida que calculamos el nuevo estado de una celda en una iteración, guardamos sus coordenadas en el `set`. Antes de calcular cualquier celda vecina, verificamos si ya existe en el conjunto; si es así, se omite. De este modo nos aseguramos de evaluar cada posición **exactamente una vez** por generación.

## Instalación y Uso

Para probar y visualizar el Juego de la Vida en tu propia máquina, sigue estos pasos:

### Requisitos previos

Asegúrate de tener instalado en tu sistema:

- **Python 3.x** (preferiblemente 3.12 o superior).
- **Pip** (Gestor de paquetes de Python).

### Pasos de instalación

1. **Clona este repositorio:**

```bash
git clone [https://github.com/suaadev/conway-s-game-of-life](https://github.com/suaadev/conway-s-game-of-life)
cd conway-s-game-of-life

```

2. **Crea un entorno virtual (Recomendado):**
Es una buena práctica aislar las dependencias del proyecto.

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS y Linux:
source venv/bin/activate

```

3. **Instala las dependencias:**
Este proyecto depende de `pygame` para el renderizado visual y de `numpy`.

```bash
pip install -r requirements.txt

```

### Ejecución

Para iniciar el entorno gráfico y ver la simulación en acción, ejecuta el archivo principal de Python:

```bash
python src/main.py

```

### Controles del juego

* **Clic Izquierdo:** Colocar célula viva.
* **Clic Derecho:** Borrar célula viva.
* **Tecla S:** Inicia/Pausa la simulación.
* **Tecla C:** Limpia el tablero y reinicia el mundo.
* **Tecla B:** Activa/Desactiva la cuadrícula.
* **Tecla M:** Disminuye el tiempo entre generaciones.
* **Tecla N:** Aumenta el tiempo entre generaciones.
