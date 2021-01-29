# create_snapshotmatrix_from_ascii_file.py
# -----------------------------------------
# Script to compute the snapshot matrix from an output ascii file from Compass.

# Import libraries
import numpy as np

# Open file in reading mode
name_file = 'beam_simple.flavia.res'
f = open(name_file, 'r')

# Read lines and close file
lines = f.readlines()
f.close()

# Create list of time steps
deg_freedom = 3  # displ_x, displ_y, displ_z
t = []
values_list = []

for i_line, line in enumerate(lines):
    if 'Result "Displacements (m)"' in line:
        t.append(float(line.split()[4]))
        i_jump = 3  # Lines to jump between header and values.
        values = []

        while lines[i_line + i_jump][0].isdigit():
            values.append(lines[i_line + i_jump])
            i_jump = i_jump + 1

        values_list.append(values)


nb_nodes = len(values_list[0])
nb_time_steps = len(values_list)

# Create snapshot matrix
snapshot_mtx = np.empty(shape=(nb_nodes * deg_freedom, nb_time_steps))

for i_time_step in np.arange(nb_time_steps):
    values_to_list = []

    # Convert string to float values (displ_x, displ_y, displ_z)
    for i_node in np.arange(nb_nodes):
        values_to_list.append(float(values_list[i_time_step][i_node].split()[1]))
        values_to_list.append(float(values_list[i_time_step][i_node].split()[2]))
        values_to_list.append(float(values_list[i_time_step][i_node].split()[3]))

    snapshot_mtx[:, i_time_step] = np.array(values_to_list)