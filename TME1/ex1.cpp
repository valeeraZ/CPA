#include <stdlib.h>
#include <stdio.h>
#include <set>
#include <time.h>//to estimate the runing time

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

    std::set<long> nodes;
    unsigned long s, t;
    unsigned long numberNodes = 0;
    unsigned long numberEdges = 0;    

    while(fscanf(file,"%lu %lu", &s, &t) == 2){
        numberEdges++;
        nodes.insert(s);
        nodes.insert(t);
    }
    numberNodes = nodes.size();

    fclose(file);
    printf("Number of edges: %lu\n", numberEdges);
    printf("Number of nodes: %lu\n", numberNodes);

    t2=time(NULL);

    printf("- Overall time = %ldh%ldm%lds\n",(t2-t1)/3600,((t2-t1)%3600)/60,((t2-t1)%60));

}