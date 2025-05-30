export function exportFlow(instance, onError) {
  if (!instance) {
    console.error('❌ VueFlow instance is required');
    if (onError) onError('导出错误：画布未正确加载');
    return;
  }
  try {
    const flowData = instance.toObject();
    const json = JSON.stringify(flowData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'flow.json';
    a.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('❌ 导出失败', error);
    if (onError) onError('导出错误：无法导出流程');
  }
}

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