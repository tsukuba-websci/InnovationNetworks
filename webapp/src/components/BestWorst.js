import * as React from 'react'
import { Box, Grid } from '@mui/material';
import { useWindowSize } from '@react-hook/window-size';
import Graph from './Graph';

import best0 from '../data/best_nctf_0.json';
import best1 from '../data/best_nctf_1.json';
import best2 from '../data/best_nctf_2.json';
import best3 from '../data/best_nctf_3.json';
import worst1 from '../data/worst_nctf_0.json';
import worst2 from '../data/worst_nctf_1.json';
import worst3 from '../data/worst_nctf_2.json';
import worst4 from '../data/worst_nctf_3.json';

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