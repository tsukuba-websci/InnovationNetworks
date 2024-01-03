import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.colors as mcolors

plt.rcParams["font.size"] = 18

types = {"nctf": "NCTF", "ttf": "TTF"}

my_color = {
    "red": "#FC8484",
    "dark_red": "#FA5050",
    "light_blue": "#94C4E0",
    "light_green": "#9CDAA0",
    "dark_blue": "#76ABCB",
    "dark_green": "#51BD56",
    "black": "#505050",
    "purple": "#CBA6DD",
    "yellow": "#FFE959",
    "yellow_green": "#C1FF87",
}

for type, name in types.items():
    # Load the CSV data into DataFrames
    explorative_df = pd.read_csv("../../full_search/results/explorative/output.csv")
    explorative_df['rho_over_nu'] = explorative_df['rho'] / explorative_df['nu']

    best_ttf = {
        "rho": explorative_df.sort_values(by='ttf_mean').head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='ttf_mean').head(1)["nu"].iloc[0],
        "nctf": explorative_df.sort_values(by='ttf_mean').head(1)["nctf_mean"].iloc[0],
        "ttf": explorative_df.sort_values(by='ttf_mean').head(1)["ttf_mean"].iloc[0]
    }

    best_nctf = {
        "rho": explorative_df.sort_values(by='nctf_mean').head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='nctf_mean').head(1)["nu"].iloc[0],
        "nctf": explorative_df.sort_values(by='nctf_mean').head(1)["nctf_mean"].iloc[0],
        "ttf": explorative_df.sort_values(by='nctf_mean').head(1)["ttf_mean"].iloc[0]
    }

    worst_ttf = {
        "rho": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["nu"].iloc[0],
        "nctf": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
        "ttf": explorative_df.sort_values(by='ttf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]
    }

    worst_nctf = {
        "rho": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
        "nctf": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
        "ttf": explorative_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]
    }

    tmn_df = pd.read_csv("../../empirical/results/tmn/output.csv")

    tmn = {
        "rho": tmn_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": tmn_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
        "nctf": tmn_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
        "ttf": tmn_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]    
        }
    
    aps_df = pd.read_csv("../../empirical/results/aps/output.csv")

    aps = {
        "rho": aps_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": aps_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
        "nctf": aps_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
        "ttf": aps_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]    
        }
    
    ida_df = pd.read_csv("../../empirical/results/ida/output.csv")

    ida = {
        "rho": ida_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": ida_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
        "nctf": ida_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
        "ttf": ida_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]    
        }
    
    eight_df = pd.read_csv("../../empirical/results/eight/output.csv")

    eight = {
        "rho": eight_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
        "nu": eight_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
        "nctf": eight_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
        "ttf": eight_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]    
        }

    param_dict = {
        "best_ttf": best_ttf,
        "best_nctf": best_nctf,
        "worst_ttf": worst_ttf,
        "worst_nctf": worst_nctf,
        "tmn": tmn,
        "aps": aps,
        "ida": ida,
        "eight": eight
    }

for type, name in types.items():
    fig, ax = plt.subplots(figsize=(10, 6))
    

    if type == "nctf":
        best, worst = best_nctf, worst_nctf
    else:
        best, worst = best_ttf, worst_ttf

    def generate_label(prefix, rho, nu, value):
        return f"{prefix} ($\\rho$={rho}, $\\nu$={nu})"

    # Plot best and worst points with updated labels
    if best['rho']/best['nu'] < 1:
        side = 'left'
    else:
        side = 'right'
    ax.scatter(best['rho']/best['nu'], best[type], s=200, color=my_color['light_green'], 
            label=generate_label("Best", best['rho'], best['nu'], best[type]))
    # ax.scatter(best['rho']/best['nu'], best[type], s=2, color='black')
    ax.text(best['rho']/best['nu'], best[type], 'Best', fontsize=22, ha=side)

    if worst['rho']/worst['nu'] < 1:
        side = 'left'
    else:
        side = 'right'
    ax.scatter(worst['rho']/worst['nu'], worst[type], s=200, color=my_color['red'], 
            label=generate_label("Worst", worst['rho'], worst['nu'], worst[type]))
    # ax.scatter(worst['rho']/worst['nu'], worst[type], s=2, color='black')
    ax.text(worst['rho']/worst['nu'], worst[type], 'Worst', fontsize=22, ha=side, va='top')

    ax.scatter(tmn['rho']/tmn['nu'], tmn[type], s=200, color=my_color['light_blue'], 
               label=generate_label("TMN", tmn['rho'], tmn['nu'], tmn[type]))
    # ax.scatter(tmn['rho']/tmn['nu'], tmn[type], s=2, color='black')
    ax.text(tmn['rho']/tmn['nu'], tmn[type], 'TMN', fontsize=22, ha='right')

    ax.scatter(aps['rho']/aps['nu'], aps[type], s=200, color=my_color['purple'], 
               label=generate_label("APS", aps['rho'], aps['nu'], aps[type]))
    # ax.scatter(aps['rho']/aps['nu'], aps[type], s=2, color='black')
    ax.text(aps['rho']/aps['nu'], aps[type], 'APS', fontsize=22, ha='right')

    ax.scatter(ida['rho']/ida['nu'], ida[type], s=200, color=my_color['yellow'], 
               label=generate_label("ISN", ida['rho'], ida['nu'], ida[type]))
    # ax.scatter(ida['rho']/ida['nu'], ida[type], s=2, color='black')
    ax.text(ida['rho']/ida['nu'], ida[type], 'ISN', fontsize=22, ha='left')
    
    ax.scatter(eight['rho']/eight['nu'], eight[type], s=200, color=my_color['yellow_green'], 
               label=generate_label("EUN", eight['rho'], eight['nu'], eight[type]))
    # ax.scatter(eight['rho']/eight['nu'], eight[type], s=2, color='black')
    ax.text(eight['rho']/eight['nu'], eight[type], 'EUN', fontsize=22, ha='right')

    ax.set_xlim(0, 5)
    ax.set_title(name + ' vs. ' + '$\\rho / \\nu$', fontsize=24)
    ax.set_xlabel('$\\rho / \\nu$', fontsize=24)
    ax.set_ylabel(f"{type.upper()}", fontsize=24)
    ax.legend()

    # Save the figure
    fig.tight_layout()  # Ensures that all elements of the plot fit within the figure boundaries
    
    # Save the figure
    fig.savefig(f"../results/rho_nu_space_{type}.png", dpi=300)