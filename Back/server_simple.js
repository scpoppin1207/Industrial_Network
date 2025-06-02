// backend/server.js

const express = require('express')
const axios = require('axios')

const app = express()
const PORT = 3000

app.use(express.json())

// ✅ 替换成你自己的 API Key 和 endpoint
const API_URL = 'https://maas-cn-east-4.modelarts-maas.com/v1/infers/5f114f77-65c2-4e79-82df-d84b25b89d42/v1/chat/completions'
const API_KEY = 'vWUQVo7N1__ZejNJj7JKIeXVKRele2xY1sIOe8hxtsvDsU0PFNQtEKJCJWlRbD9LUwbx1kJvTc7iO4k416kzYg' // <- 替换成你自己的

app.post('/api/dialog', async (req, res) => {
  const { content } = req.body

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`,
  }

  const data = {
    model: 'Qwen2.5-72B-32K',
    messages: [
      { role: 'system', content: '你是一个仓储运输设计者。你接收到一段仓储设计的需求后，从中提炼出以下两个信息： \
        总共有几个源头货架；每个源头货架对应几个目标货架；用数组来回答。比如你提炼出来总共用3个源头货架，分别有3个、1个、10个目的货架，你就返回(3,1,10)。只用回答数组，其他的什么都不用回答。' },
      { role: 'user', content }
    ],
    stream: false,
    temperature: 0
  }

  try {
    const response = await axios.post(API_URL, data, { headers })
    const reply = response.data.choices[0].message.content
    res.json({ reply })
  } catch (error) {
    console.error('请求LLM失败:', error.message)
    res.status(500).json({ reply: 'LLM请求失败' })
  }
})

app.listen(PORT, () => {
  console.log(`✅ 后端服务器运行中：http://localhost:${PORT}`)
})