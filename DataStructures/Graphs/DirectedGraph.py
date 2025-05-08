"""A specialized directed graph implementation.

This module provides a directed graph implementation with additional features
specific to directed graphs, such as:
- Topological sorting
- Strongly connected components
- Path finding with direction constraints
- Cycle detection in directed graphs
- Graph reversal operations

Example:
    >>> graph = DirectedGraph()
    >>> graph.add_vertex(1)
    >>> graph.add_vertex(2)
    >>> graph.add_edge(1, 2, weight=5)
    >>> print(graph.has_edge(1, 2))
    True
    >>> print(graph.has_edge(2, 1))  # Different from undirected graphs
    False
"""

from typing import List, Set, Any, Deque, Tuple, Optional
from collections import deque
from AdjacencyMatrix import AdjacencyMatrix, GraphError, VertexError, EdgeError


class DirectedGraph(AdjacencyMatrix):
    """A specialized directed graph implementation.
    
    This class extends AdjacencyMatrix to provide additional features
    specific to directed graphs. It enforces the directed nature of the graph
    and provides specialized algorithms for directed graph analysis.
    
    The implementation provides:
    - Topological sorting for DAGs
    - Strongly connected component detection
    - Directed path finding
    - Cycle detection in directed graphs
    - Graph reversal operations
    
    Attributes:
        vertices: Dictionary mapping vertex values to indices
        matrix: 2D numpy array storing edge weights
    """
    
    def __init__(self) -> None:
        """Initialize an empty directed graph."""
        super().__init__(directed=True)
    
    def add_edge(self, vertex1: Any, vertex2: Any, weight: float = 1.0) -> None:
        """Add a directed edge from vertex1 to vertex2.
        
        Args:
            vertex1: The source vertex
            vertex2: The target vertex
            weight: The edge weight (default: 1.0)
            
        Raises:
            VertexError: If either vertex doesn't exist
            EdgeError: If the edge already exists
        """
        super().add_edge(vertex1, vertex2, weight)
    
    def get_in_degree(self, vertex: Any) -> int:
        """Get the in-degree of a vertex.
        
        The in-degree is the number of edges pointing to the vertex.
        
        Args:
            vertex: The vertex to get in-degree for
            
        Returns:
            The in-degree of the vertex
            
        Raises:
            VertexError: If the vertex doesn't exist
        """
        if vertex not in self.vertices:
            raise VertexError(f"Vertex {vertex} doesn't exist")
        
        j = self.vertices[vertex]
        return sum(1 for i in range(len(self.vertices)) if self.matrix[i, j] != 0)
    
    def get_out_degree(self, vertex: Any) -> int:
        """Get the out-degree of a vertex.
        
        The out-degree is the number of edges pointing from the vertex.
        
        Args:
            vertex: The vertex to get out-degree for
            
        Returns:
            The out-degree of the vertex
            
        Raises:
            VertexError: If the vertex doesn't exist
        """
        if vertex not in self.vertices:
            raise VertexError(f"Vertex {vertex} doesn't exist")
        
        i = self.vertices[vertex]
        return sum(1 for j in range(len(self.vertices)) if self.matrix[i, j] != 0)
    
    def get_sources(self) -> List[Any]:
        """Get all source vertices in the graph.
        
        A source vertex has no incoming edges.
        
        Returns:
            List of source vertices
        """
        return [v for v in self.vertices if self.get_in_degree(v) == 0]
    
    def get_sinks(self) -> List[Any]:
        """Get all sink vertices in the graph.
        
        A sink vertex has no outgoing edges.
        
        Returns:
            List of sink vertices
        """
        return [v for v in self.vertices if self.get_out_degree(v) == 0]
    
    def topological_sort(self) -> List[Any]:
        """Perform topological sorting of the graph.
        
        This method returns a list of vertices in topological order.
        The graph must be a DAG (Directed Acyclic Graph).
        
        Returns:
            List of vertices in topological order
            
        Raises:
            GraphError: If the graph contains a cycle
        """
        if self.has_cycle():
            raise GraphError("Graph contains a cycle, cannot perform topological sort")
        
        # Calculate in-degrees
        in_degrees = {v: self.get_in_degree(v) for v in self.vertices}
        
        # Initialize queue with source vertices
        queue: Deque[Any] = deque(v for v, d in in_degrees.items() if d == 0)
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            # Update in-degrees of neighbors
            for neighbor in self.get_neighbors(vertex):
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(self.vertices):
            raise GraphError("Graph contains a cycle")
        
        return result
    
    def get_strongly_connected_components(self) -> List[Set[Any]]:
        """Find all strongly connected components in the graph.
        
        A strongly connected component is a maximal subgraph where every
        vertex is reachable from every other vertex.
        
        Returns:
            List of sets, where each set contains vertices in a strongly
            connected component
        """
        # First DFS to get finish times
        visited = set()
        finish_times = []
        
        def dfs1(vertex: Any) -> None:
            visited.add(vertex)
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in visited:
                    dfs1(neighbor)
            finish_times.append(vertex)
        
        for vertex in self.vertices:
            if vertex not in visited:
                dfs1(vertex)
        
        # Second DFS on transposed graph
        visited.clear()
        components = []
        
        def dfs2(vertex: Any, component: Set[Any]) -> None:
            visited.add(vertex)
            component.add(vertex)
            for neighbor in self.transpose().get_neighbors(vertex):
                if neighbor not in visited:
                    dfs2(neighbor, component)
        
        for vertex in reversed(finish_times):
            if vertex not in visited:
                component = set()
                dfs2(vertex, component)
                components.append(component)
        
        return components
    
    def find_path(self, start: Any, end: Any) -> Optional[List[Any]]:
        """Find a directed path from start to end vertex.
        
        Args:
            start: The starting vertex
            end: The target vertex
            
        Returns:
            List of vertices forming a path from start to end,
            or None if no path exists
            
        Raises:
            VertexError: If either vertex doesn't exist
        """
        if start not in self.vertices or end not in self.vertices:
            raise VertexError("Both vertices must exist in the graph")
        
        if start == end:
            return [start]
        
        # Use BFS to find the shortest path
        visited = {start}
        queue: Deque[Tuple[Any, List[Any]]] = deque([(start, [start])])
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor in self.get_neighbors(vertex):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def is_strongly_connected(self) -> bool:
        """Check if the graph is strongly connected.
        
        A graph is strongly connected if there is a directed path from
        any vertex to any other vertex.
        
        Returns:
            True if the graph is strongly connected, False otherwise
        """
        if not self.vertices:
            return True
        
        # Check if there's a path from the first vertex to all others
        start = next(iter(self.vertices))
        for vertex in self.vertices:
            if vertex != start and not self.find_path(start, vertex):
                return False
        
        # Check if there's a path from all vertices to the first vertex
        for vertex in self.vertices:
            if vertex != start and not self.find_path(vertex, start):
                return False
        
        return True
    
    def get_condensation(self) -> 'DirectedGraph':
        """Create the condensation of the graph.
        
        The condensation is a DAG where each vertex represents a strongly
        connected component of the original graph.
        
        Returns:
            A new directed graph representing the condensation
        """
        # Find strongly connected components
        components = self.get_strongly_connected_components()
        
        # Create component mapping
        component_map = {}
        for i, component in enumerate(components):
            for vertex in component:
                component_map[vertex] = i
        
        # Create condensation graph
        condensation = DirectedGraph()
        
        # Add vertices (one for each component)
        for i in range(len(components)):
            condensation.add_vertex(i)
        
        # Add edges between components
        for i, component in enumerate(components):
            for vertex in component:
                for neighbor in self.get_neighbors(vertex):
                    neighbor_component = component_map[neighbor]
                    if i != neighbor_component:
                        condensation.add_edge(i, neighbor_component)
        
        return condensation
    
    def __str__(self) -> str:
        """Return a string representation of the directed graph.
        
        Returns:
            A string showing the graph's structure with edge directions
        """
        if not self.vertices:
            return "Empty Directed Graph"
        
        result = []
        for vertex in sorted(self.vertices.keys()):
            neighbors = self.get_neighbors(vertex)
            if neighbors:
                weights = [f"{n}({self.get_edge_weight(vertex, n)})" for n in neighbors]
                result.append(f"{vertex} -> {', '.join(weights)}")
            else:
                result.append(f"{vertex} -> (no outgoing edges)")
        return "\n".join(result)


if __name__ == "__main__":
    # Test the implementation
    def test_directed_graph():
        # Create a directed graph
        graph = DirectedGraph()
        
        # Add vertices
        for i in range(6):
            graph.add_vertex(i)
        
        # Add edges to create a DAG
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
            print(f"Vertex {vertex}: in-degree={graph.get_in_degree(vertex)}, "
                  f"out-degree={graph.get_out_degree(vertex)}")
        
        # Test sources and sinks
        print("\nSources:", graph.get_sources())
        print("Sinks:", graph.get_sinks())
        
        # Test topological sort
        print("\nTopological order:", graph.topological_sort())
        
        # Test path finding
        print("\nPath from 0 to 5:", graph.find_path(0, 5))
        print("Path from 5 to 0:", graph.find_path(5, 0))  # Should be None
        
        # Create a graph with cycles for SCC testing
        cyclic_graph = DirectedGraph()
        for i in range(4):
            cyclic_graph.add_vertex(i)
        
        cyclic_graph.add_edge(0, 1)
        cyclic_graph.add_edge(1, 2)
        cyclic_graph.add_edge(2, 3)
        cyclic_graph.add_edge(3, 0)
        cyclic_graph.add_edge(1, 3)
        
        print("\nCyclic graph structure:")
        print(cyclic_graph)
        
        # Test strongly connected components
        print("\nStrongly connected components:")
        components = cyclic_graph.get_strongly_connected_components()
        for i, component in enumerate(components):
            print(f"Component {i}: {component}")
        
        # Test condensation
        print("\nCondensation graph:")
        print(cyclic_graph.get_condensation())
        
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
    
    test_directed_graph()
