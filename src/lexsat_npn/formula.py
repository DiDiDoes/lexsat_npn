from itertools import product

import aiger
from pysat.formula import CNF


class Formula(object):
    def __init__(self, aig_filename: str):
        self.aig = aiger.load(aig_filename)
        assert len(self.aig.outputs) == 1, "Only single-output AIGs are supported."
        assert len(self.aig.latches) == 0, "Latches are not supported."
        self.num_bit = len(self.aig.inputs)
        self.input_names = list(reversed(sorted(self.aig.inputs)))
        self.output_name = list(self.aig.outputs)[0]

    def simulate(self, inputs: list[bool]) -> bool:
        input_dict = {name: value for name, value in zip(self.input_names, inputs)}
        output_dict, _ = self.aig(inputs=input_dict)
        return output_dict[self.output_name]

    def truth_table(self) -> str:
        truth_table = [
            self.simulate(combination)
            for combination in product([False, True], repeat=self.num_bit)
        ]
        truth_table = ["1" if value else "0" for value in reversed(truth_table)]
        return "".join(truth_table)

    def build_cnf(self):
        self.cnf = CNF(from_aiger=self.aig.aig)
