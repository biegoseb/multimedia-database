# Proyecto 3 - Base de Datos 2

## Integrantes

| Nombre y Apellidos |
|---|
|Diego Enciso Lozano |
|Luis Jauregui Vera	 |
|Alonso Barrios Silva|


## Tabla de contenido
<details>
<summary>"Clic para navegar: "</summary>

- [Introducción](#Introducción)
- [Fundamentos y descripción de las técnicas](#Fundamentos-y-descripción-de-las-técnicas)
- [Resultados experimentales](#Resultados-experimentales)

</details>

## Introducción

Mediante este proyecto se busca entender y construir una estructura multidimensional óptima para dar soporte a las búsquedas y recuperación eficiente de imágenes mediante un servicio de reconocimiento facial.
Para ello, se implementa la búsqueda KNN y la búsqueda por rango, las cuales reciben como parámetro K elementos a recuperar y un radio de búsqueda respectivamente.
Para este proyecto se hizo uso de una colección de imágenes dadas por el profesor.

En este informe se muestra las comparaciones al usar queries con los mejores resultados.

## Fundamentos y descripción de las técnicas

### Backend

#### R-Tree

Lo primero que se hizo fue implementar el índice R-tree. Este tiene los siguientes métodos:

1.  Constructor

![r-tree-constructor](./img/r-tree-constructor.png)

Lo más resaltante del constructor es que el árbol debe de tener una dimensión de 128, esto debido al tamaño del vector característico.

2. Extract features:

![r-tree-extract-features](./img/r-tree-extract-features.png)

Este método se encarga de extraer los vectores característicos de cada una de las imágenes dadas.

**Descripción del código:** El segundo *for* (línea 6) se encarga de recorrer cada una de las imágenes de los archivos. Luego se encarga de procesar las imágenes. En el *if* de la línea 10 se encarga de comprobar que efectivamente haya mínimo un rostro en la imágen. Posteriormente, con ayuda de la librería *face_recognition* se extraen los vectores caraterísticos. Por último, se guarda el nombre de la imagen junto con sus vectores característicos en el diccionario *face_encodings*.

3. Insert all

![r-tree-insert-all](./img/r-tree-insert-all.png)

Este método nos ayuda a extraer los datos más rápidamente, esto con el fin de poder mostrarlos sin necesidad de usar varias veces la estructura.

**Descripción del código:** Se recorre el diccionario *face_encodings* y se guarda los datos (nombre de la persona, ruta de la imagen, vector característico) en otro diccionario el cual tendrá como key un *id*. Finalmente, en el R-Tree se inserta el *id* y el punto, el cual es extraido en la línea 5 y en la línea siguiente duplica este punto debido a que está en 2 dimensiones.

4. Mindist

![r-tree-mindist](./img/r-tree-mindist.png)


## Resultados experimentales
Para la parte experimental se comparó la eficiencia en tiempos de ejecución del KNN de la estructura RTree y el KNN secuencial para esto se incrementa el tamaño de las colecciones dadas (N).

  | Tiempo   | KNN-RTree  	 |  KNN-Secuencial |
  |:-------:|:------------:|:----------------:|
  |  N = 100 |               |                 |
  |  N = 200 |               |                 |
  |  N = 400 |               |                 |
  |  N = 800 |               |                 |
  | N = 1600 |               |                 |
  | N = 3200 |               |                 |
  | N = 6400 |               |                 |
  |N = 12800 |               |                 |


**Discusión y Análisis**