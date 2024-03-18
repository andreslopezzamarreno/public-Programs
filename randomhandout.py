import numpy as np
import math

def repartir_cosas_azar(cosas, personas):
    num = math.ceil(len(cosas)/len(personas))
    
    np.random.shuffle(cosas)
    np.random.shuffle(personas)
    
    while len(cosas) >= 0:
        
        movieguapa = personas
        for i in range(num):
            cosa = np.random.choice(cosas)
            cosas = list(filter(lambda x: x != cosa, cosas))

            if len(movieguapa)-1 != 0:
                    persona = np.random.choice(movieguapa)
                    movieguapa = list(filter(lambda x: x != persona, movieguapa)) 
        print(cosa,persona)

if __name__ == "__main__":
    cosas_a_repartir = ['Ambiental', 'Primera','Segunda', 'Evangelio', 'Preces', 'Preces2', 'Preces3', 'Preces4', 'Preces5', 'Preces6', 'Preces7']
    cosas_a_repartir2 = ['Ambiental', 'Primera','Segunda', 'Evangelio', 'Preces']
    personas = ['Andres', 'moreno', 'stanis', 'carlos']
    repartir_cosas_azar(cosas_a_repartir2, personas)
