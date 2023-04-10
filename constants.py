env = 'not_test'

# Number of individuals in population
DEFAULT_POPULATION_SIZE = 100

# Max number of iterations
MAX_ITERATIONS = 100

# Used for double equality comparison
EPS = 0.0001

# Used to identify if Run was successful
# за наявності мутації: ідентифіковано збіжність алгоритму ТА >=90% особин фінальної популяції є копіями оптимального ланцюжка.
SUCCESSFUL_RUN_OPTIMAL_GENOTYPE_RATE = 0.9

# Used to identify convergence in case of mutation.
# Shows percentage of desired homogenous genes
DESIRED_GENE_HOMOGENEITY_LEVEL = 0.99

# Number of runs done per each parameter set
MAX_RUNS = 10 if env == 'test' else 100

# Used to estimate correctness of results: expected - actual <= DELTA for y, SIGMA for x
SIGMA = 0.01
DELTA = 0.01
# %%
