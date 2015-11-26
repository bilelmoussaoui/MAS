#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================


import mas_agent as a
import mas_environment as e
import mas_cell as c 
import mas as m 
import mas_utils as u
from random import shuffle,choice

#==================================================
#  POPULATION
#==================================================   

# --- Constants ---
POP_MAX_IDX = 3
POP_MAS_IDX = 0            # MAS the population belongs to
POP_AGENTS_LIST_IDX = 1    # The matrix of agents
POP_PROPERTIES_IDX = 2
POP_DEAD_AGENT = 3
# --- Private functions --- 

# Note: These functions should not be called outside this module.
def __get_property(pop, property_idx):
    if not (0 <= property_idx <= POP_MAX_IDX):
    	raise Exception(" __get_property file: mas_population propoery_idx: ",property_idx)
    return pop[property_idx]

def __set_property(pop, property_idx, value):
	if not (0 <= property_idx <= POP_MAX_IDX):
   		raise Exception(" __get_property file: mas_population propoery_idx: ",property_idx)
	pop[property_idx] = value
	
def __empty_instance():
    # Return an empty environment instance.
    return [None]*(POP_MAX_IDX+1)

def new_instance(mas,config):
	size = u.cfg_pop_size(config)
	properties = u.cfg_pop_properties(config)
	pop = __empty_instance()
	set_properties(pop,properties)
	set_mas(pop, mas)
	set_dead_agents(pop,0)
	agents = __empty_agent_list( pop,size)
	set_agents(pop, agents)
	return pop

def __empty_agent_list(pop,size):
	agents_list = []
	for i in range (size):
		agents_list.append(a.new_instance(pop))
	return agents_list

def get_mas(pop):
	return __get_property(pop,POP_MAS_IDX)

def set_mas(pop,mas):
	__set_property(pop,POP_MAS_IDX,mas)

def set_agents(pop,agents_list):
	__set_property(pop,POP_AGENTS_LIST_IDX,agents_list)

def get_agents(pop):
	return __get_property(pop,POP_AGENTS_LIST_IDX)

def set_dead_agents(pop,dead_agents):
	if dead_agents < 0:
		raise ValueError("cannot have a negative dead agents number")
	__set_property(pop,POP_DEAD_AGENT,dead_agents)

def increment_dead_agents(pop):
	set_dead_agents(pop,get_dead_agents(pop)+1)

def get_dead_agents(pop):
	return __get_property(pop,POP_DEAD_AGENT)

def get_pop_property(pop,property):
	"""
	l'ensemble des propriétés sont regroupées dans un dictionnaires, 
	cette fonction cherche dans ce dictionnaire la clé correspondant à la propriété cherchée 
	et retourne la valeur associé
	"""
	properties = get_properties(pop)
	return properties[property]

def set_properties(pop,properties):
	__set_property(pop,POP_PROPERTIES_IDX,properties)

def get_properties(pop):
	return __get_property(pop,POP_PROPERTIES_IDX)

def get_env(pop):
	mas = get_mas(pop)
	env = m.get_env(mas)
	return env

def size(pop):
	"""
		fonction renvoyant la taille de la population
	"""
	return len(get_agents(pop))

def show(pop):
	"""
		affiche à la fin de la simulation un résumé
	"""
	agents = get_agents(pop)
	male,female = get_agents_alive_by_sex(pop)
	print("alive agents ", male+female)
	print("alive male : ",male)
	print("alive female : ", female)
	for agent in agents:
		a.show(agent)


def get_agents_alive_by_sex(pop):
	"""
		compte le nombre d'agent vivant en fonction du sexe
	"""
	male = 0
	female = 0
	agents = get_agents(pop)
	for i in range(len(agents)):
		if a.get_sex(agents[i]) == 1:
			female +=1
		else:
			male += 1
	return (male,female)


def apply_rule(pop,rule):
	"""
		Fonction appliquant une règle à l'ensemble des agents
	"""
	agents = get_agents(pop)
	size = len(agents)
	for i in range(size):
		rule(agents[i])

#==================================================
#  Population Rules (ordre d'activation)
#==================================================

def active_agents_randomly(pop):
	"""
		OA1: ordre d’activation aléatoire : 
			aucun agent n'est privilégié et donc chacun des agent à la même chance de "s'activer"
	"""
	agents = get_agents(pop)
	size = len(agents)
	suffled_agents_list = []
	for i in range(size):
		agent = choice(agents)
		del agents[agents.index(agent)]
		suffled_agents_list.append(agent)
	set_agents(pop,suffled_agents_list)

def active_agents_by_sugar_level(pop):
	"""
		OA2: ordre d'activation régulé: les agents sont activés dans l'ordre croissant de leur niveau de sucre,
			donc ceux avec le moins de sucre sont activés en premier: fovorise les plus "faibles”
	"""
	agents_list = get_agents(pop)
	sugar_level_list = []
	for i in range(len(agents_list)):
		sugar_level_list.append(a.get_sugar_level(agents_list[i]))
	u.sort_on_second_list(agents_list,sugar_level_list,u.order_scalar_asc)
	sorted_agents_list = agents_list[::-1]
	set_agents(pop,sorted_agents_list)
