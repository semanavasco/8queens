import random

BOARD_SIZE = 8


class Individual:
    """
    Represents a board configuration.
    For each board column we specifiy the position of a queen in the Y axis.

    positions: List of queens positions on the Y axis of the board.
    n_conflicts: Amount of conflicts for this configuration.
    """

    positions: list[int] = []
    n_conflicts: int = 0

    def __init__(self, positions: list[int] | None = None):
        self.positions = (
            positions if positions else random.sample(range(BOARD_SIZE), BOARD_SIZE)
        )

        self.n_conflicts = self.fitness()

    def __str__(self):
        return f"positions: {self.positions}\nconflicts: {self.n_conflicts}"

    def has_conflict(self, p1: tuple[int, int], p2: tuple[int, int]) -> bool:
        """
        Checks if 2 queens X and Y coordinates have any `conflicts`.

        p1: X and Y coordinates of queen 1 on the board.
        p2: X and Y coordinates of queen 2 on the board.

        returns: True if queens conflict, False otherwise.
        """
        if (
            p1[0] == p2[0]
            or p1[1] == p2[1]
            or max(p1[0], p2[0]) - min(p1[0], p2[0])
            == max(p1[1], p2[1]) - min(p1[1], p2[1])
        ):
            return True

        return False

    def fitness(self) -> int:
        """
        Calculates the number of `conflicts` the current configuration has.

        returns: The number of conflicts the configuration has.
        """
        conflicts = 0

        for x1, y1 in enumerate(self.positions):
            for x2 in range(x1 + 1, len(self.positions)):
                y2 = self.positions[x2]

                if self.has_conflict((x1, y1), (x2, y2)):
                    conflicts += 1

        return conflicts


def create_random_pop(count: int) -> list[Individual]:
    """
    Generates an initial population of `count` individuals.

    count: The amount of individuals to generate.

    returns: The list of individuals of "count" length.
    """
    return [Individual() for _ in range(count)]


def evaluate(population: list[Individual]):
    """
    Sorts the `population` using the amount of conflicts of each individual.
    Population is sorted on an ascending order.

    population: A list of individuals, the population to sort.
    """
    population.sort(key=lambda individu: individu.n_conflicts)


def selection(population: list[Individual], hcount: int, lcount: int):
    """
    Selects the `hcount` best and `lcount` worst elements from the `population`.
    It supposes the population has been sorted on an ascending order with `Individual.n_conflicts`.

    population: The population to do the selection from.
    hcount: Number of "Best" elements to keep.
    lcount: Number of "Worst" elements to keep.
    """
    del population[hcount : len(population) - lcount]


def crossover(ind1: Individual, ind2: Individual):
    """
    Combines the first (`BOARD_SIZE / 2`) positions of `ind1` configuration with the last (`BOARD_SIZE / 2`) positions of `ind2` configuration
    and the first (`BOARD_SIZE / 2`) positions of `ind2` with the last (`BOARD_SIZE / 2`) positions of `ind1.

    ind1: First individual.
    ind2: Second individual.
    """
    half = BOARD_SIZE // 2
    ind1_slice = ind1.positions[:half]
    ind2_slice = ind2.positions[-half:]
    ind1.positions[:half] = ind2_slice
    ind2.positions[-half:] = ind1_slice
    ind1.n_conflicts = ind1.fitness()
    ind2.n_conflicts = ind2.fitness()


def mutate(ind: Individual):
    """
    Mutates a random queen position of a configuration and re-calculates its fitness.

    ind: The individual to mutate.
    """
    ind.positions[random.randint(0, 7)] = random.randint(0, 7)
    ind.n_conflicts = ind.fitness()


def repopulate(population: list[Individual], size: int):
    """
    Repopulates a `population` to the desired `size`.

    population: The population to repopulate.
    size: The desired population size.
    """
    if len(population) < size:
        population += [Individual() for _ in range(0, size - len(population))]


def simple_algorithm(size: int = 20, hcount: int = 5, lcount: int = 5):
    """
    Simple version of the algorithm.

    1. Creates a random population of `subjects` individuals.
    2. While no solution is found :
        - Evaluates population (sort by `conflicts`)
        - Exits if solution was found
        - Selects `hcount` best and `lcount` worst individuals in `population`
        - Creates a new generation of individuals (swaps positions)
        - Mutates every individual in `population`
        - Repopulates population to match the desired `size`


    size (default=20): Size of the population.
    hcount (default=5): Number of best elements to keep from population.
    lcount (default=5): Number of worst elements to keep from population.
    """
    population = create_random_pop(size)

    attempt = 0

    while True:
        attempt += 1
        print(f"Attempt #{attempt}")
        evaluate(population)

        if population[0].n_conflicts == 0:
            print(population[0])
            break

        selection(population, hcount, lcount)
        crossover(population[random.randint(0, 7)], population[random.randint(0, 7)])
        mutate(population[random.randint(0, 7)])
        repopulate(population, size)


def all_solutions_algorithm(size: int = 20, hcount: int = 5, lcount: int = 5):
    """
    This version of the algorithm shows every solution for the 8 Queens problem.

    1. Creates a random population of `size` individuals.
    2. While `solutions_found` is less than 92 :
        - Evaluates population (sort by `conflicts`)
        - Adds all 0 conflict solutions to solutions_found set
        - Selects `hcount` best and `lcount` worst individuals in `population`
        - Creates a new generation of individuals (swaps positions)
        - Mutates every individual in `population`
        - Repopulates population to match the desired `size`

    size (default=20): Size of the population.
    hcount (default=5): Number of best elements to keep from population.
    lcount (default=5): Number of worst elements to keep from population.
    """
    population = create_random_pop(size)

    solutions_found: set[str] = set()

    attempt = 0

    while len(solutions_found) != 92:
        attempt += 1
        print(f"Attempt #{attempt}")
        evaluate(population)

        for ind in population:
            if ind.n_conflicts == 0:
                solutions_found.add(str(ind.positions))

        print(f"    Found {len(solutions_found)} solutions")

        selection(population, hcount, lcount)
        crossover(population[random.randint(0, 7)], population[random.randint(0, 7)])
        mutate(population[random.randint(0, 7)])
        repopulate(population, size)


all_solutions_algorithm()
