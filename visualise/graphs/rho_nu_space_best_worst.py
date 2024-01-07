import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 18

innovation_types = {"explorative": "Explorative", "exploitative": "Exploitative"}

innovation_measures = {"nctf": "NCTF", "ttf": "TTF"}

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

for innovation_type, name in innovation_types.items():

    for measure, name in innovation_measures.items():
        # Load the CSV data into DataFrames
        full_search_df = pd.read_csv(f"../../full_search/results/{innovation_type}/output.csv")
        full_search_df['rho_over_nu'] = full_search_df['rho'] / full_search_df['nu']

        best_ttf = {
            "rho": full_search_df.sort_values(by='ttf_mean').head(1)["rho"].iloc[0],
            "nu": full_search_df.sort_values(by='ttf_mean').head(1)["nu"].iloc[0],
            "nctf": full_search_df.sort_values(by='ttf_mean').head(1)["nctf_mean"].iloc[0],
            "ttf": full_search_df.sort_values(by='ttf_mean').head(1)["ttf_mean"].iloc[0]
        }

        best_nctf = {
            "rho": full_search_df.sort_values(by='nctf_mean').head(1)["rho"].iloc[0],
            "nu": full_search_df.sort_values(by='nctf_mean').head(1)["nu"].iloc[0],
            "nctf": full_search_df.sort_values(by='nctf_mean').head(1)["nctf_mean"].iloc[0],
            "ttf": full_search_df.sort_values(by='nctf_mean').head(1)["ttf_mean"].iloc[0]
        }

        worst_ttf = {
            "rho": full_search_df.sort_values(by='ttf_mean', ascending=False).head(1)["rho"].iloc[0],
            "nu": full_search_df.sort_values(by='ttf_mean', ascending=False).head(1)["nu"].iloc[0],
            "nctf": full_search_df.sort_values(by='ttf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
            "ttf": full_search_df.sort_values(by='ttf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]
        }

        worst_nctf = {
            "rho": full_search_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
            "nu": full_search_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
            "nctf": full_search_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
            "ttf": full_search_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]
        }

        tmn_df = pd.read_csv(f"../../empirical/results/tmn/{innovation_type}/output.csv")

        tmn = {
            "rho": tmn_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
            "nu": tmn_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
            "nctf": tmn_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
            "ttf": tmn_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]    
            }
        
        aps_df = pd.read_csv(f"../../empirical/results/aps/{innovation_type}/output.csv")

        aps = {
            "rho": aps_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
            "nu": aps_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
            "nctf": aps_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
            "ttf": aps_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]    
            }
        
        ida_df = pd.read_csv(f"../../empirical/results/ida/{innovation_type}/output.csv")

        ida = {
            "rho": ida_df.sort_values(by='nctf_mean', ascending=False).head(1)["rho"].iloc[0],
            "nu": ida_df.sort_values(by='nctf_mean', ascending=False).head(1)["nu"].iloc[0],
            "nctf": ida_df.sort_values(by='nctf_mean', ascending=False).head(1)["nctf_mean"].iloc[0],
            "ttf": ida_df.sort_values(by='nctf_mean', ascending=False).head(1)["ttf_mean"].iloc[0]    
            }
        
        eight_df = pd.read_csv(f"../../empirical/results/eight/{innovation_type}/output.csv")

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

    for measure, name in innovation_measures.items():
        # Create a figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if measure == "nctf":
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
        ax.scatter(best['rho']/best['nu'], best[measure], s=200, color=my_color['light_green'], 
                label=generate_label("Best", best['rho'], best['nu'], best[measure]))
        ax.text(best['rho']/best['nu'], best[measure], 'Best', fontsize=22, ha='left')

        if worst['rho']/worst['nu'] < 1:
            side = 'left'
        else:
            side = 'right'
        ax.scatter(worst['rho']/worst['nu'], worst[measure], s=200, color=my_color['red'], 
                label=generate_label("Worst", worst['rho'], worst['nu'], worst[measure]))
        ax.text(worst['rho']/worst['nu'], worst[measure], 'Worst', fontsize=22, ha=side, va='top')

        ax.scatter(tmn['rho']/tmn['nu'], tmn[measure], s=200, color=my_color['light_blue'], 
                label=generate_label("TMN", tmn['rho'], tmn['nu'], tmn[measure]))
        ax.text(tmn['rho']/tmn['nu'], tmn[measure], 'TMN', fontsize=22, ha='right')

        ax.scatter(aps['rho']/aps['nu'], aps[measure], s=200, color=my_color['purple'], 
                label=generate_label("APS", aps['rho'], aps['nu'], aps[measure]))
        ax.text(aps['rho']/aps['nu'], aps[measure], 'APS', fontsize=22, ha='right')

        ax.scatter(ida['rho']/ida['nu'], ida[measure], s=200, color=my_color['yellow'], 
                label=generate_label("ISN", ida['rho'], ida['nu'], ida[measure]))
        ax.text(ida['rho']/ida['nu'], ida[measure], 'ISN', fontsize=22, ha='left')
        
        ax.scatter(eight['rho']/eight['nu'], eight[measure], s=200, color=my_color['yellow_green'], 
                label=generate_label("EUN", eight['rho'], eight['nu'], eight[measure]))
        ax.text(eight['rho']/eight['nu'], eight[measure], 'EUN', fontsize=22, ha='right')

        ax.set_xlim(0, 5)
        ax.set_title(f"{name} vs. $\\rho / \\nu$: {innovation_types[innovation_type]} Innovation", fontsize=24)
        ax.set_xlabel('$\\rho / \\nu$', fontsize=24)
        ax.set_ylabel(f"{measure.upper()}", fontsize=24)

        legend_location  = 'lower right' if measure == 'nctf' else 'upper right'
        ax.legend(loc=legend_location, fontsize=18, framealpha=0.5)

        fig.tight_layout()  # Ensures that all elements of the plot fit within the figure boundaries
        
        # Save the figure
        fig.savefig(f"../results/rho_nu_space_{measure}_{innovation_type}.png", dpi=300)