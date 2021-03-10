# Edge List file

Prepare your file of edges list, in the format of  
`source-node \t destination-node`. 
For exemple: download the data set in the first question in `tme1.pdf`. Download and extract the files.

# Compilation

Use command `g++ file.cpp -o file -O9`

# Execution

Use command `./<prog-name> <edgelist-filename>`.  
If there are some header lines in the file, use `./<prog-name> <edgelist-filename> <headerlines-ignore>` to ignore the first header lines.

# ex1: Load Graph
 This program will give the number of nodes and edges in output.

# ex2_adjmatrix: print the Adjacency matrix of graph

This program will print the Adjacency matrix of graph. The matrix is implemented with a 2-dimension array so it might take a high occupation of memory.

# ex2_adjarray: print the adjacency list of graph

This program will print the Adjacency list of graph. With `list` in C++, the neighbours will be pushed into the list of each node.  

# ex3_bfs: calculate the lower and upper bound of diameter of graph

This program will calculate the lower and upper bound of diameter of graph with the algorithm BFS.

# triangles.ipynb: calculate the triangles of graph
Run the file `triangle.ipynb`, in the last cell modify the parameter of function `tme1_triangle` with the filename of graph.  
This program will list the triangles of graph into memory and give the number of triangles.


