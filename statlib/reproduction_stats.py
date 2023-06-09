from statistics import mean


# Втрата різноманітності та швидкість репродукції
class ReproductionStats:
    def __init__(self):
        self.rr_list = []
        self.best_rr_list = []
        # мінімальна швидкість репродукції та номер ітерації, за якої вона спостерігалась
        self.rr_min = None
        self.ni_rr_min = None
        # максимальна швидкість репродукції та номер ітерації, за якої вона спостерігалась
        self.rr_max = None
        self.ni_rr_max = None
        # середня швидкість репродукції за всі ітерації
        self.rr_avg = None
        # мінімальна втрата різноманітності та номер ітерації, за якої вона спостерігалась
        self.teta_min = None
        self.ni_teta_min = None
        # максимальна втрата різноманітності та номер ітерації, за якої вона спостерігалась
        self.teta_max = None
        self.ni_teta_max = None
        # середня втрата різноманітності за всі ітерації
        self.teta_avg = None

    def calculate(self):
        #  мінімальна швидкість репродукції та номер ітерації, за якої вона спостерігалась
        self.rr_min = min(self.rr_list)
        self.ni_rr_min = self.rr_list.index(self.rr_min) + 1
        # RR_max, NI_RR_max
        self.rr_max = max(self.rr_list)
        self.ni_rr_max = self.rr_list.index(self.rr_max) + 1
        # середня швидкість репродукції за всі ітерації
        self.rr_avg = mean(self.rr_list)
        # Втрата різноманітності (loss of diversity) θ – частка особин популяції, яких не було обрано до батьківського пулу.
        teta_list = [1 - rr for rr in self.rr_list]
        # мінімальна втрата різноманітності та номер ітерації, за якої вона спостерігалась
        self.teta_min = min(teta_list)
        self.ni_teta_min = teta_list.index(self.teta_min) + 1
        # максимальна втрата різноманітності та номер ітерації, за якої вона спостерігалась
        self.teta_max = max(teta_list)
        self.ni_teta_max = teta_list.index(self.teta_max) + 1
        # середня втрата різноманітності за всі ітерації
        self.teta_avg = mean(teta_list)

    def __str__(self):
        return ("\nRR_min: " + str(self.rr_min) + " NI_RR_min: " + str(self.ni_rr_min) +
                "\nRR_max: " + str(self.rr_max) + " NI_RR_max: " + str(self.ni_rr_max) + "\nRR_avg: " + str(
                    self.rr_avg) +
                "\nTeta_min: " + str(self.teta_min) + " NI_Teta_min: " + str(self.ni_teta_min) +
                "\nTeta_max: " + str(self.teta_max) + " NI_Teta_max: " + str(self.ni_teta_max) + "\nTeta_avg: " + str(
                    self.teta_avg))

    def as_dict(self):
        return {'RR_min': [self.rr_min], 'NI_RR_min': [self.ni_rr_min],
                'RR_max': [self.rr_max], 'NI_RR_max': [self.ni_rr_max], 'RR_avg': [self.rr_avg],
                'Teta_min': [self.teta_min], 'NI_Teta_min': [self.ni_teta_min],
                'Teta_max': [self.teta_max], 'NI_Teta_max': [self.ni_teta_max], 'Teta_avg': [self.teta_avg]}
# %%
