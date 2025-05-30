import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def plan_material_flow(m_lifters:list[int]):
    """
    规划货架到提升机的物料流路径
    :param m_lifters: 每个货架对应的提升机数量
    :return: (device_grid, connection_grid)
    """
    n_shelves = len(m_lifters)
    # 计算所需网格大小 (行数基于最大设备数，列数固定为5)
    rows = sum(m_lifters)
    cols = 5
    
    # 初始化设备栅格图 (字符表示)
    device_grid = np.full((rows, cols), ' ', dtype='U10')
    # 初始化连接栅格图 (字符表示方向)
    connection_grid = np.full((rows, cols), ' ', dtype='U10')

    step = 0
    for i in range(n_shelves):
        # 放置货架
        device_grid[step, 0] = 'S'
        connection_grid[step, 0] = '-' # 向右流动
        # 放置输送机1
        device_grid[step, 1] = 'C'
        connection_grid[step, 1] = '-'  # 向右流动
        for j in range(m_lifters[i]):
            # 放置提升机 (最右侧)
            device_grid[step+j, cols-1] = 'L'
            # 放置输送机2
            device_grid[step+j, 3] = 'C'
            connection_grid[step+j, 3] = '-'  # 向右流动
            # 放置移栽机
            device_grid[step+j, 2] = 'T'
            if m_lifters[i] == 1:
                connection_grid[step+j, 2] = '-'
            else:
                if j == 0:
                    connection_grid[step+j, 2] = 'T'
                elif j == m_lifters[i]-1:
                    connection_grid[step+j, 2] = 'L'
                else:
                    connection_grid[step+j, 2] = '+'
        step += m_lifters[i]
    
    return device_grid, connection_grid

def visualize_grids(device_grid, connection_grid):
    """
    可视化设备栅格图和连接栅格图
    """
    fig = plt.figure(figsize=(15, 8))
    gs = GridSpec(1, 2, width_ratios=[1, 1])
    
    # 设备栅格图
    ax1 = fig.add_subplot(gs[0])
    ax1.set_title("Function Blocks", fontsize=14)
    ax1.set_xticks(np.arange(-0.5, device_grid.shape[1], 1), minor=True)
    ax1.set_yticks(np.arange(-0.5, device_grid.shape[0], 1), minor=True)
    ax1.grid(which='minor', color='gray', linestyle='-', linewidth=1)
    ax1.tick_params(which='minor', size=0)
    
    # 添加设备标签
    for i in range(device_grid.shape[0]):
        for j in range(device_grid.shape[1]):
            if device_grid[i, j] != ' ':
                color = {
                    'S': 'lightgreen',    # 货架
                    'L': 'lightcoral',    # 提升机
                    'C': 'lightblue',     # 输送机
                    'T': 'violet'         # 移栽机
                }.get(device_grid[i, j], 'white')
                
                ax1.text(j, i, device_grid[i, j], 
                         ha='center', va='center', 
                         fontsize=12, fontweight='bold',
                         bbox=dict(boxstyle='round', facecolor=color, alpha=0.7))
    
    ax1.set_xlim(-0.5, device_grid.shape[1]-0.5)
    ax1.set_ylim(device_grid.shape[0]-0.5, -0.5)
    ax1.set_xticks(range(device_grid.shape[1]))
    ax1.set_yticks(range(device_grid.shape[0]))
    ax1.set_xticklabels([f"Col {i}" for i in range(device_grid.shape[1])])
    ax1.set_yticklabels([f"Row {i}" for i in range(device_grid.shape[0])])
    
    # 连接栅格图
    ax2 = fig.add_subplot(gs[1])
    ax2.set_title("Connections", fontsize=14)
    ax2.set_xticks(np.arange(-0.5, connection_grid.shape[1], 1), minor=True)
    ax2.set_yticks(np.arange(-0.5, connection_grid.shape[0], 1), minor=True)
    ax2.grid(which='minor', color='gray', linestyle='-', linewidth=1)
    ax2.tick_params(which='minor', size=0)
    
    # 添加方向箭头
    for i in range(connection_grid.shape[0]):
        for j in range(connection_grid.shape[1]):
            if connection_grid[i, j] != ' ':
                color = {
                    '-': 'red',
                    '+': 'green'
                }.get(connection_grid[i, j], 'black')
                
                ax2.text(j, i, connection_grid[i, j], 
                         ha='center', va='center', 
                         fontsize=14, fontweight='bold', color=color)
    
    ax2.set_xlim(-0.5, connection_grid.shape[1]-0.5)
    ax2.set_ylim(connection_grid.shape[0]-0.5, -0.5)
    ax2.set_xticks(range(connection_grid.shape[1]))
    ax2.set_yticks(range(connection_grid.shape[0]))
    ax2.set_xticklabels([f"Col {i}" for i in range(connection_grid.shape[1])])
    ax2.set_yticklabels([f"Row {i}" for i in range(connection_grid.shape[0])])
    
    plt.tight_layout()
    # plt.savefig('material_flow_grids.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    pass