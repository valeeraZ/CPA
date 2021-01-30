#include <stdlib.h>
#include <stdio.h>
#include <set>
#include <list>
#include <time.h>

struct Edge{
	unsigned long s;
	unsigned long t;
};

unsigned long numberNodes;
unsigned long numberEdges;
std::set<long> nodes;
std::list<Edge> edges; 

void readEdgeList(FILE* file){
    unsigned long s, t;
    Edge edge;
    while(fscanf(file,"%lu %lu", &(edge.s), &(edge.t)) == 2){
        nodes.insert(edge.s);
        nodes.insert(edge.t);
        edges.push_back(edge);
    }
    numberEdges = edges.size();
    numberNodes = nodes.size();
    fclose(file);
}

int main(int argc,char** argv){
    if(argc < 2){
        perror("usage: <file_name> optional: <header_lines_to_ignore>");
        exit(1);
    }
        
    time_t t1,t2;
	t1 = time(NULL);
	printf("Reading graph from file %s\n",argv[1]);
    FILE *file = fopen(argv[1],"r");
    //ignore the first N lines of file (information about graph)
    if (argc == 3){
        int headerLines = atoi(argv[2]);
        for (int i = 0; i < headerLines; i ++) fscanf(file, "%*[^\n]%*c");
    }
    readEdgeList(file);
    
    printf("Number of edges: %lu\n", numberEdges);
    printf("Number of nodes: %lu\n", numberNodes);
}