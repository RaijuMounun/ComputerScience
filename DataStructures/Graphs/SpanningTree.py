"""A specialized spanning tree implementation.

This module provides implementations of minimum spanning tree (MST) algorithms,
including:
- Kruskal's algorithm
- Prim's algorithm
- MST verification
- MST comparison
- Edge weight analysis

Example:
    >>> graph = UndirectedGraph()
    >>> graph.add_vertex(1)
    >>> graph.add_vertex(2)
    >>> graph.add_edge(1, 2, weight=5)
    >>> mst = SpanningTree.kruskal(graph)
    >>> print(mst.get_total_weight())
    5.0
"""

from typing import Dict, Any, Optional
from heapq import heappush, heappop
from UndirectedGraph import UndirectedGraph
from AdjacencyMatrix import GraphError, VertexError


class SpanningTree:
    """A class providing minimum spanning tree algorithms.
    
    This class provides static methods for finding minimum spanning trees
    using different algorithms. It also includes utilities for MST analysis
    and verification.
    
    The implementation provides:
    - Kruskal's algorithm
    - Prim's algorithm
    - MST verification
    - MST comparison
    - Edge weight analysis
    """
    
    @staticmethod
    def kruskal(graph: UndirectedGraph) -> UndirectedGraph:
        """Find the minimum spanning tree using Kruskal's algorithm.
        
        Kruskal's algorithm builds the MST by adding edges in order of
        increasing weight, avoiding cycles.
        
        Args:
            graph: The input undirected graph
            
        Returns:
            A new undirected graph representing the minimum spanning tree
            
        Raises:
            GraphError: If the graph is not connected
        """
        if not graph.is_connected():
            raise GraphError("Graph must be connected to find minimum spanning tree")
        
        # Create disjoint set for union-find
        parent = {v: v for v in graph.get_vertices()}
        rank = {v: 0 for v in graph.get_vertices()}
        
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
        for v in graph.get_vertices():
            mst.add_vertex(v)
        
        # Sort edges by weight
        edges = []
        for v1 in graph.get_vertices():
            for v2 in graph.get_vertices():
                if v1 < v2 and graph.has_edge(v1, v2):
                    edges.append((v1, v2, graph.get_edge_weight(v1, v2)))
        edges.sort(key=lambda x: x[2])
        
        # Add edges to MST
        for v1, v2, weight in edges:
            if find(v1) != find(v2):
                mst.add_edge(v1, v2, weight)
                union(v1, v2)
        
        return mst
    
    @staticmethod
    def prim(graph: UndirectedGraph, start: Optional[Any] = None) -> UndirectedGraph:
        """Find the minimum spanning tree using Prim's algorithm.
        
        Prim's algorithm builds the MST by growing a tree from a starting
        vertex, always adding the minimum weight edge that connects to
        a new vertex.
        
        Args:
            graph: The input undirected graph
            start: The starting vertex (default: first vertex)
            
        Returns:
            A new undirected graph representing the minimum spanning tree
            
        Raises:
            GraphError: If the graph is not connected
            VertexError: If the start vertex doesn't exist
        """
        if not graph.is_connected():
            raise GraphError("Graph must be connected to find minimum spanning tree")
        
        if start is not None and start not in graph.get_vertices():
            raise VertexError(f"Start vertex {start} doesn't exist")
        
        # Create MST
        mst = UndirectedGraph()
        for v in graph.get_vertices():
            mst.add_vertex(v)
        
        # Initialize data structures
        if start is None:
            start = next(iter(graph.get_vertices()))
        
        visited = {start}
        edges = []  # Priority queue of (weight, vertex1, vertex2)
        
        # Add edges from start vertex
        for neighbor in graph.get_neighbors(start):
            weight = graph.get_edge_weight(start, neighbor)
            heappush(edges, (weight, start, neighbor))
        
        # Build MST
        while edges and len(visited) < len(graph.get_vertices()):
            weight, v1, v2 = heappop(edges)
            
            if v2 not in visited:
                mst.add_edge(v1, v2, weight)
                visited.add(v2)
                
                # Add edges from new vertex
                for neighbor in graph.get_neighbors(v2):
                    if neighbor not in visited:
                        weight = graph.get_edge_weight(v2, neighbor)
                        heappush(edges, (weight, v2, neighbor))
        
        return mst
    
    @staticmethod
    def verify_mst(graph: UndirectedGraph, mst: UndirectedGraph) -> bool:
        """Verify if a graph is a valid minimum spanning tree.
        
        A valid MST must:
        1. Be a tree (connected and acyclic)
        2. Include all vertices from the original graph
        3. Have edges only from the original graph
        4. Have minimum total weight
        
        Args:
            graph: The original undirected graph
            mst: The graph to verify as an MST
            
        Returns:
            True if the graph is a valid MST, False otherwise
        """
        # Check if MST is connected
        if not mst.is_connected():
            return False
        
        # Check if MST includes all vertices
        if set(mst.get_vertices()) != set(graph.get_vertices()):
            return False
        
        # Check if MST has correct number of edges
        if mst.get_edge_count() != len(mst.get_vertices()) - 1:
            return False
        
        # Check if all edges in MST exist in original graph
        for v1, v2 in mst.get_edges():
            if not graph.has_edge(v1, v2):
                return False
        
        # Check if MST has minimum total weight
        mst_weight = sum(mst.get_edge_weight(v1, v2) for v1, v2 in mst.get_edges())
        kruskal_mst = SpanningTree.kruskal(graph)
        kruskal_weight = sum(kruskal_mst.get_edge_weight(v1, v2)
                           for v1, v2 in kruskal_mst.get_edges())
        
        return abs(mst_weight - kruskal_weight) < 1e-10
    
    @staticmethod
    def compare_msts(mst1: UndirectedGraph, mst2: UndirectedGraph) -> Dict[str, float]:
        """Compare two minimum spanning trees.
        
        Args:
            mst1: First minimum spanning tree
            mst2: Second minimum spanning tree
            
        Returns:
            Dictionary containing comparison metrics:
            - total_weight_diff: Difference in total weights
            - common_edges: Number of common edges
            - edge_weight_diff: Average difference in edge weights
        """
        # Calculate total weights
        weight1 = sum(mst1.get_edge_weight(v1, v2) for v1, v2 in mst1.get_edges())
        weight2 = sum(mst2.get_edge_weight(v1, v2) for v1, v2 in mst2.get_edges())
        
        # Find common edges
        edges1 = set((min(v1, v2), max(v1, v2)) for v1, v2 in mst1.get_edges())
        edges2 = set((min(v1, v2), max(v1, v2)) for v1, v2 in mst2.get_edges())
        common_edges = edges1.intersection(edges2)
        
        # Calculate average edge weight difference
        weight_diffs = []
        for v1, v2 in common_edges:
            w1 = mst1.get_edge_weight(v1, v2)
            w2 = mst2.get_edge_weight(v1, v2)
            weight_diffs.append(abs(w1 - w2))
        
        avg_weight_diff = sum(weight_diffs) / len(weight_diffs) if weight_diffs else 0
        
        return {
            'total_weight_diff': abs(weight1 - weight2),
            'common_edges': len(common_edges),
            'edge_weight_diff': avg_weight_diff
        }
    
    @staticmethod
    def analyze_edge_weights(graph: UndirectedGraph) -> Dict[str, float]:
        """Analyze edge weights in the graph.
        
        Args:
            graph: The input undirected graph
            
        Returns:
            Dictionary containing weight statistics:
            - min_weight: Minimum edge weight
            - max_weight: Maximum edge weight
            - avg_weight: Average edge weight
            - total_weight: Total weight of all edges
        """
        weights = [graph.get_edge_weight(v1, v2)
                  for v1, v2 in graph.get_edges()]
        
        if not weights:
            return {
                'min_weight': 0.0,
                'max_weight': 0.0,
                'avg_weight': 0.0,
                'total_weight': 0.0
            }
        
        return {
            'min_weight': min(weights),
            'max_weight': max(weights),
            'avg_weight': sum(weights) / len(weights),
            'total_weight': sum(weights)
        }


if __name__ == "__main__":
    # Test the implementation
    def test_spanning_tree():
        # Create a test graph
        graph = UndirectedGraph()
        
        # Add vertices
        for i in range(6):
            graph.add_vertex(i)
        
        # Add edges
        graph.add_edge(0, 1, 4.0)
        graph.add_edge(0, 2, 3.0)
        graph.add_edge(1, 2, 1.0)
        graph.add_edge(1, 3, 2.0)
        graph.add_edge(2, 3, 4.0)
        graph.add_edge(3, 4, 2.0)
        graph.add_edge(3, 5, 5.0)
        graph.add_edge(4, 5, 1.0)
        
        print("Original graph:")
        print(graph)
        
        # Test Kruskal's algorithm
        print("\nKruskal's MST:")
        kruskal_mst = SpanningTree.kruskal(graph)
        print(kruskal_mst)
        
        # Test Prim's algorithm
        print("\nPrim's MST:")
        prim_mst = SpanningTree.prim(graph)
        print(prim_mst)
        
        # Test MST verification
        print("\nMST verification:")
        print(f"Kruskal's MST is valid: {SpanningTree.verify_mst(graph, kruskal_mst)}")
        print(f"Prim's MST is valid: {SpanningTree.verify_mst(graph, prim_mst)}")
        
        # Test MST comparison
        print("\nMST comparison:")
        comparison = SpanningTree.compare_msts(kruskal_mst, prim_mst)
        print(f"Total weight difference: {comparison['total_weight_diff']}")
        print(f"Common edges: {comparison['common_edges']}")
        print(f"Average edge weight difference: {comparison['edge_weight_diff']}")
        
        # Test edge weight analysis
        print("\nEdge weight analysis:")
        analysis = SpanningTree.analyze_edge_weights(graph)
        print(f"Minimum weight: {analysis['min_weight']}")
        print(f"Maximum weight: {analysis['max_weight']}")
        print(f"Average weight: {analysis['avg_weight']}")
        print(f"Total weight: {analysis['total_weight']}")
        
        # Test error handling
        try:
            # Create a disconnected graph
            disconnected = UndirectedGraph()
            for i in range(3):
                disconnected.add_vertex(i)
            disconnected.add_edge(0, 1)
            
            print("\nTesting error handling:")
            SpanningTree.kruskal(disconnected)
        except GraphError as e:
            print(f"Expected error: {e}")
    
    test_spanning_tree()
