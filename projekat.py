import random

def generate_individual(dimensions):
    """
    Generiše jednu jedinku: redosled pravougaonika + rotacije.

    dimensions (list[dict]): lista pravougaonika sa ključevima:
        - 'width': širina
        - 'height': visina
        - 'number': koliko komada tog pravougaonika
    """
    shape_order = []
    for idx, rect in enumerate(dimensions):
        shape_order.extend([idx] * rect["number"])

    random.shuffle(shape_order)

    rotations = [random.randint(0, 1) for _ in range(len(shape_order))]

    return (shape_order, rotations)


def generate_population(pop_size, dimensions):
    """
    Generiše početnu populaciju sa datim brojem jedinki.
    
    :param pop_size: broj jedinki u populaciji
    :param dimensions: lista pravougaonika
    :return: lista jedinki (svaka jedinka je tuple: (shape_order, rotations))
    """
    return [generate_individual(dimensions) for _ in range(pop_size)]


def rangiraj_populaciju(populacija, fitnesi):
    """
    Vraća listu (jedinka, fitnes) sortiranu po opadajućem fitnesu.
    """
    return sorted(zip(populacija, fitnesi), key=lambda x: x[1], reverse=True)


def primeni_elitizam(rangirana_populacija, elitizam_broj):
    """
    Vraća elitne jedinke (najbolje u populaciji).
    """
    return [jedinka for jedinka, _ in rangirana_populacija[:elitizam_broj]]


def selektuj_roditelje(rangirana_populacija, broj_roditelja):
    """
    Turnirska selekcija: za svakog roditelja bira najboljeg iz 3 nasumične jedinke.
    """
    roditelji = []
    populacija = [jedinka for jedinka, _ in rangirana_populacija]

    for _ in range(broj_roditelja):
        kandidati = random.sample(populacija, k=3)
        # Može se unaprediti izborom po fitnesu ako se doda lista (kandidat, fitnes)
        roditelji.append(kandidati[0])  # uzima se prvi kao "pobednik"
    return roditelji


# test
if __name__ == "__main__":
    dimensions = [
        {"width": 10, "height": 20, "number": 3},
        {"width": 15, "height": 15, "number": 2}
    ]

    # Generiši populaciju
    populacija = generate_population(10, dimensions)

    # Simulirani fitnesi
    fitnesi = [random.uniform(0.5, 0.95) for _ in populacija]

    # Rangiraj populaciju
    rangirana = rangiraj_populaciju(populacija, fitnesi)

    # Elitizam – top 2
    elitne = primeni_elitizam(rangirana, elitizam_broj=2)

    # Selekcija roditelja – uzmi 6
    roditelji = selektuj_roditelje(rangirana, broj_roditelja=6)

    print("\n Primer jedinke (redosled, rotacije):")
    print(populacija[0])

    print("\n Elitne jedinke:")
    for e in elitne:
        print(e)

    print("\n Odabrani roditelji:")
    for r in roditelji:
        print(r)
