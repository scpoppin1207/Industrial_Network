import random
import string

# 设备映射表：输送机===A, 移栽机===B, 提升机===C
reference = {}
reference['C'] = 'A'
reference['T'] = 'B'
reference['L'] = 'C'
reference['S'] = 'D'

def generate_random_id(prefix, length=10):
    """根据工件前缀映射到reference，并生成随机ID"""
    if prefix in ['C', 'T', 'L', 'S']:
        return f"{reference[prefix]}-{''.join(random.choices(string.digits, k=length))}"
    return f"{reference}-{''.join(random.choices(string.digits, k=length))}"
    

def grids_to_flow(device_grid, connection_grid):
    """将设备栅格图和连接栅格图转换为example.json格式"""
    # 初始化数据结构
    flow_data = {
        "nodes": [],
        "edges": [],
        "position": [0, 0],
        "zoom": 1.0,
        "viewport": {"x": 0, "y": 0, "zoom": 1.0}
    }
    
    # 节点映射表: (row, col) -> node_id
    node_map = {}
    
    # 1. 创建节点
    for row in range(device_grid.shape[0]):
        for col in range(device_grid.shape[1]):
            device_type = device_grid[row, col]
            if device_type == ' ':  # 忽略空格
                continue
                
            # 根据设备类型确定节点类型和标签
            node_type = f"node-{reference[device_type]}"
            label = {
                'C': '模块 A',
                'T': '模块 B',
                'L': '模块 C',
                'S': '模块 D'
            }.get(device_type, device_type)
            
            # 创建节点
            node_id = generate_random_id(device_type)
            node_map[(row, col)] = node_id
            
            # 根据设备类型设置输入输出端口和处理点
            inputs = []
            outputs = []
            handles = []
            
            if device_type == 'C':  # 输送机
                inputs = ["input-a"]
                outputs = ["output-a"]
                handles = [
                    {"position": "left", "id": "input-a", "type": "target"},
                    {"position": "right", "id": "output-a", "type": "source"}
                ]
            elif device_type == 'T':  # 移栽机
                inputs = ["input-b"]
                outputs = ["output-b1", "output-b2", "output-b3"]
                handles = [
                    {"position": "left", "id": "input-b", "type": "target"},
                    {"position": "left", "id": "output-b1", "type": "source"},
                    {"position": "right", "id": "output-b2", "type": "source"},
                    {"position": "bottom", "id": "output-b3", "type": "source"}
                ]
            elif device_type == 'L':  # 提升机
                inputs = ["input-c"]
                outputs = []
                handles = [
                    {"position": "top", "id": "input-c", "type": "target"}
                ]
            elif device_type == 'S': # 货架
                inputs = ["input-d"]
                outputs = ["output-d"]
                handles = [
                    {"position": "left", "id": "input-d", "type": "target"},
                    {"position": "right", "id": "output-d", "type": "source"}
                ]
            
            flow_data["nodes"].append({
                "id": node_id,
                "type": node_type,
                "draggable": True,
                "connectable": True,
                "initialized": False,
                "position": {
                    "x": col * 500,  # 水平位置
                    "y": row * 400   # 垂直位置
                },
                "data": {
                    "label": label,
                    "inputs": inputs,
                    "outputs": outputs,
                    "style": {"background": "#fff", "padding": "3px", "borderRadius": "20px"},
                    "rotate": 0,
                    "translate": [0, 0],
                    "dimensions": {"width": None, "height": None}
                },
                "handles": handles,
                "dragHandle": f"[data-moveable-id='{node_id}']"
            })
    
    # 2. 创建连接边
    for row in range(connection_grid.shape[0]):
        for col in range(connection_grid.shape[1]):
            conn_type = connection_grid[row, col]
            if conn_type == ' ':
                continue
                
            current_node = node_map.get((row, col))
            if not current_node:
                continue
            
            # 根据连接类型确定连接方向
            if conn_type in ['-', 'T', '+', 'L']:  # 向右连接
                if col + 1 < device_grid.shape[1]:
                    right_node = node_map.get((row, col + 1))
                    if right_node:
                        # 确定源端口
                        if device_grid[row, col] == 'C':
                            source_handle = "output-a"
                        elif device_grid[row, col] == 'T':
                            source_handle = "output-b3"
                        elif device_grid[row, col] == 'S':
                            source_handle = "output-d"
                        
                        # 确定目标端口
                        if device_grid[row, col+1] == 'C':
                            target_handle = "input-a"
                        elif device_grid[row, col+1] == 'T':
                            target_handle = "input-b"
                        elif device_grid[row, col+1] == 'L':
                            target_handle = "input-c"
                        elif device_grid[row, col+1] == 'S':
                            target_handle = "input-d"
                        
                        # 创建连接
                        edge_id = generate_random_id("edge")
                        flow_data["edges"].append({
                            "id": edge_id,
                            "type": "default",
                            "source": current_node,
                            "target": right_node,
                            "sourceHandle": source_handle,
                            "targetHandle": target_handle,
                            "data": {},
                            "label": "",
                            "animated": True,
                            "style": {"stroke": "#674ea7", "strokeWidth": 5},
                            "markerEnd": {"type": "arrowclosed", "color": "#674ea7"}
                        })
            
            if conn_type in ['T', '+']:  # 向下连接
                if row + 1 < device_grid.shape[0]:
                    down_node = node_map.get((row + 1, col))
                    if down_node:
                        # 确定源端口
                        if device_grid[row, col] == 'C':
                            source_handle = "output-a"
                        elif device_grid[row, col] == 'T':
                            source_handle = "output-b2"
                        elif device_grid[row, col] == 'S':
                            source_handle = "output-d"
                        
                        # 确定目标端口
                        if device_grid[row+1, col] == 'C':
                            target_handle = "input-a"
                        elif device_grid[row+1, col] == 'T':
                            target_handle = "input-b"
                        elif device_grid[row+1, col] == 'L':
                            target_handle = "input-c"
                        elif device_grid[row+1, col] == 'S':
                            target_handle = "input-d"
                        
                        # 创建连接
                        edge_id = generate_random_id("edge")
                        flow_data["edges"].append({
                            "id": edge_id,
                            "type": "default",
                            "source": current_node,
                            "target": down_node,
                            "sourceHandle": source_handle,
                            "targetHandle": target_handle,
                            "data": {},
                            "label": "",
                            "animated": True,
                            "style": {"stroke": "#674ea7", "strokeWidth": 5},
                            "markerEnd": {"type": "arrowclosed", "color": "#674ea7"}
                        })
    
    return flow_data

# 主程序
if __name__ == "__main__":
    pass