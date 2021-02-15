"""
create_snapshotmatrix_from_ascii_file.py
========================================

Script to compute the snapshot matrix from an output ascii file from Compass.
"""
# Import libraries
import pathlib
import numpy as np
import matplotlib.pyplot as plt


def create_snapshotmatrix_from_file(path_file):
    """ Compute snapshot matrix from output ascii file of Compass."""

    # Read lines and close file
    f = open(path_file, 'r')
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

    return snapshot_mtx


def plot_displacements_time_per_node(
        snapshot_matrix, deg_freedom=3, nb_nodes_decimation=20):
    """
    Plot displacements as function of time per node.
    Only implemented for the output file: 
    beam_simple_f01hz_dt01_tsteps800_msh005.flavia.res
    """

    # Create parameters figure
    fig, ax = plt.subplots()
    ax.set_xlabel("t(s)")
    ax.set_ylabel("u (m)")

    # Create array time
    times = np.arange(0, 80, 0.1)

    # Create array indices
    array_indices = np.arange(1, 201, deg_freedom * nb_nodes_decimation)

    # Plot each node
    for ii, node in enumerate(array_indices):
        ax.plot(times, snapshot_matrix[node], "-o", label=f"Node {node}")

    plt.legend()

    return fig, ax


if __name__ == "__main__":

    # Define path results file
    path_root = pathlib.Path().absolute()
    # name_file = "beam_simple.flavia.res"
    name_file = "beam_simple_f01hz_dt01_tsteps800_msh005.flavia.res"
    path_file = path_root / name_file

    # Create snapshot matrix from output file
    snapshot_matrix = create_snapshotmatrix_from_file(path_file)

    # Plot displacement at some nodes
    if name_file == "beam_simple_f01hz_dt01_tsteps800_msh005.flavia.res":
        fig, ax = plot_displacements_time_per_node(snapshot_matrix)
    else:
        print(
            "Plot only implemented for output file          beam_simple_f01hz_dt01_tsteps800_msh005.flavia.res")

    plt.show()
