#include <stdlib.h>
#include <stdio.h>
#include <set>
#include <list>
#include <time.h>
#include <string.h>
#include <unordered_map>

struct Edge{
	unsigned long s;
	unsigned long t;
};

struct Matrix{
    unsigned long numberNodes;
    unsigned long numberEdges;
    int** mat;  
} matrix;

unsigned long numberNodes;
unsigned long numberEdges;
std::set<long> nodes;
std::list<Edge> edges; 
std::unordered_map<long, long> mapNodes; 

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
    std::set<long>::iterator it = nodes.begin();
    for (int i = 0; i < numberNodes, it != nodes.end(); i++, it++){
        mapNodes[*it] = i;
    }
}

void makeMatrix(){
    matrix.numberEdges = numberEdges;
    matrix.numberNodes = numberNodes;
    matrix.mat = new int*[numberNodes];
    for(int i = 0; i < numberNodes; ++i){
        matrix.mat[i] = new int[numberNodes];
        memset(matrix.mat[i], 0, sizeof(int)*(numberNodes));
    }
    for(Edge edge : edges){

        long position_s = mapNodes[edge.s];
        long position_t = mapNodes[edge.t];

        matrix.mat[position_s][position_t] = 1;
        matrix.mat[position_t][position_s] = 1;
    }
}

void printMatrix(){
    for(int i = 0; i < matrix.numberNodes; ++i){
        for(int j = 0; j < matrix.numberNodes; ++j){
            printf("%d ", matrix.mat[i][j]);
        }
        printf("\n");
    }
}

void freeMatrix(){
    matrix.mat = NULL;
    delete matrix.mat;
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

    makeMatrix();
    printMatrix();
    freeMatrix();
    
    t2=time(NULL);

	printf("- Overall time = %ldh%ldm%lds\n",(t2-t1)/3600,((t2-t1)%3600)/60,((t2-t1)%60));
}