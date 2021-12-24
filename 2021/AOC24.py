"""
Started by writing an Intcode computer. Realized brute forcing would takes an
impossibly long amount of time. Went through the program with pen and paper.
Recognized a pattern but couldn't quite explain it. Skimmed through the Reddit
thread. Decided to try writing down the logic more succinctly in Python. Wrote
down the instructions. Started piecing together the intent of the code. Clicked
when I ran through a couple of examples, printing z out. Eventually got this
"no-code" solution down.

Some notes:
    * only 3 values change after initializing w to a new value:
        * the digit from div z {:d}
        * the digit from add x {:d}
        * the digit from add y {:d}
    * a is always either 1 or 26
    * for a == 1
        * by observation, b > 9
        * then x + b != w is True
        * z gets multiplied by 26 and is added a number
    * for a == 26
        * by observation, b <= 0
        * if x + b == w, z = z // 26
        * else, z += w + c

As a result, the operations can be read as adding/subtracting numbers to z.

More specifically, they are like pushing and popping values from a stack, with a
power of 26.

For z = 0, we need all the operations successfully cancel out, i.e., the stack to
be empty after all operations are over.

This gives us a bound on the values of w, since popping is only successful when
z % 26 + b == w - this z % 26 is equal to the value of z when the item being popped
was added.

The visualization below shows visually how the stack should change if all the
operations are successful and how the operations line up:
    1. [A], Push(A)
    2. [A,B], Push(B)
    3. [A,B,C], Push(C)
    4. [A,B], Pop(C) if (z % 26) + b == w
    5. [A,B,D],Push(D)
    6. [A,B], Pop(D) if (z % 26) + b == w
    7. [A], Pop(B) if (z % 26) + b == w
    8. [A,E], Push(E)
    9. [A,E,F], Push(F)
   10. [A,E,F,G], Push(G)
   11. [A,E,F],Pop(G) if (z % 26) + b == w
   12. [A,E], Pop(F) if (z % 26) + b == w
   13. [A], Pop(E) if (z % 26) + b == w
   14. [], Pop(A) if (z % 26) + b == w

For instance, the first and last operation imply the following equations:
    (1) (1, 13, [3]) -> z = w1 + 3
    (14) (26, [-7], 3) -> z - 7 = w14
    -> w14 = w1 - 4

When maximizing the model number, we want to pick the highest value possible for w1,
given the constraints on w (0 < w < 10).
This implies w14 = 5 hence a model number of the format: 9____________5.

We do the opposite when minimizing the module numbers: w1 = 5, w14 = 1,
which gives us 5____________1.

Going through the equations gives us the 2 solutions:
   MAX: 91699394894995
   MIN: 51147191161261
"""

from _utils import timer

instructions = [
    (1, 13, 3),
    (1, 11, 12),
    (1, 15, 9),
    (26, -6, 12),
    (1, 15, 2),
    (26, -8, 1),
    (26, -4, 1),
    (1, 15, 13),
    (1, 10, 1),
    (1, 11, 6),
    (26, -11, 2),
    (26, 0, 11),
    (26, -8, 10),
    (26, -7, 3),
]


def recompiled_code(w: int, z: int, a: int, b: int, c: int) -> int:
    """
    Returns the value of z given a value of w, z, a, b, and c.

    w: int, part of the module number
    z: int
    a: int, digit from div z {:d}
    b: int, digit from add x {:d}
    c: int, digit from add y {:d}

    Note: if x + b == w, x = 0 -> the value of z doesn't change after z // a.
    """
    x = z % 26
    z = z // a
    if x + b != w:
        z *= 26
        z += w + c
    return z


def compute_z(module_number: str):
    module_number = [int(c) for c in module_number]
    zipped = zip(instructions, module_number)
    z = 0

    for instr, w in zipped:
        a, b, c = instr
        z = recompiled_code(w, z, a, b, c)

    return z


@timer
def main():
    """
    Checks that the solutions are valid.
    """
    part_1_solution = 91699394894995
    part_2_solution = 51147191161261
    assert compute_z(str(part_1_solution)) == 0
    assert compute_z(str(part_2_solution)) == 0
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_score, part_2_score = main()
    print(f"PART 1: {part_1_score}")  # 91699394894995
    print(f"PART 2: {part_2_score}")  # 51147191161261
