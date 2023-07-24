import * as React from 'react';
import { useRef } from 'react';
import { ForceGraph2D } from 'react-force-graph';
import { Box, Grid } from '@mui/material';
import { useWindowSize } from '@react-hook/window-size';
import graph_data_empirical from '../data/graph_empirical.json';
import graph_data_simulation from '../data/graph_simulation.json';

function Graph({data}) {
  const fgRef = useRef();
  const [width, height] = useWindowSize();
  return (
    <div>
      <ForceGraph2D
        ref={fgRef}
        graphData={data}
        width={width/2.01}
        height={height}
        nodeLabel="id"
        nodeAutoColorBy="group"
        linkColor={() => 'rgba(255, 255, 255, 0.04)'}
        nodeVal={node => node.GoodIdea > 0 ? 2 : 2}
        nodeColor={node => node.GoodIdea > 0 ? 'white' : '#474747'}
        onNodeClick={node => {
          fgRef.current.centerAt(node.x, node.y, 1000);
          fgRef.current.zoom(8, 500);
        }}
      />
    </div>
  );
}

function Comparison() {
  return (
    <Grid container spacing={0.2} style={{overflow: "hidden", background:"black"}}>
      <Grid item xs={12} sm={6}>
        <Box sx={{backgroundColor:'#121212', height: '100%', width: '100%'}}>
          <Graph data={graph_data_empirical} />
        </Box>
      </Grid>
      <Grid item xs={12} sm={6}>
        <Box sx={{backgroundColor:'#121212', height: '100%', width: '100%'}}>
          <Graph data={graph_data_simulation} />
        </Box>
      </Grid>
    </Grid>
  );
}

export default Comparison