# Tracking de Objetos y calculo de la velocidad de movimiento de vehiculos

El presente trabajo tiene por objetivo realizar el tracking de un objeto y calcula su velocidad de movimiento. Para ello se realiza la selección de un área de seguimiento.

- Requerimientos
  - Sistema Operativo: Windows
  - Lenguaje de Programación : Python v3.6
  - Entorno :  Anaconda
  -  Dependencias:
    - OpenCV : conda install -c michael_wild opencv-contrib

- Instrucciones de ejecución
  - Ejecución: $ python ejecucion.py 
  - Seleccionar con el Mouse el área de seguimiento.
  - Presionar Enter

- Caracteristicas de la Cámara
    - Ubicación : Altura 10m
    - Resolución: 1920 x 1080 px
    - Distancia focal: 3.9
    - Campo de visión: 69º
    - Velocidad de fotogramas: 25 fps
    - Distancia Cámara a los objetos: 13.435
    

- Consideraciones
  - Cámara: La cámara se encuentra orientada para tomar una vista lateral.     
  - Algoritmo de seguimiento:  Se utiliza el algoritmo de Lucas Kanade (LK).
  https://en.wikipedia.org/wiki/Lucas%E2%80%93Kanade_method
  - Tipo de Rastreo: KFC

