import * as React from 'react'
import { Box } from '@mui/material';
import { useWindowSize } from '@react-hook/window-size';
import Graph from './Graph';

import best from '../data/best_nctf_0.json';

function BestNCTF() {
  const [width, height] = useWindowSize();

  return (
        <Box sx={{backgroundColor:'#618264', height: '100%', width: '100%'}}>
          <Graph data={best} width={width*2.01} height={height} linkColor='black' nodeColor='black' />
        </Box>
  );
}

export default BestNCTF;