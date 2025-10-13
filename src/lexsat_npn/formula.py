from itertools import product

import aiger
from pysat.formula import CNF

from .transformation import NPNTransformation


class TruthTable(object):
    def __init__(self, table: str):
        if isinstance(table, str):
            self.table = table
        else:
            self.table = "".join("1" if v else "0" for v in table)

    def __lt__(self, other: "TruthTable") -> bool:
        for a, b in zip(self.table, other.table):
            if a != b:
                return a < b
        return False

    def __str__(self) -> str:
        return self.table


class Formula(object):
    def __init__(self, aig_filename: str):
        self.aig = aiger.load(aig_filename)
        assert len(self.aig.outputs) == 1, "Only single-output AIGs are supported."
        assert len(self.aig.latches) == 0, "Latches are not supported."
        self.num_bit = len(self.aig.inputs)
        self.input_names = list(reversed(sorted(self.aig.inputs)))
        self.output_name = list(self.aig.outputs)[0]
        self.transformation = NPNTransformation(num_bit=self.num_bit)

    def simulate(self, inputs: list[bool]) -> bool:
        input_dict = {name: value for name, value in zip(self.input_names, inputs)}
        output_dict, _ = self.aig(inputs=input_dict)
        return output_dict[self.output_name]

    def truth_table(self) -> TruthTable:
        polarities = [
            [True, False] if neg else [False, True]
            for neg in self.transformation.input_negation
        ]
        truth_table = [
            self.simulate([combination[p] for p in self.transformation.input_permutation])
            for combination in product(*polarities)
        ]
        if self.transformation.output_negation:
            truth_table = [not value for value in truth_table]
        return TruthTable(reversed(truth_table))

    def build_cnf(self):
        self.cnf = CNF(from_aiger=self.aig.aig)
