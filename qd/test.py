import sys
sys.path.append("..")
from typing import List
from dataclasses import dataclass

from lib.julia_initializer import JuliaInitializer

jl_main, thread_num = JuliaInitializer().initialize()

# a, b, c = jl_main.run_waves_model(1, 1, "asw", 0.1, 0.9, steps=100)

# print(a.history)

@dataclass
class Params:
    rho: float
    nu: float
    s: str
    gamma: float
    eta: float
    steps: int
    nodes: int = 100
    threads: int = 4

params_list: List[Params] = [Params(1, 1, "asw", 0.1, 0.9, 100, 5, 4) for _ in range(1)]

results = jl_main.parallel_run_waves_model(params_list)

for result in results:
    print()
    print("HISTORY")
    print(result)
    print()

print("JULIA SETUP FINISHED")