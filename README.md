# Conway-s-game-of-life

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-green.svg?style=for-the-badge)](https://www.pygame.org/)

## Tabla de Contenidos

- [Acerca del proyecto](#acerca-del-proyecto)
- [Comportamiento](#comportamiento)
  - [Generaciones](#generaciones)
- [Implementación](#implementacion)
- [Optimizaciones](#optimizaciones)
  - [Analizando estados](#analizando-estados)
  - [Subproblemas repetidos](#subproblemas-repetidos)
- [Instalación y Uso](#instalación-y-uso)

## Acerca del proyecto

Hace un año me tope con un juego llamado `game-of-life` del matematico britanico Jhon Conway y me resulto muy fascinante el como con tan solo 3 simples reglas se pueda llegar a simular un compartamiento extraordinario, Asi que motivado y emocionado decidi hacer la implementacion de este juego usando python y pygame de base para poder darle vida a este maravilloso juego y el resultado fue algo fascinante con el cual podemos entender y visualizar el comportamiento de este juego y poder visualiar multiples patrones que nacen de tan solo una configuracion inicial de un cojunto de celulas vivas.

<div >
<img  style="display: block; margin: 5 auto" src="docs/ezgif-12a5b859dc35bc1b.gif">
</div>

## Comportamiento

El juego de la vida se basa en mundo bidimensional infinito donde cada celda representa una celula que tiene 2 estados: viva o muerta, para determinar el estado de una celula en su siguiente generacion es donde entra en juego las 4 simples reglas que el matematico jhon conway establecio:

- Cualquier celda viva que tenga menos de dos vecinas vivas muere, como si estuviera infrapoblada.
- Cualquier celda viva que tenga dos o tres vecinas vivas sobrevive hasta la siguiente generación.
- Toda celda viva que tenga más de tres vecinas vivas muere, como si estuviera sobrepoblada.
- Toda celda muerta que tenga exactamente tres vecinas vivas se convierte en una celda viva, como si se hubiera reproducido.

Estas relgas son muy interesantes debido a que si lo vemos con un comportamiento natural del mundo en el que vivimos podemos observar que una celula muere por sobrepoblacion o por soleda o si simplemente se dan las condiciones perfectas en su entorno puede surgir la vida, increible ¿no?, De ahi surge sun nombre del juego de la vida, por que simula la vida con tan solo 4 reglas se puede determina si hay vida o no.

#### Generaciones

El juego tiene lo que se denomina generaciones donde cada generacion es simplemente una iteracion de un estado actual del mundo el cual con las reglas anteriores podemos obtener un patron aleatorio, podemos iterar tantas generaciones queramos o simplemente podemos obtener infinitas generaciones, pero ¿ habra algun momento donde finalice? Si. Se puede llegar al caso donde partiendo de una configuracion inicial
se llegue a una generacion donde simplemente todas las celulas mueren este se considera un estado final del juego, pero por otro lado dado una configuracion incial podemos tener infinitas generaciones ya que llega un estado donde en cada generacion va un conjunto de celulasvivas donde formaran una estructura donde en cada generacion viven y muere, esto se conoce como estructura ciclica.

# Implementacion

Para la implementacion de este juego vamos a contar con un mundo finito de nxm para efectos practicos, este mundo va ser representado como una matriz donde cada posicion representara el estado de una celula, 0 representa ausencia de vida y 1 representa la vida, en cada iteracion (generacion) vamos a analizar los vecinos adyancentes incluyendo las diagonales de cada celula con el fin de determina su siguiente estado para la siguiente generacion. para esto se implemento en python un motor donde esta toda la logica incluyendo las reglas del juego, y por otro lado usamos pygame para darle vida visualmente al comportamente de este juego.

## Optimizaciones

### Analizando estados

A medida que desarrollaba el juego y probaba multiples configuciones con diferentes tamaños del mundo finitos es que a medida que el mundo se hace mas grande la complejida computacional para generar cada generacion aumenta haciendo para mundos muy grandes el algoritmo es muy lento ya toca analizar nxm posiciones, Supongamos que tenemos una matriz de 10000x10000 significa que en cada generacion se tangan que analizar 100.000.000 de posiciones esto se reducen a tener una complejidad de `O(n²)` haciendo muy lento el juego para matrices muy grandes.

<div >
<img  style="display: block; margin: 5 auto" src="docs/image-8.png">
<p style="text-align: center">Matriz de 25x25, Celulas vivas: 5</p>
</div>

##### Solucion

Analizando el problema a fondo, en mi mente surgio la pregunta _¿Y si no tendria que analizar todo el mundo ?_ esto me llevo a pensar una solucion ingeniosa donde en vez de tener que analizar nxm posiciones solo analizo las posiciones donde tengan mas probabilidad de mutar, Oh vaya sorpresa me lleve,¿ cuales serian estas posiciones ? nada mas y nada menos que las posiciones donde hay una celula viva. Centrandonos en las posiciones que tienen una celula viva ya que son las que tienen el poder de determinar el estado de las celulas a su alrededor por ende reducimos el problema de analizar todo el mundo `O(n²)` a simplemente `O(n)` donde `n` ya representa el numero de celulas vivas en cada generacion. Para esto en vez de analizar todo el mundo solo me centro en analizar las posiciones alrededor de una celula viva lo cual es una complejidad de O(3x3) ya incluye las diagonales, en pocas palabas es analizar el mundo pero a una escala reducida de 3x3 alrededor de una celula viva, esto reduce un monto la complejidad computacional al momento de computar cada generacion.

<div >
<img  style="display: block; margin: 5 auto" src="docs/image-7.png">
<p style="text-align: center">Area delimidata a explorar</p>
</div>

##### Ejemplo practico

Analizando la generacion de la imagen donde tenemos una mundo de 25x25 y solo hay 5 celulas vivas, solo iteramos 5 x 3x3 x 3x3 ¿por que? Tenemos 5 celulas vivas, eso significa que hay que explorar las celulas a su alreder incluyendosoe asi misma lo cual seria 3x3 (como se muestra en el area delimitada en la imagen anterior), ahora analizar una celula para determinar su estado es 3x3 por que toca analizar la cantidad de vecinos para saber su proximo estado, esto nos da un resultado de 324 iteraciones, es simplemente 625 > 405.

#### Efectos secundarios

Ahora vale la pena detenernos a analizar estos puntos:

- **¿Que pasa si hay muchas celulas vivas en mi tablero?** : Efectivamente el `n` se hace cada vez mas grande hasta llegar a un punto que es igual a la complejidad inicial de `O(n²)`ya que habria la misma cantidad de celuals vivas que posiciones en el mundo pero gracias a las reglas del juego es practicamente imposible que esto pase por ende siempre el numero de celulas vivas va ser menor que el total de posiciones del mundo.

- En tableros pequeños como 10x10 con un numero de 5 celulas vivas seria seria 100 < 405, Esto es contradictorio por que basicamente estamos interando mas veces que el tamaño de la matriz, pero mas adelante vamos a ver como mitigar este problema usando programacion dinamica.

<hr>

### Subproblemas repetidos

Logramos reducir una complejidad de `O(n²)` a `O(n)` pero analicemos que pasa con las celulas que estan muy cercas entre si, por ejemplo:

<div >
<img  style="display: block; margin: 5 auto" src="docs/image-3.png">
<p style="text-align: center;">Matriz de 3x5, Celulas vivas: 3</p>
</div>

Analicemos este mini mundo de 3x5 podemos observar que tenemos celulas vivas en las posiciones `(1,1) (1,2) (1,3)` aplicando nuestro algoritmo a la celula `(1,1)` analizamos las posiciones que esta celula viva puede influir a mutar asi que tenemos las siguientes posiciones incluyendose asi misma: `(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)`.

El algorimto recorre cada una de estas posiciones y determina su estado para la proxima generacion quedando como resultado:

```
(0,0) -> 0
(0,1) -> 0
(0,2) -> 1
(1,0) -> 0
(1,1) -> 0
(1,2) -> 1
(2,0) -> 0
(2,1) -> 0
(2,2) -> 1
```

Hasta el momento bien hemos replicado como se comporta el algoritmo, pero pasemos a analizar la siguiente celula viva `(1,2)`, Generamos las posiciones vecinas: `(0,1), (0,2), (0,3), (1,1), (1,2), (1,3) (2,1), (2,2), (2,3)` y procedemos a determinar sus futuros estados:

```
(0,1) -> 0 <- Repetido
(0,2) -> 1 <- Repetido
(0,3) -> 0
(1,1) -> 0
(1,2) -> 1 <- Repetido
(1,3) -> 0
(2,1) -> 0
(2,2) -> 1 <- Repetido
(2,3) -> 0
```

Como se puede observar hay estados en el que el paso anterior ya fuero calculados por el hecho de estar cercar de la celula viva actual `(1,2)`, Asi que estamos verificando celulas que ya hemos calculado anteriormente.

#### solucion

Como se pudo observar estamos analizando problemas que ya hemos analizado en pasos anteriores, para esto usamos un enfoque de programacion dinamica `top-down` de modo que a medida que verificamos cada posicion la alamacenamos en un **set()** para posteriormente en cada interacion verificar si ya hemos verificado esa posicion de tal modo evitar verificarla de nuevo.

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
   Es buena práctica aislar las dependencias del proyecto.

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

- **Clic Izquierdo:** Colocar celula viva.
- **Clic Derecho:** Borrar celula viva.
- **Tecla S:** Inicia/Pausa la simulacion.
- **Tecla C:** Limpia el tablero y reinicia el mundo.
- **Tecla B:** Activa/Desactiva la cuadricula.
- **Tecla M:** Dismuniye el tiempo entre generaciones.
- **Tecla N:** Aumenta el tiempo entre generaciones.
