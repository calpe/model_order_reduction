"""
create_snapshot_matrix_from_modal_analysis.py
==============================================
Compute the snapshot matrix from one or a linear combination of eigenmodes of a structure.

The eigenmodes (and eigenfrequencies) have been obtained from a modal analysis with RamSeries.
"""
import numpy as np

path_file = '/home/usuari/Documentos/CIMNE/bibliografia/model_order_reduction/python_scripts/cantilever_eigenvalue.flavia.res'

f = open(path_file, "r")
lines = f.readlines()
f.close()

# Choose the modes
modes = [1]


# Create list of time steps
deg_freedom = 3  # displ_x, displ_y, displ_z
frequencies = []
values_list = []
for i_line, line in enumerate(lines):
    for mode in modes:
        if f'Result "Mode_{mode}_' in line and not "Modes_rotations" in line:
            print(line)
            frequencies.append(float(line.split()[2].split(")")[0]))
            i_jump = 3  # Lines to jump between header and values.
            values = []
            while lines[i_line + i_jump][0].isdigit():
                values.append(lines[i_line + i_jump])
                i_jump = i_jump + 1
            values_list.append(values)

# Choose duration of the sinthetic displacement field
t_start = 0
t_end = 10
duration = t_end - t_start  # in seconds

# 10 sampling points of the maximum frequency.
dt_sampling = 0.1 * 1. / np.max(frequencies)

# Compute number of time steps
nb_time_steps = round(duration / dt_sampling)

# Create snapshot matrix
nb_nodes = len(values_list[0])
snapshot_mtx = np.empty(shape=(len(modes), nb_nodes * deg_freedom, nb_time_steps))

# Create array of time
times = np.linspace(t_start, t_end, nb_time_steps)

i_node_snapshot_mtx = 0

## Buggy!
for i_mode in np.arange(len(modes)):
    for i_node in np.arange(nb_nodes)[:2]:
        print(i_node)
        displ_x = float(values_list[i_mode][i_node].split()[1]) * np.sin(0.8 * frequencies[i_mode] * 2 * np.pi * times)
        displ_y = float(values_list[i_mode][i_node].split()[2]) * np.sin(0.8 * frequencies[i_mode] * 2 * np.pi * times)
        displ_z = float(values_list[i_mode][i_node].split()[3]) * np.sin(0.8 * frequencies[i_mode] * 2 * np.pi * times)

        print(displ_z)
        # Add to snapshot matrix
        snapshot_mtx[i_mode, i_node_snapshot_mtx, :] = displ_x
        snapshot_mtx[i_mode, i_node_snapshot_mtx + 1, :] = displ_y
        snapshot_mtx[i_mode, i_node_snapshot_mtx + 2, :] = displ_z

        i_node_snapshot_mtx = i_node + 3