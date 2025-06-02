import sys
import json
from utils.level_planner import plan_3d_flow
from utils.level_exporter import grids_to_flow_2

"""
与后端交互，接收数据，生成栅格图
"""

class Parser:
    """
    将字符串解析为数组
    """
    def __init__(self, s):
        self.s = s
        self.index = 0

    def parse_list(self):
        """Parse a nested list starting with '(' and ending with ')'."""
        assert self.s[self.index] == '(', "Expected '('"
        self.index += 1  # Skip '('
        result = []
        
        while self.index < len(self.s) and self.s[self.index] != ')':
            if self.s[self.index].isdigit():
                num = self.parse_number()
                result.append(num)
            elif self.s[self.index] == '(':
                sub_list = self.parse_list()
                result.append(sub_list)
            else:
                raise ValueError(f"Unexpected character '{self.s[self.index]}' at position {self.index}")
            
            # Skip comma if present
            if self.index < len(self.s) and self.s[self.index] == ',':
                self.index += 1
        
        assert self.s[self.index] == ')', "Expected ')'"
        self.index += 1  # Skip ')'
        return result

    def parse_number(self):
        """Parse a number from the current position."""
        start = self.index
        while self.index < len(self.s) and self.s[self.index].isdigit():
            self.index += 1
        num_str = self.s[start:self.index]
        return int(num_str)

def parse_nested_list(s):
    """Convert a string representation of a nested list into a Python list."""
    parser = Parser(s)
    return parser.parse_list()


if __name__ == "__main__":
    # 解析输入
    n_outputs = json.loads(sys.argv[1])
    if isinstance(n_outputs, str):
        n_outputs = parse_nested_list(n_outputs)
    # 规划物料流路径
    device_grid, connection_grid = plan_3d_flow(n_outputs)
    # 生成json并输出
    flow_data = grids_to_flow_2(device_grid, connection_grid)
    print(json.dumps(flow_data))
