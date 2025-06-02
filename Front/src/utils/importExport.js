// 新的导出函数（to .sys）
export function exportFlow(instance, onError, convertToSys = false) {
  if (!instance) {
    console.error('❌ VueFlow instance is required');
    if (onError) onError('导出错误：画布未正确加载');
    return;
  }
  
  try {
    const flowData = instance.toObject();
    
    if (convertToSys) {
      // 将数据发送到后端进行转换
      fetch('/api/convert-to-sys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(flowData)
      })
      .then(response => {
        if (!response.ok) throw new Error('转换失败');
        return response.blob();
      })
      .then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'workflow.sys';
        a.click();
        URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('❌ 转换失败', error);
        if (onError) onError('转换错误：无法生成SYS文件');
      });
    } else {
      // 直接导出 JSON
      const json = JSON.stringify(flowData, null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'flow.json';
      a.click();
      URL.revokeObjectURL(url);
    }
  } catch (error) {
    console.error('❌ 导出失败', error);
    if (onError) onError('导出错误：无法导出流程');
  }
}

// 导入函数, 原版
// export function importFlow(instance, event, onError) {
//   if (!instance) {
//     console.error('❌ VueFlow instance is required');
//     if (onError) onError('导入错误：画布未正确加载');
//     return;
//   }

//   const fileInput = event.target;
//   const file = fileInput.files[0];
//   if (file) {
//     const reader = new FileReader();
//     reader.onload = function (e) {
//       try {
//         const content = e.target.result;
//         const data = JSON.parse(content);
//         instance.setNodes(data.nodes || []);
//         instance.setEdges(data.edges || []);
//         if (data.viewport) {
//           instance.setViewport(data.viewport);
//         }
//       } catch (error) {
//         console.error('❌ 导入失败: 无效的 JSON 文件', error);
//         if (onError) onError('导入错误：请确保选择有效的 JSON 文件');
//       } finally {
//         fileInput.value = '';
//       }
//     };
//     reader.readAsText(file);
//   }
// }

/**
 * 导入流程：只负责读取 JSON 文件并 parse，读完后把 data 对象交给回调
 * 
 * @param {Event} event     原生 <input type="file" @change="..." /> 触发的事件
 * @param {(data:{nodes:Array, edges:Array, viewport?:Object})=>void} onSuccess  成功后回调，参数是解析好的 flowData
 * @param {(errMsg:string)=>void} onError       失败时回调，带一个错误提示
 */
export function importFlow(event, onSuccess, onError) {
  const fileInput = event.target;
  const file = fileInput.files[0];
  if (!file) {
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const text = e.target.result;
      const data = JSON.parse(text);

      // 最低限度校验一下格式：必须有 nodes 和 edges
      if (!data.nodes || !Array.isArray(data.nodes) || !data.edges || !Array.isArray(data.edges)) {
        throw new Error('无效的 JSON 结构：必须包含 nodes/edges 数组');
      }

      // 走到这说明 JSON 正确
      if (onSuccess) {
        onSuccess(data);
      }
    } catch (err) {
      console.error('❌ 导入失败: 无效的 JSON 文件', err);
      if (onError) onError('导入错误：请确保选择有效的 JSON 文件');
    } finally {
      // 清空 input 的值，以便下次选同一个文件也能触发 onChange
      fileInput.value = '';
    }
  };

  reader.readAsText(file);
}