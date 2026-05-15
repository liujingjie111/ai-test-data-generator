import React, { useState, useEffect, useRef } from 'react'
import { Table, Button, Space, Modal, Form, Input, message, Card, Typography, Tag, Popconfirm, DatePicker, Radio } from 'antd'
import { PlusOutlined, DeleteOutlined, CopyOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { getApiKeys, createApiKey, deleteApiKey } from '../services/apiKeys'
import type { ApiKey } from '../types'
import dayjs from 'dayjs'

const { Title, Text, Paragraph } = Typography
const { Group: RadioGroup } = Radio

type ExpireOption = 'never' | '1day' | '3days' | '7days' | 'custom'

const ApiKeys: React.FC = () => {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([])
  const [loading, setLoading] = useState(false)
  const [createModalVisible, setCreateModalVisible] = useState(false)
  const [newKeyModalVisible, setNewKeyModalVisible] = useState(false)
  const [newKey, setNewKey] = useState<string | null>(null)
  const [expireOption, setExpireOption] = useState<ExpireOption>('never')
  const [form] = Form.useForm()
  const hasShownWarning = useRef(false)

  const fetchApiKeys = async (showWarning = true) => {
    setLoading(true)
    try {
      const data = await getApiKeys()
      setApiKeys(data)
      
      // 检查过期状态并显示提醒
      if (showWarning && !hasShownWarning.current) {
        const now = dayjs()
        let expiredCount = 0
        let soonExpireCount = 0
        
        data.forEach(key => {
          const isActive = key.isActive ?? key.is_active
          const expiresDate = key.expiresAt ?? key.expires_at
          
          if (isActive && expiresDate) {
            const expireTime = dayjs(expiresDate)
            if (expireTime.isBefore(now)) {
              expiredCount++
            } else if (expireTime.isBefore(now.add(1, 'day'))) {
              soonExpireCount++
            }
          }
        })
        
        if (expiredCount > 0) {
          message.warning(`有 ${expiredCount} 个API密钥已过期！`)
        }
        if (soonExpireCount > 0) {
          message.info(`有 ${soonExpireCount} 个API密钥即将在24小时内过期！`)
        }
        hasShownWarning.current = true
      }
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : '获取API密钥失败'
      message.error(msg)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchApiKeys()
  }, [])

  const handleCreate = async (values: { name: string; expires_at?: any }) => {
    try {
      let expires_at: string | undefined
      
      switch (expireOption) {
        case '1day':
          expires_at = dayjs().add(1, 'day').toISOString()
          break
        case '3days':
          expires_at = dayjs().add(3, 'day').toISOString()
          break
        case '7days':
          expires_at = dayjs().add(7, 'day').toISOString()
          break
        case 'custom':
          if (values.expires_at) {
            const selectedDate = dayjs(values.expires_at)
            if (selectedDate.isBefore(dayjs())) {
              message.error('过期时间必须在当前时间之后')
              return
            }
            expires_at = selectedDate.toISOString()
          }
          break
        case 'never':
        default:
          expires_at = undefined
      }
      
      const data = await createApiKey({ name: values.name, expires_at })
      setNewKey(data.key)
      setNewKeyModalVisible(true)
      setCreateModalVisible(false)
      setExpireOption('never')
      form.resetFields()
      fetchApiKeys(false)
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : '创建API密钥失败'
      message.error(msg)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await deleteApiKey(id)
      message.success('删除成功')
      fetchApiKeys(false)
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : '删除失败'
      message.error(msg)
    }
  }

  const handleCopy = () => {
    if (newKey) {
      navigator.clipboard.writeText(newKey)
      message.success('已复制到剪贴板')
    }
  }

  const columns: ColumnsType<ApiKey> = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '密钥',
      dataIndex: 'key',
      key: 'key',
      render: (key: string) => (
        <Text code copyable={{ text: key }}>
          {key.substring(0, 12)}...
        </Text>
      ),
    },
    {
      title: '状态',
      key: 'status',
      render: (_, record) => {
        const isActive = record.isActive ?? record.is_active
        const expiresDate = record.expiresAt ?? record.expires_at
        const now = dayjs()
        
        let statusText = '启用'
        let statusColor = 'green'
        
        if (!isActive) {
          statusText = '禁用'
          statusColor = 'red'
        } else if (expiresDate) {
          const expireTime = dayjs(expiresDate)
          if (expireTime.isBefore(now)) {
            statusText = '已过期'
            statusColor = 'red'
          } else if (expireTime.isBefore(now.add(1, 'day'))) {
            statusText = '即将过期'
            statusColor = 'orange'
          } else if (expireTime.isBefore(now.add(7, 'day'))) {
            statusText = '将过期'
            statusColor = 'gold'
          }
        }
        
        return (
          <Tag color={statusColor}>
            {statusText}
          </Tag>
        )
      },
    },
    {
      title: '创建时间',
      key: 'createdAt',
      render: (_, record) => {
        const date = record.createdAt ?? record.created_at
        return new Date(date).toLocaleString('zh-CN')
      },
    },
    {
      title: '过期时间',
      key: 'expiresAt',
      render: (_, record) => {
        const date = record.expiresAt ?? record.expires_at
        if (!date) return '永不过期'
        
        const expireTime = dayjs(date)
        const now = dayjs()
        const diff = expireTime.diff(now, 'day')
        
        let color: string | undefined
        if (diff < 0) {
          color = 'red'
        } else if (diff < 1) {
          color = 'orange'
        } else if (diff < 7) {
          color = 'gold'
        }
        
        return (
          <Text type={color as any}>
            {expireTime.toLocaleString('zh-CN')}
          </Text>
        )
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Popconfirm
          title="确认删除"
          description="确定要删除这个API密钥吗？"
          onConfirm={() => handleDelete(record.id)}
          okText="确定"
          cancelText="取消"
        >
          <Button
            type="text"
            danger
            icon={<DeleteOutlined />}
          >
            删除
          </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <Title>API密钥管理</Title>
      
      <Card style={{ marginBottom: 16 }}>
        <Paragraph>
          API密钥用于外部程序调用本平台的API接口。创建后请妥善保管，密钥只在创建时显示一次！
        </Paragraph>
      </Card>

      <Card>
        <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setCreateModalVisible(true)}
          >
            创建API密钥
          </Button>
        </div>
        <Table
          columns={columns}
          dataSource={apiKeys}
          rowKey="id"
          loading={loading}
        />
      </Card>

      <Modal
        title="创建API密钥"
        open={createModalVisible}
        onCancel={() => {
          setCreateModalVisible(false)
          setExpireOption('never')
          form.resetFields()
        }}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreate}
        >
          <Form.Item
            name="name"
            label="密钥名称"
            rules={[{ required: true, message: '请输入密钥名称' }]}
          >
            <Input placeholder="例如：测试脚本" />
          </Form.Item>
          <Form.Item label="过期时间">
            <RadioGroup 
              value={expireOption} 
              onChange={(e) => setExpireOption(e.target.value)}
            >
              <Space direction="vertical">
                <Radio value="never">永不过期</Radio>
                <Radio value="1day">1天后过期</Radio>
                <Radio value="3days">3天后过期</Radio>
                <Radio value="7days">7天后过期</Radio>
                <Radio value="custom">自定义时间</Radio>
              </Space>
            </RadioGroup>
          </Form.Item>
          {expireOption === 'custom' && (
            <Form.Item
              name="expires_at"
              label="选择过期时间"
              rules={[{ required: true, message: '请选择过期时间' }]}
            >
              <DatePicker
                showTime
                format="YYYY-MM-DD HH:mm:ss"
                style={{ width: '100%' }}
                disabledDate={(current) => current && current.isBefore(dayjs().startOf('day'))}
              />
            </Form.Item>
          )}
          <Form.Item>
            <Button type="primary" htmlType="submit">
            创建
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => {
            setCreateModalVisible(false)
            setExpireOption('never')
            form.resetFields()
          }}>
            取消
          </Button>
        </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="API密钥创建成功"
        open={newKeyModalVisible}
        onCancel={() => setNewKeyModalVisible(false)}
        onOk={() => setNewKeyModalVisible(false)}
      >
        <Paragraph>
          请复制下面的API密钥，只显示这一次！
        </Paragraph>
        <div style={{ 
          background: '#f5f5f5',
          padding: '16px',
          borderRadius: '4px',
          marginBottom: '16px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <Text code style={{ fontSize: '14px', wordBreak: 'break-all' }}>
            {newKey}
          </Text>
          <Button icon={<CopyOutlined />} onClick={handleCopy}>
            复制
          </Button>
        </div>
        </Modal>
    </div>
  )
}

export default ApiKeys
