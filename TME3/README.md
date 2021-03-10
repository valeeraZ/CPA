# Prepare
You need `pip3 install networkx`.

# generate_graph.py: générer des graphs and save to files
The program will generate and draw 5 graphs with different values p and q (cf. tme3.pdf). The graph and its clusters are saved as files in `/data`.

# label_propagation.py: Label Propagation algorithm
Run the program with `python3 label_propagation.py <graph-filename>`. The graph file could by `benchmark_*.txt`, `amazon.txt` or `n400_*.txt`in `/data`. The result(clusters) will be displayed and saved to `/graph` and its mapping in text will be saved to `/result`.

# Louvain
See the `README.md` in `/gen-louvain`.

# Divisive approach
Same usage as `label_propagation.py`. The program is implemented with divisive approach and it only works on graph `data/benchmark_n128_e1024.txt` as its complexity is O(n^2).

# Benchmark
See the `README.md` in `/LFR-Benchmark`. We use:
```
./benchmark -N 128 -k 16 -maxk 16 -muw 0.1 -minc 32 -maxc 32 -beta 1
./benchmark -N 1000 -k 16 -maxk 16 -muw 0.1 -minc 32 -maxc 32 -beta 1
```
to generate the 2 graphs `benchmark*.txt` in `/data`.
