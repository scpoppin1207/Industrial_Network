// backend/server.js

const express = require('express')
const axios = require('axios')
const { spawn } = require('child_process') // 用于调用Python脚本
const fs = require('fs') // 用于文件操作
const path = require('path') // 用于处理文件路径

const app = express()
const PORT = 3000

app.use(express.json())

// ✅ 替换成你自己的 API Key 和 endpoint
const API_URL = 'https://maas-cn-east-4.modelarts-maas.com/v1/infers/5f114f77-65c2-4e79-82df-d84b25b89d42/v1/chat/completions'
const API_KEY = 'vWUQVo7N1__ZejNJj7JKIeXVKRele2xY1sIOe8hxtsvDsU0PFNQtEKJCJWlRbD9LUwbx1kJvTc7iO4k416kzYg' // <- 替换成你自己的

// 调用Python脚本的函数
function runPythonScript(scriptName, args, callback) {
  const pythonProcess = spawn('python', [scriptName, ...args])
  
  let output = ''
  let errorOutput = ''
  
  pythonProcess.stdout.on('data', (data) => {
    output += data.toString()
  })
  
  pythonProcess.stderr.on('data', (data) => {
    errorOutput += data.toString()
  })
  
  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python脚本 ${scriptName} 执行失败: ${errorOutput}`)
      callback(new Error(`Python脚本执行失败，退出代码: ${code}`), null)
    } else {
      callback(null, output)
    }
  })
}

app.post('/api/dialog', async (req, res) => {
  const { content } = req.body

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`,
  }

  const data = {
    model: 'Qwen2.5-72B-32K',
    messages: [
      { 
        role: 'system', 
        content: '你是一个仓储运输设计者。你接收到一段仓储设计的需求后，从中提炼出以下两个信息： \
        总共有几个源头货架；每个源头货架对应几个目标货架；用数组来回答。比如你提炼出来总共用3个源头货架，分别有3个、1个、10个目的货架，你就返回(3,1,10)。只用回答数组，其他的什么都不用回答。' 
      },
      { role: 'user', content }
    ],
    stream: false,
    temperature: 0
  }

  try {
    const response = await axios.post(API_URL, data, { headers })
    const reply = response.data.choices[0].message.content
    
    // 1. 解析LLM返回的数组
    // 尝试从回复中提取数字数组
    const arrayMatch = reply.match(/\(([\d,\s]+)\)|\[([\d,\s]+)\]/)
    if (!arrayMatch) {
      throw new Error('无法从LLM回复中解析数组')
    }
    
    // 提取匹配到的数组字符串（可能是第一个或第二个捕获组）
    const arrayStr = arrayMatch[1] || arrayMatch[2]
    const numbers = arrayStr.split(',').map(num => parseInt(num.trim()))
    
    console.log(`✅ 解析到的提升机数量数组: [${numbers}]`)
    
    // 2. 调用js_gen.py生成json
    runPythonScript('js_gen.py', [JSON.stringify(numbers)], (error, jsonOutput) => {
      if (error) {
        console.error('生成JSON失败:', error.message)
        return res.status(500).json({ error: '生成JSON失败' })
      }   
  
      try {
        // 解析js_gen.py的输出
        const flowJson = JSON.parse(jsonOutput)
        console.log('✅ JSON数据生成成功')
        
        // 4. 返回结果给前端
        res.json({ 
          reply, 
          flow: flowJson 
        })
      } catch (parseError) {
        console.error('解析JSON数据失败:', parseError)
        res.status(500).json({ error: '解析JSON数据失败' })
      }
    })
  } catch (error) {
    console.error('请求LLM失败:', error.message)
    res.status(500).json({ reply: 'LLM请求失败' })
  }
})

app.listen(PORT, () => {
  console.log(`✅ 后端服务器运行中：http://localhost:${PORT}`)
})


// 添加新的路由处理 SYS 转换
app.post('/api/convert-to-sys', async (req, res) => {
  const flowData = req.body;
  
  try {
    // 调用 Python 转换脚本
    const xmlOutput = await runPythonConversion(flowData);
    
    // 设置正确的响应头
    res.setHeader('Content-Type', 'application/xml');
    res.setHeader('Content-Disposition', 'attachment; filename="workflow.sys"');
    
    // 发送 XML 数据
    res.send(xmlOutput);
  } catch (error) {
    console.error('SYS 转换失败:', error);
    res.status(500).send('SYS 转换失败');
  }
});

// 封装 Python 转换函数
function runPythonConversion(flowData) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['json2sys.py', JSON.stringify(flowData)]);
    
    let output = '';
    let errorOutput = '';
    
    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python脚本执行失败: ${errorOutput}`);
        reject(new Error(`Python脚本执行失败，退出代码: ${code}`));
      } else {
        resolve(output);
      }
    });
  });
}