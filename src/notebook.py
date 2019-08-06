import itertools
from IPython.core.display import HTML
import json
import matplotlib.pyplot as plt
import random
from string import Template
import html
import uuid
import src.templates as templates

def top_k(C, k):
	return C["[COUNTS]"].sort_values(ascending=False)[:k]

def top_k_cooc(C, w, k, normalizer=None):
	#first item is the counter token
	t = C[w].sort_values(ascending=False)[1:k+1]
	if normalizer:
		t /= normalizer
		t = t.round(3)
	return t

def get_coos(C, words):
	return C.loc[words, words]

def sigmaJSGraph(graph_data):
	#random container id
	uid = str(uuid.uuid4())
	javascript_template = Template(templates.javascript)
	html_template = Template(templates.html)
	js_text = javascript_template.substitute({'graph_data': json.dumps(graph_data),
												'container': "cnt-"+uid,
												'force_status':"frs-"+uid}
												)
	ht = html_template.substitute({'js_text':js_text, 'container': "cnt-"+uid,
									'force_status':"frs-"+uid})

	return ht

def graph(C, words, target_word, top_k_edges=None, random_seed=42, style='bmh'):
	random.seed(random_seed)
	colors = [x['color'] for x in list(plt.style.library[style]['axes.prop_cycle'])]
	g = {"nodes":[],
		"edges":[]}	
	# nodes
	color_map = {}
	for i,w in enumerate(words):
		g["nodes"].append({'label': w,                    
					'x': random.random(),
					'y': random.random(),
					'id': str(words.index(w)),
					'size': int(C[target_word][w]), #node proportional to cooc with target
					'color': colors[i%len(colors)]}) #rotate colors 
		color_map[w] = colors[i%len(colors)]
	tmp_edges = {}
	for i, (w1, w2) in enumerate(itertools.combinations(words,2)):
		#co-occurrences between w1 and w2 
		c = int(C[w1][w2])
		if c==0:continue
		key = "{},{}".format(w1,w2)
		tmp_edges[key] = c
	
	sorted_edges = sorted(tmp_edges.items(), key=lambda kv: kv[1])	
	#get the top k edges
	if top_k_edges:		
		sorted_edges.reverse()
		edges = sorted_edges[:top_k_edges]
	else:
		edges = sorted_edges
	# import pdb; pdb.set_trace()
	for i, (w, v) in enumerate(edges):
		w1,w2 = w.split(",")      
		g["edges"].append({'source': str(words.index(w1)),
					'target': str(words.index(w2)),
					'id': i,
					'size': v,
					'color': '#ccc',
					'type': 'curve',
					'label':str(v),
					'hover_color': color_map[w1]})

	return g





# def graph(C, words, target_word, style='bmh'):
#     colors = [x['color'] for x in list(plt.style.library[style]['axes.prop_cycle'])]
#     g = {"nodes":[],
#         "edges":[]}
#     random.seed(42)
#     for i,w in enumerate(words):
#         g["nodes"].append({'label': w,                    
#                     'x': random.random(),
#                     'y': random.random(),
#                     'id': words.index(w),
#                     'size': int(C[target_word][w]), #node proportional to frequency
#                     'color': colors[i%len(colors)]}) #rotate colors 
#     # nodes
#     for i, (w1, w2) in enumerate(itertools.combinations(words,2)):
#         #co-occurrences between w1 and w2 
#         c = C[w1][w2]
#         if c==0:continue
#         g["edges"].append({'source': words.index(w1),
#                     'target': words.index(w2),
#                     'id': i,
#                     'size': int(c),
#                     'color': '#ccc'})
    
#     print(len(g["edges"]))
#     return g


# def graph(C, words, style='bmh'):
#     colors = [x['color'] for x in list(plt.style.library[style]['axes.prop_cycle'])]
#     g = {"nodes":[],
#         "edges":[]}
#     random.seed(42)
#     for i,w in enumerate(words):
#         g["nodes"].append({'label': w,                    
#                     'x': random.random(),
#                     'y': random.random(),
#                     'id': words.index(w),
#                     'size': int(C["[COUNTS]"][w]), #node proportional to frequency
#                     'color': colors[i%len(colors)]}) #rotate colors 
#     # nodes
#     for i, (w1, w2) in enumerate(itertools.combinations(words,2)):
#         #co-occurrences between w1 and w2 
#         c = C[w1][w2]
#         if c==0:continue
#         g["edges"].append({'source': words.index(w1),
#                     'target': words.index(w2),
#                     'id': i,
#                     'size': int(c),
#                     'color': '#ccc'})
  
#     print(len(g["edges"]))
#     return g

# def k_connected_graph(C, words, k, style='bmh'):
#   colors = [x['color'] for x in list(plt.style.library[style]['axes.prop_cycle'])]
#   g = {"nodes":[],
#       "edges":[]}
#   random.seed(42)
#   for i,w in enumerate(words):
#       g["nodes"].append({'label': w,                    
#                   'x': random.random(),
#                   'y': random.random(),
#                   'id': words.index(w),
#                   'size': int(C["[COUNTS]"][w]), #node proportional to frequency
#                   'color': colors[i%len(colors)]}) #rotate colors 
#   # nodes
#   tmp_edges = {}
#   for i, (w1, w2) in enumerate(itertools.combinations(words,2)):
#       #co-occurrences between w1 and w2 
#       c = int(C[w1][w2])
#       if c==0:continue
#       key = "{},{}".format(w1,w2)
#       tmp_edges[key] = c
#   sorted_edges = sorted(tmp_edges.items(), key=lambda kv: kv[1])
#   sorted_edges.reverse()
#   print(len(sorted_edges))
#   for i, (w, v) in enumerate(sorted_edges[:k]):
#     w1,w2 = w.split(",")      
#     g["edges"].append({'source': words.index(w1),
#                 'target': words.index(w2),
#                 'id': i,
#                 'size': v,
#                 'color': '#ccc'})

#   return g

  # for i, (w1, w2) in enumerate(itertools.combinations(words,2)):
  #     #co-occurrences between w1 and w2 
  #     c = C[w1][w2]
  #     if c==0:continue
  #     g["edges"].append({'source': words.index(w1),
  #                 'target': words.index(w2),
  #                 'id': i,
  #                 'size': int(c),
  #                 'color': '#ccc'})
  