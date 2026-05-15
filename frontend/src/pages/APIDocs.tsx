import React, { useState } from 'react'
import { Tabs, Typography, Card, Button, message, Table, Space, Tag } from 'antd'
import { CopyOutlined, KeyOutlined, ThunderboltOutlined, ApiOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'

const { Title, Paragraph, Text } = Typography

interface ApiEndpoint {
  method: string
  path: string
  description: string
  requestExample: string
  responseExample: string
  pythonExample: string
  jsExample: string
  requiresAuth?: boolean
}

const apiEndpoints: Record<string, ApiEndpoint[]> = {
  '数据生成': [
    {
      method: 'POST',
      path: '/api/generate',
      description: '使用内置生成器生成测试数据',
      requestExample: JSON.stringify(
        {
          generator_type: 'name',
          count: 10,
          params: {},
        },
        null,
        2,
      ),
      responseExample: JSON.stringify(
        {
          count: 10,
          data: [
            { data: { name: '张三' } },
            { data: { name: '李四' } },
          ],
        },
        null,
        2,
      ),
      pythonExample: `import requests

response = requests.post(
    'http://localhost:8000/api/generate',
    json={
        'generator_type': 'name',
        'count': 10,
        'params': {}
    }
)

data = response.json()
print(data)`,
      jsExample: `const response = await fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    generator_type: 'name',
    count: 10,
    params: {}
  })
})

const data = await response.json()
console.log(data)`,
    },
    {
      method: 'POST',
      path: '/api/generate/{generator_type}/export',
      description: '生成数据并导出为文件（支持 json/csv/excel/sql 格式）',
      requestExample: JSON.stringify(
        {
          count: 10,
        },
        null,
        2,
      ),
      responseExample: 'Binary file (取决于格式)',
      pythonExample: `import requests

# 生成并导出为 CSV
response = requests.post(
    'http://localhost:8000/api/generate/name/export?format=csv',
    json={'count': 10}
)

with open('names.csv', 'wb') as f:
    f.write(response.content)`,
      jsExample: `const response = await fetch('http://localhost:8000/api/generate/name/export?format=csv', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ count: 10 })
})

const blob = await response.blob()
// 后续可以创建下载链接`,
    },
  ],
  '模板管理': [
    {
      method: 'GET',
      path: '/api/templates',
      description: '获取所有模板列表（支持分页）',
      requestExample: '',
      responseExample: JSON.stringify(
        [
          {
            id: 1,
            name: '用户信息模板',
            description: '基础用户信息',
            fields: [],
            createdAt: '2024-01-01T00:00:00',
            updatedAt: '2024-01-01T00:00:00',
          },
        ],
        null,
        2,
      ),
      pythonExample: `import requests

# 基础查询
response = requests.get('http://localhost:8000/api/templates')
templates = response.json()
print(templates)

# 分页查询
response = requests.get('http://localhost:8000/api/templates?skip=0&limit=10')`,
      jsExample: `const response = await fetch('http://localhost:8000/api/templates')
const templates = await response.json()
console.log(templates)`,
    },
    {
      method: 'GET',
      path: '/api/templates/{template_id}',
      description: '获取单个模板的详细信息',
      requestExample: '',
      responseExample: JSON.stringify(
        {
          id: 1,
          name: '用户信息模板',
          description: '包含姓名、邮箱和手机号',
          fields: [
            { type: 'name', label: '姓名', required: true },
            { type: 'email', label: '邮箱', required: true },
          ],
          createdAt: '2024-01-01T00:00:00',
          updatedAt: '2024-01-01T00:00:00',
        },
        null,
        2,
      ),
      pythonExample: `import requests

response = requests.get('http://localhost:8000/api/templates/1')
template = response.json()
print(template)`,
      jsExample: `const response = await fetch('http://localhost:8000/api/templates/1')
const template = await response.json()
console.log(template)`,
    },
    {
      method: 'POST',
      path: '/api/templates',
      description: '创建新模板',
      requestExample: JSON.stringify(
        {
          name: '用户信息模板',
          description: '包含姓名、邮箱和手机号',
          fields: [
            { type: 'name', label: '姓名', required: true },
            { type: 'email', label: '邮箱', required: true },
          ],
        },
        null,
        2,
      ),
      responseExample: JSON.stringify(
        {
          id: 1,
          name: '用户信息模板',
          description: '包含姓名、邮箱和手机号',
          fields: [],
          createdAt: '2024-01-01T00:00:00',
          updatedAt: '2024-01-01T00:00:00',
        },
        null,
        2,
      ),
      pythonExample: `import requests

response = requests.post(
    'http://localhost:8000/api/templates',
    json={
        'name': '用户信息模板',
        'description': '包含姓名、邮箱和手机号',
        'fields': [
            {'type': 'name', 'label': '姓名', 'required': True},
            {'type': 'email', 'label': '邮箱', 'required': True}
        ]
    }
)

template = response.json()
print(template)`,
      jsExample: `const response = await fetch('http://localhost:8000/api/templates', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: '用户信息模板',
    description: '包含姓名、邮箱和手机号',
    fields: [
      { type: 'name', label: '姓名', required: true },
      { type: 'email', label: '邮箱', required: true }
    ]
  })
})

const template = await response.json()
console.log(template)`,
    },
    {
      method: 'PUT',
      path: '/api/templates/{template_id}',
      description: '更新已存在的模板信息',
      requestExample: JSON.stringify(
        {
          name: '更新后的模板名',
          description: '更新后的描述',
        },
        null,
        2,
      ),
      responseExample: JSON.stringify(
        {
          id: 1,
          name: '更新后的模板名',
          description: '更新后的描述',
          fields: [],
          createdAt: '2024-01-01T00:00:00',
          updatedAt: '2024-01-02T00:00:00',
        },
        null,
        2,
      ),
      pythonExample: `import requests

response = requests.put(
    'http://localhost:8000/api/templates/1',
    json={
        'name': '更新后的模板名',
        'description': '更新后的描述'
    }
)

template = response.json()
print(template)`,
      jsExample: `const response = await fetch('http://localhost:8000/api/templates/1', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: '更新后的模板名',
    description: '更新后的描述'
  })
})

const template = await response.json()
console.log(template)`,
    },
    {
      method: 'DELETE',
      path: '/api/templates/{template_id}',
      description: '根据ID删除模板（删除后不可恢复）',
      requestExample: '',
      responseExample: '204 No Content',
      pythonExample: `import requests

response = requests.delete('http://localhost:8000/api/templates/1')
print('删除成功')`,
      jsExample: `const response = await fetch('http://localhost:8000/api/templates/1', {
  method: 'DELETE'
})
console.log('删除成功')`,
    },
    {
      method: 'POST',
      path: '/api/templates/{template_id}/copy',
      description: '复制一个已存在的模板',
      requestExample: '',
      responseExample: JSON.stringify(
        {
          id: 2,
          name: '用户信息模板（副本）',
          description: '包含姓名、邮箱和手机号',
          fields: [],
          createdAt: '2024-01-02T00:00:00',
          updatedAt: '2024-01-02T00:00:00',
        },
        null,
        2,
      ),
      pythonExample: `import requests

response = requests.post('http://localhost:8000/api/templates/1/copy')
copied_template = response.json()
print(copied_template)`,
      jsExample: `const response = await fetch('http://localhost:8000/api/templates/1/copy', {
  method: 'POST'
})
const copiedTemplate = await response.json()
console.log(copiedTemplate)`,
    },
  ],
  'AI生成': [
    {
      method: 'POST',
      path: '/api/ai/generate',
      description: '使用AI生成测试数据（需要API密钥认证）',
      requestExample: JSON.stringify(
        {
          prompt: '生成10个中国用户信息',
          count: 10,
        },
        null,
        2,
      ),
      responseExample: JSON.stringify(
        {
          prompt: '生成10个中国用户信息',
          count: 10,
          data: [
            { name: '张三', email: 'zhangsan@example.com' },
            { name: '李四', email: 'lisi@example.com' },
          ],
        },
        null,
        2,
      ),
      requiresAuth: true,
      pythonExample: `import requests

response = requests.post(
    'http://localhost:8000/api/ai/generate',
    json={
        'prompt': '生成10个中国用户信息',
        'count': 10
    },
    headers={
        'Authorization': 'Bearer YOUR_API_KEY'
    }
)

data = response.json()
print(data)`,
      jsExample: `const response = await fetch('http://localhost:8000/api/ai/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    prompt: '生成10个中国用户信息',
    count: 10
  })
})

const data = await response.json()
console.log(data)`,
    },
  ],
  'API密钥管理': [
    {
      method: 'GET',
      path: '/api/api-keys',
      description: '获取所有已创建的API密钥列表',
      requestExample: '',
      responseExample: JSON.stringify(
        [
          {
            id: 1,
            key: 'sk-xxxxxxxxxxxxx',
            name: '我的测试密钥',
            isActive: true,
            createdAt: '2024-01-01T00:00:00',
            expiresAt: '2025-12-31T23:59:59',
          },
        ],
        null,
        2,
      ),
      pythonExample: `import requests

response = requests.get('http://localhost:8000/api/api-keys')
keys = response.json()
print(keys)`,
      jsExample: `const response = await fetch('http://localhost:8000/api/api-keys')
const keys = await response.json()
console.log(keys)`,
    },
    {
      method: 'POST',
      path: '/api/api-keys',
      description: '创建新的API访问密钥（密钥创建后请立即保存，无法找回）',
      requestExample: JSON.stringify(
        {
          name: '我的测试密钥',
          expiresAt: '2025-12-31T23:59:59',
        },
        null,
        2,
      ),
      responseExample: JSON.stringify(
        {
          id: 1,
          key: 'sk-xxxxxxxxxxxxx',
          name: '我的测试密钥',
          isActive: true,
          createdAt: '2024-01-01T00:00:00',
          expiresAt: '2025-12-31T23:59:59',
        },
        null,
        2,
      ),
      pythonExample: `import requests

response = requests.post(
    'http://localhost:8000/api/api-keys',
    json={
        'name': '我的测试密钥',
        'expiresAt': '2025-12-31T23:59:59'
    }
)

api_key = response.json()
print('请妥善保存密钥：', api_key['key'])`,
      jsExample: `const response = await fetch('http://localhost:8000/api/api-keys', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: '我的测试密钥',
    expiresAt: '2025-12-31T23:59:59'
  })
})

const apiKey = await response.json()
console.log('请妥善保存密钥：', apiKey.key)`,
    },
    {
      method: 'DELETE',
      path: '/api/api-keys/{key_id}',
      description: '根据ID删除API密钥（删除后立即失效，不可恢复）',
      requestExample: '',
      responseExample: '204 No Content',
      pythonExample: `import requests

response = requests.delete('http://localhost:8000/api/api-keys/1')
print('删除成功')`,
      jsExample: `const response = await fetch('http://localhost:8000/api/api-keys/1', {
  method: 'DELETE'
})
console.log('删除成功')`,
    },
  ],
}

const CodeBlock: React.FC<{ code: string }> = ({ code }) => {
  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    message.success('已复制到剪贴板')
  }

  return (
    <div style={{ position: 'relative' }}>
      <Button
        type="text"
        icon={<CopyOutlined />}
        onClick={handleCopy}
        style={{ position: 'absolute', top: 8, right: 8 }}
      />
      <pre
        style={{
          background: '#f5f5f5',
          padding: 16,
          borderRadius: 4,
          overflow: 'auto',
          fontFamily: 'monospace',
          fontSize: 14,
        }}
      >
        <code>{code}</code>
      </pre>
    </div>
  )
}

const APIDocs: React.FC = () => {
  const [activeTab, setActiveTab] = useState('数据生成')

  const endpointColumns: ColumnsType<ApiEndpoint> = [
    {
      title: '方法',
      dataIndex: 'method',
      key: 'method',
      width: 100,
      render: (method: string) => (
        <Text
          strong
          style={{
            color: method === 'GET' ? '#52c41a' : method === 'POST' ? '#1890ff' : method === 'PUT' ? '#faad14' : '#ff4d4f',
          }}
        >
          {method}
        </Text>
      ),
    },
    {
      title: '路径',
      dataIndex: 'path',
      key: 'path',
      width: 250,
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      render: (text: string, record: ApiEndpoint) => (
        <Space>
          {text}
          {record.requiresAuth && <Tag color="red">需认证</Tag>}
        </Space>
      ),
    },
  ]

  return (
    <div>
      <Title>API文档</Title>

      <Space direction="vertical" style={{ width: '100%', marginBottom: 24 }}>
        <Card title={<><ApiOutlined /> 接口调试工具</>}>
          <Space>
            <Button 
              type="primary" 
              size="large" 
              icon={<ThunderboltOutlined />}
              onClick={() => window.open('http://localhost:8000/docs', '_blank')}
            >
              Swagger UI
            </Button>
            <Button 
              size="large" 
              onClick={() => window.open('http://localhost:8000/redoc', '_blank')}
            >
              ReDoc
            </Button>
          </Space>
          <Paragraph style={{ marginTop: 16, color: '#666' }}>
            点击上方按钮打开接口在线调试工具，支持可视化请求参数配置和调试
          </Paragraph>
        </Card>

        <Card title={<><KeyOutlined /> API密钥说明</>}>
          <Title level={5}>用途</Title>
          <Paragraph>
            API密钥用于外部程序（如自动化脚本）调用本平台的API接口。
          </Paragraph>
          
          <Title level={5}>如何获取API密钥</Title>
          <ul>
            <li>点击左侧菜单"API密钥"，创建新密钥</li>
            <li>密钥创建后只显示一次，请妥善保管</li>
          </ul>
          
          <Title level={5}>如何使用API密钥</Title>
          <Paragraph>
            在请求头中添加：<Text code>Authorization: Bearer YOUR_API_KEY</Text>
          </Paragraph>
          
          <Title level={5}>注意事项</Title>
          <ul>
            <li>Web页面使用不需要API密钥</li>
            <li>外部脚本调用时需要提供API密钥</li>
            <li>丢失密钥请删除后重新创建</li>
          </ul>
        </Card>
      </Space>

      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        items={Object.keys(apiEndpoints).map(category => ({
          key: category,
          label: category,
          children: (
            <div>
              <Table
                columns={endpointColumns}
                dataSource={apiEndpoints[category]}
                rowKey="path"
                pagination={false}
                style={{ marginBottom: 24 }}
              />

              {apiEndpoints[category].map((endpoint, index) => (
                <Card
                  key={index}
                  title={
                    <Space>
                      <Text
                        strong
                        style={{
                          color: endpoint.method === 'GET' ? '#52c41a' : endpoint.method === 'POST' ? '#1890ff' : endpoint.method === 'PUT' ? '#faad14' : '#ff4d4f',
                        }}
                      >
                        {endpoint.method}
                      </Text>
                      <Text code>{endpoint.path}</Text>
                      {endpoint.requiresAuth && <Tag color="red">需认证</Tag>}
                    </Space>
                  }
                  style={{ marginBottom: 24 }}
                >
                  <Paragraph>{endpoint.description}</Paragraph>

                  {endpoint.requestExample && (
                    <>
                      <Title level={5}>请求示例</Title>
                      <CodeBlock code={endpoint.requestExample} />
                    </>
                  )}

                  <Title level={5} style={{ marginTop: 16 }}>
                    响应示例
                  </Title>
                  <CodeBlock code={endpoint.responseExample} />

                  <Title level={5} style={{ marginTop: 16 }}>
                    Python示例
                  </Title>
                  <CodeBlock code={endpoint.pythonExample} />

                  <Title level={5} style={{ marginTop: 16 }}>
                    JavaScript示例
                  </Title>
                  <CodeBlock code={endpoint.jsExample} />
                </Card>
              ))}
            </div>
          ),
        }))}
      />
    </div>
  )
}

export default APIDocs
