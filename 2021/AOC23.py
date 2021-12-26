"""
Struggled quite a bit with this. My first instinct was to do a BFS, keeping the state of the board as
dict of pos:letters. There were a couple of intractable bugs though and the performance was bad.
(The puzzle this reminded me of, day 20 of the 2019 edition, was also one of the AOC problems
I had the must difficulty with.)

I ended up re-implementing this solution:
u/tharko
https://topaz.github.io/paste/#XQAAAQDaDgAAAAAAAAAzHIoib6poHLpewxtGE3pTrRdzrponK3G2+gEMNmwefr0hbXUA9LtjzN7RxDO9JqlGGZMcasidY6/FZMaXunv5h4GF+5ptcMiLAKag7s8LUiXQU7N1yfExim+ge8gRF+lBKktxD4qeJZPVXHR+7/F/P87/P0TKvPXshBMrb1qlGZu+qL+pE2G+yk63AqK1ggCV2QIov230XbC0B/XZcKXQpVmUl15+9siWh9pjU6pRaNG+yhGPPzXcmPW73nV1TqfaLF57m70ZnKEoAVuUdsXJJ4SbSY7DtE71Lg2hG45kOaIC/RSBQ1gQ/ooyLL9wtL7ju7LPTOZCg4+Dtgnc91ryUh52uWX//qGLxbw6weeA+3MZlEUP91YKoV/Y+bvcoL8Ms/2r7kF9OajRWSUVvpXFgizU7Elk57q2T4LjnbI434qIW/hMZTii0lY65l1o27zcNXG2aN8LKC8WS2/HmALgwfdw1Ysh9Dg7L5qAjFnh4eUolEQC2QqdcANGx/L4580WN9jG6rF7XTUkQOeIggNkzg7C4utklKDKIfoNKK1XkiwI1dGVCPUm2IgUZDp++rl+2ak6SkjBktmAlMk0POw5QB1+ab6tJmZYMCIg0RO8oktAqiKoveIgsWquoUadxqJX6OI2c5REHapYJAbNpsqe9MTN/8yr1V0YjOACyzxaN3ZjDbflJ9mAt7WRAU/GFQhWbAhnsPTmFGkupGVkWbmdjndJw9z/7/wWhOS2wB8NF1QaXPPLLpKAmN/fRJcR6UJmN/1BF/2wVj92Y4rZ+B7ESZQ95YV+E47Q9ZyvpqmZdvz8eXS1Md6+y1lrVLgvGfvZSTlAu17aqk3XxEFP3Hsys5H6WG/XsPKrq0DrdNrSNb1kpy1lwL/EngxMZS6RcYtsEbLfZD4SmK7MhABMMw8Jl4O0RtqfEsAvxyH5J4Z/qGmO72m1CWg3JFOrvZpM6jTkjlwNPxGhS5jN6AInI+ULYBJVQR5netMpHC5YJUkvWy8qgfy6xV5Y7E9vsXvI3f4OyB8q+UVdkruF8P+JpZRjjMoYwq6yTjJSrv92Cm1plSUYiBSG+CTYzfdVQSVYJ2nZx9H8Y71tyt3e7Q9dfCJ9TsoAuoC1vKmNrXdILP5plLPIeqXfdP4kOr/BZptstG8dc9M+KKwhEYioebcVluRghPvjxqdyXctYCtX/W6q7MSLJVddf6JlpOXcDWLWCQW7acyYAdR0D9lUSZY0h2HgxMujnNbiTpNxHuhjm4Fnf7FpiAohUB2JtwtUwEVYTHnY01i4r//MijtV0Q8tFmTlYBAgO8cluZm62UwN9J+OmqKoP4LXLBhciLB5EdNHBjPKXT8/F195SVw9CBLSnVLXW4OtRGgIB9jXMPiLetnTuBMy8vEGle3Fg+ABjL0Eb+v9KH3gA

Will need to retry doing it from scratch at some point.

-------------
Code below writes down the logic for the 2 valid moves in the game:
* moving from a room to the hallway
* moving from the hallway to the right room, with only letters of the matching type

Uses recursion + memoization to find the optimal move for a particular state of the game.
Keeps track of the state using 2 tuples, one for hallway positions and the other for rooms.
"""
from functools import lru_cache

from _utils import timer

from typing import Tuple


class Solver:
    def __init__(self, initial_rooms: Tuple):
        self.initial_rooms = initial_rooms

        self.room_size = len(self.initial_rooms[0])
        self.room_map = (2, 4, 6, 8)
        self.hallway_map = (0, 1, 3, 5, 7, 9, 10)
        self.end_rooms = {"A": 0, "B": 1, "C": 2, "D": 3}
        self.energy_mapping = {"A": 1, "B": 10, "C": 100, "D": 1000}
        self.final_state = (
            ("A",) * self.room_size,
            ("B",) * self.room_size,
            ("C",) * self.room_size,
            ("D",) * self.room_size,
        )

    def check_move_into_room(self, letter: str, dest: int, rooms: Tuple) -> bool:
        """
        Check that the letter can move into the destination room.
        Per the rules of the game, the room must not have any letter
        that doesn't match the desired type.
        """
        move = True
        for char in rooms[dest]:
            if char and char != letter:
                move = False
                break
        return move

    def check_clear_path(self, cur_pos: int, end_pos: int, hallway: Tuple) -> bool:
        """
        Check that the path from cur_pos to end_pos isn't obstructed.
        """
        move = True
        direction = 1 if cur_pos < end_pos else -1

        while cur_pos != end_pos:
            cur_pos += direction
            if hallway[cur_pos]:
                move = False
                break

        return move

    def update_state_hallway_to_room(
        self,
        letter: str,
        none_count: int,
        ix: int,
        dest: int,
        hallway: Tuple,
        rooms: Tuple,
    ):
        """
        Update the current state after a move from the hallway into a room.

        none_count: int, number of empty vertical spaces above letter (letter goes to bottom)
        ix: int, initial position of letter in hallway
        dest: int, number of destination room (e.g., first or second room)
        """
        new_room = (None,) * (none_count - 1) + (letter,) * (
            self.room_size - none_count + 1
        )
        new_hallway = hallway[:ix] + (None,) + hallway[ix + 1 :]
        new_rooms = rooms[:dest] + (new_room,) + rooms[dest + 1 :]
        return new_hallway, new_rooms

    def update_state_room_to_hallway(
        self,
        letter: str,
        char_pos: int,
        ix: int,
        end_pos: int,
        hallway: Tuple,
        rooms: Tuple,
    ):
        """
        Update the current state after a move from a room into the hallway.

        none_count: int, position of letter in room (vertically)
        ix: int, number of initial room (e.g., first or second room)
        end_pos: int, final position of letter in hallway
        """
        new_hallway = hallway[:end_pos] + (letter,) + hallway[end_pos + 1 :]
        new_room = (None,) * (char_pos + 1) + rooms[ix][char_pos + 1 :]
        new_rooms = rooms[:ix] + (new_room,) + rooms[ix + 1 :]
        return new_hallway, new_rooms

    def calculate_energy(
        self,
        letter: str,
        steps: int,
        start_pos: int,
        end_pos: int,
        hallway: Tuple,
        rooms: Tuple,
    ) -> int:
        """
        Returns total energy from current + all future optimal moves from this state.
        """
        total_steps = steps + abs(end_pos - start_pos)
        future_energy = self.minimal_cost(hallway, rooms)
        energy = total_steps * self.energy_mapping[letter] + future_energy
        return energy

    # recursive, over initial hallway and room arrangement
    @lru_cache(maxsize=None)
    def minimal_cost(self, hallway: Tuple, rooms: Tuple) -> int:
        """
        Returns minimal cost to arrange letters in the proper order given a state.

        Given this map:
            #######
            #.A...#
            ##.#B##
            ##A#B##
            #######

        Hallway is tuple of str, e.g., (None, 'A', None, None, None).
        Rooms is tuple of str, e.g.,   ((None, 'A'), ('B', 'B')).
        """
        # if final state, return 0
        if rooms == self.final_state:
            return 0

        min_energy = 10 ** 8

        # for space in hallway
        for ix, letter in enumerate(hallway):
            # if not a letter, stop
            if not letter:
                continue

            # check destination room doesnt have undesirable
            dest = self.end_rooms[letter]
            move = self.check_move_into_room(letter, dest, rooms)

            if not move:
                continue

            # room is empty, try moving there (moving either left or right)
            cur_pos = ix  # e.g., 2 -> maps to (1,2)
            end_pos = self.room_map[dest]  # e.g., 7 -> maps to (1, 7)
            move = self.check_clear_path(cur_pos, end_pos, hallway)

            if not move:
                continue

            # update hallway, rooms
            none_count = sum(
                elem is None for elem in rooms[dest]
            )  # vertical steps to bottom of room
            new_hallway, new_rooms = self.update_state_hallway_to_room(
                letter, none_count, ix, dest, hallway, rooms
            )

            # compute cost (recurse: find optimal path given this choice)
            energy = self.calculate_energy(
                letter, none_count, ix, self.room_map[dest], new_hallway, new_rooms
            )
            if energy < min_energy:
                min_energy = energy

        # for space in room
        for ix, cur_room in enumerate(rooms):
            move = False

            # if one of the elements in the move doesnt fit, initiate a move
            for char in cur_room:
                if char and ix != self.end_rooms[char]:
                    move = True
                    break

            if not move:
                continue

            # count steps to exit room (vertical steps)
            char_pos = sum(1 if not char else 0 for char in cur_room)
            steps = 1 + char_pos
            letter = cur_room[char_pos]

            # try moving to corridor - any spot
            for end_pos in self.hallway_map:
                # stop if something in the way
                init_pos = self.room_map[ix]
                move = self.check_clear_path(init_pos, end_pos, hallway)

                if not move:
                    continue

                # update room
                new_hallway, new_rooms = self.update_state_room_to_hallway(
                    letter, char_pos, ix, end_pos, hallway, rooms
                )

                # compute cost (recurse: find optimal path given this choice)
                energy = self.calculate_energy(
                    letter, steps, init_pos, end_pos, new_hallway, new_rooms
                )
                if energy < min_energy:
                    min_energy = energy

        return min_energy

    def main(self) -> int:
        initial_hallway = tuple(
            None for _ in range(len(self.room_map) + len(self.hallway_map))
        )
        cost = self.minimal_cost(initial_hallway, self.initial_rooms)
        return cost


@timer
def main():
    part_1_rooms = (("D", "C"), ("B", "C"), ("B", "D"), ("A", "A"))
    part_2_rooms = (
        ("D", "D", "D", "C"),
        ("B", "C", "B", "C"),
        ("B", "B", "A", "D"),
        ("A", "A", "C", "A"),
    )
    part_1_score = Solver(part_1_rooms).main()
    part_2_score = Solver(part_2_rooms).main()
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main()
    print(f"PART 1: {part_1_score}")  # 15472
    print(f"PART 2: {part_2_score}")  # 46182
