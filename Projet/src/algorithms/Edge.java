package algorithms;

import java.awt.*;
import java.util.ArrayList;
import java.util.Objects;

public class Edge implements Comparable<Edge>{
    private Point p, q;

    public Edge(Point p, Point q) {
        this.p = p;
        this.q = q;
    }

    public Point getP() {
        return p;
    }

    public Point getQ() {
        return q;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Edge edge = (Edge) o;
        return (Objects.equals(p, edge.p) && Objects.equals(q, edge.q)) || (Objects.equals(p, edge.q) && Objects.equals(q, edge.p));
    }

    @Override
    public int hashCode() {
        return Objects.hash(p, q);
    }

    public double distance() {
        return p.distance(q);
    }

    public Point getCommonPointWith(Edge e2) {
        if ((p == e2.getP() && q != e2.getQ()) || (q != e2.getP() && p == e2.getQ()))
            return p;
        if ((p != e2.getP() && q == e2.getQ()) || (q == e2.getP() && p != e2.getQ()))
            return q;
        return null;
    }

    public Point getUncommonPointWith(Edge e2) {
        if ((p == e2.getP() && q != e2.getQ()) || (q != e2.getP() && p == e2.getQ()))
            return q;
        if ((p != e2.getP() && q == e2.getQ()) || (q == e2.getP() && p != e2.getQ()))
            return p;
        return null;
    }

    private double dotProduct(Point p, Point q, Point s, Point t) {
        return ((q.x - p.x) * (t.x - s.x) + (q.y - p.y) * (t.y - s.y));
    }

    private double angle(Point p, Point q, Point s, Point t) {
        if (p.equals(q) || s.equals(t)) return Double.MAX_VALUE;
        double cosTheta = dotProduct(p, q, s, t) / (double) (p.distance(q) * s.distance(t));
        return Math.acos(cosTheta);
    }

    public double getAngleWith(Edge e2) {
        Point A = this.getCommonPointWith(e2);
        Point B = this.getUncommonPointWith(e2);
        Point C = e2.getUncommonPointWith(this);
        if (A == null || B == null || C == null)
            return 0;
        return angle(A, B, A, C);
    }

    public static ArrayList<Edge> createEdges(ArrayList<Point> points) {
        ArrayList<Edge> edges = new ArrayList<>();
        for (Point p : points) {
            for (Point q : points) {
                if (p.equals(q) || contains(edges, p, q)) continue;
                edges.add(new Edge(p, q));
            }
        }
        return edges;
    }

    private static boolean contains(ArrayList<Edge> edges, Point p, Point q) {
        for (Edge e : edges) {
            if (e.getP().equals(p) && e.getQ().equals(q) ||
                    e.getP().equals(q) && e.getQ().equals(p)) return true;
        }
        return false;
    }

    public static Tree2D edgesToTree(ArrayList<Edge> edges){
        Point root = edges.get(0).getP();
        ArrayList<Edge> edges1 = (ArrayList<Edge>) edges.clone();
        return edgesToTreeRec(edges1, root);
    }

    private static Tree2D edgesToTreeRec(ArrayList<Edge> edges, Point root) {
        ArrayList<Edge> remainder = new ArrayList<>();
        ArrayList<Point> subTreeRoots = new ArrayList<>();
        Edge current;
        while (edges.size() != 0) {
            current = edges.remove(0);
            if (current.getP().equals(root)) {
                subTreeRoots.add(current.getQ());
            } else {
                if (current.getQ().equals(root)) {
                    subTreeRoots.add(current.getP());
                } else {
                    remainder.add(current);
                }
            }
        }

        ArrayList<Tree2D> subTrees = new ArrayList<>();
        for (Point subTreeRoot : subTreeRoots)
            subTrees.add(edgesToTreeRec((ArrayList<Edge>) remainder.clone(), subTreeRoot));

        return new Tree2D(root, subTrees);
    }

    public static ArrayList<Edge> getEdgesFromTree(Tree2D tree){
        return getEdgesFromTreeRec(tree, new ArrayList<Edge>());
    }

    private static ArrayList<Edge> getEdgesFromTreeRec(Tree2D tree, ArrayList<Edge> res){
        for(int i=0;i<tree.getSubTrees().size();i++){
            Edge a = new Edge(tree.getRoot(),tree.getSubTrees().get(i).getRoot());
            res.add(a);
            getEdgesFromTreeRec(tree.getSubTrees().get(i),res);
        }
        return res;
    }


    @Override
    public int compareTo(Edge o) {
        int res = 0;
        if (this.distance() > o.distance())
            res = 1;
        else if (this.distance() < o.distance())
            res = -1;
        return res;
    }
}
