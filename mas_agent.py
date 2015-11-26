#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================

import mas_cell as c
import mas_utils as u
import mas_population as p
import mas_environment as e

from random import randint,uniform

#==================================================
#  AGENT
#==================================================   

# --- Constants ---
AGENT_MAX_IDX = 6
AGENT_METABOLISM_IDX = 0
AGENT_POSITION_IDX = 1
AGENT_SUGAR_LEVEL_IDX = 2
AGENT_VISION_CAPACITY_IDX = 3
AGENT_AGE_IDX = 4
AGENT_POPULATION_IDX =  5
AGENT_SEX_IDX = 6

# --- Private functions --- 

# Note: These functions should not be called outside this module.
def __get_property(agent,property_idx):
	if not (0 <= property_idx <= AGENT_MAX_IDX):
		raise Exception(" __get_property file: mas_agent propoery_idx: ",property_idx)
	return agent[property_idx]

def __set_property(agent,property_idx,value):
	if not (0 <= property_idx <= AGENT_MAX_IDX):
		raise Exception(" __set_property file: mas_agent propoery_idx: ",property_idx)
	agent[property_idx] = value

def __empty_instance():
    # Return an empty agent instance.
    return [None]*(AGENT_MAX_IDX+1)

def new_instance(pop):
	agent = __empty_instance()
	#Recupère la liste des propriétés 
	prop = p.get_properties(pop)
	set_population(agent,pop)
	#choisi une valeur aléatoire entre les minimum et maximum venant du fichier de configuration
	set_vision_capacity(agent,randint(prop["MIN_VISION_CAPACITY"],prop["MAX_VISION_CAPACITY"]))
	set_metabolism(agent,uniform(prop["MIN_METABOLISM"],prop["MAX_METABOLISM"]))
	#les agents ont au départ un âge reflettant le réalisme
	set_age(agent,randint(prop["MIN_AGENT_AGE"],prop["MAX_AGENT_AGE"]))
	#La réserve en sucre au départ est suffisante à sa survie (métabolism)
	set_sugar_level(agent,get_metabolism(agent))
	env = p.get_env(pop)
	random_position = e.random_cell_ref_without_agent(env)
	set_pos(agent,random_position)
	cell = e.get_cell(env,random_position)
	set_sex(agent,randint(1,2))
	c.set_present_agent(cell,agent)
	return agent

# --- Getters and Setters ---
def get_sugar_level(agent):
	return __get_property(agent,AGENT_SUGAR_LEVEL_IDX)

def set_sugar_level(agent,sugar_level):
	if sugar_level < 0:
		raise ValueError("Attention niveau sucre toujours positif")
	#vérification que le niveau de sucre ne dépasse pas la limite
	elif sugar_level > p.get_pop_property(get_population(agent),"MAX_SUGAR_LEVEL"):
		raise ValueError("attention niveau de sucre supérieur à celui de la population")
	__set_property(agent,AGENT_SUGAR_LEVEL_IDX,sugar_level)

def set_sex(agent,sex):
	if not sex in [1,2]:
		raise ValueError("Attention, dans notre simulation on envisage que deux sexe. le 1 corresepend à la famme, et le 2 corresepend à l'homme ")
	__set_property(agent,AGENT_SEX_IDX,sex)

def get_sex(agent):
	return __get_property(agent,AGENT_SEX_IDX)
	
def get_vision_capacity(agent):
	return __get_property(agent,AGENT_VISION_CAPACITY_IDX)

def set_vision_capacity(agent,vision_capacity):
	if vision_capacity <= 0: 
		raise ValueError(" Attention la vision est strictement positif")
	__set_property(agent,AGENT_VISION_CAPACITY_IDX,int(vision_capacity))

def get_metabolism(agent):
	return __get_property(agent,AGENT_METABOLISM_IDX)

def set_metabolism(agent,metabolism):
	if metabolism <= 0: 
		raise ValueError(" Attention le métabolisme est strictement positif")
	__set_property(agent,AGENT_METABOLISM_IDX,metabolism)

def get_pos(agent):
	return __get_property(agent,AGENT_POSITION_IDX)

def set_pos(agent,position):
	__set_property(agent,AGENT_POSITION_IDX,position)

def get_age(agent):
	return __get_property(agent,AGENT_AGE_IDX)

def set_age(agent,age):
	if age < 0:
		raise Exception("Attention un âge ne peut être négatif")
	__set_property(agent,AGENT_AGE_IDX,age)

def get_population(agent):
	return __get_property(agent,AGENT_POPULATION_IDX)

def set_population(agent,population):
	__set_property(agent,AGENT_POPULATION_IDX,population)

def get_env(agent):
	return p.get_env(get_population(agent))

def get_cell(agent):
	return e.get_cell(get_env(agent),get_pos(agent))

def show(agent):
	"""
		affiche à la fin de la simulation un résumé sur l'état final de chaque agent
	"""
	print(get_pos(agent),":",end=" ")
	sex = ('female:' if get_sex(agent) == 1 else 'male')
	print(sex,end=" ")
	print("age:",get_age(agent),end=" ")
	print("metabolism:",round(get_metabolism(agent),2),end=" ")
	print("reserve:",round(get_sugar_level(agent),2),end=" ")
	print("vision capacity:", get_vision_capacity(agent))

def has_max_sugar_level(agent):
	"""
		vérifie que l'agent a déjà un niveau de sucre saturé
	"""
	sugar_level = get_sugar_level(agent)
	pop = get_population(agent)
	max_sugar_level = p.get_pop_property(pop,"MAX_SUGAR_LEVEL")
	return (sugar_level >= max_sugar_level)

def move(agent,position):
	"""
		Change la position de l'agent
	"""
	env = get_env(agent)	
	current_position = get_pos(agent)
	cell = e.get_cell(env,current_position)
	target_cell = e.get_cell(env,position)
	if c.agent_is_present(target_cell):
		raise Exception("cannot move an agent to a cell while theres is an other agent")
	set_pos(agent,position)
	c.set_present_agent(cell,None)
	c.set_present_agent(target_cell,agent)

def consumption_sugar(agent,amount):
	"""
		consomation de sucre par l'agent
		amount : quantité de sucre qui va être consomé (s'il le peut)
	"""
	cell = get_cell(agent)
	pop  = get_population(agent)
	c_sugar_level  = c.get_sugar_level(cell)
	a_sugar_level = get_sugar_level(agent)
	metabolism 	= get_metabolism(agent)
	max_sugar_level = p.get_pop_property(pop,"MAX_SUGAR_LEVEL")
	if (amount >= metabolism):
		if not has_max_sugar_level(agent):
			a_sugar_level += amount - metabolism
			if a_sugar_level > max_sugar_level:
				a_sugar_level = max_sugar_level
				c_sugar_level  -= amount 
		else:
			a_sugar_level -= metabolism
	elif (amount + a_sugar_level) >= metabolism:
		a_sugar_level -= metabolism - amount
		c_sugar_level -= amount
	set_sugar_level(agent,a_sugar_level)
	c.set_sugar_level(cell,c_sugar_level)

def accecible_positions(agent):
	"""
		cherche toutes les positions accesibles à l'agent
	"""	
	env = get_env(agent)
	x , y = get_pos(agent) 
	positions = []
	#le surpoids d'un agent entraîne la diminution de sa capacité de vision
	if not has_max_sugar_level(agent) :
		vision = get_vision_capacity(agent)
	else:
		vision = 1 
	step = -vision
	while step <= vision:
		if step != 0:
			move_x = correct_position((x+step,y),env)
			move_y = correct_position((x,y+step),env)
			if is_possible_to_move(agent,move_x):
				positions.append(move_x)
			if is_possible_to_move(agent,move_y):
				positions.append( move_y )
		step+=1
	return positions

def is_possible_to_move(agent,position):
	"""
		vérifie si un agent peut se déplcer, on vérifie si: la quantité de sucre de la cellule additionnée 
			à la réserve de sucre de l'agent est suffisante au métabolisme, 
			si il n'y a pas d'agent dans sa cellule
	"""
	env = get_env(agent)
	cell = e.get_cell(env,position)	
	possible_to_move =  not c.agent_is_present(cell)  \
				and (c.get_sugar_level(cell)+get_sugar_level(agent)) >= get_metabolism(agent)
	return possible_to_move

def get_is_living(agent):
	"""
		vérifie si un agent est vivant : s'il a assez à manger, s'il peut se déplacer et si son age ne dépasse pas la limite 
	"""
	cell = get_cell(agent)
	cell_sugar_level = c.get_sugar_level(cell)
	metabolism = get_metabolism(agent)
	agent_sugar_level = get_sugar_level(agent)
	age = get_age(agent)
	pop = get_population(agent)
	max_age = p.get_pop_property(pop,"MAX_AGENT_AGE")
	is_alive = (cell_sugar_level+agent_sugar_level >= metabolism) and age <= max_age
	if not is_alive:
		kill(agent)
	return is_alive

def kill(agent):
	"""
		Fonction qui tue un agent 
	"""
	pop = get_population(agent)
	agents = p.get_agents(pop)
	cell = get_cell(agent)
	p.increment_dead_agents(pop)
	if agent in agents:
		del agents[agents.index(agent)]
	c.set_present_agent(cell,None)

def correct_position(position,env):
	"""
		corrige la position : passer d'une cellule du bord de l'environement à la cellule opposé
	"""
	n_line = n_row = e.size(env) 
	x,y = position
	return (x % n_row, y % n_line)

def average_living(pop,cell_refs):
	""" 
		cherche le niveau de vie moyen des agents situé dans un bloc de coté 6 (zone*2) centré dans la cellule cible 
	"""
	x,y = cell_refs
	zone = 3
	cells_average_list = []
	sugar_level_sum = 0
	agents_in_zone_of_cell = 0
	env = p.get_env(pop)
	pos_start_calc = correct_position((x-zone,y+zone),env)
	xi,yi = pos_start_calc
	i = 0
	j = -2*zone
	for j in range(-2*zone,0,1):
		for i in range(0,2*zone):
			if i!=j:
				cell = e.get_cell(env,correct_position((xi+i,yi+j),env))
				if c.agent_is_present(cell):
					agents_in_zone_of_cell +=1
					sugar_level_sum += get_sugar_level(c.get_present_agent(cell))
	if agents_in_zone_of_cell != 0:
		average = sugar_level_sum/agents_in_zone_of_cell
	else:
		average = 0
	return average

def theres_is_an_other_sex_around(agent):
	"""
		évaluer la présence d’un potentiel (dans le sens ou il peut se reproduire avec) agent à proximité
	"""
	vision = 1
	x,y = get_pos(agent)
	agent_sex = get_sex(agent)
	env = get_env(agent)
	already_found = False
	i = -vision
	while i <= vision and not already_found:
		if i !=0:
			cell_x = e.get_cell(env,correct_position((x,y+vision),env))
			cell_y = e.get_cell(env,correct_position((x+vision,y),env))
			if c.agent_is_present(cell_x):
				already_found = (get_sex(c.get_present_agent(cell_x)) != agent_sex)
			if c.agent_is_present(cell_y):
				already_found = (get_sex(c.get_present_agent(cell_y)) != agent_sex)
		i+=1
	return already_found

def is_an_agent_can_be_there_faster(agent,target):
	"""
		si un autre agent peut atteindre avant la cellule visée
	"""	
	pop = get_population(agent)
	agents = p.get_agents(pop)
	i=0
	already_found = False
	while i < len(agents) and not already_found:
		if agents[i] != agent and target in accecible_positions(agents[i]):
			already_found = (u.eucl_dist(get_pos(agents[i]),target) < u.eucl_dist(get_pos(agent),target)) 
		i+=1
	return already_found

def total_gain(agent,target):
	"""
		calculer les réserves de l’agent additionnée à l’ensemble du sucre qu’il récupérera durant son voyage soustrait 
			au métabolisme consommé à chaque étape	
	"""	
	pop = get_population(agent)
	env = get_env(agent)
	pos = get_pos(agent)
	sugar_level = get_sugar_level(agent)
	#x_diff,y_diff
	xd,yd = u.vector_diff(pos,target)
	if xd == 0: #the same line
		steps = abs(yd)
		step  = (1 if yd < 0 else -1)
		for i in range(steps):
			cell_refs = correct_position((pos[0],pos[1]+step*i),env)
			cell  = e.get_cell(env,cell_refs)
			sugar_level += c.get_sugar_level(cell)
	else: #the same row
		steps = abs(xd)
		step  = (1 if xd < 0 else -1)
		for i in range(steps):
			cell_refs = correct_position((pos[0]+step*i,pos[1]),env)
			cell  = e.get_cell(env,cell_refs)
			sugar_level += c.get_sugar_level(cell)
	return sugar_level - get_metabolism(agent)*steps
	
def is_interested_to_move(agent,target):
	"""
		- vérifier si le total_gain(agent,target) est plus grand que zèro 
		- si un autre agent peut atteindre la cellule avant lui
		- si il n'y a pas d'agents dans la direction choisie 
	"""
	pos = get_pos(agent)
	xd,yd = u.vector_diff(pos,target)
	env = get_env(agent)
	agent_on_way = False
	if xd == 0:
		step  = (1 if yd < 0 else -1)
		next_move = correct_position((pos[0],pos[1]+step),env)
		agent_on_way = c.get_present_agent(e.get_cell(env,next_move))
	else:
		step  = (1 if xd < 0 else -1)
		next_move = correct_position((pos[0]+step,pos[1]),env)
		agent_on_way = c.get_present_agent(e.get_cell(env,next_move))
	return (not is_an_agent_can_be_there_faster(agent,target) and not agent_on_way and total_gain(agent,target) > 0)

#====================	==============================
#  AGENT RULES 
#==================================================
#
# Agent rule functions must comply to the following
# signature:
# 
#  INPUT:  The agent the rules is applied on
#
#  OUTPUT: None.
#
#==================================================

def grow_up(agent):
	""" règle de l'evolution de l'âge de l'agent par cycle
	"""
	age = get_age(agent)
	pop = get_population(agent)
	max_age = p.get_pop_property(pop,"MAX_AGENT_AGE")
	if age <= max_age:
		set_age(agent,age+1)

def eat_all(agent):
	"""
		consomme tout le sucre de la cellule
	"""
	cell = get_cell(agent)
	amount = c.get_sugar_level(cell) 
	consumption_sugar(agent,amount)

def eat_half(agent):
	"""
		consomme la moitié du sucre de la cellule
	"""
	cell = get_cell(agent)	
	amount = c.get_sugar_level(cell)/2
	consumption_sugar(agent,amount)

def eat_quarter(agent):
	"""
		consomme le quart du sucre de la cellule
	"""
	cell = get_cell(agent)
	amount = c.get_sugar_level(cell)/4
	consumption_sugar(agent,amount)

def eat_metabolism(agent):
	"""
		consomme uniquement ce qu'il faut de sucre pour sa survie (métabolisme)
	"""
	metabolism = get_metabolism(agent)
	consumption_sugar(agent,metabolism)

def move_to_a_random_cell(agent):
	"""
		déplacer un agent à une position aléatoire
	"""
	cells_refs = accecible_positions(agent)
	if (len(cells_refs) > 1 ):
		move(agent,cells_refs[randint(0,len(cells_refs)-1)] )
	elif (len(cells_refs) == 1 ):
		move(agent,cells_refs[0])

def move_to_the_highest_sugar_level_cell(agent):

	"""
		RA1 : déplace l'agent dans la cellule à quantité de sucre la plus élevée
	"""
	cells_refs = accecible_positions(agent)
	if len(cells_refs) > 0:
		highest = cells_refs[0]
		env = get_env(agent)
		for i in range(len(cells_refs)):
			cell = e.get_cell(env,cells_refs[i])
			highest_cell = e.get_cell(env,highest)
			if c.get_sugar_level(cell) > c.get_sugar_level(highest_cell):
				highest = cells_refs[i]
		move (agent,highest)

def move_by_only_a_cell(agent):
	"""
		RA2 : l'agent ne peut se déplacer que d'une cellule par cycle en verifiant certains conditions développées dans la fonction 
			is_interested_to_move
	"""
	xi,yi = get_pos(agent)
	env = get_env(agent)
	acc_refs = accecible_positions(agent)
	found_target = False
	size_poss = len(acc_refs)
	if size_poss != 0:
		sorted_list = e.sort_sugar_level_desc(env,acc_refs)
		i = 0
		#car la liste est triée
		maximum = sorted_list[0]
		while i < size_poss and not found_target:
			if not is_interested_to_move(agent,maximum):
				if i+1 < size_poss:
					maximum = sorted_list[i+1]
			else:
				found_target = True
			i+=1
	if found_target:
		xf,yf = maximum
		xd,yd = u.vector_diff(get_pos(agent),maximum)
		if xd == 0:
			step  = (1 if yd < 0 else -1)
			move_y =  correct_position((xi,yi+step),env)
			move(agent,move_y)
		else:
			step  = (1 if xd < 0 else -1)
			move_x =  correct_position((xi+step,yi),env)
			move(agent,move_x)

def move_to_the_lowest_sugar_level_cell(agent):
	"""
		RA3 : déplace l'agent dans la cellule à quantité de sucre la moins élevée
		et assez pour son métabolisme
	"""
	cells_refs = accecible_positions(agent)
	if len(cells_refs) > 0:
		lowest = cells_refs[0]
		env = get_env(agent)
		for i in range(len(cells_refs)):
			cell = e.get_cell(env,cells_refs[i])
			lowest_cell = e.get_cell(env,lowest)
			if c.get_sugar_level(cell) < c.get_sugar_level(lowest_cell):
				lowest = cells_refs[i]
		move (agent,lowest)

def move_by_averrage_living(agent):
	"""
		RA4 : déplace l'agent là ou le niveau de vie est plus élevé que son niveau de sucre
	"""
	pop = get_population(agent)
	cell_refs = get_pos(agent)
	cells_refs = accecible_positions(agent)
	already_moved = False
	i = 0
	while i < len(cells_refs) and not(already_moved):
		average = average_living(pop,cells_refs[i])
		if average > get_sugar_level(agent):
			move(agent,cells_refs[i])
			already_moved = True
		i+=1
	if not (already_moved):
		move_to_the_highest_sugar_level_cell(agent) # à verifier

def make_a_child(agent):
	"""
		règle permettant la reproduction asexuée selon une certaine probablité
		les agents doivent être dans un intervalle d'âge précis
	"""
	pop = get_population(agent)
	env = get_env(agent)
	min_age = p.get_pop_property(pop,"MIN_AGE_TO_MAKE_CHILDS")
	max_age = p.get_pop_property(pop,"MAX_AGE_TO_MAKE_CHILDS")
	max_pop = p.get_pop_property(pop,"MAX_POP")
	min_prob,max_prob = p.get_pop_property(pop,"PROB_TO_HAVE_SEX")
	if (min_age <= get_age(agent) <= max_age and theres_is_an_other_sex_around(agent) \
			  and randint(min_prob,max_prob) == 1 and p.size(pop) < max_pop ):
		new_child = new_instance(pop)
		set_age(new_child,0)
		set_sugar_level(agent,0)
		#le nouveau-née hérite du métabolisme et de la vision de capacité de son géniteur
		set_metabolism(new_child,get_metabolism(agent))
		set_vision_capacity(new_child,get_vision_capacity(agent))
		agents_list = p.get_agents(pop)
		agents_list.append(new_child)
