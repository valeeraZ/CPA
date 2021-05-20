package algorithms;

import java.awt.*;
import java.util.ArrayList;

public class FloydWarshall {
    public static int[][] calculShortestPaths(ArrayList<Point> points, int edgeThreshold) {
        int[][] paths = new int[points.size()][points.size()];
        for (int i = 0; i < paths.length; i++)
            for (int j = 0; j < paths.length; j++)
                paths[i][j] = i;
        double[][] dist = new double[points.size()][points.size()];
        for (int i = 0; i < paths.length; i++) {
            for (int j = 0; j < paths.length; j++) {
                if (i == j) {
                    dist[i][j] = 0;
                    continue;
                }
                if (points.get(i).distance(points.get(j)) <= edgeThreshold)
                    dist[i][j] = points.get(i).distance(points.get(j));
                else dist[i][j] = Double.POSITIVE_INFINITY;
                paths[i][j] = j;
            }
        }
        for (int k = 0; k < paths.length; k++) {
            for (int i = 0; i < paths.length; i++) {
                for (int j = 0; j < paths.length; j++) {
                    if (dist[i][j] > dist[i][k] + dist[k][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                        paths[i][j] = paths[i][k];
                    }
                }
            }
        }
        return paths;
    }
}
