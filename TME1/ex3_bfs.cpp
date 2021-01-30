#include <stdlib.h>
#include <stdio.h>
#include <set>
#include <list>
#include <time.h>
#include <string.h>
#include <iostream>
#include <algorithm>
#include <unordered_map>
#include <queue>
#include <map>

//the node on edge connected to the start node of array
struct EdgeNode
{
    long adjVex;
    //EdgeNode *next;
    EdgeNode(long data)
    {
        adjVex = data;
        //next = NULL;
    }
};
//the start node of array
struct VertexNode
{
    long data;
    std::list<EdgeNode> first;
};

struct Edge
{
    unsigned long s;
    unsigned long t;
};

unsigned long numberNodes;
unsigned long numberEdges;
std::set<long> nodes;
std::list<Edge> edges;
//key for the symbol of node, value for the position(increasing order) of node
std::unordered_map<long, long> mapNodes;
//the list of "start nodes"
VertexNode *AL_Node;

void readEdgeList(FILE *file)
{
    unsigned long s, t;
    Edge edge;
    while (fscanf(file, "%lu %lu", &(edge.s), &(edge.t)) == 2)
    {
        nodes.insert(edge.s);
        nodes.insert(edge.t);
        edges.push_back(edge);
    }
    numberEdges = edges.size();
    numberNodes = nodes.size();
    fclose(file);
}

void makeAjdArray()
{
    AL_Node = new VertexNode[numberNodes];
    std::set<long>::iterator it = nodes.begin();
    for (int i = 0; i < numberNodes, it != nodes.end(); i++, it++)
    {
        AL_Node[i].data = *it;
        mapNodes[*it] = i;
    }

    for (Edge edge : edges)
    {
        long position_s = mapNodes[edge.s];
        long position_t = mapNodes[edge.t];

        AL_Node[position_s].first.push_back(EdgeNode(edge.t));

        //another direction also
        AL_Node[position_t].first.push_back(EdgeNode(edge.s));
    }
}

void freeAdjArray()
{
    AL_Node = NULL;
    delete AL_Node;
}

std::map<unsigned long, unsigned long> bfs(unsigned long start)
{
    std::queue<unsigned long> queue;
    //pair<node, distance>: distance of each node from start
    std::map<unsigned long, unsigned long> distance;
    queue.push(start);
    distance.insert(std::pair<unsigned long, unsigned long>(start, 0));
    int i = 0;
    while (!queue.empty())
    {
        unsigned long top = queue.front();
        queue.pop();
        //std::cout << "The NODE " << top << " Distance from START " << start << " is " << distance[top] << std::endl;
        long position = mapNodes[top];
        int d = distance[top] + 1;
        for (EdgeNode node : AL_Node[position].first)
        {
            //not visited
            if (distance.find(node.adjVex) == distance.end())
            {
                distance.insert(std::pair<long, long>(node.adjVex, d));
                queue.push(node.adjVex);
            }
        }
    }
    return distance;
}

struct cmp
{
    bool operator()(const std::pair<long, long> &P1, const std::pair<long, long> &P2)
    {
        return P1.second > P2.second;
    }
};

void diameter()
{
    std::map<unsigned long, unsigned long> mapDistance = bfs(*(nodes.begin()));
    //find the furthest node A: sort the distance map by value, in order decreasing
    std::vector<std::pair<unsigned long, unsigned long>> vectorDistance(mapDistance.begin(), mapDistance.end());
    std::sort(vectorDistance.begin(), vectorDistance.end(), cmp());
    //the furthest node
    unsigned long furthestNode = vectorDistance.begin()->first;
    //do bfs again, from the furthest node A
    mapDistance = bfs(furthestNode);
    //sort
    vectorDistance.assign(mapDistance.begin(), mapDistance.end());
    std::sort(vectorDistance.begin(), vectorDistance.end(), cmp());
    //the lower bound diameter
    std::cout << "The diameter of graph: " << vectorDistance.begin()->second << std::endl;
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        perror("usage: <file_name> optional: <header_lines_to_ignore>");
        exit(1);
    }

    time_t t1, t2;
    t1 = time(NULL);
    printf("Reading graph from file %s\n", argv[1]);
    FILE *file = fopen(argv[1], "r");
    //ignore the first N lines of file (information about graph)
    if (argc == 3)
    {
        int headerLines = atoi(argv[2]);
        for (int i = 0; i < headerLines; i++)
            fscanf(file, "%*[^\n]%*c");
    }

    readEdgeList(file);

    printf("Number of edges: %lu\n", numberEdges);
    printf("Number of nodes: %lu\n", numberNodes);

    makeAjdArray();
    diameter();
    freeAdjArray();
    t2 = time(NULL);

    printf("- Overall time = %ldh%ldm%lds\n", (t2 - t1) / 3600, ((t2 - t1) % 3600) / 60, ((t2 - t1) % 60));
}
