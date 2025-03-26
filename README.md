# Graphical-Simulator-for-Resource-Allocation-Graphs
The Graphical Simulator for Resource Allocation Graphs is an interactive tool designed to visualize and analyze resource allocation in computer systems.

Project Overview
The project aims to develop a graphical simulator for resource allocation graphs (RAGs) to help users visualize how processes request and release resources, detect deadlocks.

Expected Outcomes:
A graph-based UI to simulate processes, resources, and edges dynamically.

Real-time deadlock detection and analysis.

Interactive controls for adding/removing nodes and edges.

An educational tool to help students understand deadlocks and resource allocation concepts.

The project can be divided into three modules:

Module 1: Graph Visualization & Interaction

Purpose: Build an interactive UI to construct resource allocation graphs.

Features:

Create process (P) nodes and resource (R) nodes.

Add and remove edges (allocation & request edges).

Display graph dynamically using network visualization.

Show process/resource states with different colors.

Module 2: Deadlock Detection & Prevention

Purpose: Implement deadlock detection and prevention algorithms.

Features:

Implement Wait-for Graph (WFG) deadlock detection.

Implement Banker’s Algorithm for deadlock avoidance.

Highlight deadlocked processes visually.

Show simulation steps and logs.

Module 3: User Controls & Reporting

Purpose: Allow users to interact, simulate, and analyze results.

Features:

Start/Pause Simulation button.

Step-wise execution for deeper analysis.

#Functionalities & Examples

Module 1: Graph Visualization & Interaction
Functionality:

Add process/resource nodes.

Connect nodes to represent allocation/request edges.

Remove edges dynamically.


Module 2: Deadlock Detection & Prevention
Functionality:

Detect circular wait conditions.

Highlight deadlocked processes.

Run Banker’s Algorithm to prevent unsafe allocations.


Module 3: User Controls & Reporting
Functionality:

Allow users to simulate step-by-step.

Export simulation results as images or logs.

Provide a real-time analysis of deadlock conditions.
