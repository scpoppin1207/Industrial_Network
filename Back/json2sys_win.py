import sys
import json
import os
import re
import uuid
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert_json_to_xml(json_data):
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
    for node in json_data["nodes"]:
        # 获取模块类型
        node_type = module_type_map.get(node["type"])
        if not node_type:
            continue
        
        # 更新类型计数并生成唯一名称
        type_count[node_type] += 1
        node_name = f"{node_type}_{type_count[node_type]:03d}"
        node_map[node["id"]] = node_name

        # 注册节点
        mapping = ET.SubElement(root, "Mapping")
        mapping.set("From", f"APPNAME.{node_name}")
        mapping.set("To", "")
        
        # 创建 FB 元素
        fb = ET.SubElement(subapp_network, "FB")
        # fb.set("Key", f"-{type_count[node_type]}")
        fb.set("Key", f"-{cnt}")
        cnt += 1

        fb.set("Name", node_name)
        fb.set("Namespace", "flow")
        fb.set("Version", "")
        fb.set("Comment", "")
        fb.set("Type", node_type)
        
        # 设置位置（使用原始坐标）
        fb.set("x", str(int(node["position"]["x"])))
        fb.set("y", str(int(node["position"]["y"])))
    
    # 处理边（连接）
    for edge in json_data["edges"]:
        source_node = node_map.get(edge["source"])
        target_node = node_map.get(edge["target"])
        
        if not source_node or not target_node:
            continue
        
        # 获取源端口和目标端口
        source_port = edge["sourceHandle"]
        target_port = edge["targetHandle"]
        
        # 获取事件端口名称
        source_event = event_port_map.get(source_port)
        target_event = event_port_map.get(target_port)
        
        # 获取数据端口名称
        source_data = data_port_map.get(source_port)
        target_data = data_port_map.get(target_port)
        
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python json2sys.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        # 从文件读取JSON数据
        with open(input_file, 'r') as f:
            flow_data = json.load(f)
        
        # 原有转换逻辑...
        xml_output = convert_json_to_xml(flow_data)
        
        # 输出结果
        print(xml_output)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()