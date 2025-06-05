import json
import uuid
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import sys

type_map = {
    'string':'WSTRING',
    'number':'INT',
    'bool':'BOOL'
}

def generate_fb_type(json_data):
    """根据JSON数据生成功能块XML结构"""
    fb_name = json_data.get("name", "GeneratedFB").replace(" ", "_")
    
    # 创建根元素
    fb_type = Element('FBType')
    fb_type.set('ID', str(uuid.uuid4()))
    fb_type.set('Name', fb_name)
    fb_type.set('Namespace', 'ADDITIONAL')
    fb_type.set('Version', '')
    fb_type.set('IDEVersion', 'v1.2.1')
    fb_type.set('Comment', f'Auto-generated from {json_data.get("name", "N/A")}')
    
    # 添加Identification
    identification = SubElement(fb_type, 'Identification')
    identification.set('Standard', '61499-2')
    
    # 创建接口列表
    interface_list = SubElement(fb_type, 'InterfaceList')

    # 遍历输入与输出，挨个绑定事件与数据输入/输出
    # 处理输入
    event_inputs = SubElement(interface_list, 'EventInputs')
    input_vars = SubElement(interface_list, 'InputVars')
    for i, input_port in enumerate(json_data.get('inputs', []), 1):
        event_name = f"ARRIVAL{i}"
        material_name = f"INPUT{i}"
        # 创建输入事件
        start_event = SubElement(event_inputs, 'Event')
        start_event.set('Key', str(uuid.uuid4()))
        start_event.set('Name', event_name)
        start_event.set('Type', 'EVENT')
        # 创建输入变量
        var_decl = SubElement(input_vars, 'VarDeclaration')
        var_decl.set('Name', material_name)
        var_decl.set('Type', 'INT')
        var_decl.set('ArraySize', '1')
        var_decl.set('Temp', 'false')
        var_decl.set('Key', str(uuid.uuid4()))
        # 将输入变量绑定到事件
        bind = SubElement(start_event, 'With')
        bind.set('Var', material_name)

    # 处理输出
    event_outputs = SubElement(interface_list, 'EventOutputs')
    output_vars = SubElement(interface_list, 'OutputVars')
    for i, output_port in enumerate(json_data.get('outputs', []), 1):
        event_name = f"DEPARTURE{i}"
        material_name = f"OUTPUT{i}"
        # 创建输出事件
        end_event = SubElement(event_outputs, 'Event')
        end_event.set('Key', str(uuid.uuid4()))
        end_event.set('Name', event_name)
        end_event.set('Type', 'EVENT')
        # 创建输出变量
        var_decl = SubElement(output_vars, 'VarDeclaration')
        var_decl.set('Name', material_name)
        var_decl.set('Type', 'INT')
        var_decl.set('ArraySize', '1')
        var_decl.set('Temp', 'false')
        var_decl.set('Key', str(uuid.uuid4()))
        # 将输出变量绑定到事件
        bind = SubElement(end_event, 'With')
        bind.set('Var', material_name)
    
    # 内部变量
    basic_fb = SubElement(fb_type, 'BasicFB')
    internal_vars = SubElement(basic_fb, 'InternalVars')
    
    # 添加通用内部变量
    for var_name in ['FAULT', 'END']:
        var_decl = SubElement(internal_vars, 'VarDeclaration')
        var_decl.set('Name', var_name)
        var_decl.set('Type', 'BOOL')
        var_decl.set('ArraySize', '1')
        var_decl.set('Temp', 'false')
        var_decl.set('Key', str(uuid.uuid4()))
    
    # 添加属性作为内部变量
    for prop in json_data.get('properties', []):
        var_decl = SubElement(internal_vars, 'VarDeclaration')
        var_decl.set('Name', prop['name'])
        # 默认为INT类型
        var_decl.set('Type', type_map.get(prop['type'], 'INT'))
        var_decl.set('ArraySize', '1')
        var_decl.set('Temp', 'false')
        var_decl.set('Key', str(uuid.uuid4()))
        # if 'default' in prop:
            # var_decl.set('InitialValue', str(prop['default']))
    
    # 执行控制图 (ECC)
    ecc = SubElement(basic_fb, 'ECC')
    
    # 状态定义
    states = {
        'START': SubElement(ecc, 'ECState'),
        'WORKING': SubElement(ecc, 'ECState'),
        'SHUT': SubElement(ecc, 'ECState')
    }
    
    # 设置状态属性
    states['START'].set('Key', '1')
    states['START'].set('Name', 'START')
    states['START'].set('x', '0')
    states['START'].set('y', '0')
    
    states['WORKING'].set('Key', '2')
    # states['WORKING'].set('Name', json_data['state_machine']['working_state'])
    states['WORKING'].set('Name', 'WORKING')
    states['WORKING'].set('x', '200')
    states['WORKING'].set('y', '200')
    
    states['SHUT'].set('Key', '-1')
    states['SHUT'].set('Name', 'SHUT')
    states['SHUT'].set('x', '400')
    states['SHUT'].set('y', '0')
    
    # 算法定义
    algorithm = SubElement(basic_fb, 'Algorithm')
    algorithm.set('Key', str(uuid.uuid4()))
    algorithm.set('Name', json_data['state_machine']['algorithm'])
    algorithm.set('Type', 'ST')
    st = SubElement(algorithm, 'ST')
    # st.text = f"(* {json_data['state_machine']['algorithm']} implementation *)"
    st.set('Text', '')

    # 添加工作状态的动作：有多少输出端口就复制多少算法
    for i, output_port in enumerate(json_data.get('outputs', []), 1):
        event_name = f"DEPARTURE{i}"

        action = SubElement(states['WORKING'], 'ECAction')
        action.set('Algorithm', json_data['state_machine']['algorithm'])
        action.set('Output', event_name)
    
    # 状态转移
    transitions = [
        ('START', 'WORKING', ''),
        ('WORKING', 'START', '[END]'),
        ('WORKING', 'SHUT', '[FAULT]')
    ]
    # START到WORKING有多少输入端口就有多少转法
    for src, dest, cond in transitions:
        if src == 'START' and dest == 'WORKING':
            for i, input_port in enumerate(json_data.get('inputs', []), 1):
                _cond = f"ARRIVAL{i}"
                trans = SubElement(ecc, 'ECTransition')
                trans.set('Source', src)
                trans.set('Destination', dest)
                trans.set('Condition', _cond)
        else:
            trans = SubElement(ecc, 'ECTransition')
            trans.set('Source', src)
            trans.set('Destination', dest)
            trans.set('Condition', cond)


    return fb_type

def prettify(elem):
    """将XML元素转换为格式化的字符串"""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_fb_from_json(json_file):
    """从JSON文件生成功能块XML文本"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fb_type = generate_fb_type(data)
    xml_str = prettify(fb_type)
    
    # 添加XML声明
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_content = xml_declaration + '\n' + xml_str.split('?>', 1)[-1].lstrip()
    return xml_content

if __name__ == "__main__":
    input_file = sys.argv[1]    
    try:
        xml_output = generate_fb_from_json(input_file)
        # 输出结果
        print(xml_output)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)