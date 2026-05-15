import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Table, Button, Space, Modal, message, Typography, Dropdown } from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  CopyOutlined,
  PlayCircleOutlined,
  EllipsisOutlined,
} from '@ant-design/icons'
import { getTemplates, updateTemplate, deleteTemplate, copyTemplate, createTemplate } from '../services/template'
import TemplateEditor from '../components/TemplateEditor'
import type { Template } from '../types'
import type { ColumnsType } from 'antd/es/table'
import type { MenuProps } from 'antd'

const { Title } = Typography

const Templates: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(false)
  const [editorVisible, setEditorVisible] = useState(false)
  const [currentTemplate, setCurrentTemplate] = useState<Template | null>(null)
  const [saving, setSaving] = useState(false)
  const navigate = useNavigate()

  const fetchTemplates = async () => {
    setLoading(true)
    try {
      const data = await getTemplates()
      setTemplates(data)
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '获取模板列表失败'
      message.error(messageText)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTemplates()
  }, [])

  const handleCreate = () => {
    setCurrentTemplate(null)
    setEditorVisible(true)
  }

  const handleEdit = (record: Template) => {
    setCurrentTemplate(record)
    setEditorVisible(true)
  }

  const handleDelete = async (id: number) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个模板吗？此操作不可撤销。',
      onOk: async () => {
        try {
          await deleteTemplate(id)
          message.success('删除成功')
          fetchTemplates()
        } catch (error: unknown) {
          const messageText = error instanceof Error ? error.message : '删除失败'
          message.error(messageText)
        }
      },
    })
  }

  const handleCopy = async (id: number) => {
    try {
      await copyTemplate(id)
      message.success('复制成功')
      fetchTemplates()
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '复制失败'
      message.error(messageText)
    }
  }

  const handleGenerate = (record: Template) => {
    navigate(`/generator/${record.id}`)
  }

  const handleSave = async (data: { name: string; description: string; fields: Template['fields'] }) => {
    setSaving(true)
    try {
      if (currentTemplate) {
        await updateTemplate(currentTemplate.id, data)
        message.success('更新成功')
      } else {
        await createTemplate(data)
        message.success('创建成功')
      }
      setEditorVisible(false)
      fetchTemplates()
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '保存失败'
      message.error(messageText)
    } finally {
      setSaving(false)
    }
  }

  const getActionMenu = (record: Template): MenuProps['items'] => [
    {
      key: 'generate',
      label: '生成数据',
      icon: <PlayCircleOutlined />,
      onClick: () => handleGenerate(record),
    },
    {
      key: 'edit',
      label: '编辑',
      icon: <EditOutlined />,
      onClick: () => handleEdit(record),
    },
    {
      key: 'copy',
      label: '复制',
      icon: <CopyOutlined />,
      onClick: () => handleCopy(record.id),
    },
    { type: 'divider' },
    {
      key: 'delete',
      label: '删除',
      icon: <DeleteOutlined />,
      danger: true,
      onClick: () => handleDelete(record.id),
    },
  ]

  const formatDate = (dateStr: string) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const columns: ColumnsType<Template> = [
    {
      title: '模板名称',
      dataIndex: 'name',
      key: 'name',
      width: 150,
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '字段数量',
      key: 'fields',
      width: 100,
      align: 'center',
      render: (_, record) => record.fields.length,
    },
    {
      title: '更新时间',
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 180,
      render: (text: string) => formatDate(text),
    },
    {
      title: '操作',
      key: 'action',
      width: 60,
      align: 'center',
      render: (_, record) => (
        <Dropdown menu={{ items: getActionMenu(record) }} placement="bottomRight">
          <Button type="text" icon={<EllipsisOutlined />} />
        </Dropdown>
      ),
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
        <Title>模板管理</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
          新建模板
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={templates}
        loading={loading}
        rowKey="id"
      />

      <Modal
        title={currentTemplate ? '编辑模板' : '新建模板'}
        open={editorVisible}
        onCancel={() => setEditorVisible(false)}
        footer={null}
        width={720}
        bodyStyle={{ 
          maxHeight: '70vh',
          overflowY: 'auto', 
          paddingRight: '16px' 
        }}
      >
        <TemplateEditor
          initialData={
            currentTemplate
              ? {
                  name: currentTemplate.name,
                  description: currentTemplate.description,
                  fields: currentTemplate.fields,
                }
              : undefined
          }
          onSave={handleSave}
          onCancel={() => setEditorVisible(false)}
          loading={saving}
        />
      </Modal>
    </div>
  )
}

export default Templates