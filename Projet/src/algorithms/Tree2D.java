package algorithms;

import java.awt.Point;
import java.util.ArrayList;

public class Tree2D {
    private Point root;
    private ArrayList<Tree2D> subtrees;

    public Tree2D(Point p, ArrayList<Tree2D> trees) {
        this.root = p;
        this.subtrees = trees;
    }

    public Point getRoot() {
        return this.root;
    }

    public ArrayList<Tree2D> getSubTrees() {
        return this.subtrees;
    }

    public double distanceRootToSubTrees() {
        double d = 0;
        for (Tree2D subtree : this.subtrees)
            d += subtree.getRoot().distance(root);
        return d;
    }

    public double score() {
        double d = this.distanceRootToSubTrees();
        for (int i = 0; i < this.getSubTrees().size(); i++) {
            d += this.getSubTrees().get(i).score();
        }
        return d;
    }
}
