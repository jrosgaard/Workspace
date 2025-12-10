# Genetic Algorithm module
# This version modified to work with non-dimensional variables x, y, z

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np


from Model.KP_model import dx_dt, dy_dt, dz_dt
#from Main import x ,y, z

class GeneticAlgorithm:
    """
    Initialize Genetic Algorithm for non-dimensional KP model.
    """
    def __init__(self, parameters=None, id=None):
        self.parameters = parameters
        self.id = id
        self.last_fitness = None
    
    def fitness_func(ga_instance, solution, solution_idx):
        """
        Fitness function maximizing E and minimizing T.
        """
        t = ga_instance.environment['t']
        x = ga_instance.environment['x']
        y = ga_instance.environment['y']
        z = ga_instance.environment['z']

        # Extract genes from solution
        genes1 = solution[0:4]
        genes2 = solution[4:8]

        # Calculate s_1 and s_2 based on genes and current state
        s_1 = genes1[0]*x + genes1[1]*y + genes1[2]*z + genes1[3]
        s_2 = genes2[0]*x + genes2[1]*y + genes2[2]*z + genes2[3]

        # Restrict negative input
        s_1 = max(0, s_1)
        s_2 = max(0, s_2)

        E_input = s_1  # Effector cell input from GA
        IL_input = s_2  # IL-2 input from GA

        t_step = 1  # time step for prediction

        # Calculate derivatives using non-dimensional KP model equations
        x_pred = x + dx_dt(t=t,x=x, y=y, z=z, 
                           c=0.02, mu_2=0.03, p_1=0.1245, g_1=2e4, s_1=E_input) * t_step
        
        y_pred = y + dy_dt(t=t, y=y, x=x, z=z, 
                          r_2=0.18, b=1e-5, alpha=0.002, g_2=1e5) * t_step
        
        z_pred = z + dz_dt(t=t, z=z, x=x, y=y, 
                          p_2=5e-7, g_3=1e4, mu_3=10, s_2=IL_input) * t_step


        # Define fitness as maximizing dE_dt and minimizing dT_dt.
        # Penalize over dose of IL-2.

        a1, a2 = 0.1, 0.1 # weights for immunotherapy components
        b1, b2, b3, b4 = 0.1, 0.1, 0.1, 0.1  # weights for toxicity components

        immunotherapy = a1*(x_pred) - a2*(y_pred)  # Reward high effector cells and low tumor cells
        toxicity = b1*s_2 + b2*s_1 + b3*(x_pred*s_2) + b4*(z_pred)**2  # Penalty for IL-2 overdose

        c1, c2 = 1.0, 3.0

        fitness = c1*immunotherapy - c2*toxicity # final fitness

        #fitness = 1 # for testing

        return fitness

    def on_start(self, ga_instance):
        print("on_start()")

    def on_fitness(self, population_fitness):
        print("on_fitness()")

    def on_parents(self, selected_parents):
        print("on_parents()")

    def on_crossover(self, ga_instance, offspring_crossover):
        print("on_crossover()")

    def on_mutation(self, ga_instance, offspring_mutation):
        print("on_mutation()")

    def on_generation(ga_instance):

        if not hasattr(ga_instance, 'last_fitness'):
            ga_instance.last_fitness = None

        best_solution, current_fitness, _ = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)
        #print(f"Generation {ga_instance.generations_completed}: Best Fitness = {current_fitness}")

        ga_instance.last_fitness = current_fitness
    def on_stop(self, ga_instance, last_population_fitness):
        print("on_stop()")

    def run(self, environment):
        self.ga_instance.environment = environment
        self.ga_instance.run()
