# Prepare

Download the 4 first files from http://cfinder.org/wiki/?n=Main.Data#toc1  
Extract the files into folder `/data`.

# pagerank.py: in the form of pseudo code 
This program shows the result of page rank of graph in file `dirLinks.txt` with name-node mapping in "pageNum2Name.txt".   
Run this program with alpha value (damping factor) as argument:  
`python3 pagerank.py <alpha-value>`. The alpha value recommended is 0.15.

# pagerank_highPerformance.py: represent the matrix by an array
This program will run the algorithm of page rank on graph in file `data/alr21--dirLinks--enwiki-20071018.txt` with name-node mapping in `data/alr21--pageNum2Name--enwiki-20071018.txt`.  
Run this program with alpha value (damping factor) as argument:  
`python3 pagerank_highPerformance.py <alpha-value>`. The alpha value recommended is 0.15.

# pagerank_personalized.py: with a personnalized interesting vector
Search the category in which you are interested in the file `data/alr21--categNum2Name--enwiki-20071018.txt`. For exemple the cateogry "Chess" has ID of 691713 and the category "Boxing" has ID of 738624.  
Run `python3 pagerank_personalized.py <alpha-value> 691713 738624` to have a page rank related to these 2 categories.

# pagerank_push.py: use push method to run personalized page rank
Same usage with pagerank_personalized.py but implemented with "push" method of algorithm Page Rank. Read: http://www.math.ucsd.edu/~fan/wp/localpartition.pdf
