import React, { useState, useEffect } from 'react'
import { Form, Input, InputNumber, Button, message, Typography, Card, Progress, Select } from 'antd'
import { generateWithAI } from '../services/api'
import DataPreview from '../components/DataPreview'
import { exportToJSON, exportToCSV, exportToExcel, exportToSQL } from '../utils/export'
import type { AIResult } from '../types'
import type { ColumnsType } from 'antd/es/table'

const { Title, Paragraph } = Typography
const { Option } = Select

const examplePrompts = [
  '生成中国用户的个人信息，包含姓名、邮箱和手机号',
  '生成电商订单数据，包含订单号、商品名称、价格和状态',
  '生成日志数据，包含时间戳、IP地址、请求路径和状态码',
  '生成企业客户信息，包含公司名称、联系人、地址和信用代码',
]

const modelOptions = [
  { label: 'Qwen Plus (推荐)', value: 'qwen-plus' },
  { label: 'Qwen Turbo (快速)', value: 'qwen-turbo' },
  { label: 'Qwen Max (强大)', value: 'qwen-max' },
]

const AIGenerator: React.FC = () => {
  const [form] = Form.useForm()
  const [generating, setGenerating] = useState(false)
  const [result, setResult] = useState<AIResult | null>(null)
  const [progress, setProgress] = useState(0)
  const [statusText, setStatusText] = useState('')
  const [savedApiKey, setSavedApiKey] = useState<string>('')

  useEffect(() => {
    const storedApiKey = localStorage.getItem('qwen_api_key')
    if (storedApiKey) {
      setSavedApiKey(storedApiKey)
      form.setFieldValue('apiKey', storedApiKey)
    }
    const storedModel = localStorage.getItem('qwen_model')
    if (storedModel) {
      form.setFieldValue('model', storedModel)
    }
  }, [form])

  const handleLoadKeyFromEnv = () => {
    message.info('提示：您的API密钥可能在项目的 backend/.env 文件中！请复制后粘贴到上方输入框')
  }

  const handleSaveApiKey = (apiKey: string) => {
    setSavedApiKey(apiKey)
    localStorage.setItem('qwen_api_key', apiKey)
    message.success('API密钥已保存')
  }

  const handleSaveModel = (model: string) => {
    localStorage.setItem('qwen_model', model)
    message.success('模型已保存')
  }

  const handleGenerate = async (values: { prompt: string; count: number; apiKey?: string; model?: string }) => {
    setGenerating(true)
    setResult(null)
    setProgress(0)
    setStatusText('正在初始化...')

    console.log('开始AI生成，参数：', values)

    if (!values.apiKey) {
      message.error('请先输入API密钥')
      setGenerating(false)
      return
    }

    const storedApiKey = localStorage.getItem('qwen_api_key')
    const storedModel = localStorage.getItem('qwen_model')
    
    if (values.apiKey && values.apiKey !== storedApiKey) {
      handleSaveApiKey(values.apiKey)
    }
    if (values.model && values.model !== storedModel) {
      handleSaveModel(values.model)
    }

    const estimatedTime = Math.min(values.count * 2, 120)
    const steps = 90
    const intervalMs = (estimatedTime * 1000) / steps
    let currentStep = 0

    const progressInterval = setInterval(() => {
      currentStep++
      const newProgress = Math.floor(Math.min((currentStep / steps) * 90, 90))
      setProgress(newProgress)
      setStatusText(`正在生成数据... ${newProgress}%`)
    }, intervalMs)

    try {
      setStatusText('正在调用AI生成数据...')
      const data = await generateWithAI(values.prompt, values.count, values.apiKey, values.model)
      console.log('AI生成成功，数据：', data)
      setProgress(100)
      setStatusText('生成完成！')
      setResult(data)
      message.success('AI生成成功')
    } catch (error: unknown) {
      console.error('AI生成失败：', error)
      setProgress(0)
      setStatusText('')
      
      let errorMsg = 'AI生成失败'
      if (error instanceof Error) {
        errorMsg = error.message
        if (errorMsg.includes('timeout') || errorMsg.includes('超时')) {
          errorMsg = '请求超时，请减少生成数量后重试'
        } else if (errorMsg.includes('API') && errorMsg.includes('key')) {
          errorMsg = 'API密钥配置有问题，请检查配置'
        } else if (errorMsg.includes('Invalid') || errorMsg.includes('JSON')) {
          errorMsg = 'AI返回数据格式错误，请重试'
        } else if (errorMsg.includes('getaddrinfo') || errorMsg.includes('network') || errorMsg.includes('网络')) {
          errorMsg = '网络连接失败，请检查网络连接或API地址是否正确'
        } else if (errorMsg.includes('ECONNREFUSED') || errorMsg.includes('连接')) {
          errorMsg = '无法连接到AI服务，请检查网络配置'
        }
      }
      message.error(errorMsg, 5)
    } finally {
      clearInterval(progressInterval)
      setGenerating(false)
    }
  }

  const handleExampleClick = (prompt: string) => {
    form.setFieldValue('prompt', prompt)
  }

  const handleExport = (format: string) => {
    if (!result || result.data.length === 0) {
      message.warning('请先生成数据')
      return
    }

    const timestamp = new Date().toISOString().slice(0, 10)

    if (format === 'json') {
      exportToJSON(result.data, `ai_generated_${timestamp}.json`)
    } else if (format === 'csv') {
      exportToCSV(result.data, `ai_generated_${timestamp}.csv`)
    } else if (format === 'excel') {
      exportToExcel(result.data, `ai_generated_${timestamp}.xlsx`)
    } else if (format === 'sql') {
      exportToSQL(result.data, 'ai_generated_data', `ai_generated_${timestamp}.sql`)
    } else {
      message.warning('不支持的导出格式')
      return
    }

    message.success(`已导出 ${result.data.length} 条数据`)
  }

  const columns: ColumnsType<Record<string, unknown>> = result && result.data.length > 0
    ? Object.keys(result.data[0]).map(key => ({
        title: key,
        dataIndex: key,
        key,
        ellipsis: true,
      }))
    : []

  return (
    <div>
      <Title>AI智能生成</Title>

      <Card style={{ marginBottom: 16 }}>
        <Paragraph>
          使用自然语言描述您需要的测试数据，AI将自动生成符合要求的测试数据。
        </Paragraph>
        <div style={{ color: '#1890ff', marginBottom: 16, fontSize: '14px' }}>
          ℹ️ 提示：您的API密钥将安全地保存在浏览器本地，不会上传到服务器。
        </div>
      </Card>

      <Card style={{ marginBottom: 24 }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGenerate}
          initialValues={{ count: 10, model: 'qwen-plus' }}
        >
          <Form.Item
            name="apiKey"
            label="API密钥"
            rules={[{ required: true, message: '请输入API密钥' }]}
            extra="请输入您的通义千问API密钥"
          >
            <Input.Password
              placeholder="sk-xxxxxxxxxxxxxxxxxxxx"
            />
          </Form.Item>

          <Form.Item
            name="model"
            label="模型选择"
          >
            <Select style={{ width: '100%' }}>
              {modelOptions.map(opt => (
                <Option key={opt.value} value={opt.value}>
                  {opt.label}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="prompt"
            label="生成描述"
            rules={[{ required: true, message: '请输入生成描述' }]}
          >
            <Input.TextArea
              placeholder="例如：生成100个中国用户的个人信息，包含姓名、邮箱和手机号"
              rows={4}
              maxLength={500}
              showCount
            />
          </Form.Item>

          <Form.Item label="示例提示">
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {examplePrompts.map((prompt, index) => (
                <Button
                  key={index}
                  size="small"
                  onClick={() => handleExampleClick(prompt)}
                >
                  {prompt}
                </Button>
              ))}
            </div>
          </Form.Item>

          <Form.Item
            name="count"
            label="生成数量 (最多100条)"
            rules={[{ required: true, message: '请输入生成数量' }]}
          >
            <InputNumber min={1} max={100} style={{ width: '100%' }} />
          </Form.Item>

          {generating && (
            <Card size="small" style={{ marginBottom: 16 }}>
              <Progress percent={progress} status="active" />
              <div style={{ textAlign: 'center', marginTop: 8, color: '#666' }}>
                {statusText || '正在生成数据，请稍候...'}
              </div>
            </Card>
          )}
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={generating}
              block
            >
              AI生成
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {result && result.data.length > 0 && (
        <DataPreview
          dataSource={result.data}
          columns={columns}
          loading={false}
          onExport={handleExport}
        />
      )}
    </div>
  )
}

export default AIGenerator
