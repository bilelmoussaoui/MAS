#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================



import mas as m
import mas_environment as e
import mas_cell as c
import mas_population as p
import mas_agent as a

import matplotlib.pyplot as plt



#==================================================
#  PLOTTING
#==================================================

def env_plot(env, showGrid=True):
    """
        Add a plot of the environment (possibly including a
        grid) to the current pylab plot. 
        To actually show the plot, the pylab.show() method
        still has to be invoked.
    """
    ax = plt.gca()
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    sz = e.size(env)
    mat = []
    row = []
    col = []
    sugar = []
    size_factor = 3000.0/sz/e.get_max_capacity(env)
    # Plot sugar level of each cell
    for cell_ref in e.get_cell_refs(env):
        cell = e.get_cell(env, cell_ref)
        (y, x) = cell_ref
        row.append(y+0.5)
        col.append(x+0.5)
        sugar.append(size_factor*c.get_sugar_level(cell))
    plt.scatter(row, col, sugar, color='yellow', alpha=1)#, marker='s')
    # Plot the grid (or only an outer border)
    for k in range(sz+1):
        if showGrid or k == 0 or k == sz:
            plt.plot([k, k], [0, sz], color='black', alpha=0.1, ls='-')
            plt.plot([0, sz], [k, k], color='black', alpha=0.1, ls='-')

def pop_plot(pop):
    """
        Add a plot of the each agent to the current pylab plot. 
        To actually show the plot, the pylab.show() method
        still has to be invoked.
    """
    agents_list = p.get_agents(pop)
    for agent in agents_list:
        agent_plot(agent)

def agent_plot(agent):
    if a.get_is_living(agent):
        pos = a.get_pos(agent)
        env = a.get_env(agent)
        plt.scatter([pos[0]+0.5], [pos[1]+0.5], color='red', s=500.0/e.size(env))

def mas_plot(mas, showGrid=True):
    """
    	Plot the complete complete MAS as a matplotlib graphic.
    """	
    env = m.get_env(mas)
    pop = m.get_pop(mas)
    plt.axes([0, 0, 1, 1], axisbg=None, frameon = False) 
    if env is not None:
        env_plot(env, showGrid)
        # Only consider plotting the population if there is an environment
        if pop is not None:
            pop_plot(pop)
    plt.show()
