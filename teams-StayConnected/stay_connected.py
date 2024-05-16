"""
Este script mantiene abierta una instancia de Notepad mientras simula la escritura automática de letras aleatorias a intervalos regulares. La ejecución se detiene mediante la combinación de teclas "Ctrl+C". Se requiere la biblioteca 'keyboard' para su funcionamiento.

Atajos de teclado utilizados:
- 'Win+1': Activa o selecciona la ventana de la aplicación con el índice 1 en la barra de tareas de Windows.
- 'Ctrl+C': Detiene la ejecución del programa.

Variables globales:
- CHAR_COUNT: Número de caracteres escritos en Notepad.
- TIME: Intervalo de tiempo en segundos entre la escritura de caracteres.
"""
import time
import subprocess
import random
import string
import keyboard

def main():
    """
    Esta función es la entrada principal del programa. Controla el flujo principal 
    del programa, manteniendo abierta una instancia de Notepad y simulando la 
    escritura automática de letras aleatorias.
    """
    keyboard.press_and_release("win+1")
    time_sleep = 200

    with subprocess.Popen(["notepad.exe"]) as notepad_process:
        try:
            time.sleep(0.5)
            tiempo_inicial = time.time()
            while True:
                tiempo_transcurrido = time.time() - tiempo_inicial
                if tiempo_transcurrido >= time_sleep:
                    tiempo_inicial = time.time()
                    random_letter = random.choice(string.ascii_lowercase)
                    keyboard.write(random_letter)

                if notepad_process.poll() is not None:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            notepad_process.terminate()
            notepad_process.wait()

if __name__ == "__main__":
    main()
