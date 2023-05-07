# GOKU SMART
### Integrantes:
- Valery Molina Burgos - 1942630
- Maria Camila Jaramilo Andrade - 1942386
- Juan Esteban Betancourt Narváez - 1927215


Este proyecto tiene como objetivo la creación de un goku inteligente, el cual tiene como objetivo encontrar dos esferas del dragon en un mapa de 10x10 casillas, las cuales pueden tener enemigos que afectan el bienestar de Goku o semillas del Ermitaño que le otorgan beneficios. Esto se logrará por medio de la implementación de algoritmos de Inteligencia Artificial. 

El programa cuenta con **cinco** algoritmos de busqueda:

**Busqueda No informada**
- Busqueda por Amplitud
- Busqueda por Costo Uniforme
- Busqueda por Profundidad

**Busqueda Informada**
- Busqueda Avara
- Busqueda A*

### Solución
Para la solución se mostrara de forma grafica el camino que tomará Goku según la busqueda implementada, adicional a esto para cada búsqueda se genera un reporte con la cantidad de nodos expandidos, profundidad del árbol y tiempo de cómputo. En el caso de los algoritmos de Costo Uniforme y A* se muestra también el costo de la solución encontrada. 

### Clonación del repositorio
```
git clone https://github.com/camyj2010/IA_Proyecto_1.git
```

### Instalación de dependencias

El programa requiere dos dependencias básicas: ```PyGame``` y ```pygame_gui```. Estas se pueden instalar mediante el archivo de requerimientos.

- **Opcional**: creación de un [ambiente virtual de Python](https://docs.python.org/3/library/venv.html)
```bash
python -m venv .venv
cd .venv/Scripts
./activate
```

- Instalación del archivo ```requirements.txt```
```bash
pip install -r requirements.txt
```

### Ejecución del programa
Para ejecutar el programa basta con ejecutar el archivo ```interfaz.py```, para esto, se debe ubicar en la carpeta del programa y ejecutar el siguiente comando:
```bash
python interfaz.py
```
También es posible ejecutar el programa desde cualquier IDE.

### Subir nuevos mapas
El programa tiene una función para subir tus propios mapas de prueba, solo se debe ir a la opción "Map" y dar click en "Upload New Map", luego de esto, seleccionar el o los mapas que se quiera subir y dar click en aceptar.
También es posible subir los mapas copiando los archivos y pegandolos en la carpeta *map* de los archivos del programa.