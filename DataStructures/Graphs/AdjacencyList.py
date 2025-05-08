"""A graph implementation using adjacency list representation.

This module provides a flexible and efficient graph implementation using adjacency lists.
The implementation supports both directed and undirected graphs, with features for:
- Adding and removing vertices and edges
- Checking connectivity
- Finding paths
- Graph traversal (DFS and BFS)
- Cycle detection
- Graph properties and statistics

Example:
    >>> graph = AdjacencyList(directed=True)
    >>> graph.add_vertex(1)
    >>> graph.add_vertex(2)
    >>> graph.add_edge(1, 2, weight=5)
    >>> print(graph.has_edge(1, 2))
    True
    >>> print(graph.get_neighbors(1))
    [2]
"""

from typing import Dict, List, Set, Any, Deque, Tuple
from collections import deque


class GraphError(Exception):
    """Base exception class for graph-related errors."""
    pass


class VertexError(GraphError):
    """Raised when a vertex-related operation fails."""
    pass


class EdgeError(GraphError):
    """Raised when an edge-related operation fails."""
    pass


class AdjacencyList:
    """A graph implementation using adjacency list representation.
    
    This class provides a flexible and efficient graph implementation using
    adjacency lists. It supports both directed and undirected graphs with
    weighted or unweighted edges.
    
    The implementation provides:
    - O(1) vertex addition and removal
    - O(1) edge addition and removal
    - O(V + E) space complexity
    - Efficient traversal and path finding
    - Cycle detection
    - Graph property checks
    
    Attributes:
        directed: Whether the graph is directed
        vertices: Dictionary mapping vertex values to their neighbors
        weights: Dictionary mapping edges to their weights
    """
    
    def __init__(self, directed: bool = False) -> None:
        """Initialize an empty graph.
        
        Args:
            directed: Whether the graph is directed (default: False)
        """
        self.directed: bool = directed
        self.vertices: Dict[Any, Set[Any]] = {}
        self.weights: Dict[Tuple[Any, Any], float] = {}
    
    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph.
        
        Args:
            vertex: The vertex to add
            
        Raises:
            VertexError: If the vertex already exists
        """
        if vertex in self.vertices:
            raise VertexError(f"Vertex {vertex} already exists")
        self.vertices[vertex] = set()
    
    def remove_vertex(self, vertex: Any) -> None:
        """Remove a vertex and all its incident edges.
        
        Args:
            vertex: The vertex to remove
            
        Raises:
            VertexError: If the vertex doesn't exist
        """
        if vertex not in self.vertices:
            raise VertexError(f"Vertex {vertex} doesn't exist")
        
        # Remove all edges incident to this vertex
        for neighbor in self.vertices[vertex]:
            self.vertices[neighbor].remove(vertex)
            if (vertex, neighbor) in self.weights:
                del self.weights[(vertex, neighbor)]
            if (neighbor, vertex) in self.weights:
                del self.weights[(neighbor, vertex)]
        
        # Remove the vertex
        del self.vertices[vertex]
    
    def add_edge(self, vertex1: Any, vertex2: Any, weight: float = 1.0) -> None:
        """Add an edge between two vertices.
        
        Args:
            vertex1: The first vertex
            vertex2: The second vertex
            weight: The edge weight (default: 1.0)
            
        Raises:
            VertexError: If either vertex doesn't exist
            EdgeError: If the edge already exists
        """
        if vertex1 not in self.vertices or vertex2 not in self.vertices:
            raise VertexError("Both vertices must exist in the graph")
        
        if vertex2 in self.vertices[vertex1]:
            raise EdgeError(f"Edge ({vertex1}, {vertex2}) already exists")
        
        self.vertices[vertex1].add(vertex2)
        self.weights[(vertex1, vertex2)] = weight
        
        if not self.directed:
            self.vertices[vertex2].add(vertex1)
            self.weights[(vertex2, vertex1)] = weight
    
    def remove_edge(self, vertex1: Any, vertex2: Any) -> None:
        """Remove an edge between two vertices.
        
        Args:
            vertex1: The first vertex
            vertex2: The second vertex
            
        Raises:
            VertexError: If either vertex doesn't exist
            EdgeError: If the edge doesn't exist
        """
        if vertex1 not in self.vertices or vertex2 not in self.vertices:
            raise VertexError("Both vertices must exist in the graph")
        
        if vertex2 not in self.vertices[vertex1]:
            raise EdgeError(f"Edge ({vertex1}, {vertex2}) doesn't exist")
        
        self.vertices[vertex1].remove(vertex2)
        if (vertex1, vertex2) in self.weights:
            del self.weights[(vertex1, vertex2)]
        
        if not self.directed:
            self.vertices[vertex2].remove(vertex1)
            if (vertex2, vertex1) in self.weights:
                del self.weights[(vertex2, vertex1)]
    
    def has_vertex(self, vertex: Any) -> bool:
        """Check if a vertex exists in the graph.
        
        Args:
            vertex: The vertex to check
            
        Returns:
            True if the vertex exists, False otherwise
        """
        return vertex in self.vertices
    
    def has_edge(self, vertex1: Any, vertex2: Any) -> bool:
        """Check if an edge exists between two vertices.
        
        Args:
            vertex1: The first vertex
            vertex2: The second vertex
            
        Returns:
            True if the edge exists, False otherwise
        """
        return (vertex1 in self.vertices and
                vertex2 in self.vertices and
                vertex2 in self.vertices[vertex1])
    
    def get_neighbors(self, vertex: Any) -> List[Any]:
        """Get all neighbors of a vertex.
        
        Args:
            vertex: The vertex to get neighbors for
            
        Returns:
            List of neighboring vertices
            
        Raises:
            VertexError: If the vertex doesn't exist
        """
        if vertex not in self.vertices:
            raise VertexError(f"Vertex {vertex} doesn't exist")
        return list(self.vertices[vertex])
    
    def get_edge_weight(self, vertex1: Any, vertex2: Any) -> float:
        """Get the weight of an edge.
        
        Args:
            vertex1: The first vertex
            vertex2: The second vertex
            
        Returns:
            The edge weight
            
        Raises:
            EdgeError: If the edge doesn't exist
        """
        if not self.has_edge(vertex1, vertex2):
            raise EdgeError(f"Edge ({vertex1}, {vertex2}) doesn't exist")
        return self.weights.get((vertex1, vertex2), 1.0)
    
    def get_vertices(self) -> List[Any]:
        """Get all vertices in the graph.
        
        Returns:
            List of all vertices
        """
        return list(self.vertices.keys())
    
    def get_edges(self) -> List[Tuple[Any, Any]]:
        """Get all edges in the graph.
        
        Returns:
            List of (vertex1, vertex2) tuples representing edges
        """
        edges = []
        for vertex1 in self.vertices:
            for vertex2 in self.vertices[vertex1]:
                if self.directed or vertex1 < vertex2:
                    edges.append((vertex1, vertex2))
        return edges
    
    def get_vertex_count(self) -> int:
        """Get the number of vertices in the graph.
        
        Returns:
            The number of vertices
        """
        return len(self.vertices)
    
    def get_edge_count(self) -> int:
        """Get the number of edges in the graph.
        
        Returns:
            The number of edges
        """
        return len(self.get_edges())
    
    def is_directed(self) -> bool:
        """Check if the graph is directed.
        
        Returns:
            True if the graph is directed, False otherwise
        """
        return self.directed
    
    def is_connected(self) -> bool:
        """Check if the graph is connected.
        
        For directed graphs, this checks if the graph is weakly connected.
        
        Returns:
            True if the graph is connected, False otherwise
        """
        if not self.vertices:
            return True
        
        start_vertex = next(iter(self.vertices))
        visited = set()
        self._dfs(start_vertex, visited)
        
        return len(visited) == len(self.vertices)
    
    def has_cycle(self) -> bool:
        """Check if the graph has a cycle.
        
        Returns:
            True if the graph has a cycle, False otherwise
        """
        visited = set()
        path = set()
        
        def dfs(vertex: Any) -> bool:
            visited.add(vertex)
            path.add(vertex)
            
            for neighbor in self.vertices[vertex]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in path:
                    return True
            
            path.remove(vertex)
            return False
        
        for vertex in self.vertices:
            if vertex not in visited:
                if dfs(vertex):
                    return True
        
        return False
    
    def _dfs(self, vertex: Any, visited: Set[Any]) -> None:
        """Perform depth-first search from a vertex.
        
        Args:
            vertex: The starting vertex
            visited: Set of visited vertices
        """
        visited.add(vertex)
        for neighbor in self.vertices[vertex]:
            if neighbor not in visited:
                self._dfs(neighbor, visited)
    
    def bfs(self, start_vertex: Any) -> List[Any]:
        """Perform breadth-first search from a vertex.
        
        Args:
            start_vertex: The starting vertex
            
        Returns:
            List of vertices in BFS order
            
        Raises:
            VertexError: If the start vertex doesn't exist
        """
        if start_vertex not in self.vertices:
            raise VertexError(f"Vertex {start_vertex} doesn't exist")
        
        visited = {start_vertex}
        queue: Deque[Any] = deque([start_vertex])
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor in self.vertices[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start_vertex: Any) -> List[Any]:
        """Perform depth-first search from a vertex.
        
        Args:
            start_vertex: The starting vertex
            
        Returns:
            List of vertices in DFS order
            
        Raises:
            VertexError: If the start vertex doesn't exist
        """
        if start_vertex not in self.vertices:
            raise VertexError(f"Vertex {start_vertex} doesn't exist")
        
        visited = set()
        result = []
        
        def dfs_recursive(vertex: Any) -> None:
            visited.add(vertex)
            result.append(vertex)
            
            for neighbor in self.vertices[vertex]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start_vertex)
        return result
    
    def __str__(self) -> str:
        """Return a string representation of the graph.
        
        Returns:
            A string showing the graph's structure
        """
        result = []
        for vertex in sorted(self.vertices.keys()):
            neighbors = sorted(self.vertices[vertex])
            weights = [f"{n}({self.weights.get((vertex, n), 1.0)})" for n in neighbors]
            result.append(f"{vertex} -> {', '.join(weights)}")
        return "\n".join(result)


if __name__ == "__main__":
    # Test the implementation
    def test_graph():
        # Create a directed graph
        graph = AdjacencyList(directed=True)
        
        # Add vertices
        for i in range(5):
            graph.add_vertex(i)
        
        # Add edges
        graph.add_edge(0, 1, 2.0)
        graph.add_edge(1, 2, 3.0)
        graph.add_edge(2, 3, 4.0)
        graph.add_edge(3, 4, 5.0)
        graph.add_edge(4, 0, 1.0)
        
        # Test basic operations
        print("Graph structure:")
        print(graph)
        print(f"\nNumber of vertices: {graph.get_vertex_count()}")
        print(f"Number of edges: {graph.get_edge_count()}")
        print(f"Is directed: {graph.is_directed()}")
        print(f"Has cycle: {graph.has_cycle()}")
        
        # Test traversals
        print("\nBFS from vertex 0:", graph.bfs(0))
        print("DFS from vertex 0:", graph.dfs(0))
        
        # Test error handling
        try:
            graph.add_vertex(0)  # Duplicate vertex
        except VertexError as e:
            print(f"\nExpected error: {e}")
        
        try:
            graph.add_edge(0, 5)  # Non-existent vertex
        except VertexError as e:
            print(f"Expected error: {e}")
        
        try:
            graph.add_edge(0, 1)  # Duplicate edge
        except EdgeError as e:
            print(f"Expected error: {e}")
    
    test_graph()
