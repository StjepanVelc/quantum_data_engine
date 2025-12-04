import random


class Stabilizer:
    """
    Modul koji stabilizira čvorove u grafu.
    Ovo imitira prirodnu tendenciju sustava da smanjuje
    ekstremne vrijednosti i vraća balans.
    """

    @staticmethod
    def stabilize_nodes(nodes):
        for node in nodes:
            # Amplitude preblizu 0 ili 1 se lagano guraju prema sredini (0.5)
            node.amplitude += (0.5 - node.amplitude) * 0.1

            # Ako je energija previsoka, smanjuj malo (sistem balansira)
            if node.energy > 80:
                node.energy -= random.uniform(1, 3)

            # Ako je preniska, malo je podigni
            elif node.energy < 20:
                node.energy += random.uniform(1, 3)

            # Ograniči domet
            node.energy = max(0, min(100, node.energy))
