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

        # make sure it is power of 2
        assert len(self.table) & (len(self.table) - 1) == 0, "Truth table length must be a power of 2."

    def __lt__(self, other: "TruthTable") -> bool:
        for a, b in zip(self.table, other.table):
            if a != b:
                return a < b
        return False

    def __eq__(self, other: "TruthTable") -> bool:
        return self.table == other.table

    def __str__(self) -> str:
        return self.table


def build_relation_clauses(formula: CNF, v1: int, v2: int, equal: bool = True):
    if equal:
        formula.append([-v1, v2])
        formula.append([v1, -v2])
    else:
        formula.append([-v1, -v2])
        formula.append([v1, v2])


class Formula(object):
    cnf_built = False

    def __init__(self, aig_filename: str):
        self.aig = aiger.load(aig_filename)
        assert len(self.aig.outputs) == 1, "Only single-output AIGs are supported."
        assert len(self.aig.latches) == 0, "Latches are not supported."
        self.num_bit = len(self.aig.inputs)
        self.input_names = list(sorted(self.aig.inputs, reverse=True))
        self.output_name = list(self.aig.outputs)[0]
        self.transformation = NPNTransformation(num_bit=self.num_bit)

    def simulate(self, inputs: list[bool]) -> bool:
        assert len(inputs) == self.num_bit, "Input length does not match number of bits."
        input_dict = {
            name: value ^ neg
            for name, value, neg in zip(self.input_names, inputs, self.transformation.input_negation)
        }
        input_dict = {
            self.input_names[self.transformation.input_permutation.index(i)]: inputs[i] ^ self.transformation.input_negation[i]
            for i in range(self.num_bit)
        }
        output_dict, _ = self.aig(inputs=input_dict)
        result = output_dict[self.output_name] ^ self.transformation.output_negation
        return result

    def truth_table(self) -> TruthTable:
        truth_table = [self.simulate(c) for c in product([True, False], repeat=self.num_bit)]
        return TruthTable(truth_table)

    def try_transformation(self, candidate: NPNTransformation) -> TruthTable:
        original_transformation = self.transformation
        self.transformation = candidate
        truth_table = self.truth_table()
        self.transformation = original_transformation
        return truth_table

    def build_cnf(self):
        self.cnf = CNF(from_aiger=self.aig.aig)
        self.nv = self.cnf.nv
        self.input_variables = sorted(
            self.cnf.inps,
            key=lambda v: self.cnf.vpool.obj(v).name,
            reverse=True
        )
        self.output_variable = self.cnf.outs[0]
        self.cnf_built = True

        # build duplicated CNF
        self.duplicated_cnf = CNF()
        for clause in self.cnf.clauses:
            new_clause = []
            for literal in clause:
                var = abs(literal)
                sign = 1 if literal > 0 else -1
                new_clause.append(sign * (var + self.nv))
            self.duplicated_cnf.append(new_clause)

    def build_lexsat(self, candidate: NPNTransformation) -> tuple[CNF, list[int]]:
        assert self.cnf_built, "CNF must be built before constructing LEXSAT."

        # Add CNF clauses for both original and duplicated formula
        formula = CNF()
        formula.extend(self.cnf.clauses)
        formula.extend(self.duplicated_cnf.clauses)
        lexsat_target = [
            self.input_variables[self.transformation.input_permutation.index(i)] *\
                (-1 if self.transformation.input_negation[i] else 1)
            for i in range(self.num_bit)
        ]

        # Add input relations
        for i in range(self.num_bit):
            left = self.input_variables[i]
            index = self.transformation.input_permutation[i]
            right = self.input_variables[candidate.input_permutation.index(index)] + self.nv
            equal = not self.transformation.input_negation[index] ^ candidate.input_negation[index]
            build_relation_clauses(formula, left, right, equal)

        # Add output relation
        build_relation_clauses(
            formula,
            self.output_variable,
            self.output_variable + self.nv,
            self.transformation.output_negation != candidate.output_negation
        )

        return formula, lexsat_target
