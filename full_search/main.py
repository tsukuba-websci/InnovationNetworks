import sys
sys.path.append("..")

from lib.julia_initializer import JuliaInitializer
from lib.utils import *
from lib.run_innovation_process import *
from full_search import FullSearch, InnovationType

if __name__ == "__main__":

    # todo: verify these values
    innovation_types = {
        "explorative" : InnovationType(1, 20, 1),
        "exploitative" : InnovationType(20, 2, 1)
    }

    targets = ["explorative", "exploitative"]

    for target in targets:
        fs = FullSearch(
            innovation_type=innovation_types[target],
            target=target,
            results_dir_path=f"results/{target}",
        )

        fs.run()

