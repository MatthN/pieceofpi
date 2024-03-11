from monte_carlo import monte_carlo_pi

nb_points = 5_000_000

for point_info, inside_count, total_points in monte_carlo_pi(nb_points):
    (x, y, inside) = point_info
    current_pi_estimate = 4 * inside_count / total_points

    if not total_points % 100_000:
        print(current_pi_estimate)