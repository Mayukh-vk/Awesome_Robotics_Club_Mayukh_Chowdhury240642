#include <iostream>
using namespace std;

const int MAX = 100; // Max size for safety
char grid[MAX][MAX];
int visited[MAX][MAX];
int cost[MAX][MAX];
int parentRow[MAX][MAX];
int parentCol[MAX][MAX];

int dr[4] = {-1, 1, 0, 0}; // Up, Down, Left, Right
int dc[4] = {0, 0, -1, 1};

int ROWS, COLS;

int getCost(char ch) {
    if (ch == '.') return 1;
    if (ch == '~') return 3;
    if (ch == '^') return 5;
    if (ch == 'S' || ch == 'G') return 0;
    return -1;
}

void printPath(int sr, int sc, int gr, int gc) {
    int pathRow[MAX * MAX], pathCol[MAX * MAX];
    int length = 0;
    int r = gr, c = gc;
    int totalCost = 0;

    while (!(r == sr && c == sc)) {
        pathRow[length] = r;
        pathCol[length] = c;
        totalCost += getCost(grid[r][c]);
        int pr = parentRow[r][c];
        int pc = parentCol[r][c];
        r = pr;
        c = pc;
        length++;
    }

    pathRow[length] = sr;
    pathCol[length] = sc;
    length++;

    cout << "Step-by-step path (row, col):" << endl;
    for (int i = length - 1; i >= 0; i--) {
        cout << "(" << pathRow[i] << ", " << pathCol[i] << ")" << endl;
    }

    cout << "Total path cost: " << totalCost << endl;
}

void dijkstra(int sr, int sc, int gr, int gc) {
    const int INF = 1e9;

    for (int i = 0; i < ROWS; i++)
        for (int j = 0; j < COLS; j++) {
            cost[i][j] = INF;
            visited[i][j] = 0;
        }

    cost[sr][sc] = 0;

    while (true) {
        int minCost = INF, r = -1, c = -1;

        for (int i = 0; i < ROWS; i++)
            for (int j = 0; j < COLS; j++)
                if (!visited[i][j] && cost[i][j] < minCost) {
                    minCost = cost[i][j];
                    r = i;
                    c = j;
                }

        if (r == -1) break;
        if (r == gr && c == gc) break;

        visited[r][c] = 1;

        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d];
            int nc = c + dc[d];

            if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && grid[nr][nc] != '#') {
                int newCost = cost[r][c] + getCost(grid[nr][nc]);

                if (newCost < cost[nr][nc]) {
                    cost[nr][nc] = newCost;
                    parentRow[nr][nc] = r;
                    parentCol[nr][nc] = c;
                }
            }
        }
    }

    if (cost[gr][gc] == INF) {
        cout << "No path found." << endl;
    } else {
        printPath(sr, sc, gr, gc);
    }
}

int main() {
    cout << "Enter number of rows and columns: ";
    cin >> ROWS >> COLS;

    int sr = 0, sc = 0, gr = 0, gc = 0;

    cout << "Enter the grid row by row:" << endl;
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            cin >> grid[i][j];
            if (grid[i][j] == 'S') {
                sr = i;
                sc = j;
            }
            if (grid[i][j] == 'G') {
                gr = i;
                gc = j;
            }
        }
    }

    dijkstra(sr, sc, gr, gc);
    return 0;
}

