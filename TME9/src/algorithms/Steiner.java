package algorithms;

import java.awt.*;
import java.util.ArrayList;

public class Steiner {

    /**
     * barycenter rule
     *
     * @param points points on the plan
     * @return a Minimum Spanning Tree
     */
    public Tree2D steiner(ArrayList<Point> points) {
        Tree2D kruskal = new Kruskal().kruskal(points);
        ArrayList<Edge> edges = Edge.getEdgesFromTree(kruskal, new ArrayList<Edge>());
        //ArrayList<Edge> edges = Edge.createEdges(points);
        ArrayList<Edge> solution = new ArrayList<>(edges);
        Point A = null, B = null, C = null, I = null;
        double score = 0;
        double scoreBarycenter = 0;
        boolean stable = false;
        int counter = 0;
        while(!stable){
            stable = true;
            counter++;
            System.out.println("counter = " + counter);
            for (int i = 0; i < edges.size(); i++) {
                for (int j = i + 1; j < edges.size(); j++) {
                    Edge e1 = edges.get(i);
                    Edge e2 = edges.get(j);

                    if (e1.getP().equals(e2.getP())) {
                        A = e1.getQ();
                        B = e1.getP();
                        C = e2.getQ();
                    } else if (e1.getP().equals(e2.getQ())) {
                        A = e1.getQ();
                        B = e1.getP();
                        C = e2.getP();
                    } else if (e2.getP().equals(e1.getQ())) {
                        A = e1.getP();
                        B = e1.getQ();
                        C = e2.getQ();
                    } else if (e1.getQ().equals(e2.getQ())) {
                        A = e1.getP();
                        B = e1.getQ();
                        C = e2.getP();
                    } else continue;

                    //I = nearestPoint(baryCenter(A, B, C), points);
                    I = baryCenter(A, B, C);

                    score = A.distance(B) + B.distance(C);
                    scoreBarycenter = A.distance(I) + B.distance(I) + C.distance(I);

                    if (scoreBarycenter < score) {
                        stable = false;
                        points.add(I);
                        /*
                        solution.add(new Edge(A, I));
                        solution.add(new Edge(B, I));
                        solution.add(new Edge(C, I));
                        solution.remove(e1);
                        solution.remove(e2);
                        */
                        edges.add(new Edge(A, I));
                        edges.add(new Edge(B, I));
                        edges.add(new Edge(C, I));
                        edges.remove(e1);
                        edges.remove(e2);
                        i--;
                        break;
                    }
                }
            }
        }
        
        System.out.println("Barycenter solution size = " + solution.size());
        return Edge.EdgeToTreeRec(edges, edges.get(0).getP());
    }


    private Point baryCenter(Point a, Point b, Point c) {
        return new Point((int) (a.getX() + b.getX() + c.getX()) / 3, (int) (a.getY() + b.getY() + c.getY()) / 3);
    }

    public Point nearestPoint(Point point, ArrayList<Point> list) {
        double distance = java.lang.Double.MAX_VALUE;
        Point res = null;
        for (Point p : list) {
            if (point.distance(p) < distance) {
                distance = point.distance(p);
                res = p;
            }
        }
        return res;
    }
}
