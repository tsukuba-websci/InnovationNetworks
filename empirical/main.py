import sys
sys.path.append("..")
from dataclasses import dataclass
from empirical import Empirical, InnovationType

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
        "aps": Params(rho=4, nu=10, s="asw", zeta=0.5, eta=0.5, steps=1),
        "tmn": Params(rho=2, nu=1, s="asw", zeta=0.5, eta=0.5, steps=1),
        "ida": Params(rho=3, nu=4, s="asw", zeta=0.5, eta=0.5, steps=1),
        "eight": Params(rho=1, nu=2, s="asw", zeta=0.5, eta=0.5, steps=1),
    }

    innovation_types = {
        "explorative" : InnovationType(1, 20, 1),
        "exploitative" : InnovationType(20, 2, 1)
    }

    for target, params in targets.items():
        for innovation_type, innovation_parameters in innovation_types.items():
            emp = Empirical(
                target=target,
                params=params,
                results_dir_path=f"results/{target}/{innovation_type}",
                innovation_type=innovation_parameters,
            )
            emp.run()