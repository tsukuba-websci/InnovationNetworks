import * as React from 'react';
import { useRef } from 'react';
import { ForceGraph2D } from 'react-force-graph';

function Graph({data, width, height, linkColor='rgba(255, 255, 255, 0.2)', nodeColor='#474747'}) {
    const fgRef = useRef();
    return (
      <div>
        <ForceGraph2D
          ref={fgRef}
          cooldownTicks={100}
          graphData={data}
          onEngineStop={() => fgRef.current.zoomToFit(400,10)}
          width={width/2.01}
          height={height}
          nodeLabel="id"
          nodeAutoColorBy="group"
          linkColor={() => linkColor}
          nodeVal={node => node.GoodIdea > 0 ? 2 : 5}
          nodeColor={node => node.GoodIdea > 0 ? 'white' :  nodeColor}
          onNodeClick={node => {
            fgRef.current.centerAt(node.x, node.y, 1000);
            fgRef.current.zoom(8, 500);
          }}
        />
      </div>
    );
  }

  export default Graph