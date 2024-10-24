import random

from practica import joc
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.visitat = set()
     #   self.__proves = [
     #       (Accions.MOURE, "E"),
     #       (Accions.MOURE, "S"),
     #       (Accions.MOURE, "N"),
     #       (Accions.MOURE, "O"),
     #       (Accions.BOTAR, "S"),
     #       (Accions.BOTAR, "N"),
     #       (Accions.BOTAR, "E"),
     #       (Accions.BOTAR, "O"),
     #       (Accions.POSAR_PARET, "S"),
     #       (Accions.POSAR_PARET, "N"),
     #       (Accions.POSAR_PARET, "E"),
     #       (Accions.POSAR_PARET, "O"),
     #   ]
     

    def pinta(self, display):
        pass

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        #if self.__proves:
        #    acc = random.choice(self.__proves)
        #    return acc
        parets = set(percepcio["PARETS"]) #Llista de les cordenades de les parets
        #En principi no hi pot haver dues parets a la mateixa cordenada, peró es fa com a set per si a cas
        desti=  percepcio["DESTI"] #Ubicació casella destí
        posicio= percepcio["AGENTS"][self.nom] #Guardem posicó actual del agent
        
        cami = self.cerca_prof(posicio, desti, parets)
        
        if cami:
            seguent_moviment = cami[0]
            return seguent_moviment
        
        return Accions.ESPERAR
    
    def cerca_prof(self, posicio, desti, parets):
        stack = [(posicio, [])]  # Pila que guarda (posició actual, camí explorat)
        visitat = set()  # Set que guarda les posicions ja visitades per evitar bucles

        while stack: 
            actual, cami = stack.pop()  # Extreu la posició actual del agent i el camí

            if actual == desti:
                return cami  # Si ha arribat al destí retorna el camí

            if actual not in visitat:
                visitat.add(actual)  # Si la posició explorada no está visitada li posa
                x, y = actual

                # Direcciones posibles (N, S, E, O)
                directions = {
                    "N": (x, y - 1),
                    "S": (x, y + 1),
                    "E": (x + 1, y),
                    "O": (x - 1, y),
                }
                # nx i ny noves cordenades que es calcularan en base a la posició actual dir
                for dir, (nx, ny) in directions.items():
                    # Comprovació de si la nova posició és accessible o no
                    if (0 <= nx < self.__mida_taulell[0] and
                            0 <= ny < self.__mida_taulell[1] and
                            (nx, ny) not in parets):
                        #Comprova que nova posició no sigui pora del taulell o estigui en la tupla parets
                        stack.append(((nx, ny), cami + [dir]))  # Agrega a la pila

        return []  # Al no trobar camí retorna una llista buida.

