// export function exportFlow(instance, onError) {
//   if (!instance) {
//     console.error('❌ VueFlow instance is required');
//     if (onError) onError('导出错误：画布未正确加载');
//     return;
//   }
//   try {
//     const flowData = instance.toObject();
//     const json = JSON.stringify(flowData, null, 2);
//     const blob = new Blob([json], { type: 'application/json' });
//     const url = URL.createObjectURL(blob);
//     const a = document.createElement('a');
//     a.href = url;
//     a.download = 'flow.json';
//     a.click();
//     URL.revokeObjectURL(url);
//   } catch (error) {
//     console.error('❌ 导出失败', error);
//     if (onError) onError('导出错误：无法导出流程');
//   }
// }

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

// 导入函数
export function importFlow(instance, event, onError) {
  if (!instance) {
    console.error('❌ VueFlow instance is required');
    if (onError) onError('导入错误：画布未正确加载');
    return;
  }

  const fileInput = event.target;
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      try {
        const content = e.target.result;
        const data = JSON.parse(content);
        instance.setNodes(data.nodes || []);
        instance.setEdges(data.edges || []);
        if (data.viewport) {
          instance.setViewport(data.viewport);
        }
      } catch (error) {
        console.error('❌ 导入失败: 无效的 JSON 文件', error);
        if (onError) onError('导入错误：请确保选择有效的 JSON 文件');
      } finally {
        fileInput.value = '';
      }
    };
    reader.readAsText(file);
  }
}