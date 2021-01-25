import KratosMultiphysics
import KratosMultiphysics.RomApplication as romapp
from KratosMultiphysics.RomApplication.randomized_singular_value_decomposition import RandomizedSingularValueDecomposition
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import StructuralMechanicsAnalysis
from KratosMultiphysics.RomApplication.structural_mechanics_analysis_rom import StructuralMechanicsAnalysisROM
from matplotlib import pyplot as plt
import numpy as np
import json




"""
For user-scripting it is intended that a new class is derived
from StructuralMechanicsAnalysis to do modifications
"""

class StructuralMechanicsAnalysisSavingData(StructuralMechanicsAnalysis):

    def __init__(self,model,project_parameters):
        super().__init__(model,project_parameters)
        self.time_step_solution_container = []

    def FinalizeSolutionStep(self):
        super().FinalizeSolutionStep()
        ArrayOfDisplacements = []
        for node in self._GetSolver().GetComputingModelPart().Nodes:
            ArrayOfDisplacements.append(node.GetSolutionStepValue(KratosMultiphysics.DISPLACEMENT_X, 0))
            ArrayOfDisplacements.append(node.GetSolutionStepValue(KratosMultiphysics.DISPLACEMENT_Y, 0))
            ArrayOfDisplacements.append(node.GetSolutionStepValue(KratosMultiphysics.DISPLACEMENT_Z, 0))
        self.time_step_solution_container.append(ArrayOfDisplacements)


    def EvaluateQuantityOfInterest(self):
       ##############################################################################################
       #     Functions evaluating the QoI of the problem: Snapshot matrix of every time step        #
       #                                                                                            #
       ##############################################################################################
        SnapshotMatrix = np.zeros((len(self.time_step_solution_container[0]), len(self.time_step_solution_container)))
        for i in range(len(self.time_step_solution_container)):
            Snapshot_i= np.array(self.time_step_solution_container[i])
            SnapshotMatrix[:,i] = Snapshot_i.transpose()
        return SnapshotMatrix









if __name__ == "__main__":
    ##############################################################################################
    #                                           TRAIN ROM                                        #
    ##############################################################################################
    with open("ProjectParameters.json",'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())


    model = KratosMultiphysics.Model()
    simulation = StructuralMechanicsAnalysisSavingData(model,parameters)
    simulation.Run()
    SnapshotMatrix = simulation.EvaluateQuantityOfInterest()


    ## Taking the SVD ###
    u,s,_,_= RandomizedSingularValueDecomposition().Calculate(SnapshotMatrix,1e-6)


    ### Plotting singular values  ###
    plt.plot( range(0,len(s)), np.log(s), marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    plt.title('Singular Values')
    plt.show()

    ### Saving the nodal basis ###  (Need to make this more robust, hard coded here)
    basis_POD={"rom_settings":{},"nodal_modes":{}}
    basis_POD["rom_settings"]["nodal_unknowns"] = ["DISPLACEMENT_X","DISPLACEMENT_Y","DISPLACEMENT_Z"]
    basis_POD["rom_settings"]["number_of_rom_dofs"] = np.shape(u)[1]
    Dimensions = len(basis_POD["rom_settings"]["nodal_unknowns"])
    N_nodes=np.shape(u)[0]/Dimensions
    N_nodes = int(N_nodes)
    node_Id=np.linspace(1,N_nodes,N_nodes)
    i = 0
    for j in range (0,N_nodes):
        basis_POD["nodal_modes"][int(node_Id[j])] = (u[i:i+Dimensions].tolist())
        i=i+Dimensions

    with open('RomParameters.json', 'w') as f:
        json.dump(basis_POD,f, indent=2)

    print('\n\nNodal basis printed in json format\n\n')








    ##############################################################################################
    #                                          TRAIN HROM                                        #
    ##############################################################################################
    with open("ProjectParameters.json",'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())
    model = KratosMultiphysics.Model()
    simulation = StructuralMechanicsAnalysisROM(model,parameters,"EmpiricalCubature")
    simulation.Run()
