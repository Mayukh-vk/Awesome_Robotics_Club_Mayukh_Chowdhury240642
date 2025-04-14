## Path Planning Approach
We use a simplified Dijkstra Algorithm.A Dijkstra Algorithm basically works as follows:We keep calculating distances from a fixed vertex to another vertex .We keep updating the distance with the least distance found yet.We maintain two arrrays of visited and unvisited vertices , and then keep transferrinf vertices one by one from unvisited to visited array.
### How It Works
1. User enters the grid size and grid data.
2. The program finds the start and goal points.
3. Dijkstra's logic checks the cheapest way to reach each cell.
4. After reaching the goal, the path is reconstructed using parent pointers.
5. Outputs both the **step-by-step path** and the **total path cost**.
