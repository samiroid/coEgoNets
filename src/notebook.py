import itertools
from IPython.core.display import HTML
import json
import matplotlib.pyplot as plt
import random
from string import Template
import html

def top_k(C, k):
    return C["[COUNTS]"].sort_values(ascending=False)[:k]

def top_k_cooc(C, w, k, normalize=False):
    #first item is the counter token
    t = C[w].sort_values(ascending=False)[1:k+1]
    if normalize:
        t /= t.sum()
        t = t.round(3)
    return t

def get_coos(C, words):
    return C.loc[words, words]

def graph(C, words, style='bmh'):
    colors = [x['color'] for x in list(plt.style.library[style]['axes.prop_cycle'])]
    g = {"nodes":[],
        "edges":[]}
    random.seed(42)
    for i,w in enumerate(words):
        g["nodes"].append({'label': w,
                    # 'x': random.randint(0,100),
                    # 'y': random.randint(0,100),
                    'x': random.random(),
                    'y': random.random(),
                    'id': words.index(w),
                    'size': int(C["[COUNTS]"][w]), #node proportional to frequency
                    'color': colors[i%len(colors)]}) #rotate colors 
    # nodes
    for i, (w1, w2) in enumerate(itertools.combinations(words,2)):
        #co-occurrences between w1 and w2 
        c = C[w1][w2]
        if c==0:continue
        g["edges"].append({'source': words.index(w1),
                    'target': words.index(w2),
                    'id': i,
                    'size': int(c),
                    'color': '#ccc'})

    return g

def getSigmaGraph(graph_data, html_container_id):
    
    js_text_template = Template('''
    
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
            labelSize:"proportional"} } );

atlas_conf = {worker: true, barnesHutOptimize: false, 
                startingIterations:100, iterationsPerRender:2000,
                edgeWeightInfluence:1,
                slowDown:10,
                scalingRatio:1},

s.startForceAtlas2(atlas_conf);

var force = true;
svg_display = false;

//setTimeout( function(){
 //    s.stopForceAtlas2();
//force=false;
// }, 10000)

// Listeners
document.getElementById('layout').onclick = function() {
  if (!force){
    s.startForceAtlas2(atlas_conf);
    btn = document.getElementById('layout')
    btn.innerHTML = "Stop Force"
    btn.style.backgroundColor = "#B22222"
    
    }
  else{
    s.stopForceAtlas2();
    btn = document.getElementById('layout')
    btn.innerHTML = "Start Force"
    btn.style.backgroundColor = "#228B22"
    
    }
  force = !force;
  
};

document.getElementById('export').onclick = function() {
  s.renderers[0].snapshot({format: 'jpg', background: 'white', filename: 'my-graph.png', download: true, labels: true})
};

document.getElementById('svg').onclick = function() {
    svg_display = !svg_display
    if(svg_display){
        document.getElementById("svg_text").innerHTML = s.toSVG({download: false, labels:true, filename: 'mygraph.svg', size: 500})
        document.getElementById("$container").style.display = "none";
        document.getElementById('svg').innerHTML = "plot"
    }else{
        document.getElementById("svg_text").innerHTML = "";
        document.getElementById("$container").style.display = "block";
        document.getElementById('svg').innerHTML = "snapshot"
    }
};

''')

    html_template = Template('''
<p id="svg_text"></p>
<br>
<div id="$container" style="height:500px; position:relative"></div>
<button id="layout" type="button" style=" background-color:#B22222">stop force</button>
<button id="svg" type="SVG">snapshot</button>
<button id="export" type="PNG">export</button>
<script> $js_text </script>
''')
    js_text = js_text_template.substitute({'graph_data': json.dumps(graph_data),
                                'container': html_container_id})
    ht = html_template.substitute({'js_text':js_text,
                                    'container': html_container_id})
    
    return ht
