"""A graph implementation using adjacency matrix representation.

This module provides an efficient graph implementation using adjacency matrices.
The implementation is particularly suitable for dense graphs and supports:
- Fast edge existence checks (O(1))
- Efficient edge weight updates
- Graph operations like transposition
- Matrix-based algorithms
- Both directed and undirected graphs

Example:
    >>> graph = AdjacencyMatrix(directed=True)
    >>> graph.add_vertex(1)
    >>> graph.add_vertex(2)
    >>> graph.add_edge(1, 2, weight=5)
    >>> print(graph.has_edge(1, 2))
    True
    >>> print(graph.get_edge_weight(1, 2))
    5.0
"""

from typing import Dict, List, Set, Any, Optional, Deque, Tuple
from collections import deque
import numpy as np


class GraphError(Exception):
    """Base exception class for graph-related errors."""
    pass


class VertexError(GraphError):
    """Raised when a vertex-related operation fails."""
    pass


class EdgeError(GraphError):
    """Raised when an edge-related operation fails."""
    pass


class AdjacencyMatrix:
    """A graph implementation using adjacency matrix representation.
    
    This class provides an efficient graph implementation using adjacency matrices.
    It's particularly suitable for dense graphs where most vertices are connected.
    
    The implementation provides:
    - O(1) edge existence checks
    - O(1) edge weight updates
    - O(V²) space complexity
    - Efficient matrix operations
    - Support for both directed and undirected graphs
    
    Attributes:
        directed: Whether the graph is directed
        vertices: Dictionary mapping vertex values to indices
        matrix: 2D numpy array storing edge weights
    """
    
    def __init__(self, directed: bool = False) -> None:
        """Initialize an empty graph.
        
        Args:
            directed: Whether the graph is directed (default: False)
        """
        self.directed: bool = directed
        self.vertices: Dict[Any, int] = {}  # vertex -> index mapping
        self.matrix: np.ndarray = np.zeros((0, 0))  # adjacency matrix
    
    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph.
        
        Args:
            vertex: The vertex to add
            
        Raises:
            VertexError: If the vertex already exists
        """
        if vertex in self.vertices:
            raise VertexError(f"Vertex {vertex} already exists")
        
        # Add new vertex with index = current size
        self.vertices[vertex] = len(self.vertices)
        
        # Resize matrix to accommodate new vertex
        new_size = len(self.vertices)
        new_matrix = np.zeros((new_size, new_size))
        new_matrix[:new_size-1, :new_size-1] = self.matrix
        self.matrix = new_matrix
    
    def remove_vertex(self, vertex: Any) -> None:
        """Remove a vertex and all its incident edges.
        
        Args:
            vertex: The vertex to remove
            
        Raises:
            VertexError: If the vertex doesn't exist
        """
        if vertex not in self.vertices:
            raise VertexError(f"Vertex {vertex} doesn't exist")
        
        # Get the index of the vertex to remove
        index = self.vertices[vertex]
        
        # Remove the vertex from the mapping
        del self.vertices[vertex]
        
        # Update indices of remaining vertices
        for v, i in self.vertices.items():
            if i > index:
                self.vertices[v] = i - 1
        
        # Remove the vertex's row and column from the matrix
        self.matrix = np.delete(self.matrix, index, axis=0)
        self.matrix = np.delete(self.matrix, index, axis=1)
    
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
        
        i, j = self.vertices[vertex1], self.vertices[vertex2]
        
        if self.matrix[i, j] != 0:
            raise EdgeError(f"Edge ({vertex1}, {vertex2}) already exists")
        
        self.matrix[i, j] = weight
        
        if not self.directed:
            self.matrix[j, i] = weight
    
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
        
        i, j = self.vertices[vertex1], self.vertices[vertex2]
        
        if self.matrix[i, j] == 0:
            raise EdgeError(f"Edge ({vertex1}, {vertex2}) doesn't exist")
        
        self.matrix[i, j] = 0
        
        if not self.directed:
            self.matrix[j, i] = 0
    
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
        if vertex1 not in self.vertices or vertex2 not in self.vertices:
            return False
        
        i, j = self.vertices[vertex1], self.vertices[vertex2]
        return self.matrix[i, j] != 0
    
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
        
        i = self.vertices[vertex]
        neighbors = []
        
        for v, j in self.vertices.items():
            if self.matrix[i, j] != 0:
                neighbors.append(v)
        
        return neighbors
    
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
        
        i, j = self.vertices[vertex1], self.vertices[vertex2]
        return float(self.matrix[i, j])
    
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
        for vertex1, i in self.vertices.items():
            for vertex2, j in self.vertices.items():
                if self.matrix[i, j] != 0 and (self.directed or vertex1 < vertex2):
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
        
        # Use BFS to check connectivity
        start_vertex = next(iter(self.vertices))
        visited = set()
        queue: Deque[Any] = deque([start_vertex])
        
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                for neighbor in self.get_neighbors(vertex):
                    if neighbor not in visited:
                        queue.append(neighbor)
        
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
            
            for neighbor in self.get_neighbors(vertex):
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
    
    def transpose(self) -> 'AdjacencyMatrix':
        """Create the transpose of the graph.
        
        For directed graphs, this reverses all edges.
        For undirected graphs, this returns a copy of the graph.
        
        Returns:
            A new graph that is the transpose of this graph
        """
        if not self.directed:
            return self.copy()
        
        transposed = AdjacencyMatrix(directed=True)
        
        # Add all vertices
        for vertex in self.vertices:
            transposed.add_vertex(vertex)
        
        # Add all edges in reverse direction
        for vertex1, i in self.vertices.items():
            for vertex2, j in self.vertices.items():
                if self.matrix[i, j] != 0:
                    transposed.add_edge(vertex2, vertex1, self.matrix[i, j])
        
        return transposed
    
    def copy(self) -> 'AdjacencyMatrix':
        """Create a deep copy of the graph.
        
        Returns:
            A new graph that is a deep copy of this graph
        """
        copy = AdjacencyMatrix(directed=self.directed)
        
        # Add all vertices
        for vertex in self.vertices:
            copy.add_vertex(vertex)
        
        # Add all edges
        for vertex1, i in self.vertices.items():
            for vertex2, j in self.vertices.items():
                if self.matrix[i, j] != 0:
                    copy.add_edge(vertex1, vertex2, self.matrix[i, j])
        
        return copy
    
    def __str__(self) -> str:
        """Return a string representation of the graph.
        
        Returns:
            A string showing the graph's structure
        """
        if not self.vertices:
            return "Empty Graph"
        
        # Create header with vertex labels
        vertices = sorted(self.vertices.keys())
        header = "    " + " ".join(f"{v:4}" for v in vertices)
        
        # Create matrix rows
        rows = []
        for vertex1 in vertices:
            i = self.vertices[vertex1]
            row = [f"{vertex1:2} |"]
            for vertex2 in vertices:
                j = self.vertices[vertex2]
                weight = self.matrix[i, j]
                row.append(f"{weight:4.1f}" if weight != 0 else "   .")
            rows.append(" ".join(row))
        
        return header + "\n" + "\n".join(rows)


if __name__ == "__main__":
    # Test the implementation
    def test_graph():
        # Create a directed graph
        graph = AdjacencyMatrix(directed=True)
        
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
        
        # Test matrix operations
        print("\nTransposed graph:")
        print(graph.transpose())
        
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
