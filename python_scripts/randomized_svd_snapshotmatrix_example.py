"""
randomized_svd_snapshotmatrix_example.py
========================================
Apply the randomized Singular Value Decomposition (rSVD) to the snapshot matrix.
"""
import pathlib
from create_snapshotmatrix_from_ascii_file import (
    create_snapshotmatrix_from_file)
from KratosMultiphysics.RomApplication.randomized_singular_value_decomposition import (RandomizedSingularValueDecomposition)

if __name__ == "__main__":

    # Define path results file
    path_root = pathlib.Path().absolute()
    # name_file = "beam_simple.flavia.res"
    # name_file = "beam_simple.flavia_tstep1000_dt01.res"
    name_file = "beam_simple_f01hz_dt01_tsteps800_msh005.flavia.res"
    path_file = path_root / name_file

    snapshot_matrix = create_snapshotmatrix_from_file(path_file)

    # Compute randomized Singular Value Decomposition of the snapshot matrix
    tolerance = 1e-6
    u, s, _, _ = RandomizedSingularValueDecomposition().Calculate(
        snapshot_matrix, tolerance)
