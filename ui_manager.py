import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
plt.rcParams['toolbar'] = 'None'
plt.style.use('seaborn-v0_8-whitegrid')

class UIManager:
    def __init__(self, initial_nodes, initial_prob):
        self.colors = {
            'bg': '#f8fafc',
            'node_active': '#4ade80',  
            'node_disabled': '#f87171', 
            'edge_normal': '#cbd5e1',  
            'edge_mst': '#3b82f6',     
            'text_dark': '#1e293b'
        }
        
        # UI Setup
        self.fig, self.ax = plt.subplots(figsize=(12, 8), facecolor=self.colors['bg'])
        self.fig.canvas.manager.set_window_title('Network Topology Simulator')
        self.fig.subplots_adjust(bottom=0.30, top=0.85, left=0.05, right=0.95)
        self.ax.set_facecolor(self.colors['bg'])

        # Sliders
        ax_nodes = plt.axes([0.3, 0.16, 0.4, 0.03], facecolor=self.colors['bg'])
        self.slider_nodes = Slider(ax_nodes, 'Number of Nodes  ', 4, 25, valinit=initial_nodes, valstep=1, color=self.colors['edge_mst'])
        
        ax_prob = plt.axes([0.3, 0.11, 0.4, 0.03], facecolor=self.colors['bg'])
        self.slider_prob = Slider(ax_prob, 'Connection Prob  ', 0.2, 1.0, valinit=initial_prob, color=self.colors['edge_mst'])

        # Button
        self.ax_button = plt.axes([0.4, 0.03, 0.2, 0.05])
        self.btn = Button(self.ax_button, 'Generate New Graph', color='#e2e8f0', hovercolor='#cbd5e1')
        self.btn.label.set_fontsize(12)
        self.btn.label.set_fontweight('bold')
        self.btn.label.set_color(self.colors['text_dark'])
        
        self.scatter = None # Will hold the clickable node object

    def draw(self, engine, preserve_view=False):
        if preserve_view:
            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()
            
        self.ax.clear()
        self.ax.axis('off')
        
        active_nodes = set(range(engine.num_nodes)) - engine.disabled_nodes
        active_edges = [(u, v, w) for (u, v, w) in engine.edges if u in active_nodes and v in active_nodes]
        
        self.fig.suptitle("Network Resilience Simulator", fontsize=18, fontweight='bold', color=self.colors['text_dark'], y=0.95)
        
        if active_nodes:
            engine.reconnect_graph(active_nodes, active_edges)
            mst = engine.get_minimum_spanning_tree(active_nodes, active_edges)
            mst_pairs = {(u, v) for u, v, w in mst} | {(v, u) for u, v, w in mst}
            
            for u, v, w in active_edges:
                x_vals = [engine.positions[u][0], engine.positions[v][0]]
                y_vals = [engine.positions[u][1], engine.positions[v][1]]
                
                if (u, v) in mst_pairs:
                    self.ax.plot(x_vals, y_vals, color=self.colors['edge_mst'], linewidth=3.5, zorder=1, alpha=0.9)
                else:
                    self.ax.plot(x_vals, y_vals, color=self.colors['edge_normal'], linewidth=1.5, zorder=1, alpha=0.5)
                
                mid_x = sum(x_vals) / 2
                mid_y = sum(y_vals) / 2
                bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.8)
                self.ax.text(mid_x, mid_y, str(w), color=self.colors['text_dark'], fontsize=9, 
                             fontweight='bold', ha='center', va='center', bbox=bbox_props, zorder=2)
            
            avg_path = engine.get_average_shortest_path(active_nodes, active_edges)
            subtitle = f"Active Nodes: {len(active_nodes)}/{engine.num_nodes}   |   Avg Route Latency (Dijkstra): {avg_path:.2f}"
        else:
            subtitle = "CRITICAL FAILURE: All nodes are offline."

        self.ax.set_title(subtitle + "\n(Left-Click to toggle nodes | Right-Click to pan | Scroll to zoom)", 
                          fontsize=12, color='#64748b', pad=15)

        xs, ys, colors = [], [], []
        for i in range(engine.num_nodes):
            xs.append(engine.positions[i][0])
            ys.append(engine.positions[i][1])
            colors.append(self.colors['node_disabled'] if i in engine.disabled_nodes else self.colors['node_active'])
            
            self.ax.text(engine.positions[i][0], engine.positions[i][1], str(i), 
                         ha='center', va='center', fontweight='bold', color=self.colors['text_dark'], zorder=4)

        self.scatter = self.ax.scatter(xs, ys, s=700, c=colors, zorder=3, picker=10, 
                                       edgecolors='white', linewidths=2.5)
        
        if preserve_view:
            self.ax.set_xlim(cur_xlim)
            self.ax.set_ylim(cur_ylim)
            
        self.fig.canvas.draw()