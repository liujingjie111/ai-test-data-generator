import React, { useState } from 'react'
import { Form, Input, InputNumber, Button, message, Typography, Card, Tag } from 'antd'
import { generateWithAI } from '../services/ai'
import DataPreview from '../components/DataPreview'
import type { AIResult } from '../types'
import type { ColumnsType } from 'antd/es/table'

const { Title, Paragraph } = Typography

const examplePrompts = [
  '生成100个中国用户的个人信息，包含姓名、邮箱和手机号',
  '生成50个电商订单数据，包含订单号、商品名称、价格和状态',
  '生成200条日志数据，包含时间戳、IP地址、请求路径和状态码',
  '生成30个企业客户信息，包含公司名称、联系人、地址和信用代码',
]

const AIGenerator: React.FC = () => {
  const [form] = Form.useForm()
  const [generating, setGenerating] = useState(false)
  const [result, setResult] = useState<AIResult | null>(null)

  const handleGenerate = async (values: { prompt: string; count: number }) => {
    setGenerating(true)
    setResult(null)

    try {
      const data = await generateWithAI(values.prompt, values.count)
      setResult(data)
      message.success('AI生成成功')
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : 'AI生成失败'
      message.error(messageText)
    } finally {
      setGenerating(false)
    }
  }

  const handleExampleClick = (prompt: string) => {
    form.setFieldValue('prompt', prompt)
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
        <Tag color="warning" style={{ marginBottom: 16 }}>
          注意：需要配置有效的API密钥才能使用AI生成功能
        </Tag>
      </Card>

      <Card style={{ marginBottom: 24 }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGenerate}
          initialValues={{ count: 10 }}
        >
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
                <Tag
                  key={index}
                  style={{ cursor: 'pointer' }}
                  onClick={() => handleExampleClick(prompt)}
                >
                  {prompt}
                </Tag>
              ))}
            </div>
          </Form.Item>

          <Form.Item
            name="count"
            label="生成数量"
            rules={[{ required: true, message: '请输入生成数量' }]}
          >
            <InputNumber min={1} max={1000} style={{ width: '100%' }} />
          </Form.Item>

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
        />
      )}
    </div>
  )
}

export default AIGenerator
