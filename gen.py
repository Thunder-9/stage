import networkx as nx 
import matplotlib.pyplot as plt
import sys


n=int(sys.argv[1])  #50
k=int(sys.argv[2])   #4
p=float(sys.argv[3])   #0.5
seed=int(sys.argv[4]) #1



#G=nx.newman_watts_strogatz_graph(n,k,p,seed)
G=nx.watts_strogatz_graph(n,k,p,seed)
#G = nx.petersen_graph()
#plt.subplot(121)
# <matplotlib.axes._subplots.AxesSubplot object at ...>
nx.draw(G, with_labels=True, font_weight='bold')
#plt.subplot(122)
# <matplotlib.axes._subplots.AxesSubplot object at ...>
#nx.draw_shell(G, with_labels=True, font_weight='bold')
plt.show()


nx.write_adjlist(G,"graph.data")
