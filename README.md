# DotCSV-pix2pix-demo

Este proyecto tiene por objetivo demostrar una aplicación de utilidad de la arquitectura Pix2pix (https://arxiv.org/abs/1611.07004). Este
proyecto ha sido motivado por el concurso de DotCSV publicado en https://www.youtube.com/watch?v=BNgAaCK920E&t=607s.

El caso propuesto consiste en eliminar de manera automática imperfecciones faciales. Desde la publicación del paper pix2pix original, han
surgido otros métodos que parecen resolver este problema mejor (por ejemplo, https://arxiv.org/abs/1804.07723), pero ese no es el
objetivo del proyecto.

El proyecto se ha basado en el código del notebook de pix2pix disponible en la documentación de Tensorflow (https://www.tensorflow.org/beta/tutorials/generative/pix2pix).

## Arquitectura de la red
La arquitectura se ha dejado intacta con respecto al código original. Consiste en un esquema tipo GAN. El generador es de tipo U-Net (una arquitectura codificador-decodificador con skip-connections entre las capas análogas de cod- y decodificador). El discriminador se denomina PatchGAN y consiste en un conjunto de discriminadores, cada uno "vigilando" una región de 70x70 píxeles.

La justificación de este tipo de discriminador, según los autores, reside en la observación de que una regulación L1 ó L2 logra una calidad más o menos buena en las características de baja frecuencia de la imagen generada, pero no en las de alta frecuencia. En otras palabras, que la imagen generada es algo borrosilla. Al discriminar de manera independiente regiones más pequeñas se pretende resolver este problema. En los experimentos mostrados, no parece que haya diferencias apreciables visualmente entre discriminar regiones de 70x70 o discriminar la imagen completa, pero según su propia métrica (consistente en medir la calidad de la segmentación de una red tipo FCN) es ligeramente menor. No he experimentado personalmente, pero según eso el PatchGAN no tendría ningún beneficio objetivo en el resultado, aunque sí que imagino que hará la computación de la discriminación más eficiente.

## Datos de entrenamiento
El esquema original toma una imagen que consiste en dos mitades juntas: la primera mitad corresponde a la imagen real de una fachada que se quiere generar y la segunda del dibujo que se emplea como input.

El esquema que se ha empleado es idéntico. En este caso la primera mitad corresponde a la imagen original de una cara y la segunda a la misma imagen donde se han eliminado aleatoriamente algunas regiones. Más adelante se explica cómo se lleva a cabo esta eliminación aleatoria. A continuación se muestra un ejemplo:
                                                IMAGEN EJEMPLO DE DATOS DE ENTRADA!!
                                                
Los datos se han tomado de https://www.kaggle.com/dataturks/face-detection-in-images. En el repositorio se encuentra el archivo face_detection.json que contiene toda la información necesaria. También los scripts necesarios para crear el dataset.

## ¿Cómo crear las eliminaciones aleatorias en las imágenes?
A continuación se detallan los pasos seguidos:
1. Crear máscaras en paint. Se crean las formas que se van a borrar en las imágenes. Son imágenes de 50x50. Algunos ejemplos a continuación.
                                                IMAGEN EJEMPLO DE DATOS DE MÁSCARAS!!
2. Para cada imagen original se escogen aleatoriamente entre 1 y el máximo de máscaras que se quiera. En nuestro caso 2, ya que 3 era demasiado borrar. Para cada máscara se escoge un escalado aleatorio entre 1 y 5 veces, y una posición aleatoria con la única condición de que quede dentro de la imagen.
3. Una vez escogidas la escala y posición aleatorias, se multiplica la imagen por las máscaras. Este proceso se repite varias veces (3 en nuestro caso, ya que 5 generaba demasiadas imágenes y había problemas varios).
4. Se "pegan" juntas la imagen original y la imagen "enmascarada", ambas escaladas para medir 256x256 y así coincidir con las dimensiones establecidas en el paper.

## Cómo configurar el entorno para entrenar el modelo

## Experimentos futuros
--> Utilizar (255, 0, 255) en lugar de negro (hay negro en muchas imágenes y el sistema se confunde)
--> Utilizar una función de error que dé más peso a los píxeles que se han borrado. En los primeros epochs el sistema aprende a copiar casi toda la imagen. A partir de ahí, el modelo mejora muy lentamente. Este sistema se ha creado para convertir imágenes completas en otra cosa...
