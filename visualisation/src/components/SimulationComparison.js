import * as React from 'react'
import { Box, Grid } from '@mui/material';
import { useWindowSize } from '@react-hook/window-size';
import Graph from './Graph';
import graph_data_1 from '../data/graph_simulation_1.json';
import graph_data_2 from '../data/graph_simulation_2.json';
import graph_data_3 from '../data/graph_simulation_3.json';
import graph_data_4 from '../data/graph_simulation_4.json';
import graph_data_5 from '../data/graph_simulation_5.json';
import graph_data_6 from '../data/graph_simulation_6.json';
import graph_data_7 from '../data/graph_simulation_7.json';
import graph_data_8 from '../data/graph_simulation_8.json';

function SimulationComparison() {
  const [width, height] = useWindowSize();
  const graphData = [graph_data_1, graph_data_2, graph_data_3, graph_data_4, graph_data_5, graph_data_6, graph_data_7, graph_data_8];

  return (
    <Grid container spacing={0.2} style={{overflow: "hidden", background:"black"}}>
      {graphData.map((data, index) => (
        <Grid key={index} item xs={12} sm={3}>
          <Box sx={{backgroundColor:'#121212', height: '100%', width: '100%'}}>
            <Graph data={data} width={width/2} height={height/2} />
          </Box>
        </Grid>
      ))}
    </Grid>
  );
}

export default SimulationComparison;