package algorithms;

import java.awt.Point;
import java.util.ArrayList;

public class DefaultTeam {
    public Tree2D calculSteiner(ArrayList<Point> points) {
        //return naifApproximation(points);
        //return new Kruskal().kruskal(points);
        return new Steiner().steiner(points);
    }

    public Tree2D naifApproximation(ArrayList<Point> points) {
        ArrayList<Point> rest = (ArrayList<Point>) points.clone();
        Point root = rest.remove(0);
        ArrayList<Tree2D> subTrees = new ArrayList<>();
        Tree2D result = new Tree2D(root, subTrees);

        while (!rest.isEmpty()) {
            int index_nearest = 0;
            for (int i = 0; i < rest.size(); i++)
                if (rest.get(i).distance(root) < rest.get(index_nearest).distance(root))
                    index_nearest = i;
            root = rest.remove(index_nearest);
            subTrees = new ArrayList<>();
            subTrees.add(result);
            result = new Tree2D(root, subTrees);
        }
        return result;
    }
}
