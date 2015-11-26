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
import mas_population as p
import mas_utils as u

import mas_visual as v

# Uncoment the following line to use "static" plots.
# CAUTION: This only works if matplotlib is installed.
#import mas_graphics as g



#==================================================
#  TESTING
#==================================================

# Read the configuration file
conf = u.config_read_file("config.cfg")

# Create a new MAS instance from that configuration
mas = m.new_instance_from_config(conf)

# Set the sugar level of each cell to its capacity
# (otherwise, the agent would die immediately because
# there would initially be no sugar in the environment)
env = m.get_env(mas)
e.set_cell_sugar_level_to_capacity(env)

# Run experiment (with or without visualisation)
#m.run_experiment(mas)
v.run_experiment(mas)

#m.show(mas)
# Plot the result at the end of the experiment
# CAUTION: This only works if matplotlib is installed.
#g.mas_plot(mas)
