import sys
import json
from utils.planner import plan_material_flow
from utils.js_exporter import grids_to_flow

"""
与后端交互，接收数据，生成栅格图
"""

if __name__ == "__main__":
    m_lifters = json.loads(sys.argv[1])
    # 规划物料流路径
    device_grid, connection_grid = plan_material_flow(m_lifters)
    # 生成json并输出
    flow_data = grids_to_flow(device_grid, connection_grid)
    print(json.dumps(flow_data))
