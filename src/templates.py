html = '''
<div id="$container" style="height:500px; position:relative"></div>
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
          labelSize:"proportional",
          enableEdgeHovering: true,
          edgeHoverColor: 'node',
          defaultEdgeHoverColor: '#000'} } );

atlas_conf = {worker: true, barnesHutOptimize: false, 
              startingIterations:1, iterationsPerRender:100,
              edgeWeightInfluence:1,
              slowDown:10,
              scalingRatio:1},

s.graph.edges().forEach(function(e) { e.type = 'curve'; });
// Initialize the dragNodes plugin:
var dragListener = sigma.plugins.dragNodes(s, s.renderers[0]);

s.startForceAtlas2(atlas_conf);

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

atlas_conf = {worker: true, barnesHutOptimize: false, 
              startingIterations:1, iterationsPerRender:100,
              edgeWeightInfluence:1,
              slowDown:10,
              scalingRatio:1},

s.startForceAtlas2(atlas_conf);

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