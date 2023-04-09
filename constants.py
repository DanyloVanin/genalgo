env = 'test'

# Number of individuals in population
N = 100

# Max number of iterations
MAX_ITERATIONS = 100


MUTATION_LOW_LIMIT = 10

# Used for double equality comparison
EPS = 0.0001

# Used to identify if Run was successful
# за наявності мутації: ідентифіковано збіжність алгоритму ТА >=90% особин фінальної популяції є копіями оптимального ланцюжка.
SUCCESSFUL_RUN_OPTIMAL_GENOTYPE_RATE = 0.9

DESIRED_GENE_HOMOGENEITY_LEVEL = 0.99 # not used yet

# Number of runs done
MAX_RUNS = 5 if env == 'test' else 10

# Used to estimate correctness of results: expected - actual <= DELTA for y, SIGMA for x
SIGMA = 0.01
DELTA = 0.01
# %%
