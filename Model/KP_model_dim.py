# Dimensional Kirschner-Panetta model equations
# (unused)

# Imports
import numpy as np
import pandas as pd
import pygad

from Model.KP_model import r_2

# Kirschner-Panetta eqs. 1-3
def kp_dE_dt(t, E, T, I_L, s_1, c, mu_2, p_1, g_1):
    """
    Equation for activated immune cells or effector cells.
    """
    dE_dt = c*T - mu_2*E + (p_1*E*I_L)/(g_1 + I_L) + s_1
    return dE_dt

def kp_dT_dt(t, T, E, alpha, g_2, growth_function=1, eta=1, W=1, x=0, y=0):
    """
    Equation for tumor cells.
    """
    carry_cap = W
    growth = r_2(growth_function=growth_function, eta=eta, W=carry_cap, x=T, y=y)
    dT_dt = growth*T - (alpha*E*T)/(g_2 + T)
    return dT_dt

def kp_dIL_dt(t, IL, E, T, IL_input, s_2, p_2, mu_3, g_3):
    """
    Equation for IL-2 in the single tumor site being modelled.
    """ 
    dIL_dt = (p_2*E*T)/(g_3 + T) - mu_3*IL + s_2 + IL_input
    return dIL_dt
