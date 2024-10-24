import random

from practica import joc
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__directions = ["N", "S", "E", "O"]
        self.__visited = set()
        self.__stack = []  # Pila para almacenar el camino
        self.__path_to_goal = []  # Almacena el camino hasta el destino

    def pinta(self, display):
        pass

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        pos_actual = self.posicio

        # Si ya hemos alcanzado el destino, esperamos
        if percepcio["DESTI"] == pos_actual:
            return Accions.ESPERAR

        # Si aún no hemos explorado nada, comenzamos el DFS
        if not self.__stack:
            self.__stack.append((pos_actual, None))  # (Posición, dirección de origen)
            self.__visited.add(pos_actual)

        # Mientras la pila no esté vacía, realizamos la búsqueda en profundidad
        while self.__stack:
            current_pos, last_move = self.__stack.pop()

            # Exploramos todas las direcciones posibles desde la posición actual
            for direction in self.__directions:
                # Obtenemos la nueva posición posible
                next_pos = self.__obte_pos(current_pos, 1, direction)

                # Verificamos si la posición es válida y no ha sido visitada
                if next_pos not in self.__visited and self.__es_pos_valida(percepcio, next_pos):
                    self.__visited.add(next_pos)
                    self.__stack.append((current_pos, direction))
                    self.__stack.append((next_pos, None))  # Seguimos explorando desde la nueva posición
                    return Accions.MOURE, direction  # Nos movemos a la nueva posición

        # Si no hay más movimientos posibles, esperamos
        return Accions.ESPERAR

    def __es_pos_valida(self, percepcio: dict, pos: tuple[int, int]) -> bool:
        """Verifica si una posición es accesible."""
        x, y = pos
        if 0 <= x < len(percepcio["TAULELL"]) and 0 <= y < len(percepcio["TAULELL"][0]):
            return percepcio["TAULELL"][x][y] == " "  # Solo nos movemos a casillas libres
        return False

    @staticmethod
    def __obte_pos(pos_original: tuple[int, int], multiplicador: int, direccio: str):
        """Obtiene la nueva posición en función de la dirección."""
        MOVS = {
            "N": (0, -1),
            "O": (-1, 0),
            "S": (0, 1),
            "E": (1, 0),
        }
        return (
            MOVS[direccio][0] * multiplicador + pos_original[0],
            MOVS[direccio][1] * multiplicador + pos_original[1],
        )
