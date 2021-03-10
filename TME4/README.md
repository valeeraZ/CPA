# Prepare
Move into the parent folder : `cd ..`.
Download the data set mentioned in TME1. **Don't extract the file**. 

# K-Core decomposition
Run `gunzip -c data/<com-amazon|lj|orkut.ungraph.txt.gz> | python3 k_core_bigdata.py`. This will allow the program read from the standard input without extract the file from the gz.  
The metrics about k core decomposition will be shown in the output.

# Google Scholar
Run `python3 k_core_degree_plot.py`. The program will show a figure about degree and coreness about the graph Google Scholar. In the output there will be some "anomalous authors" in this graph.

