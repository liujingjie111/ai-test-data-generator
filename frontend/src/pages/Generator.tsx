import React, { useState, useEffect } from 'react'
import { useSearchParams, useNavigate, useParams } from 'react-router-dom'
import { Form, Cascader, InputNumber, Button, message, Typography, Card, Space, Spin } from 'antd'
import { generateData } from '../services/generator'
import { getTemplate } from '../services/template'
import { exportToJSON, exportToCSV, exportToSQL, exportToExcel } from '../utils/export'
import ProgressBar from '../components/ProgressBar'
import DataPreview from '../components/DataPreview'
import { generateTemplateData } from '../services/api'
import type { TemplateField } from '../types'
import type { ColumnsType } from 'antd/es/table'

const { Title } = Typography

const generatorCategories = [
  {
    value: 'personal',
    label: '个人数据',
    children: [
      { value: 'name', label: '姓名' },
      { value: 'email', label: '邮箱' },
      { value: 'phone', label: '手机号' },
      { value: 'id_card', label: '身份证号' },
      { value: 'gender', label: '性别' },
      { value: 'age', label: '年龄' },
      { value: 'birth_date', label: '出生日期' },
    ],
  },
  {
    value: 'address',
    label: '地址数据',
    children: [
      { value: 'province', label: '省份' },
      { value: 'city', label: '城市' },
      { value: 'district', label: '区县' },
      { value: 'address', label: '详细地址' },
      { value: 'postcode', label: '邮编' },
      { value: 'latitude', label: '纬度' },
      { value: 'longitude', label: '经度' },
      { value: 'full_address', label: '完整地址' },
    ],
  },
  {
    value: 'finance',
    label: '金融数据',
    children: [
      { value: 'bank_card', label: '银行卡号' },
      { value: 'credit_card', label: '信用卡号' },
      { value: 'bank_name', label: '开户行' },
      { value: 'amount', label: '金额' },
    ],
  },
  {
    value: 'enterprise',
    label: '企业数据',
    children: [
      { value: 'company_name', label: '公司名称' },
      { value: 'credit_code', label: '统一社会信用代码' },
      { value: 'industry', label: '行业' },
      { value: 'company_address', label: '公司地址' },
      { value: 'company_phone', label: '公司电话' },
    ],
  },
  {
    value: 'product',
    label: '产品数据',
    children: [
      { value: 'product_name', label: '商品名称' },
      { value: 'sku', label: 'SKU' },
      { value: 'price', label: '价格' },
      { value: 'stock', label: '库存' },
      { value: 'category', label: '分类' },
    ],
  },
  {
    value: 'other',
    label: '其他数据',
    children: [
      { value: 'uuid', label: 'UUID' },
      { value: 'ip', label: 'IP地址' },
      { value: 'mac', label: 'MAC地址' },
      { value: 'url', label: 'URL' },
      { value: 'timestamp', label: '时间戳' },
      { value: 'random_string', label: '随机字符串' },
    ],
  },
]

const flattenedGenerators = generatorCategories.flatMap(cat =>
  cat.children!.map(child => ({ value: child.value, label: child.label, category: cat.label }))
)

function getGeneratorLabel(type: string): string {
  const found = flattenedGenerators.find(gen => gen.value === type)
  if (found) return found.label
  return type
}

interface TemplateMode {
  fields: TemplateField[]
  name: string
}

type TableRowData = Record<string, unknown>

const Generator: React.FC = () => {
  const [form] = Form.useForm()
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { templateId } = useParams<{ templateId: string }>()
  const [generating, setGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [tableData, setTableData] = useState<TableRowData[]>([])
  const [columns, setColumns] = useState<ColumnsType<TableRowData>>([])
  const [templateMode, setTemplateMode] = useState<TemplateMode | null>(null)
  const [currentGeneratorType, setCurrentGeneratorType] = useState('')
  const [generatedCount, setGeneratedCount] = useState(0)
  const [loadingTemplate, setLoadingTemplate] = useState(!!templateId)

  // 范围配置映射
  const rangeFieldConfig: Record<string, { minKey: string; maxKey: string; minDefault?: number; maxDefault?: number }> = {
    age: { minKey: 'min_age', maxKey: 'max_age', minDefault: 18, maxDefault: 65 },
    amount: { minKey: 'min_amount', maxKey: 'max_amount', minDefault: 0.01, maxDefault: 99999.99 },
    price: { minKey: 'min_price', maxKey: 'max_price', minDefault: 0.01, maxDefault: 99999.99 },
    stock: { minKey: 'min_stock', maxKey: 'max_stock', minDefault: 1, maxDefault: 1000 },
  }

  // 清理 options 中的 null/undefined，用默认值代替
  const sanitizeOptions = (field: any) => {
    const options = field.options || {}
    if (!rangeFieldConfig[field.type]) return options
    const config = rangeFieldConfig[field.type]
    const fixedOptions: Record<string, unknown> = {}
    
    // 向后兼容：旧模板可能保存的是 min/max
    const legacyMin = options.min
    const legacyMax = options.max
    if (legacyMin !== undefined && (options[config.minKey] === null || options[config.minKey] === undefined)) {
      fixedOptions[config.minKey] = legacyMin
    } else {
      fixedOptions[config.minKey] = options[config.minKey] ?? config.minDefault
    }
    if (legacyMax !== undefined && (options[config.maxKey] === null || options[config.maxKey] === undefined)) {
      fixedOptions[config.maxKey] = legacyMax
    } else {
      fixedOptions[config.maxKey] = options[config.maxKey] ?? config.maxDefault
    }

    // 彻底移除旧参数名，避免传给后端
    delete fixedOptions.min
    delete fixedOptions.max

    return fixedOptions
  }

  useEffect(() => {
    if (templateId) {
      setLoadingTemplate(true)
      getTemplate(Number(templateId))
        .then(template => {
          // 修复已保存的 null 值
          const fixedFields = template.fields.map(field => ({
            ...field,
            options: sanitizeOptions(field),
          }))
          setTemplateMode({ fields: fixedFields, name: template.name })
        })
        .catch((error: unknown) => {
          const messageText = error instanceof Error ? error.message : '获取模板信息失败'
          message.error(messageText)
        })
        .finally(() => {
          setLoadingTemplate(false)
        })
      return
    }

    const fieldsParam = searchParams.get('fields')
    const nameParam = searchParams.get('name')
    if (fieldsParam) {
      try {
        const fields = JSON.parse(fieldsParam).map((field: any) => ({
          ...field,
          options: sanitizeOptions(field),
        }))
        if (Array.isArray(fields) && fields.length > 0) {
          setTemplateMode({ fields, name: nameParam || '自定义模板' })
        }
      } catch {
        message.error('模板参数解析失败')
      }
    }
  }, [searchParams, templateId])

  const handleGenerate = async (values: { count: number; generatorType?: string[] }) => {
    setGenerating(true)
    setProgress(0)
    setTableData([])
    setColumns([])

    const interval = setInterval(() => {
      setProgress(prev => Math.min(prev + 10, 80))
    }, 200)

    try {
      if (templateMode) {
        // 使用新的模板生成API，只保存一条历史记录
        const result = await generateTemplateData(
          templateMode.name,
          templateMode.fields.map(field => ({
            type: field.type,
            label: field.label,
            params: sanitizeOptions(field)
          })),
          values.count
        )

        const tableData = result.data
        const tableColumns = templateMode.fields.map(field => ({
          title: field.label,
          dataIndex: field.label,
          key: field.label,
          ellipsis: true,
        }))

        setColumns(tableColumns)
        setTableData(tableData)
        setGeneratedCount(values.count)
      } else {
        // 单字段生成
        const type = Array.isArray(values.generatorType) ? values.generatorType[values.generatorType.length - 1] : values.generatorType
        const result = await generateData(type, values.count)
        const items = result.data
        const displayLabel = getGeneratorLabel(type)

        const firstItem = items[0]?.data
        if (typeof firstItem === 'object' && firstItem !== null && !Array.isArray(firstItem)) {
          const dictColumns = Object.keys(firstItem as Record<string, unknown>).map(key => ({
            title: key,
            dataIndex: key,
            key,
          }))
          const dictTableData = items.map((item: { data: Record<string, unknown> }) => ({
            ...item.data,
          }))
          setColumns(dictColumns)
          setTableData(dictTableData)
        } else {
          setColumns([{ title: displayLabel, dataIndex: 'value', key: 'value' }])
          setTableData(items.map((item: { data: unknown }) => ({
            value: item.data,
          })))
        }

        setCurrentGeneratorType(type)
        setGeneratedCount(values.count)
      }

      setProgress(100)
      message.success('数据生成成功')
    } catch (error: unknown) {
      const messageText = error instanceof Error ? error.message : '数据生成失败'
      message.error(messageText)
    } finally {
      clearInterval(interval)
      setGenerating(false)
    }
  }

  const handleExport = (format: string) => {
    if (tableData.length === 0 || columns.length === 0) {
      message.warning('请先生成数据')
      return
    }

    const exportRows = tableData
    const timestamp = new Date().toISOString().slice(0, 10)

    if (templateMode) {
      const tableName = templateMode.name || 'template_data'
      const safeName = tableName.replace(/\s+/g, '_')

      if (format === 'json') {
        exportToJSON(exportRows, `${safeName}_${timestamp}.json`)
      } else if (format === 'csv') {
        exportToCSV(exportRows, `${safeName}_${timestamp}.csv`)
      } else if (format === 'sql') {
        exportToSQL(exportRows, safeName, `${safeName}_${timestamp}.sql`)
      } else if (format === 'excel') {
        exportToExcel(exportRows, `${safeName}_${timestamp}.xlsx`)
      } else {
        message.warning('不支持的导出格式')
        return
      }
    } else {
      const typeLabel = getGeneratorLabel(currentGeneratorType)

      if (format === 'json') {
        exportToJSON(exportRows, `${currentGeneratorType}_${timestamp}.json`)
      } else if (format === 'csv') {
        exportToCSV(exportRows, `${currentGeneratorType}_${timestamp}.csv`)
      } else if (format === 'sql') {
        exportToSQL(exportRows, currentGeneratorType, `${currentGeneratorType}_${timestamp}.sql`)
      } else if (format === 'excel') {
        exportToExcel(exportRows, `${currentGeneratorType}_${timestamp}.xlsx`)
      } else {
        message.warning('不支持的导出格式')
        return
      }
    }

    message.success(`已导出 ${exportRows.length} 条数据`)
  }

  const isTemplateMode = templateMode !== null

  if (loadingTemplate) {
    return (
      <div style={{ textAlign: 'center', padding: '48px 0' }}>
        <Spin size="large" tip="加载模板信息..." />
      </div>
    )
  }

  return (
    <div>
      <Title>{isTemplateMode ? `使用模板: ${templateMode.name}` : '内置生成器'}</Title>

      <Card style={{ marginBottom: 24 }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGenerate}
          initialValues={{ count: 10 }}
        >
          {!isTemplateMode && (
            <Form.Item
              name="generatorType"
              label="生成器类型"
              rules={[{ required: true, message: '请选择生成器类型' }]}
            >
              <Cascader
                placeholder="请选择生成器类型"
                options={generatorCategories}
                changeOnSelect={false}
                displayRender={labels => labels[labels.length - 1]}
                fieldNames={{ label: 'label', value: 'value', children: 'children' }}
              />
            </Form.Item>
          )}

          {isTemplateMode && (
            <Card size="small" title="模板字段" style={{ marginBottom: 16 }}>
              <Space direction="vertical" style={{ width: '100%' }}>
                {templateMode.fields.map((field, index) => {
                  const options = field.options || {}
                  let rangeText: string | null = null
                  if (field.type === 'age' && options.min_age !== undefined && options.max_age !== undefined) {
                    rangeText = `范围: ${options.min_age}-${options.max_age}`
                  } else if (field.type === 'amount' && options.min_amount !== undefined && options.max_amount !== undefined) {
                    rangeText = `范围: ${options.min_amount}-${options.max_amount}`
                  } else if (field.type === 'price' && options.min_price !== undefined && options.max_price !== undefined) {
                    rangeText = `范围: ${options.min_price}-${options.max_price}`
                  } else if (field.type === 'stock' && options.min_stock !== undefined && options.max_stock !== undefined) {
                    rangeText = `范围: ${options.min_stock}-${options.max_stock}`
                  }
                  return (
                    <span key={index}>
                      <strong>{field.label}</strong> ({getGeneratorLabel(field.type)})
                      {rangeText ? ` · ${rangeText}` : ''}
                    </span>
                  )
                })}
              </Space>
            </Card>
          )}

          <Form.Item
            name="count"
            label="生成数量"
            rules={[{ required: true, message: '请输入生成数量' }]}
          >
            <InputNumber min={1} max={100000} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={generating}>
                生成数据
              </Button>
              {isTemplateMode && (
                <Button onClick={() => navigate('/templates')}>
                  返回模板管理
                </Button>
              )}
            </Space>
          </Form.Item>
        </Form>
      </Card>

      {generating && (
        <Card style={{ marginBottom: 24 }}>
          <ProgressBar percent={progress} />
        </Card>
      )}

      {tableData.length > 0 && (
        <DataPreview
          dataSource={tableData}
          columns={columns}
          loading={false}
          onExport={handleExport}
        />
      )}
    </div>
  )
}

export default Generator