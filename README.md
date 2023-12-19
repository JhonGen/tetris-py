# Tetris-py

Tetris desarrollado en Python como desafío para el proceso de selección en Inventures.

## Supuestos

### Combos
El contador de combos funciona en base a la cantidad de turnos sucesivos que logran eliminar una línea. El combo aumentará de acuerdo a la cantidad de líneas sucesivas eliminadas.

## Consideraciones Técnicas

El cuadro de input que emerge cuando un jugador obtiene un récord superior en puntaje a los existentes puede tener problemas al actualizar lo escrito en él; sin embargo, funciona correctamente. Es necesario presionar la tecla Enter tras ingresar el nombre y el juego debería retornar al menú principal donde se puede ver el ranking actualizado.

## Ejecución

Para ejecutar este código se requiere la versión de Python 3.11.7 y la librería pygame, la cual puede ser instalada fácilmente ejecutando el comando:

```bash
pip install -r requirements.txt
```

Una vez instalados estos componentes, se puede iniciar el juego ejecutando:
```bash
python main.py
```

