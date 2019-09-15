# DotCSV-pix2pix-demo

Este proyecto tiene por objetivo demostrar una aplicación de utilidad de la arquitectura Pix2pix (https://arxiv.org/abs/1611.07004). Este
proyecto ha sido motivado por el concurso de DotCSV publicado en https://www.youtube.com/watch?v=BNgAaCK920E&t=607s.

El caso propuesto consiste en eliminar de manera automática imperfecciones faciales. Desde la publicación del paper pix2pix original, han
surgido otros métodos que parecen resolver este problema mejor (por ejemplo, https://arxiv.org/abs/1804.07723), pero ese no es el
objetivo del proyecto.

El proyecto se ha basado en el código del notebook de pix2pix disponible en la documentación de Tensorflow (https://www.tensorflow.org/beta/tutorials/generative/pix2pix).

## Arquitectura de la red
La arquitectura se ha dejado intacta con respecto al código original. Consiste en un esquema tipo GAN. El generador es de tipo U-Net (una arquitectura codificador-decodificador con skip-connections entre las capas análogas de cod- y decodificador). El discriminador se denomina PatchGAN y consiste en un conjunto de discriminadores, cada uno "vigilando" una región de 70x70 píxeles.

La justificación de este tipo de discriminador, según los autores, reside en la observación de que una regulación L1 o L2 logra una calidad más o menos buena en las características de baja frecuencia de la imagen generada, pero no en las de alta frecuencia. En otras palabras, que la imagen generada es algo borrosilla. Al discriminar de manera independiente regiones más pequeñas se pretende resolver este problema. En los experimentos mostrados, no parece que haya diferencias apreciables visualmente entre discriminar regiones de 70x70 o discriminar la imagen completa, pero según su propia métrica (consistente en medir la calidad de la segmentación de una red tipo FCN) es ligeramente menor. No he experimentado personalmente, pero según eso el PatchGAN no tendría ningún beneficio objetivo en el resultado, aunque sí que imagino que hará la computación de la discriminación más eficiente.


