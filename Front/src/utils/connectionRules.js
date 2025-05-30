// utils/connectionRules.js

/**
 * 检查连接是否符合以下规则：
 * 1. 不允许连接节点自身
 * 2. 一个输入口只能连接一次
 * 3. 一个输出口只能连接一次
 * 4. 连接必须是输出口 → 输入口
 * 
 * @param {Object} params - 连接参数（来自 onConnect）
 * @param {Array} edges - 当前边列表
 * @param {Array} nodes - 当前节点列表
 * @returns {Object} { valid: boolean, reason: string }
 */
export function validateConnection(params, edges, nodes) {
  const { source, sourceHandle, target, targetHandle } = params

  if (source === target) {
    return { valid: false, reason: '❌ 不能连接节点自身' ,code: '别他妈自己连自己！'}
  }

  const isTargetHandleUsed = edges.some(
    (e) => e.target === target && e.targetHandle === targetHandle
  )
  if (isTargetHandleUsed) {
    return { valid: false, reason: '❌ 输入口已被连接' ,code: '别他妈连已连接的输入口！'}
  }

  const isSourceHandleUsed = edges.some(
    (e) => e.source === source && e.sourceHandle === sourceHandle
  )
  if (isSourceHandleUsed) {
    return { valid: false, reason: '❌ 输出口已被连接' ,code: '别他妈连已连接的输出口！'}
  }

  const sourceNode = nodes.find((n) => n.id === source)
  const targetNode = nodes.find((n) => n.id === target)

  const sourceIsOutput = sourceNode?.data?.outputs?.includes(sourceHandle)
  const targetIsInput = targetNode?.data?.inputs?.includes(targetHandle)

  if (!sourceIsOutput || !targetIsInput) {
    return { valid: false, reason: '❌ 连接错误：必须从输出口连接到输入口', code: '必须从输出口连接到输入口,你傻逼啊！' }
  }

  return { valid: true }
}