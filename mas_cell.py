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

import mas_environment as e


#==================================================
#  CELL
#==================================================   

# --- Constants ---

MAX_IDX = 3
ENV_IDX = 0                             # Environment the cell belongs to
SUGAR_LEVEL_IDX = 1                     # Current sugar level
SUGAR_CAPACITY_IDX = 2                  # Sugar capacity of the cell
PRESENT_AGENT_IDX = 3                   # Agent that is currently on the cell

# --- Private functions --- 

# Note: These functions should not be called outside this module.

def __get_property(cell, property_idx):
    #  Return the value of the given property of the cell.
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid cell property index.")
    return cell[property_idx]

def __set_property(cell, property_idx, value):
    # Set the value of the given property of the cell.
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid cell property index.")
    cell[property_idx] = value    

def __empty_instance():
    # Return an empty cell instance.
    return [None]*(MAX_IDX+1)

# --- Getters and setters ---

def get_env(cell):
    """
        Return the environment the given cell belongs to.
        (Allows "navigation" between variable levels.)
    """
    return __get_property(cell, ENV_IDX)

def set_env(cell, env):
    """
        Set the environment the given cell belongs to.
        (Allows "navigation" between variable levels.)
    """
    __set_property(cell, ENV_IDX, env)    

def get_capacity(cell):
    """
        Return the sugar capacity of the cell.
    """
    return __get_property(cell, SUGAR_CAPACITY_IDX)
        
def set_capacity(cell, capacity):
    """
        Set the sugar capacity of the cell.
    """    
    env = get_env(cell)
    if capacity < 0:
        raise Exception("The sugar capacity of a cell cannot be negative.")
    if capacity > e.get_max_capacity(env):
        print("Capa = ",capacity,"   max = ",e.get_max_capacity(env))
        raise Exception("The sugar capacity of a cell cannot exceed the maximum capacity for the environment.")
    __set_property(cell, SUGAR_CAPACITY_IDX, capacity)

def get_sugar_level(cell):
    """
        Return the current sugar level of the cell.
    """    
    return __get_property(cell, SUGAR_LEVEL_IDX)

def set_sugar_level(cell, level):
    """
        Set the current sugar level of the cell.
    """    
    if level < 0:
        raise Exception("Error: The sugar level of a cell cannot be negative.")
    elif level > get_capacity(cell):
        raise Exception("Error: The sugar level of a cell cannot exceed its capacity.")
    __set_property(cell, SUGAR_LEVEL_IDX, level)

def get_present_agent(cell):
    """
        If an agent is currently present on the cell, return 
        that agent, otherwise return the constant None.
    """
    return __get_property(cell, PRESENT_AGENT_IDX)

def set_present_agent(cell, agent):
    """
        Set the agent that is currently present on the cell. 
        To tell that there is no agent, set agent to None.
    """
    __set_property(cell, PRESENT_AGENT_IDX, agent)

# --- Initialisation ---

def new_instance(env):
    """ 
        Return a new cell instance and "declare" to which 
        environment it belongs to.
    """
    cell = __empty_instance()
    set_env(cell, env)
    # We have to set the capacity before sugar level, because
    # the latter uses the former to check for validity.
    set_capacity(cell, 0.0)             
    set_sugar_level(cell, 0.0)
    set_present_agent(cell, None)
    return cell

# --- Sugar Capacity ---    
        
def add_capacity(cell, capacity):
    """
        Add capacity to a cell (in addition to the capacity)
        the cell already has.
        Usually, this function is only called by other capacity
        initialisation functions, e.g. "add_capacity_gaussian" 
        in the "mas_environment" module.
    """
    # Add the current capacity of the cell to the value of the
    # parameter "capacity".
    capacity += get_capacity(cell)
    # Limit it to the maximum capacity of the environment.
    env = get_env(cell)
    max_capacity = e.get_max_capacity(env)
    if capacity <= max_capacity:
        set_capacity(cell, capacity)
    else:
        set_capacity(cell, max_capacity)

# --- Sugar Level ---

def set_sugar_level_to_capacity(cell):
    """
        Set the sugar level of the cell to its capacity, i.e.,
        to its highest possible value.
    """
    capacity = get_capacity(cell)
    set_sugar_level(cell, capacity)

def add_sugar_level(cell, level):
    """
        Add a given level to the current sugar level of the cell.
    """
    # Add the current sugar level of the cell to the value of 
    # the parameter "level".
    level += get_sugar_level(cell)
    set_sugar_level(cell, level)

# --- Agence presence ---

def agent_is_present(cell):
    """
        Return (boolean) whether or not an agent is currently
        present on the cell. (Does not tell actual which agent.)
    """
    return get_present_agent(cell) != None

# --- Graphic display ---

def show(cell):
    """
        Print some key information about the cell.
        Mainly use this for debugging.
    """
    print("level:", round(get_sugar_level(cell), 2), \
        "  capacity:", round(get_capacity(cell), 2), \
        "  agent present:", agent_is_present(cell))



#==================================================
#  CELL RULES (some examples)
#==================================================
#
# Cell rule functions must comply to the following
# signature:
# 
#  INPUT:  The cell the rules is applied on
#
#  OUTPUT: None.
#
#==================================================

def regen_two_percent(cell):
    """
        Cell rule: regenerate 2% of the cell's capacity.
    """
    capacity = get_capacity(cell)
    level = get_sugar_level(cell)
    level += 0.02*capacity
    if level > capacity:
        level = capacity
    set_sugar_level(cell, level)

def regen_five_percent(cell):
    """
        Cell rule: regenerate 5% of the cell's capacity.
    """
    capacity = get_capacity(cell)
    level = get_sugar_level(cell)
    level += 0.05*capacity
    if level > capacity:
        level = capacity
    set_sugar_level(cell, level)    

def regen_ten_percent(cell):
    """
        Cell rule: regenerate 10% of the cell's capacity.
    """
    capacity = get_capacity(cell)
    level = get_sugar_level(cell)
    level += 0.10*capacity
    if level > capacity:
        level = capacity
    set_sugar_level(cell, level)    

def regen_full(cell):
    """
        Cell rule: regenerate the level to full capacity.
    """
    capacity = get_capacity(cell)
    set_sugar_level(cell, capacity)
