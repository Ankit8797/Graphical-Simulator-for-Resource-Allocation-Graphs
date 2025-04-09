import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="RAG Simulator", layout="wide")
st.title("Resource Allocation Graph Simulator with Deadlock Detection")

# --- Initialize Session State ---
for key in ['processes', 'resources', 'requests', 'assignments']:
    if key not in st.session_state:
        st.session_state[key] = set() if key in ['processes', 'resources'] else []

# --- Sidebar: Add / Remove Nodes ---
with st.sidebar:
    st.header("🧩 Manage Nodes")
    node_type = st.selectbox("Select Node Type", ["Process", "Resource"])
    node_name = st.text_input("Enter Name (e.g., P1 or R1)")

    if st.button("➕ Add Node"):
        if not node_name.strip():
            st.warning("Please enter a valid name.")
        elif node_name in st.session_state.processes.union(st.session_state.resources):
            st.warning("Node already exists!")
        elif node_type == "Process":
            st.session_state.processes.add(node_name.strip())
        else:
            st.session_state.resources.add(node_name.strip())

    st.divider()
    st.subheader("🗑 Remove Nodes")
    all_nodes = sorted(list(st.session_state.processes.union(st.session_state.resources)))
    node_to_remove = st.selectbox("Select Node to Remove", all_nodes)
    if st.button("❌ Remove Node"):
        st.session_state.processes.discard(node_to_remove)
        st.session_state.resources.discard(node_to_remove)
        st.session_state.requests = [r for r in st.session_state.requests if node_to_remove not in r]
        st.session_state.assignments = [a for a in st.session_state.assignments if node_to_remove not in a]

# --- Main: Define Relationships ---
st.subheader("🛠 Define Resource Relationships")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Request Edge** (Process ➝ Resource)")
    if st.session_state.processes and st.session_state.resources:
        req_proc = st.selectbox("Select Process", sorted(st.session_state.processes), key="req_proc")
        req_res = st.selectbox("Select Resource", sorted(st.session_state.resources), key="req_res")
        if st.button("Add Request ➤"):
            edge = (req_proc, req_res)
            if edge not in st.session_state.requests:
                st.session_state.requests.append(edge)
            else:
                st.warning("Request edge already exists.")
    else:
        st.info("Add both a process and a resource to create request edges.")

with col2:
    st.markdown("**Assignment Edge** (Resource ➝ Process)")
    if st.session_state.resources and st.session_state.processes:
        as_res = st.selectbox("Select Resource", sorted(st.session_state.resources), key="as_res")
        as_proc = st.selectbox("Assign To Process", sorted(st.session_state.processes), key="as_proc")
        if st.button("Add Assignment ➤"):
            edge = (as_res, as_proc)
            if edge not in st.session_state.assignments:
                st.session_state.assignments.append(edge)
            else:
                st.warning("Assignment edge already exists.")
    else:
        st.info("Add both a resource and a process to create assignment edges.")

# --- Graph Visualization ---
st.subheader("📊 RAG Graph Visualization")

G = nx.DiGraph()

# Add nodes
for p in st.session_state.processes:
    G.add_node(p, color='skyblue', shape='o', label=f"🧍 {p}")
for r in st.session_state.resources:
    G.add_node(r, color='lightgreen', shape='s', label=f"⚙️ {r}")

# Add edges
for (u, v) in st.session_state.requests:
    G.add_edge(u, v, edge_type='request')
for (u, v) in st.session_state.assignments:
    G.add_edge(u, v, edge_type='assignment')

# Detect Deadlock
deadlock_cycles = list(nx.simple_cycles(G))
has_deadlock = len(deadlock_cycles) > 0

# Draw graph
fig, ax = plt.subplots(figsize=(10, 6))

# Use spring layout with fixed seed for consistency
pos = nx.spring_layout(G, seed=42, k=1.5 / (len(G.nodes) + 1))

# Draw nodes
for shape in ['o', 's']:
    node_list = [n for n in G if G.nodes[n]['shape'] == shape]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=node_list,
        node_color=[G.nodes[n]['color'] for n in node_list],
        node_shape=shape,
        node_size=1000,
        ax=ax
    )

# Draw labels
nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['label'] for n in G.nodes()}, font_size=10)

# Draw edges
request_edges = [(u, v) for u, v, d in G.edges(data=True) if d['edge_type'] == 'request']
assignment_edges = [(u, v) for u, v, d in G.edges(data=True) if d['edge_type'] == 'assignment']
nx.draw_networkx_edges(G, pos, edgelist=request_edges, edge_color='blue', arrowstyle='-|>', arrowsize=15, width=2)
nx.draw_networkx_edges(G, pos, edgelist=assignment_edges, edge_color='green', arrowstyle='-|>', arrowsize=15, width=2)

# Legend
legend_lines = [
    plt.Line2D([0], [0], color='blue', lw=2, label='Request (P ➝ R)'),
    plt.Line2D([0], [0], color='green', lw=2, label='Assignment (R ➝ P)')
]
ax.legend(handles=legend_lines, loc='upper left')
ax.axis('off')
st.pyplot(fig)

# --- Deadlock Output ---
if has_deadlock:
    st.error("🧨 Deadlock Detected!")
    for cycle in deadlock_cycles:
        st.write(" ➰ " + " → ".join(cycle) + f" → {cycle[0]}")
else:
    st.success("✅ No Deadlock Detected.")

# --- Reset Button ---
if st.button("🔄 Reset Graph"):
    for key in ['processes', 'resources', 'requests', 'assignments']:
        st.session_state[key] = set() if isinstance(st.session_state[key], set) else []
    st.experimental_rerun()
