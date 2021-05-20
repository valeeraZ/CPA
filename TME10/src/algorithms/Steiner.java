package algorithms;

import java.awt.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

public class Steiner {

    private static int[][] paths;

    private static ArrayList<Edge> heuristic(ArrayList<Point> points, ArrayList<Point> hitPoints){
        //le graphe pondéré complet K = (S, OS, w) avec OS = S × S
        //pour tout couple de sommets u ∈ S et v ∈ S,
        //le poids de l’arête entre ces deux sommets w(uv) est défini
        //par la longueur du plus court chemin entre u et v dans G.

        //int[][] paths = FloydWarshall.calculShortestPaths(points, edgeThreshold);
        //ici l'argument `points` et `edgeThreshold` ne changent pas pendant les itérations
        //donc pas nécessaire de calculer plusieurs fois
        //une fois qu'il est calculé, sauvegarder le résultat dans une variable static

        //Dans K, construire un arbre couvrant T0(hitPoints, edgesHitPoints)
        //de longueur totale des arêtes la plus petite possible.
        ArrayList<Edge> edgesHitPoints = Kruskal.kruskal(hitPoints);
        //Dans T0, remplacer toute arête uv par un plus court chemin entre u et v dans G.
        //Soit H(pointsOnPath, paths) le graphe obtenu après cette étape
        ArrayList<Point> pointsOnPath = new ArrayList<>();
        for (Edge e: edgesHitPoints){
            int i = points.indexOf(e.getP());
            int j = points.indexOf(e.getQ());
            ArrayList<Integer> pointsIJ = getPointsOnPath(i, j, paths);
            for (Integer k: pointsIJ){
                pointsOnPath.add(points.get(k));
            }
        }
        //Dans H, construire un arbre couvrant T′(pointsOnPath, return)
        //de longueur totale des arêtes la plus petite possible.
        return Kruskal.kruskal(pointsOnPath);
    }

    /**
     * use barycenter/fermat-point rule
     * @param points points on the plan
     * @return a Minimum Spanning Tree
     */
    public static Tree2D steinerSansBudget(ArrayList<Point> points, int edgeThreshold, ArrayList<Point> hitPoints) {
        paths = FloydWarshall.calculShortestPaths(points, edgeThreshold);
        ArrayList<Edge> edges = heuristic(points, hitPoints);
        ArrayList<Edge> res = new ArrayList<>(edges);
        Point A, B, C, I, pointBarycenter, pointFermat;
        double score, scoreBarycenter, scoreFermat, betterScore;
        double oldScore = Edge.edgesToTree(edges).score();
        System.out.println("oldScore = " + oldScore);
        double newScore = 0;
        int counter = 0;
        while(true){
            counter++;
            System.out.println("counter = " + counter);
            System.out.println("steinerSansBudget edges size = " + edges.size());
            int size = edges.size();
            for (int i = 0; i < size; i++) {
                for (int j = i + 1; j < size; j++) {
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

                    pointBarycenter = baryCenter(A, B, C);
                    pointFermat = fermatPoint(A, B, C);
                    score = A.distance(B) + B.distance(C);
                    scoreBarycenter = A.distance(pointBarycenter) + B.distance(pointBarycenter) + C.distance(pointBarycenter);
                    scoreFermat = A.distance(pointFermat) + B.distance(pointFermat) + C.distance(pointFermat);

                    if (scoreFermat < scoreBarycenter){
                        betterScore = scoreFermat;
                        I = pointFermat;
                    }else {
                        betterScore = scoreBarycenter;
                        I = pointBarycenter;
                    }

                    I = nearestPoint(I, points);

                    if (betterScore < score) {
                        hitPoints.add(I);
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
            System.out.println("before edges = " + edges.size());
            edges = heuristic(points, hitPoints);
            System.out.println("after edges = " + edges.size());
            newScore = Edge.edgesToTree(edges).score();
            System.out.println("newScore = " + newScore);
            if (newScore < oldScore){
                res = edges;
                oldScore = newScore;
            }else {
                break;
            }
        }
        return Edge.edgesToTree(res);
    }

    /**
     * donner 3 points, calculer le point de bary centre
     */
    private static Point baryCenter(Point a, Point b, Point c) {
        return new Point((int) (a.getX() + b.getX() + c.getX()) / 3, (int) (a.getY() + b.getY() + c.getY()) / 3);
    }

    /**
     * donner 3 points, calculer le point de Fermat
     */
    public static Point fermatPoint(Point A, Point B, Point C) {
        Edge AB = new Edge(A, B);
        Edge BC = new Edge(B, C);
        Edge AC = new Edge(A, C);

        if(Math.abs(AB.getAngleWith(BC)) >= 120)
            return B;
        else if(Math.abs(AB.getAngleWith(AC)) >= 120)
            return A;
        else if(Math.abs(BC.getAngleWith(AC)) >= 120)
            return C;

        //E, F of equilateral triangle ACE, ABF
        Point E = null, F = null;
        int vectABx = B.x - A.x;
        int vectABy = B.y - A.y;
        int vectACx = C.x - A.x;
        int vectACy = C.y - A.y;

        double lcos = Math.cos(Math.PI / 3);
        double rcos = Math.cos(-Math.PI / 3);
        double lsin = Math.sin(Math.PI / 3);
        double rsin = Math.sin(-Math.PI / 3);
        if ((vectABx * vectACy - vectABy * vectACx) > 0) {
            E = new Point((int) Math.round(A.x + vectACx * lcos - vectACy * lsin), (int) Math.round(A.y + vectACy * lcos + vectACx * lsin));
            F = new Point((int) Math.round(A.x + vectABx * rcos - vectABy * rsin), (int) Math.round(A.y + vectABy * rcos + vectABx * rsin));
        } else {
            E = new Point((int) Math.round(A.x + vectACx * rcos - vectACy * rsin), (int) Math.round(A.y + vectACy * rcos + vectACx * rsin));
            F = new Point((int) Math.round(A.x + vectABx * lcos - vectABy * lsin), (int) Math.round(A.y + vectABy * lcos + vectABx * lsin));
        }

        double A1 = C.y - F.y;
        double B1 = F.x - C.x;
        double C1 = A1*F.x + B1*F.y;

        double A2 = B.y - E.y;
        double B2 = E.x - B.x;
        double C2 = A2*E.x + B2*E.y;

        //intersect point of lines CF - BE
        double det = A1*B2 - A2*B1;
        double x, y;
        if(det==0) {
            return A; //or B, or C, whatever
        } else {
            x = (B2*C1 - B1*C2)/det;
            y = (A1*C2 - A2*C1)/det;
        }
        return new Point((int)x, (int)y);
    }

    /**
     * lister tous les points sur le chemin entre point A et B
     * utilisé pour le résultat de Floyd-Warshall
     */
    public static ArrayList<Integer> getPointsOnPath(int i, int j, int[][] paths){
        ArrayList<Integer> path = new ArrayList<>();
        path.add(i);
        while(paths[i][j] != j){
            path.add(paths[i][j]);
            i = paths[i][j];
        }
        path.add(j);
        return path;
    }

    /**
     * donner un point A, chercher un autre point B qui est le plus proche à A dans un ensemble de points
     */
    public static Point nearestPoint(Point point, ArrayList<Point> list) {
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
