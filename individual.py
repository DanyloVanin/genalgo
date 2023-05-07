class Individual:
    def __init__(self, code, fitness, key=1):
        self.code = code
        self.fitness = fitness
        self.key = key

    def clone(self, key: int) -> "Individual":
        return Individual(
            self.code,
            self.fitness,
            key,
        )

    def __str__(self):
        return "Fitness: " + str(self.fitness) + "\nCode: " + str(self.code)
# %%
