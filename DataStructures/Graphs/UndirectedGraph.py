"""A specialized undirected graph implementation.

This module provides an undirected graph implementation with additional features
specific to undirected graphs, such as:
- Connected components
- Bipartite graph checking
- Eulerian path/circuit detection
- Minimum spanning tree algorithms
- Graph coloring

Example:
    >>> graph = UndirectedGraph()
    >>> graph.add_vertex(1)
    >>> graph.add_vertex(2)
    >>> graph.add_edge(1, 2, weight=5)
    >>> print(graph.has_edge(1, 2))
    True
    >>> print(graph.has_edge(2, 1))  # Same as (1, 2) in undirected graphs
    True
"""

from typing import Dict, List, Set, Any, Deque
from collections import deque
from AdjacencyMatrix import AdjacencyMatrix, GraphError, VertexError, EdgeError


class UndirectedGraph(AdjacencyMatrix):
    """A specialized undirected graph implementation.
    
    This class extends AdjacencyMatrix to provide additional features
    specific to undirected graphs. It enforces the undirected nature of the graph
    and provides specialized algorithms for undirected graph analysis.
    
    The implementation provides:
    - Connected component detection
    - Bipartite graph checking
    - Eulerian path/circuit detection
    - Minimum spanning tree algorithms
    - Graph coloring
    
    Attributes:
        vertices: Dictionary mapping vertex values to indices
        matrix: 2D numpy array storing edge weights
    """
    
    def __init__(self) -> None:
        """Initialize an empty undirected graph."""
        super().__init__(directed=False)
    
    def add_edge(self, vertex1: Any, vertex2: Any, weight: float = 1.0) -> None:
        """Add an undirected edge between vertex1 and vertex2.
        
        Args:
            vertex1: The first vertex
            vertex2: The second vertex
            weight: The edge weight (default: 1.0)
            
        Raises:
            VertexError: If either vertex doesn't exist
            EdgeError: If the edge already exists
        """
        super().add_edge(vertex1, vertex2, weight)
    
    def get_degree(self, vertex: Any) -> int:
        """Get the degree of a vertex.
        
        The degree is the number of edges incident to the vertex.
        
        Args:
            vertex: The vertex to get degree for
            
        Returns:
            The degree of the vertex
            
        Raises:
            VertexError: If the vertex doesn't exist
        """
        if vertex not in self.vertices:
            raise VertexError(f"Vertex {vertex} doesn't exist")
        
        i = self.vertices[vertex]
        return sum(1 for j in range(len(self.vertices)) if self.matrix[i, j] != 0)
    
    def get_connected_components(self) -> List[Set[Any]]:
        """Find all connected components in the graph.
        
        A connected component is a maximal subgraph where every
        vertex is reachable from every other vertex.
        
        Returns:
            List of sets, where each set contains vertices in a
            connected component
        """
        visited = set()
        components = []
        
        def dfs(vertex: Any, component: Set[Any]) -> None:
            visited.add(vertex)
            component.add(vertex)
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in visited:
                    dfs(neighbor, component)
        
        for vertex in self.vertices:
            if vertex not in visited:
                component = set()
                dfs(vertex, component)
                components.append(component)
        
        return components
    
    def is_connected(self) -> bool:
        """Check if the graph is connected.
        
        A graph is connected if there is a path between any two vertices.
        
        Returns:
            True if the graph is connected, False otherwise
        """
        if not self.vertices:
            return True
        
        # Use BFS to check connectivity
        start = next(iter(self.vertices))
        visited = {start}
        queue: Deque[Any] = deque([start])
        
        while queue:
            vertex = queue.popleft()
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.vertices)
    
    def is_bipartite(self) -> bool:
        """Check if the graph is bipartite.
        
        A graph is bipartite if its vertices can be divided into two
        independent sets such that every edge connects a vertex in one
        set to a vertex in the other set.
        
        Returns:
            True if the graph is bipartite, False otherwise
        """
        if not self.vertices:
            return True
        
        # Use BFS to check bipartiteness
        colors: Dict[Any, int] = {}
        queue: Deque[Any] = deque()
        
        # Start with the first vertex
        start = next(iter(self.vertices))
        colors[start] = 0
        queue.append(start)
        
        while queue:
            vertex = queue.popleft()
            current_color = colors[vertex]
            
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in colors:
                    colors[neighbor] = 1 - current_color
                    queue.append(neighbor)
                elif colors[neighbor] == current_color:
                    return False
        
        return True
    
    def has_eulerian_circuit(self) -> bool:
        """Check if the graph has an Eulerian circuit.
        
        An Eulerian circuit is a path that visits every edge exactly once
        and starts and ends at the same vertex.
        
        Returns:
            True if the graph has an Eulerian circuit, False otherwise
        """
        if not self.is_connected():
            return False
        
        # All vertices must have even degree
        return all(self.get_degree(v) % 2 == 0 for v in self.vertices)
    
    def has_eulerian_path(self) -> bool:
        """Check if the graph has an Eulerian path.
        
        An Eulerian path is a path that visits every edge exactly once.
        
        Returns:
            True if the graph has an Eulerian path, False otherwise
        """
        if not self.is_connected():
            return False
        
        # Count vertices with odd degree
        odd_degree_count = sum(1 for v in self.vertices if self.get_degree(v) % 2 != 0)
        
        # Either all vertices have even degree (circuit) or exactly two have odd degree (path)
        return odd_degree_count == 0 or odd_degree_count == 2
    
    def get_minimum_spanning_tree(self) -> 'UndirectedGraph':
        """Find the minimum spanning tree using Kruskal's algorithm.
        
        Returns:
            A new undirected graph representing the minimum spanning tree
            
        Raises:
            GraphError: If the graph is not connected
        """
        if not self.is_connected():
            raise GraphError("Graph must be connected to find minimum spanning tree")
        
        # Create disjoint set for union-find
        parent = {v: v for v in self.vertices}
        rank = {v: 0 for v in self.vertices}
        
        def find(v: Any) -> Any:
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]
        
        def union(v1: Any, v2: Any) -> None:
            root1 = find(v1)
            root2 = find(v2)
            if root1 != root2:
                if rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    if rank[root1] == rank[root2]:
                        rank[root1] += 1
        
        # Create MST
        mst = UndirectedGraph()
        for v in self.vertices:
            mst.add_vertex(v)
        
        # Sort edges by weight
        edges = []
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 < v2 and self.has_edge(v1, v2):
                    edges.append((v1, v2, self.get_edge_weight(v1, v2)))
        edges.sort(key=lambda x: x[2])
        
        # Add edges to MST
        for v1, v2, weight in edges:
            if find(v1) != find(v2):
                mst.add_edge(v1, v2, weight)
                union(v1, v2)
        
        return mst
    
    def get_vertex_coloring(self) -> Dict[Any, int]:
        """Find a vertex coloring of the graph using a greedy algorithm.
        
        Returns:
            Dictionary mapping vertices to their colors (integers)
        """
        colors: Dict[Any, int] = {}
        
        for vertex in sorted(self.vertices.keys()):
            # Find the smallest available color
            used_colors = {colors[neighbor] for neighbor in self.get_neighbors(vertex)
                          if neighbor in colors}
            color = 0
            while color in used_colors:
                color += 1
            colors[vertex] = color
        
        return colors
    
    def __str__(self) -> str:
        """Return a string representation of the undirected graph.
        
        Returns:
            A string showing the graph's structure
        """
        if not self.vertices:
            return "Empty Undirected Graph"
        
        result = []
        for vertex in sorted(self.vertices.keys()):
            neighbors = self.get_neighbors(vertex)
            if neighbors:
                weights = [f"{n}({self.get_edge_weight(vertex, n)})" for n in neighbors]
                result.append(f"{vertex} -- {', '.join(weights)}")
            else:
                result.append(f"{vertex} -- (no edges)")
        return "\n".join(result)


if __name__ == "__main__":
    # Test the implementation
    def test_undirected_graph():
        # Create an undirected graph
        graph = UndirectedGraph()
        
        # Add vertices
        for i in range(6):
            graph.add_vertex(i)
        
        # Add edges
        graph.add_edge(0, 1, 2.0)
        graph.add_edge(0, 2, 3.0)
        graph.add_edge(1, 3, 4.0)
        graph.add_edge(2, 3, 5.0)
        graph.add_edge(3, 4, 1.0)
        graph.add_edge(3, 5, 2.0)
        
        # Test basic operations
        print("Graph structure:")
        print(graph)
        print(f"\nNumber of vertices: {graph.get_vertex_count()}")
        print(f"Number of edges: {graph.get_edge_count()}")
        
        # Test vertex degrees
        print("\nVertex degrees:")
        for vertex in graph.get_vertices():
            print(f"Vertex {vertex}: degree={graph.get_degree(vertex)}")
        
        # Test connected components
        print("\nConnected components:")
        components = graph.get_connected_components()
        for i, component in enumerate(components):
            print(f"Component {i}: {component}")
        
        # Test bipartite checking
        print(f"\nIs bipartite: {graph.is_bipartite()}")
        
        # Test Eulerian properties
        print(f"Has Eulerian circuit: {graph.has_eulerian_circuit()}")
        print(f"Has Eulerian path: {graph.has_eulerian_path()}")
        
        # Test minimum spanning tree
        print("\nMinimum spanning tree:")
        mst = graph.get_minimum_spanning_tree()
        print(mst)
        
        # Test vertex coloring
        print("\nVertex coloring:")
        coloring = graph.get_vertex_coloring()
        for vertex, color in sorted(coloring.items()):
            print(f"Vertex {vertex}: color {color}")
        
        # Create a bipartite graph for testing
        bipartite = UndirectedGraph()
        for i in range(4):
            bipartite.add_vertex(i)
        
        bipartite.add_edge(0, 2)
        bipartite.add_edge(0, 3)
        bipartite.add_edge(1, 2)
        bipartite.add_edge(1, 3)
        
        print("\nBipartite graph structure:")
        print(bipartite)
        print(f"Is bipartite: {bipartite.is_bipartite()}")
        
        # Test error handling
        try:
            graph.add_vertex(0)  # Duplicate vertex
        except VertexError as e:
            print(f"\nExpected error: {e}")
        
        try:
            graph.add_edge(0, 6)  # Non-existent vertex
        except VertexError as e:
            print(f"Expected error: {e}")
        
        try:
            graph.add_edge(0, 1)  # Duplicate edge
        except EdgeError as e:
            print(f"Expected error: {e}")
    
    test_undirected_graph()
