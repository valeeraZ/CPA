import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

path = 'results/'

# PageRank with alpha = 0.15
pr_015 = pd.read_table(path + '0.15page-rank.txt', header=0, index_col=0).squeeze().values.tolist()

# PageRank with alpha = 0.1
pr_01 = pd.read_table(path + '0.1page-rank.txt', header=0, index_col=0).squeeze().values.tolist()

# PageRank with alpha = 0.2
pr_02 = pd.read_table(path + '0.2page-rank.txt', header=0, index_col=0).squeeze().values.tolist()

# PageRank with alpha = 0.5
pr_05 = pd.read_table(path + '0.5page-rank.txt', header=0, index_col=0).squeeze().values.tolist()

# PageRank with alpha = 0.9
pr_09 = pd.read_table(path + '0.9page-rank.txt', header=0, index_col=0).squeeze().values.tolist()

# in-degree
din = pd.read_table(path + 'degree-in.txt', header=0, index_col=0).squeeze().values.tolist()

# out-degree
dout = pd.read_table(path + 'degree-out.txt', header=0, index_col=0).squeeze().values.tolist()

pagerank_dict = {'pr_015': pr_015, 'pr_01': pr_01, 'pr_02': pr_02, 'pr_05': pr_05,
                 'pr_09': pr_09, 'din': din, 'dout': dout}
pagerank_df = pd.DataFrame(pagerank_dict)

to_plot = ['din', 'dout', 'pr_01', 'pr_02', 'pr_05', 'pr_09']
y_label = ['Degree in', 'Degree out', 'PageRank with alpha = 0.1',
           'PageRank with alpha = 0.2', 'PageRank with alpha = 0.5',
           'PageRank with alpha = 0.9']

for i in range(len(to_plot)):
    fig1, ax1 = plt.subplots()
    sns.regplot(x=pagerank_df['pr_015'], y=pagerank_df[to_plot[i]], fit_reg=False,
                marker="+")
    plt.title('Correlations')
    plt.xlabel('PageRank with alpha = 0.15')  # Set x-axis label
    plt.ylabel(y_label[i])  # Set y-axis label
    plt.savefig('results/corr_' + to_plot[i] + '.png')
    plt.show()

    fig2, ax2 = plt.subplots()
    ax2.set(xscale='log', yscale='log')  # Set the scale of the x-and y-axes
    sns.regplot(x=pagerank_df['pr_015'], y=pagerank_df[to_plot[i]], fit_reg=False,
                ax=ax2, marker=".", color="blue")
    plt.title('Correlations')
    plt.xlabel('PageRank with alpha = 0.15')  # Set x-axis label
    plt.ylabel(y_label[i])  # Set y-axis label
    plt.savefig('results/log_corr_' + to_plot[i] + '.png')
    plt.show()