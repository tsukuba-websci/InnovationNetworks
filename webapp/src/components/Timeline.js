import * as React from 'react';
import { useRef } from 'react';
import { ForceGraph2D } from 'react-force-graph';
import graph_data_1 from '../data/graph_simulation_1.json';

function Timeline({data, width, height}) {

    console.log(graph_data_1)

    const fgRef = useRef();
    return (
      <div>
        <ForceGraph2D
          ref={fgRef}
          cooldownTicks={100}
          graphData={graph_data_1}
          onEngineStop={() => fgRef.current.zoomToFit(400,10)}
          width={width}
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

  export default Timeline