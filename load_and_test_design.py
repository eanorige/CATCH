# =============================================================================================
# = This is the main file used to launch loading a single design and viewing cost parameters. =
# =============================================================================================

import design as d
import readDesignFromFile as readDesign
import sys
import time


# Main function
def main():
    # Get start time
    start_time = time.time()
    # Read the file names as command line arguments.
    if len(sys.argv) != 8:
        print("Usage: python load_and_test_design.py <io_file> <layer_file> <wafer_process_file> <assembly_process_file> <test_file> <netlist_file> <chip_file>")
        return 1

    # Read the File Names as Command Line Arguments
    io_file = sys.argv[1]
    layer_file = sys.argv[2]
    wafer_process_file = sys.argv[3]
    assembly_process_file = sys.argv[4]
    test_file = sys.argv[5]
    netlist_file = sys.argv[6]
    chip_file = sys.argv[7]

    # Read the Design Library Files
    io_list = readDesign.ioDefinitionListFromFile(io_file)
    layer_list = readDesign.layerDefinitionListFromFile(layer_file)
    wafer_process_list = readDesign.waferProcessDefinitionListFromFile(wafer_process_file)
    assembly_process_list = readDesign.assemblyProcessDefinitionListFromFile(assembly_process_file)
    test_process_list = readDesign.testProcessDefinitionListFromFile(test_file)

    # Read the Design Netlist File
    am, names = readDesign.globalAdjacencyMatrixFromFile(netlist_file,io_list)

    # Read the System Definition
    sip = d.Chip(filename=chip_file,dict={},waferProcessList=wafer_process_list,assemblyProcessList=assembly_process_list,testProcessList=test_process_list,layers=layer_list,ios=io_list,adjacency_matrix_definitions=am,block_names=names,static=False)

    # # Print the Design Description
    # sip.print_description()

    print(str(sip.get_cost()))
    # print("Cost of full design = " + str(sip.get_cost()))

    end_time = time.time()

    # print("Total time: " + str(end_time - start_time) + " seconds")

    return 0


# Setup auto-run of main function.
if __name__ == "__main__":
    main()
