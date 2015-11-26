#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#  ---------------------------------------------
#   Many thanks to Robert Vanden Eynde for 
#   providing this part of the code!
#  ---------------------------------------------
#
#==================================================



import mas as m
import mas_environment as e
import mas_cell as c
import mas_population as p
import mas_agent as a

import tkinter as tk



#==================================================
#  VISUALISATION
#==================================================

# --- Constants ---

TIME_OF_FRAME = 10        # millisecondes
MARGIN = 20               # margin around the environment
TEXT_HEIGHT = 10          # height of text zone above the environment

# --- Private functions --- 

# Note: These functions should not be called outside this module.

def __compute_cell_color(cell):
    # Compute the color of the cell, depending on its sugar level
    sugar_level = c.get_sugar_level(cell)
    env = c.get_env(cell)
    max_capacity = e.get_max_capacity(env)
    ratio = sugar_level / max_capacity
    color_level = int(255 * (1 - ratio))
    # convert the color level to hexadecimal representation
    hex_color_level = hex(color_level)[2:].zfill(2)
    color_code = '#' + 'ff' + 'ff' + hex_color_level
    return color_code

def __bbox_for_cell_ref(cell_ref, cell_size, scale=1):
    # Compute the size of a cell box
    x, y = cell_ref
    d = (1 - scale) / 2
    return (
        MARGIN + (x + d) * cell_size,
        MARGIN + TEXT_HEIGHT + (y + d) * cell_size, 
        MARGIN + (x + 1 - d) * cell_size, 
        MARGIN + TEXT_HEIGHT + (y + 1 - d) * cell_size
    ) 

def __swap_y (env_size, cell_ref):
    # Correct the y-coordinate to be consistent with the origin of the
    # coordinate sytem being in the lower left corner of the plot
    (x, y) = cell_ref
    return (x, env_size - y)

def __draw_env(canvas, env, cell_size):
    # Draw the environment on the canvas
    env_size = e.size(env)
    for cell_ref in e.get_cell_refs(env):
        cell = e.get_cell(env, cell_ref)
        cell_ref = __swap_y(env_size, cell_ref)
        canvas.create_rectangle(__bbox_for_cell_ref(cell_ref, cell_size), fill=__compute_cell_color(cell), outline='#dddddd')

def __draw_pop(canvas, pop, cell_size):
    # Draw the population on the canvas
    env = p.get_env(pop)
    env_size = e.size(env)
    for agent in p.get_agents(pop):
        if a.get_is_living(agent):
            if a.get_sex(agent) == 1:
                color = 'red'
            else:
                color = 'black'
            cell_ref = __swap_y(env_size, a.get_pos(agent))
            canvas.create_oval(__bbox_for_cell_ref(cell_ref, cell_size, 0.6), fill=color, width=0)

def __draw_mas(canvas, mas, cell_size):
    # Draw the MAS on the canvas
    env = m.get_env(mas)
    pop = m.get_pop(mas)
    if env is not None: 
        __draw_env(canvas, env, cell_size)
        # Only consider plotting the population if there is an environment
        if pop is not None:
            __draw_pop(canvas, pop, cell_size)

# --- Run an experiment in visual mode
def run_experiment(mas, window_size=600):
    """
        Run an experiment on the initialised MAS with
        an animated graphical representation.
    """
    # Initialise the graphical environment (tkinter)
    app = tk.Tk()
    app.geometry(str(window_size-TEXT_HEIGHT) + 'x' + str(window_size))
    canvas = tk.Canvas(app, width=window_size-TEXT_HEIGHT, height=window_size)
    canvas.pack()
    cell_size = (window_size - 2*MARGIN - TEXT_HEIGHT) / e.size(m.get_env(mas))
    # Define a local function that represents the "graphical loop"
    def tki_experiment_loop(mas):
        cycle = m.get_cycle(mas)
        canvas.delete(tk.ALL) # Clear the canvas
        __draw_mas(canvas, mas, cell_size)
        pop = m.get_pop(mas)
        canvas.create_text(MARGIN, MARGIN, anchor=tk.NW, text="Cycle #" + str(cycle))
        male,female = p.get_agents_alive_by_sex(pop)
        canvas.create_text(MARGIN, MARGIN-15, anchor=tk.NW, text="Population #" + str(male+female))
        canvas.create_text(MARGIN+100, MARGIN, anchor=tk.NW, text="Femme #" + str(female))
        canvas.create_oval(MARGIN+180,MARGIN-4,MARGIN+188,MARGIN-12,fill='black')
        canvas.create_text(MARGIN+100, MARGIN-15, anchor=tk.NW, text="Homme #" + str(male))
        canvas.create_oval(MARGIN+180,MARGIN+3,MARGIN+188,MARGIN+11,fill='red')
        canvas.create_text(MARGIN+200, MARGIN,anchor=tk.NW, text="Dead agents #" + str(p.get_dead_agents(pop)))
        if not eval("m."+ending_condition+"(mas)"):
            m.increment_cycle(mas)
            m.run_one_cycle(mas)
            app.update()
            app.after(TIME_OF_FRAME, tki_experiment_loop, mas)
    # Initialise the experiment (the MAS)
    m.set_cycle(mas, 0)
    ending_condition = m.get_ending_condition(mas)
    # Run the experiment
    tki_experiment_loop(mas)
    app.mainloop()
