import copy
import random
from typing import Iterable


class NPNTransformation(object):
    def __init__(
        self,
        num_bit: int,
        input_negation: Iterable[bool] = None,
        input_permutation: Iterable[int] = None,
        output_negation: bool = False
    ):
        self.num_bit = num_bit

        if input_negation is None:
            self.input_negation = [False] * num_bit
        else:
            assert len(input_negation) == num_bit, "Input negation length must match number of bits."
            self.input_negation = list(input_negation)

        if input_permutation is None:
            self.input_permutation = list(range(num_bit))
        else:
            assert len(input_permutation) == num_bit, "Input permutation length must match number of bits."
            assert set(input_permutation) == set(range(num_bit)), "Input permutation must be a valid permutation."
            self.input_permutation = list(input_permutation)

        self.output_negation = output_negation

    def __str__(self) -> str:
        return (
            f"NPNTransformation(num_bit={self.num_bit}, "
            f"input_negation={self.input_negation}, "
            f"input_permutation={self.input_permutation}, "
            f"output_negation={self.output_negation})"
        )

    @classmethod
    def random(cls, num_bit: int) -> "NPNTransformation":
        input_negation = [random.choice([False, True]) for _ in range(num_bit)]
        input_permutation = list(range(num_bit))
        random.shuffle(input_permutation)
        output_negation = random.choice([False, True])
        return cls(
            num_bit=num_bit,
            input_negation=input_negation,
            input_permutation=input_permutation,
            output_negation=output_negation
        )

    def flip(self, index: int) -> "NPNTransformation":
        assert index >= 0 and index <= self.num_bit, "Index out of range."
        new_transformation = copy.deepcopy(self)
        if index == 0:  # Flip output
            new_transformation.output_negation = not new_transformation.output_negation
        else:  # Flip input
            new_transformation.input_negation[index - 1] = not new_transformation.input_negation[index - 1]
        return new_transformation

    def swap(self, i: int, j: int) -> "NPNTransformation":
        assert i >= 0 and i < self.num_bit, "Index i out of range."
        assert j >= 0 and j < self.num_bit, "Index j out of range."
        new_transformation = copy.deepcopy(self)
        new_transformation.input_permutation[i], new_transformation.input_permutation[j] = \
            new_transformation.input_permutation[j], new_transformation.input_permutation[i]
        return new_transformation
