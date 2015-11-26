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
import mas_cell as c
import mas_population as p
import mas_agent as a
import mas_utils as u



#==================================================
#  MAS
#==================================================

# --- Constants ---

MAX_IDX=7
ENV_IDX = 0                           # Environment
POP_IDX = 1                           # Agent population
CELL_RULES_IDX = 2                    # List of rules applied on cells
AGENT_RULES_IDX = 3                   # List of rules applied on agents
EXPERIMENT_ENDING_CONDITION_IDX = 4   # Function with the ending condition
MAX_CYCLE_IDX = 5                     # Max number of cycles per experiment
CYCLE_IDX = 6                         # Current cycle of an experiment
ORDER_ACTIVATION_IDX = 7			  # Ordre d'activation des agents
# --- Default values ---

def DEFAULT_ENDING_CONDITION(mas):
	# End experiment of the number of cycles reaches the defined maximum.
    return (get_cycle(mas) >= get_max_cycle(mas) )

def new_ending_condition(mas):
	"""
		Fonction permettant d'arréter la simulation sous deux conditions:
		- le nombre de cycl est égal au nombre de cycle maximal
		- si plus aucun agent vivant ne subsiste
	"""
	alive_agents = p.size(get_pop(mas))
	return (get_cycle(mas) >= get_max_cycle(mas) or alive_agents == 0)

# --- Private functions --- 

# Note: These functions should not be called outside this module.

def __get_property(mas, property_idx):
	#  Return the value of the given property of the MAS.
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid MAS property index.")
    return mas[property_idx]

def __set_property(mas, property_idx, value):
	# Set the value of the given property of the MAS.
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid MAS property index.")    
    mas[property_idx] = value

def __empty_instance():
	# Return an empty MAS instance.
    return [None]*(MAX_IDX+1)

# --- Getters and setters ---

def get_env(mas):
	"""
		Return the environment of the MAS.
	"""
	return __get_property(mas, ENV_IDX)

def set_env(mas, env):
	"""
		Set the environment of the MAS.
	"""
	__set_property(mas, ENV_IDX, env)

def get_pop(mas):
	"""
		Return the agent population of the MAS.
	"""
	return __get_property(mas, POP_IDX)

def set_pop(mas, pop):
	"""
        Set the agent population of the MAS.
    """
	__set_property(mas, POP_IDX, pop)

def get_cell_rules(mas):
	"""
        Return the cell rules of the MAS as a list of functions.
    """
	return __get_property(mas, CELL_RULES_IDX)

def set_cell_rules(mas, rules_list):
	"""
        Set the cell rules of the MAS as a list of functions.
    """
	__set_property(mas, CELL_RULES_IDX, rules_list)

def get_agent_rules(mas):
	"""
        Return the agent rules of the MAS as a list of functions.
    """
	return __get_property(mas, AGENT_RULES_IDX)

def set_agent_rules(mas, rules_list):
	"""
        Set the agent rules of the MAS as a list of functions.
    """
	__set_property(mas, AGENT_RULES_IDX, rules_list)

def get_ending_condition(mas):
	"""
        Return the ending condition function of the MAS.
    """
	return __get_property(mas, EXPERIMENT_ENDING_CONDITION_IDX)

def set_ending_condition(mas, ending_condition_fn):
	"""
        Set the ending condition function of the MAS. The condition function
        receives the MAS as parameter and returns a boolean to tell whether
        or not to end the experiment.
    """
	# Function signature:  fn(mas) ---> boolean(end_experiment)
	__set_property(mas, EXPERIMENT_ENDING_CONDITION_IDX, ending_condition_fn)    

def get_max_cycle(mas):
	"""
        Return the maximum number of cycles for an experiment with the MAS.
    """
	return __get_property(mas, MAX_CYCLE_IDX)

def set_max_cycle(mas, cycle):
	"""
        Set the maximum number of cycles for an experiment with the MAS.
    """
	__set_property(mas, MAX_CYCLE_IDX, cycle)

def get_cycle(mas):
	"""
        Return the current cycle of an experiment.
    """
	return __get_property(mas, CYCLE_IDX)

def set_cycle(mas, cycle):
	"""
        Set the current cycle of an experiment. This function should usually not
        be called directly.
    """
	__set_property(mas, CYCLE_IDX, cycle)

def set_order_activation(mas,order_activation):

	__set_property(mas,ORDER_ACTIVATION_IDX,order_activation)

def get_order_activation(mas):
	return __get_property(mas,ORDER_ACTIVATION_IDX)

# --- Initialisation ---

def new_instance():
	""" 
        Return a new MAS instance.
    """
	mas = __empty_instance()
	set_env(mas, None)
	set_pop(mas, None)
	set_cell_rules(mas, [])
	set_agent_rules(mas, [])
	set_ending_condition(mas, DEFAULT_ENDING_CONDITION)
	set_max_cycle(mas, 0)
	set_cycle(mas, 0)
	return mas

def new_instance_from_config(config):
	""" 
        Return a new MAS instance that has been initialised according
        to the parameters passed by the configuration.
    """
	mas = new_instance()
	# Environment
	env = e.new_instance(mas, config)
	set_env(mas, env)
	env_capacity_distribs = u.cfg_capacity_distributions(config)
	for distrib in env_capacity_distribs:
	    e.add_capacity_from_string(env,distrib)
	# Agent population
	pop = p.new_instance(mas, config)
	set_pop(mas, pop)
	# Cell rules
	cell_rules = u.cfg_cell_rules(config)
	for rule in cell_rules:
	    add_cell_rule_from_string(mas,rule)
	# Agent rules
	agent_rules = u.cfg_agent_rules(config)
	for rule in agent_rules:
	    add_agent_rule_from_string(mas,rule)
	# Experiment settings
	set_max_cycle(mas,u.cfg_max_cycle(config))
	set_ending_condition(mas,u.cfg_ending_condition(config))
	set_order_activation(mas,u.cfg_order_activation(config))
	return mas

# --- Environment rules ---

def add_cell_rule(mas, cell_rule):
	"""
		Add a cell rule to the MAS.
	"""
	mas[CELL_RULES_IDX].append(cell_rule)

def add_cell_rule_from_string(mas, cell_rule_str):
	"""
		Add a cell rule to the MAS based on a string
		that represents the function call.
	"""
	add_cell_rule(mas, eval("c."+cell_rule_str))

def apply_cell_rules(mas):
	"""
		Apply all cell rules to each cell of the MAS's environment.
	"""
	env = get_env(mas)
	for cell_rule in get_cell_rules(mas):
		e.apply_fn_to_all_cells(env, cell_rule)

# --- Agent rules ---

def add_agent_rule(mas, agent_rule):
	"""
		Add an agent rule to the MAS.
	"""
	mas[AGENT_RULES_IDX].append(agent_rule)

def add_agent_rule_from_string(mas, agent_rule_str):
	"""
		Add an agent rule to the MAS based on a string
		that represents the function call.
	"""
	add_agent_rule(mas, eval("a."+agent_rule_str))

def apply_agent_rules(mas):
	"""
		Apply all agent rules to each agent of the MAS's population.
	"""
	pop = get_pop(mas)
	eval("p."+get_order_activation(mas)+"(pop)")
	for agent_rule in get_agent_rules(mas):
		p.apply_rule(pop, agent_rule)

# --- Execution ---

def increment_cycle(mas):
	"""
		Increment the cycle of the MAS by one unit.
	"""
	set_cycle(mas, get_cycle(mas)+1)

def run_one_cycle(mas):
	"""
		Run one experiment cycle of the MAS.
	"""
	apply_cell_rules(mas)
	apply_agent_rules(mas)

def run_experiment(mas):
	"""
	    Run a experiment on the initialised MAS.
	"""
	set_cycle(mas, 0)
	ending_condition = get_ending_condition(mas)
	while not eval(ending_condition+"(mas)"):
		run_one_cycle(mas)
		increment_cycle(mas)

# --- Terminal output ---

def show(mas):
	"""
		Print a description of the complete MAS as text.
	"""
	env = get_env(mas)
	pop = get_pop(mas)
	print("**** ENVIRONMENT ****")
	e.show(env)
	print("**** POPULATION ****")
	p.show(pop)