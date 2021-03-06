html = '''
<div id="$container" style="height:600px; position:relative"></div>
<br>
<button id="$force_status">Force On</button>
<script> $js_text </script>
'''

javascript = '''  
  g = $graph_data

  // Instantiate sigma:
  s = new sigma({graph: g,
                renderer: {
                    container: document.getElementById('$container'),
                    type: 'canvas'
                },          
          settings: {
          minEdgeSize: 1,
          maxEdgeSize: 10,
          minNodeSize: 10,
          maxNodeSize: 30,
          edgeColor: "#ccc",
          labelColor:"node",
          edgeLabelSize:"proportional",
          labelSize:"proportional",
          enableEdgeHovering: true,
          edgeHoverColor: 'node',
          defaultEdgeHoverColor: '#000'} } );

atlas_conf = {worker: true, barnesHutOptimize: true, 
              startingIterations:1000, iterationsPerRender:500,
              edgeWeightInfluence:0,
              slowDown:10,
              gravity:1,
              scalingRatio:0.001},

s.graph.edges().forEach(function(e) { e.type = 'curve'; });
// Initialize the dragNodes plugin:
var dragListener = sigma.plugins.dragNodes(s, s.renderers[0]);

s.startForceAtlas2(atlas_conf);
s.bind('clickNode',
function(e)
{  
  var nodeId = e.data.node.id;
  s.graph.adjacentEdges(nodeId).forEach(
    function (ee) {
      if (ee.color === e.data.node.color && (ee.source === nodeId || ee.target === nodeId)){
        ee.color = '#ccc'
      }
      else if (ee.source === nodeId || ee.target === nodeId){
        ee.color = e.data.node.color;
      }
    }
  );
s.refresh();
});

var force = true;
svg_display = false;

setTimeout( function(){
    s.stopForceAtlas2();
force=false;
atr = document.getElementById('$force_status')
atr.innerHTML = "Force OFF"
atr.style.color = "#228B22" 
}, 8000)

// Listeners
document.getElementById('$force_status').onclick = function() {
if (!force){
    s.startForceAtlas2(atlas_conf);
    atr = document.getElementById('$force_status')
    atr.innerHTML = "Force ON"  
    atr.style.color = "#B22222"
    }
else{
    s.stopForceAtlas2();
    atr = document.getElementById('$force_status')
    atr.innerHTML = "Force OFF"
    atr.style.color = "#228B22" 
    }
force = !force;
};

'''

javascript_old = '''

  g = $graph_data

  // Instantiate sigma:
  s = new sigma({graph: g,
          container: "$container",
          settings: {
          minEdgeSize: 1,
          maxEdgeSize: 10,
          minNodeSize: 10,
          maxNodeSize: 30,
          edgeColor: "#ccc",
          labelColor:"node",
          labelSize:"proportional"} );

atlas_conf = {worker: true, barnesHutOptimize: true, 
              startingIterations:100, iterationsPerRender:100,
              edgeWeightInfluence:0,
              slowDown:1,
              gravity:0,
              scalingRatio:0},

//atlas_conf = {worker: true,},

s.startForceAtlas2({});

var force = true;
svg_display = false;

setTimeout( function(){
    s.stopForceAtlas2();
force=false;
atr = document.getElementById('$force_status')
atr.innerHTML = "Force OFF"
atr.style.color = "#228B22" 
}, 8000)

// Listeners
document.getElementById('$force_status').onclick = function() {
if (!force){
  s.startForceAtlas2(atlas_conf);
  atr = document.getElementById('$force_status')
  atr.innerHTML = "Force ON"  
  atr.style.color = "#B22222"
  }
else{
  s.stopForceAtlas2();
  atr = document.getElementById('$force_status')
  atr.innerHTML = "Force OFF"
  atr.style.color = "#228B22" 
  
  }
force = !force;

};

document.getElementById('export').onclick = function() {
s.renderers[0].snapshot({format: 'jpg', background: 'white', filename: 'my-graph.png', download: true, labels: true})
};

document.getElementById('svg').onclick = function() {
  svg_display = !svg_display
  if(svg_display){
      s = s.toSVG({download: false, labels:true, filename: 'mygraph.svg', size: 50})
      document.getElementById("svg_text").innerHTML = "*** " + s + " ***"
      alert(s);
      document.getElementById("$container").style.display = "none";
      document.getElementById('svg').innerHTML = "plot"
  }else{
      document.getElementById("svg_text").innerHTML = "";
      document.getElementById("$container").style.display = "block";
      document.getElementById('svg').innerHTML = "snapshot"
  }
};

'''