import React, { useState, useEffect } from 'react'
import { Form, Input, InputNumber, Button, Select, Space, Card, Typography } from 'antd'
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons'
import type { TemplateField } from '../../types'

interface TemplateEditorProps {
  initialData?: {
    name: string
    description: string
    fields: TemplateField[]
  }
  onSave: (data: {
    name: string
    description: string
    fields: TemplateField[]
  }) => void
  onCancel: () => void
  loading?: boolean
}

const fieldTypes = [
  { value: 'name', label: '姓名' },
  { value: 'email', label: '邮箱' },
  { value: 'phone', label: '手机号' },
  { value: 'id_card', label: '身份证号' },
  { value: 'gender', label: '性别' },
  { value: 'age', label: '年龄' },
  { value: 'birth_date', label: '出生日期' },
  { value: 'province', label: '省份' },
  { value: 'city', label: '城市' },
  { value: 'district', label: '区县' },
  { value: 'address', label: '详细地址' },
  { value: 'postcode', label: '邮编' },
  { value: 'latitude', label: '纬度' },
  { value: 'longitude', label: '经度' },
  { value: 'full_address', label: '完整地址' },
  { value: 'bank_card', label: '银行卡号' },
  { value: 'credit_card', label: '信用卡号' },
  { value: 'bank_name', label: '开户行' },
  { value: 'amount', label: '金额' },
  { value: 'company_name', label: '公司名称' },
  { value: 'credit_code', label: '统一社会信用代码' },
  { value: 'industry', label: '行业' },
  { value: 'company_phone', label: '公司电话' },
  { value: 'company_address', label: '公司地址' },
  { value: 'product_name', label: '商品名称' },
  { value: 'sku', label: 'SKU' },
  { value: 'price', label: '价格' },
  { value: 'stock', label: '库存' },
  { value: 'category', label: '分类' },
  { value: 'uuid', label: 'UUID' },
  { value: 'ip', label: 'IP地址' },
  { value: 'mac', label: 'MAC地址' },
  { value: 'url', label: 'URL' },
  { value: 'timestamp', label: '时间戳' },
  { value: 'random_string', label: '随机字符串' },
]

const { Text } = Typography

interface RangeFieldDefinition {
  minKey: string
  maxKey: string
  minLabel: string
  maxLabel: string
  minDefault?: number
  maxDefault?: number
  isInt?: boolean
  minLimit: number
  maxLimit: number
}

const rangeFieldConfig: Record<string, RangeFieldDefinition> = {
  age: { minKey: 'min_age', maxKey: 'max_age', minLabel: '最小年龄', maxLabel: '最大年龄', minDefault: 18, maxDefault: 65, isInt: true, minLimit: 0, maxLimit: 150 },
  amount: { minKey: 'min_amount', maxKey: 'max_amount', minLabel: '最小金额', maxLabel: '最大金额', minDefault: 0.01, maxDefault: 99999.99, minLimit: 0, maxLimit: 1000000 },
  price: { minKey: 'min_price', maxKey: 'max_price', minLabel: '最低价格', maxLabel: '最高价格', minDefault: 0.01, maxDefault: 99999.99, minLimit: 0, maxLimit: 1000000 },
  stock: { minKey: 'min_stock', maxKey: 'max_stock', minLabel: '最小库存', maxLabel: '最大库存', minDefault: 1, maxDefault: 1000, isInt: true, minLimit: 0, maxLimit: 10000000 },
}

const TemplateEditor: React.FC<TemplateEditorProps> = ({
  initialData,
  onSave,
  onCancel,
  loading = false,
}) => {
  const [form] = Form.useForm()
  const [fields, setFields] = useState<TemplateField[]>(
    initialData?.fields || [],
  )
  const [rangeErrors, setRangeErrors] = useState<Record<number, string>>({})

  useEffect(() => {
    if (initialData) {
      form.setFieldsValue({
        name: initialData.name,
        description: initialData.description,
      })
      // 修复已保存的模板里的 null 值
      const fixedFields = initialData.fields.map(field => {
        // 确保标签不为空
        const label = field.label || getFieldLabelByType(field.type)
        
        if (rangeFieldConfig[field.type]) {
          const config = rangeFieldConfig[field.type]
          const options = field.options || {}
          const fixedOptions: Record<string, unknown> = { ...options }
          
          // 向后兼容：旧模板可能保存的是 min/max
          const legacyMin = fixedOptions.min
          const legacyMax = fixedOptions.max
          if (legacyMin !== undefined && (fixedOptions[config.minKey] === null || fixedOptions[config.minKey] === undefined)) {
            fixedOptions[config.minKey] = legacyMin
          }
          if (legacyMax !== undefined && (fixedOptions[config.maxKey] === null || fixedOptions[config.maxKey] === undefined)) {
            fixedOptions[config.maxKey] = legacyMax
          }

          if (fixedOptions[config.minKey] === null || fixedOptions[config.minKey] === undefined) {
            fixedOptions[config.minKey] = config.minDefault
          }
          if (fixedOptions[config.maxKey] === null || fixedOptions[config.maxKey] === undefined) {
            fixedOptions[config.maxKey] = config.maxDefault
          }
          return { ...field, label, options: fixedOptions }
        }
        return { ...field, label }
      })
      setFields(fixedFields)
    }
  }, [initialData, form])

  const getFieldLabelByType = (type: string): string => {
    const found = fieldTypes.find(item => item.value === type)
    return found ? found.label : type
  }

  const addField = () => {
    const defaultType = 'name'
    setFields([
      ...fields,
      { 
        type: defaultType, 
        label: getFieldLabelByType(defaultType), 
        required: false 
      },
    ])
  }

  const removeField = (index: number) => {
    setFields(fields.filter((_, i) => i !== index))
  }

  const updateField = (
    index: number,
    key: keyof TemplateField,
    value: unknown,
  ) => {
    const newFields = [...fields]
    newFields[index] = { ...newFields[index], [key]: value }
    setFields(newFields)
  }

  const updateFieldMultiple = (
    index: number,
    updates: Partial<TemplateField>,
  ) => {
    const newFields = [...fields]
    newFields[index] = { ...newFields[index], ...updates }
    setFields(newFields)
  }

  const getRangeError = (index: number): string | undefined => {
    const field = fields[index]
    const config = rangeFieldConfig[field.type]
    if (!config) return undefined

    const options = field.options || {}
    const minVal = options[config.minKey] ?? config.minDefault
    const maxVal = options[config.maxKey] ?? config.maxDefault

    if (minVal !== undefined && maxVal !== undefined && minVal > maxVal) {
      return '最小值不能大于最大值'
    }
    return undefined
  }

  const handleRangeChange = (
    index: number,
    config: RangeFieldDefinition,
    key: 'minKey' | 'maxKey',
    value: number | null,
  ) => {
    const field = fields[index]
    const options = field.options || {}
    updateField(index, 'options', {
      ...options,
      [config[key]]: value ?? config[key === 'minKey' ? 'minDefault' : 'maxDefault'],
    })
  }

  const handleSubmit = () => {
    for (let i = 0; i < fields.length; i++) {
      const error = getRangeError(i)
      if (error) {
        const newErrors: Record<number, string> = { ...rangeErrors, [i]: error }
        setRangeErrors(newErrors)
        return
      }
    }

    form
      .validateFields()
      .then((values) => {
        // 在保存前，彻底清理字段的 options，只保留正确的参数名，避免混淆
        const cleanedFields = fields.map(field => {
          if (!rangeFieldConfig[field.type]) return field

          const config = rangeFieldConfig[field.type]
          const options = field.options || {}
          const cleanedOptions: Record<string, unknown> = {}

          // 只保留正确的新参数名
          cleanedOptions[config.minKey] = options[config.minKey] ?? config.minDefault
          cleanedOptions[config.maxKey] = options[config.maxKey] ?? config.maxDefault

          // 确保旧的参数名彻底清除
          delete cleanedOptions.min
          delete cleanedOptions.max

          return { ...field, options: cleanedOptions }
        })

        onSave({
          name: values.name,
          description: values.description || '',
          fields: cleanedFields,
        })
      })
      .catch(() => {})
  }

  return (
    <Form form={form} layout="vertical">
      <Form.Item
        name="name"
        label="模板名称"
        rules={[{ required: true, message: '请输入模板名称' }]}
      >
        <Input placeholder="请输入模板名称" />
      </Form.Item>

      <Form.Item name="description" label="描述">
        <Input.TextArea placeholder="请输入模板描述" rows={3} />
      </Form.Item>

      <Card title="字段配置" style={{ marginBottom: 16 }}>
        {fields.map((field, index) => {
          const config = rangeFieldConfig[field.type]
          const options = field.options || {}
          const rangeError = getRangeError(index)

          return (
            <Card
              key={index}
              size="small"
              style={{ marginBottom: 12 }}
              extra={
                <Button
                  type="text"
                  danger
                  icon={<DeleteOutlined />}
                  onClick={() => removeField(index)}
                />
              }
            >
              <Space direction="vertical" style={{ width: '100%' }}>
                <Form.Item label="字段类型" style={{ marginBottom: 8 }}>
                  <Select
                    value={field.type}
                    options={fieldTypes}
                    placeholder="请选择字段类型"
                    onChange={(value) => {
                      // 当类型改变时，自动更新标签为对应类型名，一次性更新避免状态问题
                      updateFieldMultiple(index, {
                        type: value,
                        label: getFieldLabelByType(value),
                      })
                    }}
                  />
                </Form.Item>

                <Form.Item label="字段标签" style={{ marginBottom: 8 }}>
                  <Input
                    value={field.label}
                    placeholder="请输入字段标签"
                    onChange={(e) => updateField(index, 'label', e.target.value)}
                  />
                </Form.Item>

                {config && (
                  <Form.Item
                    label="范围配置"
                    style={{ marginBottom: 8 }}
                    validateStatus={rangeError ? 'error' : ''}
                    help={rangeError}
                  >
                    <Space style={{ width: '100%' }}>
                      <InputNumber
                        style={{ width: '45%' }}
                        placeholder={config.minLabel}
                        value={options[config.minKey] ?? config.minDefault}
                        onChange={(val) =>
                          handleRangeChange(index, config, 'minKey', val)
                        }
                        min={config.minLimit}
                        max={config.maxLimit}
                        precision={config.isInt ? 0 : 2}
                      />
                      <Text type="secondary">~</Text>
                      <InputNumber
                        style={{ width: '45%' }}
                        placeholder={config.maxLabel}
                        value={options[config.maxKey] ?? config.maxDefault}
                        onChange={(val) =>
                          handleRangeChange(index, config, 'maxKey', val)
                        }
                        min={config.minLimit}
                        max={config.maxLimit}
                        precision={config.isInt ? 0 : 2}
                      />
                    </Space>
                  </Form.Item>
                )}

                {field.type === 'select' && field.options?.values && (
                  <Form.Item label="选项" style={{ marginBottom: 8 }}>
                    <Input.TextArea
                      placeholder="请输入选项，每行一个"
                      rows={3}
                      defaultValue={(field.options.values as string[]).join('\n')}
                      onChange={(e) => {
                        const values = e.target.value
                          .split('\n')
                          .filter(Boolean)
                        updateField(index, 'options', { values })
                      }}
                    />
                  </Form.Item>
                )}
              </Space>
            </Card>
          )
        })}

        <Button type="dashed" onClick={addField} icon={<PlusOutlined />} block>
          添加字段
        </Button>
      </Card>

      <Form.Item>
        <Space>
          <Button type="primary" onClick={handleSubmit} loading={loading}>
            保存
          </Button>
          <Button onClick={onCancel}>取消</Button>
        </Space>
      </Form.Item>
    </Form>
  )
}

export default TemplateEditor
