import * as React from 'react'
import { Box, Grid, Typography } from '@mui/material';
import { useWindowSize } from '@react-hook/window-size';
import Graph from './Graph';

// import graph_data_1 from '../data/graph_simulation_1.json';
// import graph_data_2 from '../data/graph_simulation_2.json';
// import graph_data_3 from '../data/graph_simulation_3.json';
// import graph_data_4 from '../data/graph_simulation_4.json';
// import graph_data_5 from '../data/graph_simulation_5.json';
// import graph_data_6 from '../data/graph_simulation_6.json';
// import graph_data_7 from '../data/graph_simulation_7.json';
// import graph_data_8 from '../data/graph_simulation_8.json';

import best0 from '../data/min_NCTF0.json';
import best1 from '../data/min_NCTF1.json';
import best2 from '../data/min_NCTF2.json';
import best3 from '../data/min_NCTF3.json';
import worst1 from '../data/max_NCTF0.json';
import worst2 from '../data/max_NCTF1.json';
import worst3 from '../data/max_NCTF2.json';
import worst4 from '../data/max_NCTF3.json';

function BestWorst() {
  const [width, height] = useWindowSize();
  const best = [best0, best1, best2, best3];
  const worst = [worst1, worst2, worst3, worst4];
  worst.reverse();

  return (
    <Grid container spacing={0.2} style={{overflow: "hidden", background:"black"}}>
        {best.map((data, index) => (
        <Grid key={index} item xs={12} sm={3}>
          <Box sx={{backgroundColor:'#C9FFDE', height: '100%', width: '100%'}}>
            <Graph data={data} width={width/2} height={height/2} linkColor='black' />
          </Box>
        </Grid>
      ))}
        {worst.map((data, index) => (
        <Grid key={index} item xs={12} sm={3}>
          <Box sx={{backgroundColor:'#FFB4B0', height: '100%', width: '100%'}}>
            <Graph data={data} width={width/2} height={height/2} linkColor='black' />
          </Box>
        </Grid>
      ))}
    </Grid>
  );
}

export default BestWorst;