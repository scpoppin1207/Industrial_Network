import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def plan_3d_flow(n_outputs:list[list[int]]):
    """
    规划货架到提升机的物料流路径
    :param n_outputs: [[n1,n2],...]表示每个货架在各层的出货口（货架）数量
    :return: (device_grid, connection_grid)
    """
    n_shelves = len(n_outputs)
    # 计算所需网格大小 (行数基于输出设备数)，一层5列，每多一层就加4列
    cnt, rows = 1, 0
    for x in n_outputs:
        rows += sum(x)
        cnt = max(cnt, len(x))
    cols = 5 + 4*(cnt-1)
    
    # 初始化设备栅格图 (字符表示)
    device_grid = np.full((rows, cols), ' ', dtype='U10')
    # 初始化连接栅格图 (字符表示方向)
    connection_grid = np.full((rows, cols), ' ', dtype='U10')

    row_step = 0
    for i in range(n_shelves):
        # 放置货架
        device_grid[row_step, 0] = 'S'+'_1'
        connection_grid[row_step, 0] = '-' # 向右流动
        # 放置输送机1
        device_grid[row_step, 1] = 'C'+'_1'
        connection_grid[row_step, 1] = '-'  # 向右流动

        lst = n_outputs[i]
        n_levels = len(lst) # 当前货架需要运到的层数
        col_step = 0
        for j in range(n_levels): # 所处的层数
            n_dst = lst[j] # 本层的分发数
            # 1、若处在最后一层，维持原分发数
            # 2、若不为最后一层，分发数加1（提升至下一层）
            if j != n_levels-1:
                n_dst += 1

            for k in range(n_dst):
                # 放置输送机2
                device_grid[row_step+k, col_step+3] = 'C'+f'_{j+1}'
                connection_grid[row_step+k, col_step+3] = '-'  # 向右流动
                # 放置移栽机
                device_grid[row_step+k, col_step+2] = 'T'+f'_{j+1}'
                # 移栽机的连接方式
                # 1、当前货架/提升机仅有一排且为最后一层：-
                # 2、当前货架/提升机的第一排且有多排：T
                # 3、移栽机与提升机连接处/多排中的最后一排：L
                # 4、其他情况：+
                if (j == n_levels-1 or lst[j]==0) and n_dst == 1:
                    connection_grid[row_step+k, col_step+2] = '-'
                else:
                    if k == 0:
                        connection_grid[row_step+k, col_step+2] = 'T'
                    elif k == n_dst-1:
                        connection_grid[row_step+k, col_step+2] = 'L'
                    else:
                        connection_grid[row_step+k, col_step+2] = '+'
                # 放置货架或提升机
                # 1、若当前处在本层的最后一排且有下一层：提升机，附带接上下一层的根输送机
                # 2、其他情况：货架
                if k == n_dst-1 and j != n_levels-1:
                    device_grid[row_step+k, col_step+4] = 'L'+f'_{j+1}'
                    connection_grid[row_step+k, col_step+4] = '-'
                    device_grid[row_step+k, col_step+5] = 'C'+f'_{j+2}'
                    connection_grid[row_step+k, col_step+5] = '-'
                    # 更新col_step，接到刚刚安放的提升机之后
                    col_step += 4
                else:
                    device_grid[row_step+k, col_step+4] = 'S'+f'_{j+1}'
            # 更新row_step，接到最后最后一行
            row_step += lst[j]
    
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


# 主程序
if __name__ == "__main__":
    n_outputs = [[2,1],[1,2,1],[1]]
    dg, cg = plan_3d_flow(n_outputs)
    visualize_grids(dg, cg)