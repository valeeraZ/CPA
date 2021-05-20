package algorithms;

import java.awt.*;
import java.util.ArrayList;
import java.util.Objects;

public class Edge {
    protected Point p, q;

    protected Edge(Point p, Point q) {
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

    protected double distance() {
        return p.distance(q);
    }

    public boolean isAdjacentTo(Edge e2) {
        return ((p == e2.getP() && q != e2.getQ()) ||
                (p != e2.getP() && q == e2.getQ()) ||
                (q == e2.getP() && p != e2.getQ()) ||
                (q != e2.getP() && p == e2.getQ()));
    }

    public Point getCommonPointTo(Edge e2) {
        if (!this.isAdjacentTo(e2)) {
            return null;
        }
        if (this.p == e2.getP() || this.q == e2.getP())
            return e2.getP();
        else
            return e2.getQ();
    }

    public static Tree2D edgesToTree(ArrayList<Edge> edges, Point root) {
        ArrayList<Edge> remainder = new ArrayList<>();
        ArrayList<Point> subTreeRoots = new ArrayList<>();
        Edge current;
        while (edges.size() != 0) {
            current = edges.remove(0);
            if (current.p.equals(root)) {
                subTreeRoots.add(current.q);
            } else {
                if (current.q.equals(root)) {
                    subTreeRoots.add(current.p);
                } else {
                    remainder.add(current);
                }
            }
        }

        ArrayList<Tree2D> subTrees = new ArrayList<>();
        for (Point subTreeRoot : subTreeRoots)
            subTrees.add(edgesToTree((ArrayList<Edge>) remainder.clone(), subTreeRoot));

        return new Tree2D(root, subTrees);
    }

    public static Tree2D EdgeToTreeRec(ArrayList<Edge> solution, Point root) {
        ArrayList<Edge> solution2;
        ArrayList<Point> sons = getAllExtremity(root, solution);
        Tree2D res = new Tree2D(root, new ArrayList<Tree2D>());

        if (sons.isEmpty())
            return res;

        for (Point son : sons) {
            solution2 = (ArrayList<Edge>) solution.clone();
            Edge branche = getEdge(root, son, solution2);
            solution2.remove(branche);

            Tree2D subtree = EdgeToTreeRec(solution2, son);
            res.getSubTrees().add(subtree);
        }

        return res;
    }

    private static ArrayList<Point> getAllExtremity(Point cur, ArrayList<Edge> solution) {
        ArrayList<Point> res = new ArrayList<Point>();

        for (Edge a : solution) {
            if (a.getP().equals(cur))
                res.add(a.getQ());
            else if (a.getQ().equals(cur))
                res.add(a.getP());
        }
        return res;
    }

    private static Edge getEdge(Point point1, Point point2, ArrayList<Edge> edges) {
        for (Edge edge : edges) {
            if (edge.getP().equals(point1) && edge.getQ().equals(point2))
                return edge;
            if (edge.getP().equals(point2) && edge.getQ().equals(point1))
                return edge;
        }
        return null;
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
            if (e.p.equals(p) && e.q.equals(q) ||
                    e.p.equals(q) && e.q.equals(p)) return true;
        }
        return false;
    }

    public static ArrayList<Edge> getEdgesFromTree(Tree2D tree, ArrayList<Edge> res){
        for(int i=0;i<tree.getSubTrees().size();i++){
            Edge a = new Edge(tree.getRoot(),tree.getSubTrees().get(i).getRoot());
            res.add(a);
            getEdgesFromTree(tree.getSubTrees().get(i),res);
        }
        return res;
    }
}
