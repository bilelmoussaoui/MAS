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

import mas as m
import mas_environment as e
import mas_cell as c
import mas_agent as p



#==================================================
#  Help functions
#==================================================

def eucl_dist(pos1, pos2):
    """
        Compute the Euclidian distance between two vectors.
    """
    dim = len(pos1)
    sq_dist = 0.0
    for i in range(dim):
        delta = pos1[i]-pos2[i]
        sq_dist += delta*delta
    return math.sqrt(sq_dist)

def vector_sum(vec1, vec2):
    """
        Compute the sum of two vectors.
    """
    dim = len(vec1)
    res = []
    for i in range(dim):
        res.append(vec1[i] + vec2[i])
    return tuple(res)

def vector_list_sum(vec_list, vec_add):
    """
        Add a vector to each vector in a list of vectors.
    """
    res = []
    for vec in vec_list:
        res.append(vector_sum(vec, vec_add))
    return tuple(res)

def vector_diff(vec1, vec2):
    """
        Compute the difference of two vectors.
    """
    dim = len(vec1)
    res = []
    for i in range(dim):
        res.append(vec1[i] - vec2[i])
    return tuple(res)

def into_list(data):
    """
        Return the parameter as element of a list. If it already
        is a list, do nothing and if the value is None, return an
        empty list.
    """
    if data is not None:
    	if type(data) is not list:
    		data = [data]
    else:
    	data = []
    return data

# --- Sorting ---

def sort_list(ls, order_fn):
    """
        Sort the list accord to the ordering function.
    """
    # Insertion sort
    for i in range(1, len(ls)):
        val = ls[i]
        j = i
        while j > 0 and order_fn(ls[j - 1], val):
            ls[j] = ls[j - 1]
            j -= 1
        ls[j] = val

def sort_on_second_list(ls1, ls2, order_fn):
    """
        Sort the two lists according to the ordering function
        applied on the second list.
    """
    # Insertion sort
    for i in range(1, len(ls2)):
        val1, val2 = ls1[i], ls2[i]
        j = i
        while j > 0 and order_fn(ls2[j - 1], val2):
            ls1[j], ls2[j] = ls1[j - 1], ls2[j - 1]
            j -= 1
        ls1[j], ls2[j] = val1, val2

def order_scalar_asc(val1, val2):
    """
        Ascending ordering function on scalar values to be
        used with sorting functions.
    """
    return val1 < val2

def order_tuple_second_asc(t1, t2):
    """
        Ascending ordering function on tuples, comparing the
        second element of the tuples. To be used with sorting 
        functions.
    """
    return t1[1] < t2[1]

#==================================================
#  Configuration (from a file)
#==================================================

def config_read_file(file_name):
    """
        Return a configuration parsed from the file. Each line of that
        file can contain at most one parameter definition, in the format:
        PARAM_NAME = value.
        Empty lines and lines starting with "#" (comments) are ignored.
    """
    f = open(file_name)
    all_lines = f.read().split("\n")
    f.close()
    config = {}
    for line in all_lines:
        if len(line)>0 and line.strip()[0]!="#":
            # Starting a line with "#" allows inserting comments.
            [key, val] = line.split("=")
            key = key.strip().upper()
            val = val.strip()
            # Check if the property has already been declared.
            if key in config:
                # If the existing value is not yet a list, make it
                # one so we can add a new value.
                if not type(config[key]) is list:
                    config[key] = [config[key]]
                config[key].append(val)
            else:
                config[key] = val
    return config

def config_get_property(config, property):
    """
        Return the property from the configuration (as a string).
    """
	# If the property does not exist, return None.
    return config.get(property,None)

def cfg_pop_size(config):
    """
        Return the population size from the configuration.
    """
    return int(config_get_property(config, "POP_SIZE"))

def cfg_env_size(config):
    """
        Return the environment size from the configuration.
    """
    return int(config_get_property(config, "ENV_SIZE"))    

def cfg_max_cycle(config):
    """
        Return (from the configuration) the maximum number of cycles 
        for the experiment.
    """
    return int(config_get_property(config, "MAX_CYCLE"))    

def cfg_cell_rules(config):
    """
        Return the list of cell rules from the configuration.
    """
    res = config_get_property(config,"ADD_CELL_RULE")
    res = into_list(res)
    return res

def cfg_agent_rules(config):
    """
        Return the list of agent rules from the configuration.
    """
    res = config_get_property(config,"ADD_AGENT_RULE")
    res = into_list(res)
    return res

def cfg_capacity_distributions(config):
    """
        Return the list of capacity distribution statements from 
        the configuration.
    """
    res = config_get_property(config,"ADD_CAPACITY_DISTRIB")
    res = into_list(res)
    return res	

def cfg_order_activation(config):
    """
        Fonction qui extrait l'ordre d'activation voulu dans le fichier de configuration
    """
    return config_get_property(config,"ORDER_ACTIVATION")

def cfg_ending_condition(config):
    """
        Fonction qui extrait la fonction permettant d'arréter le simulation dans le fichier de configuration
    """
    return config_get_property(config,"ENDING_CONDITION")

def cfg_env_properties(config):
    """
        Fonction qui extrait les propriétés de l'environement du fichier de configuration
    """
    env = config_get_property(config,"ENV")
    env_properties = {}
    parameter = env.split(":")
    key   = parameter[0].strip().upper()
    value = eval(parameter[1].strip())
    env_properties[key] = value
    return env_properties

def cfg_pop_properties(config):
    """
        Fonction qui extrait les propriétés de la population du fichier de configuration et 
        qui renvoie un dictionnaire contenant les propriétés et les valeurs de la population
    """
    pop = config_get_property(config,"POP")
    pop_properties = {}
    for i in pop:
        parameter = i.split(":")
        key   = parameter[0].strip().upper()
        value = eval(parameter[1].strip())
        pop_properties[key] = value
    return pop_properties
