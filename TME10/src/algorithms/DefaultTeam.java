package algorithms;

import java.awt.Point;
import java.util.ArrayList;

public class DefaultTeam {

    public int[][] calculShortestPaths(ArrayList<Point> points, int edgeThreshold){
        return FloydWarshall.calculShortestPaths(points, edgeThreshold);
    }

    public Tree2D calculSteiner(ArrayList<Point> points, int edgeThreshold, ArrayList<Point> hitPoints) {
        return Steiner.steinerSansBudget(points, edgeThreshold, hitPoints);
    }
}
