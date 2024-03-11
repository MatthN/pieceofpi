from app.create_gui import create_app
from app.monte_carlo import monte_carlo_pi_generator

app = create_app(generator_function=monte_carlo_pi_generator)
app.setup_gui()
app.run()
