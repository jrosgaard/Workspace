# Kirschner-Panetta Model

# Non-dimensionalization function
def nondim(E0=None, T0=None, IL0=None, t_s=None, c_in=None, 
           p_1_in=None, g_1_in=None, mu_2_in=None, g_2_in=None, b_in=None, 
           r_2_in=None, alpha_in=None, mu_3_in=None, p_2_in=None, g_3_in=None, 
           s_1_in=None, s_2_in=None):
    """
    Non-dimensionalization of variables and parameters.
    """
    if E0 is None or T0 is None or IL0 is None or t_s is None:
        raise ValueError("E0, T0, IL0, and t_s must be provided for non-dimensionalization.")
    
    c = (c_in*T0) / (t_s*E0)

    p_1 = p_1_in / t_s
    g_1 = g_1_in / IL0
    mu_2 = mu_2_in / t_s
    g_2 = g_2_in / T0
    b = b_in * T0

    r_2 = r_2_in / t_s
    alpha = (alpha_in*E0) / (t_s*T0)
    mu_3 = mu_3_in / t_s
    p_2 = (p_2_in*E0) / (t_s*IL0)
    g_3 = g_3_in / T0
    
    s_1 = s_1_in / (t_s*E0)
    s_2 = s_2_in / (t_s*IL0)

    return [c, p_1, g_1, mu_2, g_2, b, r_2, alpha, mu_3, p_2, g_3, s_1, s_2]

# Non-dimensional Kirschner-Panetta eqs. for x, y, z
def dx_dt(t, x, y, z, c, mu_2, p_1, g_1, s_1):
    """
    Scaled x equation.
    """
    dxdt = c*y - mu_2*x + (p_1*x*z)/(g_1 + z) + s_1
    return dxdt

def dy_dt(t, y, x, z, r_2, b, alpha, g_2):
    """
    Scaled y equation.
    Note this uses the exponential growth function.
    """
    dydt = r_2*y*(1-b*y) - (alpha*x*y)/(g_2 + y)
    return dydt

def dz_dt(t, z, x, y, p_2, g_3, mu_3, s_2):
    """
    Scaled z equation.
    """
    # Defining s_2 as the external IL-2 input from the GA
    dzdt = (p_2*x*y)/(g_3 + y) - mu_3*z + s_2 
    return dzdt

def r_2(growth_function, x, y, z, b): 
    """
    Growth function.
    (unused)
    """
    if growth_function == 1:  # linear
        r_2 = 0.18

    elif growth_function == 2:  # exponential
        r_2 = 0.18 * (1-b*y)       
   
    else:
        raise ValueError("Invalid tumor growth function.")  
    
    return r_2

def kp_coupled(t, state, 
               c, mu_2, p_1, g_1, s_1, r_2, b, alpha, g_2, p_2, g_3, mu_3, s_2):
    """
    Coupled KP model functions to integrate.
    """
    x, y, z = state # Unpack state variables

    dxdt = dx_dt(t, x, y, z, c, mu_2, p_1, g_1, s_1)
    dydt = dy_dt(t, y, x, z, r_2, b, alpha, g_2)
    dzdt = dz_dt(t, z, x, y, p_2, g_3, mu_3, s_2)

    return [dxdt, dydt, dzdt]
