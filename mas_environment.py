#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================



import math
import random

import mas as m
import mas_cell as c
import mas_utils as u



#==================================================
#  ENVIRONMENT
#==================================================

# --- Constants ---

MAX_IDX = 2
MAS_IDX = 0              # MAS the environment belongs to
CELL_MATRIX_IDX = 1      # The matrix of cells
MAX_CAPACITY_IDX = 2     # Maximum capacity any cell can bear 

# --- Private functions --- 

# Note: These functions should not be called outside this module.

def __get_property(env, property_idx):
    # Return the value of the given property of the environment.
    return env[property_idx]

def __set_property(env, property_idx, value):
    # Set the value of the given property of the environment.
    env[property_idx] = value    

def __empty_instance():
    # Return an empty environment instance.
    return [None]*(MAX_IDX+1)

def __empty_cell_matrix(env,sz):
    # Return an empty cell matrix of given size.
    # Note: size is the number of rows/columns.
    mat = []
    for y in range(sz):
        row = []
        for x in range(sz):
            row.append(c.new_instance(env))
        mat.append(row)
    return mat

# --- Getters and setters ---

def get_mas(env):
    """
        Return the MAS the given environment belongs to.
        (Allows "navigation" between variable levels.)
    """
    return __get_property(env, MAS_IDX)

def set_mas(env, mas):
    """
        Set the MAS the given environment belongs to.
        (Allows "navigation" between variable levels.)
    """
    __set_property(env, MAS_IDX, mas)

def get_cell_matrix(env):
    """
        Return the matrix of cells of the environment.
    """
    return __get_property(env, CELL_MATRIX_IDX)

def set_cell_matrix(env, cell_matrix):
    """
        Manually set the matrix of cells of the environment.
        This will usually not be called directly. Usually,
        get_cell() should be preferred to access one specific
        cell.
    """
    __set_property(env, CELL_MATRIX_IDX, cell_matrix)

def get_max_capacity(env):
    """
        Get the maximum capacity constant for the environment. 
    """
    return __get_property(env, MAX_CAPACITY_IDX)

def set_max_capacity(env, max_capacity):
    """
        Set the maximum capacity constant for the environment.
    """
    __set_property(env, MAX_CAPACITY_IDX, max_capacity)

# ---

def get_cell(env, cell_ref):
    """
        Return the referenced cell of the environment.
    """
    mat = get_cell_matrix(env)
    sz = size(env)
    (x, y) = cell_ref
    return mat[y%sz][x%sz]

def get_cells(env):
    """
        Return the list of all cells. Useful for iterating through
        all cells without knowing the underlying data structure.
    """
    ls = []
    for cell_ref in get_cell_refs(env):
        cell = get_cell(env, cell_ref)
        ls.append(cell)
    return ls

def get_cell_refs(env):
    """ 
        Return the list of all cell references. Useful for iterating 
        through all cells without knowing the underlying data structure.
    """
    sz = size(env)
    ls = []
    for y in range(sz):
        for x in range(sz):
            ls.append((x, y))
    return ls

# --- Initialisation ---

def new_instance(mas,config):
    """ 
        Return a new environment instance of size "sz" and 
        "declare" to which MAS it belongs to.
    """
    env = __empty_instance()
    # Set max capacity first, because initialisation of cells
    # depend on it.
    properties = u.cfg_env_properties(config)
    sz = u.cfg_env_size(config)
    set_max_capacity(env, properties["MAX_CAPACITY"])
    mat = __empty_cell_matrix(env,sz)
    set_mas(env, mas)
    set_cell_matrix(env, mat)
    return env

# --- Global environment information ---

def size(env):
    """
        Return the size of the environment. This is the number of 
        rows and the number of columns of the environment. The actual 
        number of cells in the environment is the square value of 
        the size.
    """
    mat = get_cell_matrix(env)
    return len(mat)

# --- Functions on a set of cells ---

def max_sugar_level_cell_ref(env, cell_ref_list):
    """
        Return the reference of the cell (from the given list)
        with the highest sugar level.
    """
    max_cell_ref = cell_ref_list[0]
    max_cell = get_cell(env, max_cell_ref)
    for cell_ref in cell_ref_list:
        cell = get_cell(env, cell_ref)
        if c.get_sugar_level(cell) > c.get_sugar_level(max_cell):
            max_cell = cell
            max_cell_ref = cell_ref
    return max_cell_ref

def sort_sugar_level_desc(env, cell_ref_list):
    """
        Sort the list of cells reference in descending order of 
        their corresponding sugar level.
    """
    # Build a separate list that assigns the sugar level to each
    # corresponding cell referenced in the list given as parameter.
    sugar_level_list = []
    for cell_ref in cell_ref_list:
        cell = get_cell(env,cell_ref)
        level = c.get_sugar_level(cell)
        sugar_level_list.append(level)
    # Call sorting function.
    u.sort_on_second_list(cell_ref_list, sugar_level_list,u.order_scalar_asc)
    return cell_ref_list
# --- Help functions for cells ---

def default_cell_ref():
    """
        Return a default (invalid) position (e.g., for agent 
        initialisation).
    """
    return (-1, -1)

def random_cell_ref(env):
    """
        Return a random position in the environment (e.g., for
        agent initialisation).
    """
    sz = size(env)
    res = ( random.randint(0, sz-1), random.randint(0, sz-1) )
    return res

def random_cell_ref_without_agent(env):
    """
        Return a random position in the environment that has no
        agent on it (e.g., for agent initialisation). 
        Assumption: There is at least one free cell in the environment.
    """
    # Note: This is not the most efficient approach!
    continue_search = True
    while continue_search:
        cell_ref = random_cell_ref(env)
        cell = get_cell(env, cell_ref)
        continue_search = c.agent_is_present(cell)
    return cell_ref

def add_capacity_gaussian(env, max_capacity_factor, center, disp):
    """
        Add capacity to a given set of cells of the environment.
        The distribution of capacity follows the shape of a multi-
        variate (bi-dimensional) normal probability distribution 
        function (gaussian PDF) with a given center and dispersion.
        The max_capacity_factor represents the maximum level of the
        added capacity (at the center of the distribution) and is 
        a multiplicative factor of the maximum capacity property of
        the environment.
    """
    # Set the max capacity to a given factor (e.g. "1.0" for 100% 
    # of the maximum capacity defined for the environment)
    max_capacity = get_max_capacity(env)*max_capacity_factor
    (cx, cy) = center
    # Compute the minimum capacity to assign to a cell.
    min_capacity = max_capacity*1E-3
    # Compute the cell distance from the center at which to add
    # capacity.
    max_dist = math.ceil(disp*math.sqrt(-2*math.log(min_capacity)))
    for x in range(cx-max_dist, cx+max_dist):
        for y in range(cx-max_dist, cx+max_dist):
            capacity = max_capacity*math.exp(-0.5*(u.eucl_dist((x, y), center)/disp)**2)
            cell = get_cell(env, (x, y))
            c.add_capacity(cell, capacity)

def add_capacity_from_string(env, capacity_str):
    eval(capacity_str)

def apply_fn_to_all_cells(env, fn):
    """
        Apply the function fn to all cells of the environment.
    """
    for cell in get_cells(env):
        fn(cell)

def set_cell_sugar_level_to_capacity(env):
    """
        Set the sugar level of all cells to their respective
        capacity.
    """
    apply_fn_to_all_cells(env, c.set_sugar_level_to_capacity)

# --- Terminal output ---

def show(env):
    """
        Print a list of all cells and, for each, print
        some key information. Mainly use this for debugging.
    """
    cell_ref_list = get_cell_refs(env)
    for cell_ref in cell_ref_list:
        print( cell_ref, end = ": " )
        cell = get_cell(env, cell_ref)
        c.show(cell)
