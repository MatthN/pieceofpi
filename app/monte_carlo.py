import random
import math
from typing import Generator, Tuple

def monte_carlo_pi_generator(
        n_samples: int
) -> Generator[Tuple[Tuple[float, float, int], int, int], None, None]:
    inside_count = 0
    for i in range(1, n_samples + 1):
        x, y = random.random(), random.random()
        d = math.sqrt(x**2 + y**2)
        inside = 1 if d <= 1 else 0
        inside_count += inside
        yield (x, y, inside), inside_count, i





