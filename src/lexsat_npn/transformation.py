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
            self.input_negation = input_negation

        if input_permutation is None:
            self.input_permutation = list(range(num_bit))
        else:
            self.input_permutation = input_permutation

        self.output_negation = output_negation

    def __str__(self) -> str:
        return (
            f"NPNTransformation(num_bit={self.num_bit}, "
            f"input_negation={self.input_negation}, "
            f"input_permutation={self.input_permutation}, "
            f"output_negation={self.output_negation})"
        )
