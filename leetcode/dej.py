from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        grid_min_sum = [[] for _ in range(len(grid))]
        grid_min_sum[0].append(grid[0][0])
        for i  in range(len(grid)):

            for j in range(0, len(grid[0])):
                if i == j == 0:
                    continue
                if i == 0:
                    grid_min_sum[i].append(grid_min_sum[0][j-1] + grid[0][j])
                elif j == 0:
                    grid_min_sum[i].append(grid_min_sum[i-1][0] + grid[i][j])
                else:
                    grid_min_sum[i].append(min(grid_min_sum[i][j-1], grid_min_sum[i-1][j]) + grid[i][j])
                


        return grid_min_sum[-1][-1]