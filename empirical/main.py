import sys
sys.path.append("..")
from dataclasses import dataclass
from empirical import Empirical, InnovationType
# todo: add empirical fitting

@dataclass
class Params:
    rho: float
    nu: float
    s: str
    zeta: float
    eta: float
    steps: int
    nodes: int = 100

if __name__ == "__main__":

    targets = {
        "aps": Params(rho=10, nu=16, s="asw", zeta=0.2, eta=0.6, steps=1000000),
        "tmn": Params(rho=18, nu=24, s="asw", zeta=1.0, eta=0.2, steps=1000000),
    }

    innovation_types = {
        "explorative" : InnovationType(1, 20, 1),
        "exploitative" : InnovationType(20, 2, 1)
    }

    # For each target we need to run the network generation model.
    # Then we need to run the innovation model 1000 times.
    # Then we need calculate the mean nctf and ttf
    # Then we need to plot those values in the rho-nu space file: visualise/graphs/rho_nu_space_empirical.py

    for target, params in targets.items():
        emp = Empirical(
            target=target,
            params=params,
            results_dir_path=f"results/{target}",
            innovation_type=innovation_types["explorative"],
        )
        emp.run()