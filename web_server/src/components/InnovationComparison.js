import * as React from 'react'
import { Box, Grid } from '@mui/material';
import { useWindowSize } from '@react-hook/window-size';
import Graph from './Graph';
import innovation_graph from '../data/innovation_graph.json';
import no_innovation_graph from '../data/no_innovation_graph.json';


function InnovationComparison() {
  const [width, height] = useWindowSize();
  return (
    <Grid container spacing={0.2} style={{overflow: "hidden", background:"black"}}>
      <Grid item xs={12} sm={6}>
        <Box sx={{backgroundColor:'#121212', height: '100%', width: '100%'}}>
          <Graph data = {innovation_graph} width = {width} height = {height} />
        </Box>
      </Grid>
      <Grid item xs={12} sm={6}>
        <Box sx={{backgroundColor:'#121212', height: '100%', width: '100%'}}>
          <Graph data = {no_innovation_graph} width = {width} height = {height} />
        </Box>
      </Grid>
    </Grid>
  );
}

export default InnovationComparison