import * as React from 'react'
import { Box, Grid } from '@mui/material';
import { useWindowSize } from '@react-hook/window-size';
import Graph from './Graph';
import graph_data_empirical from '../data/graph_empirical.json';
import graph_data_simulation from '../data/graph_simulation.json';


function EmpiricalComparison() {
  const [width, height] = useWindowSize();
  return (
    <Grid container spacing={0.2} style={{overflow: "hidden", background:"black"}}>
      <Grid item xs={12} sm={6}>
        <Box sx={{backgroundColor:'#121212', height: '100%', width: '100%'}}>
          <Graph data = {graph_data_empirical} width = {width} height = {height} />
        </Box>
      </Grid>
      <Grid item xs={12} sm={6}>
        <Box sx={{backgroundColor:'#121212', height: '100%', width: '100%'}}>
          <Graph data = {graph_data_simulation} width = {width} height = {height} />
        </Box>
      </Grid>
    </Grid>
  );
}

export default EmpiricalComparison