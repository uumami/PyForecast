import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

######################################################################
# TIME SERIES PLOTS
######################################################################

# https://python-graph-gallery.com/100-calling-a-color-with-seaborn/
model_colors = {'Naive': '#51DBE6',
                'SeasonalNaive': '#FA6F94',
                'Naive2': 'green',
                'RandomWalkDrift': 'maroon',
                'Croston': 'black',
                'MovingAverage': 'purple',
                'SeasonalMovingAverage': 'blue'}

def plot_single_serie(uid_df, title, ax, models, plt_h=60):
    """
    uid_df: pandas df
    panel with columns unique_id, ds, y, split
    y_hat_df: pandas df
    panel with columns unique_id, ds, y_hat
    """
    # parse uid_df
    uid_df.reset_index(inplace=True)
    
    # plot last 60 observations of actual date
    sns.lineplot(x='ds', y='y',
                 hue='split', data=uid_df[-plt_h:], ax=ax)
    
    # plot fitted models
    for model_name in models.keys():
        sns.lineplot(x='ds', y=model_name,
                     color=model_colors[model_name], data=uid_df[-plt_h:],
                     ax=ax, label=model_name)
    
    # rotate x axis
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y')
    ax.set_xlabel('Date Stamp')
    ax.set_ylabel('Value')
    ax.set_title(title)
    
    # remove legend title
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles[1:], labels=labels[1:])

def plot_grid_series(y, uids, models):
    assert len(uids)==8
    
    fig, axs = plt.subplots(2, 4, figsize=(20, 7))
    plt.subplots_adjust(wspace=0.35)
    plt.subplots_adjust(hspace=0.4)
    plt.xticks(rotation=45)

    for i, uid in enumerate(uids):
        # single plot parameters
        uid_df = y.loc[uid]
        row = int(np.round(i/8 + 0.001))
        col = i % 4
        
        plot_single_serie(uid_df, title=uid, ax=axs[row, col], models=models)
    
    fig.tight_layout()
    plt.show()
    plot_file = "./results/grid_series.png"
    plt.savefig(plot_file, bbox_inches = "tight", dpi=300)
    plt.close()

######################################################################
# RESIDUALS PLOT
######################################################################

def plot_distributions(distributions_dict, fig_title=None, xlabel=None):
    n_distributions = len(distributions_dict.keys())
    fig, ax = plt.subplots(1, figsize=(7, 5.5))
    plt.subplots_adjust(wspace=0.35)
    
    n_colors = len(distributions_dict.keys())
    colors = sns.color_palette("hls", n_colors)
    
    for idx, dist_name in enumerate(distributions_dict.keys()):
        train_dist_plot = sns.kdeplot(distributions_dict[dist_name],
                                      bw='silverman',
                                      label=dist_name,
                                      color=colors[idx])
        if xlabel is not None:
          ax.set_xlabel(xlabel, fontsize=14)
        ax.set_ylabel('Density', fontsize=14)
        ax.set_title(fig_title, fontsize=15.5)
        ax.grid(True)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))    
    
    fig.tight_layout()
    if fig_title is not None:
        fig_title = fig_title.replace(' ', '_')
        plot_file = "./results/{}_distributions.png".format(fig_title)
        plt.savefig(plot_file, bbox_inches = "tight", dpi=300)
    plt.show()
