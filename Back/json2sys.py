import json
import uuid
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom

# 模块类型映射
module_type_map = {
    "node-A": "conveyor",
    "node-B": "transfer",
    "node-C": "lifter",
    "node-D": "shelf"
}

# 端口类型映射（事件端口）
event_port_map = {
    # 输送机 (A)
    "input-a": "ARRIVAL",
    "output-a": "DEPARTURE",
    # 移栽机 (B)
    "input-b": "ARRIVAL",
    "output-b1": "DEPARTURE1",
    "output-b2": "DEPARTURE2",
    "output-b3": "DEPARTURE3",
    # 提升机 (C)
    "input-c": "ARRIVAL",
    "output-c": "DEPARTURE",
    # 货架 (D)
    "input-d": "ARRIVAL",
    "output-d": "DEPARTURE"
}

# 端口类型映射（数据端口）
data_port_map = {
    # 输送机 (A)
    "input-a": "INPUT",
    "output-a": "OUTPUT",
    # 移栽机 (B)
    "input-b": "INPUT",
    "output-b1": "OUTPUT1",
    "output-b2": "OUTPUT2",
    "output-b3": "OUTPUT3",
    # 提升机 (C)
    "input-c": "INPUT",
    "output-c": "OUTPUT",
    # 货架 (D)
    "input-d": "INPUT",
    "output-d": "OUTPUT"
}

# 定义一个专门用于处理自定义模块端口的函数
def func(port, if_custom):
    """
    如果非自定义，直接获取映射；
    如果自定义，执行以下：
        1、将custom_port按'-'拆分
        2、按后缀数字生成事件端口和数据端口的名称
    """
    if not if_custom:
        # 非自定义模块
        return event_port_map.get(port), data_port_map.get(port)
    else:
        lst = port.split('-')
        port_id = int(lst[-1])+1
        if lst[0] == 'input':
            return f"ARRIVAL{port_id}", f"INPUT{port_id}"
        elif lst[0] == 'output':
            return f"DEPARTURE{port_id}", f"OUTPUT{port_id}"

def convert_json_to_xml(json_data):
    # 统计每种类型的模块数量
    type_count = defaultdict(int)
    
    # 创建 XML 根元素
    root = ET.Element("System")
    root.set("ID", str(uuid.uuid4()))
    root.set("Name", "workflow")
    root.set("Namespace", "flow")
    root.set("Version", "")
    root.set("IDEVersion", "v1.2.1")
    root.set("Comment", "System Function Block Type")
    
    # 添加 Identification
    identification = ET.SubElement(root, "Identification")
    identification.set("Standard", "61499-2")
    
    # 创建 Application 元素
    application = ET.SubElement(root, "Application")
    application.set("Name", "APPNAME")
    application.set("Comment", "")
    application.set("Key", str(uuid.uuid4()))
    
    # 创建 SubAppNetwork
    subapp_network = ET.SubElement(application, "SubAppNetwork")
    
    # 创建事件和数据连接容器
    event_connections = ET.SubElement(subapp_network, "EventConnections")
    data_connections = ET.SubElement(subapp_network, "DataConnections")
    
    # 处理节点
    node_map = {}
    cnt = 1 # 总计数
    # custom_cnt = 0 # 自定义模块计数
    custom_map = {}
    for node in json_data["nodes"]:
        # 获取模块类型
        node_type = module_type_map.get(node["type"])
        # 对于自定义模块
        custom = False        
        if not node_type:
            custom = True
            node_type = node["type"]
        
        # 更新类型计数并生成唯一名称
        # 自定义功能块的类型名与模块名完全分开，需要单独列出
        if custom:
            fb_type = node["data"]["label"]
            if not custom_map.get(node_type):
                custom_map[node_type] = fb_type
        
        type_count[node_type] += 1
        node_name = f"{node_type}_{type_count[node_type]:03d}"
        node_map[node["id"]] = node_name

        # 注册节点
        mapping = ET.SubElement(root, "Mapping")
        mapping.set("From", f"APPNAME.{node_name}")
        mapping.set("To", "")
        
        # 创建 FB 元素
        fb = ET.SubElement(subapp_network, "FB")
        fb.set("Key", f"-{cnt}")
        cnt += 1

        fb.set("Name", node_name)
        fb.set("Version", "")
        fb.set("Comment", "")
        if not custom:
            fb.set("Namespace", "flow")
            fb.set("Type", node_type)
        else:
            fb.set("Namespace", "ADDITIONAL")
            fb.set("Type", fb_type)
        
        # 设置位置（使用原始坐标）
        fb.set("x", str(int(node["position"]["x"])))
        fb.set("y", str(int(node["position"]["y"])))
    
    # print(node_map)

    # 处理边（连接）
    for edge in json_data["edges"]:
        source_node = node_map.get(edge["source"])
        target_node = node_map.get(edge["target"])
        custom = [
            'custom' in source_node,
            'custom' in target_node
        ]
        
        # 获取源端口和目标端口
        source_port = edge["sourceHandle"]
        target_port = edge["targetHandle"]

        source_event, source_data = func(source_port, custom[0])
        target_event, target_data = func(target_port, custom[1])
        
        # 创建事件连接
        if source_event and target_event:
            event_conn = ET.SubElement(event_connections, "Connection")
            event_conn.set("Source", f"{source_node}.{source_event}")
            event_conn.set("Destination", f"{target_node}.{target_event}")
            event_conn.set("dx1", "")
            event_conn.set("dx2", "")
            event_conn.set("dy", "")
            event_conn.set("Points", "")
            event_conn.set("Priority", "1")
        
        # 创建数据连接
        if source_data and target_data:
            data_conn = ET.SubElement(data_connections, "Connection")
            data_conn.set("Source", f"{source_node}.{source_data}")
            data_conn.set("Destination", f"{target_node}.{target_data}")
            data_conn.set("dx1", "")
            data_conn.set("dx2", "")
            data_conn.set("dy", "")
            data_conn.set("Points", "")
            data_conn.set("Priority", "")
    
    # 添加其他必要元素
    adapter_connections = ET.SubElement(subapp_network, "AdapterConnections")
    data_table = ET.SubElement(root, "DataTable")
    deploy_group = ET.SubElement(root, "DeployGroup")
    deploy_group.set("Key", "StartDeviceGroup")
    deploy_group.set("IsGroup", "true")
    deploy_group.set("Category", "deviceGroup")
    deploy_group.set("Size", "2100 100")
    
    # 创建 XML 树
    tree = ET.ElementTree(root)
    
    # 转换为格式化的 XML 字符串
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="    ")
    new_xml = pretty_xml.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>')

    # 添加 XML 声明
    return new_xml


if __name__ == "__main__":
    import sys
    
    # 解析 JSON 字符串
    json_data = json.loads(sys.argv[1])
    
    # 转换为 XML
    xml_output = convert_json_to_xml(json_data)
    
    # 直接输出 XML
    print(xml_output)