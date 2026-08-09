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

Hace un año me topé con un juego llamado `game-of-life` del matemático británico John Conway y me resultó muy fascinante cómo, con tan solo 4 simples reglas, se puede llegar a simular un comportamiento tan complejo y extraordinario. Así que, motivado y emocionado, decidí hacer la implementación de este juego usando Python y Pygame de base para poder darle vida. El resultado fue algo fascinante con el cual podemos entender y visualizar el comportamiento de este juego, además de observar múltiples patrones que nacen de tan solo una configuración inicial de un conjunto de células vivas.

<div>
<img style="display: block; margin: 0 auto" src="docs/ezgif-12a5b859dc35bc1b.gif">
</div>

## Comportamiento

El Juego de la Vida se basa en un mundo bidimensional infinito donde cada celda representa una célula que tiene 2 estados: viva o muerta. Para determinar el estado de una célula en su siguiente generación es donde entran en juego las 4 simples reglas que el matemático John Conway estableció:

- Cualquier célula viva que tenga menos de dos vecinas vivas muere, como si estuviera infrapoblada.
- Cualquier célula viva que tenga dos o tres vecinas vivas sobrevive hasta la siguiente generación.
- Toda célula viva que tenga más de tres vecinas vivas muere, como si estuviera sobrepoblada.
- Toda célula muerta que tenga exactamente tres vecinas vivas se convierte en una célula viva, como si se hubiera reproducido.

Estas reglas son muy interesantes debido a que, si lo vemos en relación con el comportamiento natural del mundo en el que vivimos, podemos observar que una célula muere por sobrepoblación o por soledad, o si simplemente se dan las condiciones perfectas en su entorno puede surgir la vida, ¿increíble, no? De ahí surge el nombre del juego de la vida, porque simula la vida y con tan solo 4 reglas se puede determinar si hay vida o no.

#### Generaciones

El juego cuenta con lo que se denomina generaciones, donde cada generación es simplemente una iteración de un estado actual del mundo en la cual, con las reglas anteriores, podemos obtener un patrón resultante. Podemos iterar tantas generaciones como queramos o simplemente obtener infinitas generaciones. Pero, ¿habrá algún momento donde finalice? Sí. Se puede llegar al caso en donde, partiendo de una configuración inicial, se alcance una generación donde simplemente todas las células mueran; este se considera un estado final del juego. Por otro lado, dada una configuración inicial, podemos tener infinitas generaciones si se llega a un estado recurrente donde un conjunto de células vivas forma una estructura que nace y muere en un ciclo; esto se conoce como estructura cíclica.

## Implementación

Para la implementación de este juego vamos a contar con un mundo finito de $N \times M$ para efectos prácticos. Este mundo va a ser representado como una matriz donde cada posición representará el estado de una célula (0 representa ausencia de vida y 1 representa vida). En cada iteración (generación) vamos a analizar los vecinos adyacentes, incluyendo las diagonales de cada célula, con el fin de determinar su siguiente estado para la siguiente generación. Para esto se implementó en Python un motor donde está toda la lógica incluyendo las reglas del juego y, por otro lado, usamos Pygame para darle vida visualmente al comportamiento de este juego.

## Optimizaciones

### Analizando estados

A medida que desarrollaba el juego y probaba múltiples configuraciones con diferentes tamaños de mundos finitos, noté que a medida que el mundo se hace más grande, la complejidad computacional para generar cada generación aumenta. Para mundos muy grandes el algoritmo resulta lento, ya que le toca analizar las $N \times M$ posiciones del tablero. Supongamos que tenemos una matriz de $10000 \times 10000$: significaría que en cada generación se tendrían que analizar 100.000.000 de posiciones, lo que se reduce a tener una complejidad de $O(N \times M)$ (o $O(N^2)$ en matrices cuadradas), haciendo muy lento el juego para matrices muy grandes.

<div>
<img style="display: block; margin: 0 auto" src="docs/image-8.png">
<p style="text-align: center">Matriz de 25x25, Células vivas: 5</p>
</div>

##### Solución

Analizando el problema a fondo, en mi mente surgió la pregunta: *¿Y si no tuviera que analizar todo el mundo?* 

Esto me llevó a pensar en una solución ingeniosa donde, en vez de tener que analizar $N \times M$ posiciones, solo analizo las posiciones que tienen más probabilidad de mutar: **las células vivas y su entorno inmediato**. Centrarnos en las posiciones que tienen una célula viva (ya que son las que tienen el poder de determinar el estado de las células a su alrededor) nos permite reducir el problema de analizar todo el mundo a simplemente enfocarnos en $N$, donde $N$ representa el número de células vivas en cada generación ($O(N)$).

Para esto, en vez de analizar todo el mundo, solo me centro en analizar las posiciones alrededor de una célula viva ($3 \times 3$, es decir, 9 celdas candidatas). A su vez, para determinar si cada una de esas 9 candidatas vive o muere en la siguiente generación, es necesario analizar nuevamente sus $3 \times 3$ (9) celdas vecinas. Esto nos da una complejidad de $N \times (3 \times 3) \times (3 \times 3) = N \times 81$ operaciones por generación.

<div>
<img style="display: block; margin: 0 auto" src="docs/image-7.png">
<p style="text-align: center">Área delimitada a explorar</p>
</div>

##### Ejemplo práctico

Analizando la generación de la imagen anterior donde tenemos un mundo de $25 \times 25$ ($625$ posiciones totales) y solo hay 5 células vivas ($N = 5$):

- **Enfoque tradicional:** Evalúa las $625$ posiciones de la matriz.
- **Enfoque enfocado en células vivas:** Evaluamos $5 \text{ células} \times 9 \text{ candidatas} \times 9 \text{ vecinos} = 405 \text{ iteraciones}$.

Como se observa, $405 < 625$, logrando reducir el número de operaciones requeridas por ciclo.

#### Efectos secundarios

Ahora vale la pena detenernos a analizar estos puntos:

- **¿Qué pasa si hay muchas células vivas en mi tablero?:** A medida que la cantidad de células vivas $N$ aumenta, el total de operaciones $81N$ crece hasta igualar o superar la complejidad inicial de analizar el tablero completo. Afortunadamente, gracias a las reglas del juego, es prácticamente imposible que la densidad de células vivas cubra la totalidad de la matriz de forma sostenida.
- **Ineficiencia en tableros pequeños o densos:** En un tablero de $10 \times 10$ ($100$ celdas totales) con solo $5$ células vivas, la fórmula requeriría $5 \times 81 = 405$ iteraciones. En este caso $405 > 100$, lo que resulta contradictorio ya que estaríamos iterando más veces que el tamaño de la matriz debido a la sobrecarga de reevaluar zonas vecinas.

Más adelante veremos cómo mitigar y resolver esta ineficiencia aplicando **programación dinámica**.

---

### Subproblemas repetidos

Logramos reducir la búsqueda enfocándonos en las células vivas, pero analicemos qué pasa con las células que están muy cerca entre sí. Por ejemplo:

<div>
<img style="display: block; margin: 0 auto" src="docs/image-3.png">
<p style="text-align: center;">Matriz de 3x5, Células vivas: 3</p>
</div>

En este mini mundo de $3 \times 5$, podemos observar que tenemos células vivas en las posiciones `(1,1)`, `(1,2)` y `(1,3)`. Aplicando nuestro algoritmo a la célula `(1,1)`, analizamos las posiciones que esta célula viva puede influir a mutar, así que tenemos las siguientes posiciones incluyéndose a sí misma: `(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)`.

El algoritmo recorre cada una de estas posiciones y determina su estado para la próxima generación quedando como resultado:


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

Hasta el momento bien, hemos replicado cómo se comporta el algoritmo. Pero pasemos a analizar la siguiente célula viva `(1,2)`. Generamos las posiciones vecinas: `(0,1), (0,2), (0,3), (1,1), (1,2), (1,3), (2,1), (2,2), (2,3)` y procedemos a determinar sus futuros estados:


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

Como se puede observar, hay estados que en el paso anterior ya fueron calculados por el hecho de estar cerca de la célula viva actual `(1,2)`. Así que estamos verificando células que ya hemos calculado anteriormente.

#### Solución

Como se pudo observar, estamos analizando subproblemas que ya hemos procesado previamente. Para solucionar esto y resolver los efectos secundarios, utilizamos un enfoque de **programación dinámica (*top-down* con memoización)**. 

A medida que verificamos cada posición, la almacenamos en un **`set()`** para posteriormente, en cada iteración, consultar si esa celda ya fue procesada. De este modo evitamos calcular de nuevo subproblemas repetidos, garantizando evaluar cada posición candidata **exactamente una vez** por generación.

## Instalación y Uso

Para probar y visualizar el Juego de la Vida en tu propia máquina, sigue estos pasos:

### Requisitos previos

Asegúrate de tener instalado en tu sistema:

- **Python 3.x** (preferiblemente 3.12 o superior).
- **Pip** (Gestor de paquetes de Python).

### Pasos de instalación

1. **Clona este repositorio:**

```bash
git clone https://github.com/suaadev/conway-s-game-of-life.git
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
