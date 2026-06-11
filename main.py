import matplotlib.pyplot as plt
from graph_engine import GraphEngine
from ui_manager import UIManager

class AppController:
    def __init__(self):
        self.engine = GraphEngine(num_nodes=10, connection_prob=0.4)
        self.ui = UIManager(initial_nodes=10, initial_prob=0.4)
        self._pan_active = False
        self._pan_start_x = None
        self._pan_start_y = None
        self.bind_events()
        self.ui.draw(self.engine)
        plt.show()

    def bind_events(self):
        self.ui.fig.canvas.mpl_connect('pick_event', self.on_click)
        self.ui.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.ui.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.ui.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.ui.fig.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.ui.btn.on_clicked(self.reset_graph)

    # Handling input
    def on_click(self, event):
        if event.mouseevent.button == 1 and event.artist == self.ui.scatter:
            ind = event.ind[0]
            if ind in self.engine.disabled_nodes:
                self.engine.disabled_nodes.remove(ind)
            else:
                self.engine.disabled_nodes.add(ind)
            self.ui.draw(self.engine, preserve_view=True)

    def reset_graph(self, event):
        self.engine.num_nodes = int(self.ui.slider_nodes.val)
        self.engine.prob = self.ui.slider_prob.val
        self.engine.generate_graph()
        self.ui.draw(self.engine, preserve_view=False)

    # Camera controls
    def on_scroll(self, event):
        if event.inaxes != self.ui.ax: return
        scale_factor = 1.2 if event.button == 'down' else 1 / 1.2
        cur_xlim = self.ui.ax.get_xlim()
        cur_ylim = self.ui.ax.get_ylim()
        
        xdata, ydata = event.xdata, event.ydata
        if xdata is None or ydata is None: return
        
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        
        self.ui.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        self.ui.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        self.ui.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ui.ax: return
        if event.button == 3: 
            self._pan_active = True
            self._pan_start_x = event.xdata
            self._pan_start_y = event.ydata

    def on_drag(self, event):
        if not self._pan_active or event.inaxes != self.ui.ax: return
        if event.xdata is None or event.ydata is None: return
        
        dx = self._pan_start_x - event.xdata
        dy = self._pan_start_y - event.ydata
        cur_xlim = self.ui.ax.get_xlim()
        cur_ylim = self.ui.ax.get_ylim()
        
        self.ui.ax.set_xlim(cur_xlim[0] + dx, cur_xlim[1] + dx)
        self.ui.ax.set_ylim(cur_ylim[0] + dy, cur_ylim[1] + dy)
        self.ui.fig.canvas.draw_idle()

    def on_release(self, event):
        if event.button == 3:
            self._pan_active = False

if __name__ == "__main__":
    app = AppController()