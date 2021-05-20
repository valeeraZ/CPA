package algorithms;

import java.awt.Point;
import java.util.ArrayList;

public class Kruskal {
    /**
     * KRUSKAL ALGORITHM, NOT OPTIMAL FOR STEINER!
     *
     * @param points points on the plan
     * @return a Minimum Spanning Tree
     */
    public Tree2D kruskal(ArrayList<Point> points) {
        //Construct a list of all possible edges of the tree
        ArrayList<Edge> edges = Edge.createEdges(points);

        //Sort the list of edges in ascending order by their weight (the distance between the two ends).
        edges = sort(edges);

        //Initialize an empty "solution" list.
        ArrayList<Edge> kruskal = new ArrayList<>();
        Edge current;
        NameTag forest = new NameTag(points);
        //Traverse the list of edges in ascending order
        while (edges.size() != 0) {
            current = edges.remove(0);
            //If adding the current edge does not create a cycle in the solution,
            //add it to the solution.
            if (forest.tag(current.p) != forest.tag(current.q)) {
                kruskal.add(current);
                forest.reTag(forest.tag(current.p), forest.tag(current.q));
            }
        }
        System.out.println("Kruskal solution size = " + kruskal.size());
        //Translate the "solution" list into a tree structure and return it
        return Edge.edgesToTree(kruskal, kruskal.get(0).p);
    }


    private ArrayList<Edge> sort(ArrayList<Edge> edges) {
        if (edges.size() == 1) return edges;

        ArrayList<Edge> left = new ArrayList<Edge>();
        ArrayList<Edge> right = new ArrayList<Edge>();
        int n = edges.size();
        for (int i = 0; i < n / 2; i++) {
            left.add(edges.remove(0));
        }
        while (edges.size() != 0) {
            right.add(edges.remove(0));
        }
        left = sort(left);
        right = sort(right);

        ArrayList<Edge> result = new ArrayList<Edge>();
        while (left.size() != 0 || right.size() != 0) {
            if (left.size() == 0) {
                result.add(right.remove(0));
                continue;
            }
            if (right.size() == 0) {
                result.add(left.remove(0));
                continue;
            }
            if (left.get(0).distance() < right.get(0).distance())
                result.add(left.remove(0));
            else
                result.add(right.remove(0));
        }
        return result;
    }
}

class NameTag {
    private ArrayList<Point> points;
    private int[] tag;

    protected NameTag(ArrayList<Point> points) {
        this.points = (ArrayList<Point>) points.clone();
        tag = new int[points.size()];
        for (int i = 0; i < points.size(); i++) tag[i] = i;
    }

    protected void reTag(int j, int k) {
        for (int i = 0; i < tag.length; i++) if (tag[i] == j) tag[i] = k;
    }

    protected int tag(Point p) {
        for (int i = 0; i < points.size(); i++) if (p.equals(points.get(i))) return tag[i];
        return 0xBADC0DE;
    }
}
