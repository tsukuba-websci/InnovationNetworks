# InnovationNetworks

Repository for the Innovation Networks project, accepted for NetSciX 2024.

![Example Image](./assets/example_networks.png)

## About

This project takes fits empirical social netowrks to an [agent-based model](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0294228) (ABM). After determining the reinforcement and novelty parameters, the ABM generates multiple 50-node networks to represent the original network. [Innovation simulations](https://github.com/tsukuba-websci/InnovationNetworks) are then conducted to assess how reinforcement and novelty impact innovation efficiency. The project also compares different empirical networks with innovation-optimal networks to identify differences.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

Instructions on how to install and set up the project.

## Project Structure

The following is an overview of the project structure:

 - empirical: 
 - fitting: 
 - full_search:
 - qd: used to find the best fit parameters using a quality-diversity algorithm
 - visualise: used to create plots of the results
 - webapp: used to visualise the networks in the browser
 - lib: contains the innovation simulation model, the network measuring tools and other necessary functions
 - calculate_metrics: used to calculate the networks metrics (clustering coefficient, youth coefficient, etc.) for a given network

## Usage

1. Calculate the network metrics for your social network by running the code in `calculate_metrics`. This will create `data/metrics/<dataset>.csv` with the metrics of the empirical network.

2. Fit your network to the ABM by running the code in `fitting`. This will create `fitting/results/<dataset>/best.csv` with the best fit reinforcement and novelty parameters using QD algorithms and the metrics from step 1.

3. Run the ABM and calculate the resulting innovation efficiencies by running the code in `empirical`. This will create `empirical/results/<dataset>/output.csv` with the mean NCTF and TTF of the ABM0-generated networks.

4. Run the full search to running the code in `full_search`. This will create `full_search/results/<innovation_type>/output.csv` with the mean NCTF and TTF of the ABM-generated networks for all possible reinforcement and novelty parameters.

5. To visualise the results in the browser, the optimal and least optimal innovation networks must be converted into JSON format. This is done by running `full_search/analyse.py`. This will create 100 networks for the best and worst choice of ABM parameters and create correspodning JSON files in `full_search/data/output/graph/`.

6. To run the webapp navigate to `webapp` and run `npm install` and `npm start`. This will start the webapp on `localhost:3000`. The webapp can be used to visualise the networks in the browser. You need to ensure the correct JSON files are placed in `webapp/src/data/`. See the `webapp` README for more details.

7. To create plots of the results, run the scripts in `visualise`. This will create plots in `visualise/results/`.