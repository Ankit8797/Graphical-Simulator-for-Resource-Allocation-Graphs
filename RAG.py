import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

G = nx.DiGraph()


root = tk.Tk()
root.title("Resource Allocation Graph Simulator")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

canvas_frame = tk.Frame(root)
canvas_frame.pack()

fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack()

def update_graph():
    ax.clear()
    pos = nx.spring_layout(G)
    colors = ["blue" if "P" in node else "red" for node in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=colors, edge_color="black", node_size=2000, font_size=12, ax=ax)
    canvas.draw()
    update_dropdowns()

def add_process():
    process_name = f'P{len([n for n in G.nodes if "P" in n]) + 1}'
    G.add_node(process_name, color='blue')
    update_graph()

def add_resource():
    resource_name = f'R{len([n for n in G.nodes if "R" in n]) + 1}'
    G.add_node(resource_name, color='red')
    update_graph()

def add_edge():
    from_node = from_var.get()
    to_node = to_var.get()
    if from_node and to_node and from_node in G.nodes and to_node in G.nodes:
        G.add_edge(from_node, to_node)
        update_graph()
        status_label.config(text="Edge Added!", fg="blue")
    else:
        status_label.config(text="Invalid nodes!", fg="red")

def detect_deadlock():
    try:
        nx.find_cycle(G, orientation='original')
        status_label.config(text="Deadlock Detected!", fg="red")
    except nx.NetworkXNoCycle:
        status_label.config(text="No Deadlock Detected.", fg="green")

def update_dropdowns():
    nodes = list(G.nodes)
    from_menu['values'] = nodes
    to_menu['values'] = nodes


ttk.Button(frame, text="Add Process", command=add_process).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame, text="Add Resource", command=add_resource).grid(row=0, column=1, padx=5, pady=5)

from_var = tk.StringVar()
to_var = tk.StringVar()
from_menu = ttk.Combobox(frame, textvariable=from_var, state='readonly')
from_menu.grid(row=1, column=0, padx=5, pady=5)
to_menu = ttk.Combobox(frame, textvariable=to_var, state='readonly')
to_menu.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(frame, text="Add Edge", command=add_edge).grid(row=1, column=2, padx=5, pady=5)
ttk.Button(frame, text="Detect Deadlock", command=detect_deadlock).grid(row=2, column=0, columnspan=3, pady=10)

status_label = tk.Label(root, text="Status: Waiting for input", fg="black", font=("Arial", 12), bg="#f0f0f0")
status_label.pack()

update_graph()
root.mainloop()
