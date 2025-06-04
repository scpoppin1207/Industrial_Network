// backend/server.js

const express = require('express')
const axios = require('axios')
const { spawn } = require('child_process') // 用于调用Python脚本
const fs = require('fs') // 用于文件操作
const path = require('path') // 用于处理文件路径

const app = express()
const PORT = 3000

app.use(express.json())

const API_URL = 'https://maas-cn-east-4.modelarts-maas.com/v1/infers/5f114f77-65c2-4e79-82df-d84b25b89d42/v1/chat/completions'
const API_KEY = 'vWUQVo7N1__ZejNJj7JKIeXVKRele2xY1sIOe8hxtsvDsU0PFNQtEKJCJWlRbD9LUwbx1kJvTc7iO4k416kzYg' 

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
        content: '你是一个仓储运输设计者。你接收到一段仓储设计的需求后，从中一步步提炼出以下信息并最终组织好信息返回一个嵌套元组： \
        1.有几个源头货架； \
        2.最高的层数是多少；\
        2.每个源头货架有几个目的货架； \
        3.每个源头的目的货架是如何在楼层上分布的； \
        最后得到数组按照如下规则组织： \
        1. 每个源头货架对应一个数组，数组的长度等于最高楼层数（比如最高有4层，则每个源头货架对应的数组长度就是4）； \
        2. 数组的每个元素表示该源头货架在对应楼层上的n目的货架数量，如果没有目的货架则用0补齐； \
        3. 最后用一个元组包裹所有源头货架的数组。 \
        给出两个示例： \
        我有2个源仓库，第一个源仓库共有3个终点，在一楼有1一个终点，在3楼有2个终点；第二个仓库有2个终点，在一楼有1个终点，在二楼有一个终点。返回：((1,0,2),(1,1,0)) \
        我有3个源仓库，第一个源仓库共有1个终点，在三楼有一个终点；第二个源仓库有2个终点，一个在1楼，一个在2楼；第三个源仓库有3个终点，在1楼有1个终点，在2楼有2个终点。返回：((0,0,1),(1,1,0),(1,2,0)) \
        记住，你只用回答数组，其他的什么都不用回答。' 
      },
    
      { role: 'user', content }
    ],
    stream: false,
    temperature: 0
  }

  try {
    const response = await axios.post(API_URL, data, { headers })
    const reply = response.data.choices[0].message.content

    // 由python代为解析响应
    const numbers = reply
    console.log(`✅ 解析到的提升机数量数组: ${numbers}`)
    
    // 2. 调用js_gen_level.py生成json
    runPythonScript('js_gen_level.py', [JSON.stringify(numbers)], (error, jsonOutput) => {
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

// 封装 Python 转换函数，windows特供
// 修改后的 runPythonConversion 函数
async function runPythonConversion(flowData) {
    return new Promise((resolve, reject) => {
      // 创建临时文件
      const tempFilePath = path.join(__dirname, 'temp', `flowData_${Date.now()}.json`);
      
      // 确保临时目录存在
      const tempDir = path.dirname(tempFilePath);
      if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir, { recursive: true });
      }
  
      // 将数据写入临时文件
      fs.writeFile(tempFilePath, JSON.stringify(flowData), (writeError) => {
        if (writeError) {
          return reject(writeError);
        }
  
        // 传递文件路径而不是数据内容
        const pythonProcess = spawn('python', ['json2sys_win.py', tempFilePath]);
        
        let output = '';
        let errorOutput = '';
        
        pythonProcess.stdout.on('data', (data) => {
          output += data.toString();
        });
        
        pythonProcess.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });
        
        pythonProcess.on('close', (code) => {
          // 清理临时文件
          fs.unlink(tempFilePath, (unlinkError) => {
            if (unlinkError) console.error('临时文件删除失败:', unlinkError);
          });
          
          if (code !== 0) {
            reject(new Error(`Python脚本执行失败，退出代码: ${code}\n${errorOutput}`));
          } else {
            resolve(output);
          }
        });
      });
    });
  }