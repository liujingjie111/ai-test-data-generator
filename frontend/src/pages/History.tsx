import React, { useState, useEffect, useCallback } from 'react'
import { Table, Card, Button, message, Typography, Space, Select, Tag, Modal, Descriptions, Statistic, Row, Col, Popconfirm, Empty } from 'antd'
import { DeleteOutlined, EyeOutlined, ReloadOutlined } from '@ant-design/icons'
import { getHistoryList, getHistoryDetail, deleteHistory, getHistoryStats, batchDeleteHistory } from '../services/history'
import type { HistoryItem, HistoryDetail, HistoryStats as HistoryStatsType, HistoryListResponse } from '../services/history'
import type { Key } from 'react'

const { Title } = Typography

const generatorTypeOptions = [
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
  { value: 'full_address', label: '完整地址' },
  { value: 'bank_card', label: '银行卡号' },
  { value: 'credit_card', label: '信用卡号' },
  { value: 'bank_name', label: '开户行' },
  { value: 'amount', label: '金额' },
  { value: 'company_name', label: '公司名称' },
  { value: 'credit_code', label: '统一社会信用代码' },
  { value: 'industry', label: '行业' },
  { value: 'company_address', label: '公司地址' },
  { value: 'company_phone', label: '公司电话' },
  { value: 'product_name', label: '商品名称' },
  { value: 'sku', label: 'SKU' },
  { value: 'price', label: '价格' },
  { value: 'stock', label: '库存' },
  { value: 'category', label: '分类' },
  { value: 'uuid', label: 'UUID' },
  { value: 'ip', label: 'IP地址' },
  { value: 'url', label: 'URL' },
  { value: 'timestamp', label: '时间戳' },
]

const History: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [listData, setListData] = useState<HistoryListResponse | null>(null)
  const [stats, setStats] = useState<HistoryStatsType | null>(null)
  const [filterType, setFilterType] = useState<string | undefined>(undefined)
  const [filterStatus, setFilterStatus] = useState<string | undefined>(undefined)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(50)
  const [detailModalOpen, setDetailModalOpen] = useState(false)
  const [detailData, setDetailData] = useState<HistoryDetail | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [selectedRowKeys, setSelectedRowKeys] = useState<Key[]>([])

  const fetchList = useCallback(async () => {
    setLoading(true)
    try {
      const result = await getHistoryList({
        skip: (page - 1) * pageSize,
        limit: pageSize,
        generator_type: filterType,
        status: filterStatus,
      })
      setListData(result)
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : '获取历史记录失败'
      message.error(msg)
    } finally {
      setLoading(false)
    }
  }, [page, pageSize, filterType, filterStatus])

  const fetchStats = useCallback(async () => {
    try {
      const result = await getHistoryStats()
      setStats(result)
    } catch {
      // stats is optional
    }
  }, [])

  useEffect(() => {
    fetchList()
    fetchStats()
  }, [fetchList, fetchStats])

  const handleViewDetail = async (id: number) => {
    setDetailLoading(true)
    setDetailModalOpen(true)
    try {
      const result = await getHistoryDetail(id)
      setDetailData(result)
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : '获取详情失败'
      message.error(msg)
      setDetailModalOpen(false)
    } finally {
      setDetailLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await deleteHistory(id)
      message.success('已删除')
      fetchList()
      fetchStats()
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : '删除失败'
      message.error(msg)
    }
  }

  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning('请选择要删除的记录')
      return
    }

    try {
      await batchDeleteHistory({ ids: selectedRowKeys.map(id => Number(id)) })
      message.success(`已删除 ${selectedRowKeys.length} 条记录`)
      setSelectedRowKeys([])
      fetchList()
      fetchStats()
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : '批量删除失败'
      message.error(msg)
    }
  }

  const getStatusTag = (status: string) => {
    const config: Record<string, { color: string; text: string }> = {
      completed: { color: 'success', text: '已完成' },
      failed: { color: 'error', text: '失败' },
      running: { color: 'processing', text: '进行中' },
      pending: { color: 'default', text: '等待中' },
    }
    const item = config[status] || { color: 'default', text: status }
    return <Tag color={item.color}>{item.text}</Tag>
  }

  const formatDuration = (ms?: number) => {
    if (ms === undefined || ms === null) return '-'
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(2)}s`
  }

  const rowSelection = {
    selectedRowKeys,
    onChange: (newSelectedRowKeys: Key[]) => {
      setSelectedRowKeys(newSelectedRowKeys)
    },
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '生成器类型',
      dataIndex: 'generator_type',
      key: 'generator_type',
      width: 120,
    },
    {
      title: '生成数量',
      dataIndex: 'count',
      key: 'count',
      width: 100,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => getStatusTag(status),
    },
    {
      title: '耗时',
      dataIndex: 'duration_ms',
      key: 'duration_ms',
      width: 80,
      render: (val: number) => formatDuration(val),
    },
    {
      title: '生成时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (val: string) => new Date(val).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'actions',
      width: 140,
      render: (_: unknown, record: HistoryItem) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => handleViewDetail(record.id)}
          >
            详情
          </Button>
          <Popconfirm
            title="确认删除"
            description="确定要删除这条历史记录吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确认"
            cancelText="取消"
          >
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <Title level={4} style={{ margin: 0 }}>生成历史记录</Title>
          {selectedRowKeys.length > 0 && (
            <Space>
              <span style={{ color: '#1890ff' }}>已选择 {selectedRowKeys.length} 条记录</span>
              <Popconfirm
                title="确认批量删除"
                description={`确定要删除选中的 ${selectedRowKeys.length} 条历史记录吗？`}
                onConfirm={handleBatchDelete}
                okText="确认"
                cancelText="取消"
              >
                <Button danger icon={<DeleteOutlined />}>
                  批量删除
                </Button>
              </Popconfirm>
            </Space>
          )}
        </div>
        <Button icon={<ReloadOutlined />} onClick={() => { fetchList(); fetchStats() }}>
          刷新
        </Button>
      </div>

      {stats && (
        <Row gutter={16} style={{ marginBottom: 16 }}>
          <Col span={6}>
            <Card size="small">
              <Statistic title="总生成次数" value={stats.total_count} />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic title="总生成数量" value={stats.total_generated} />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic title="成功" value={stats.completed_count} valueStyle={{ color: '#3f8600' }} />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic title="失败" value={stats.failed_count} valueStyle={{ color: stats.failed_count > 0 ? '#cf1322' : undefined }} />
            </Card>
          </Col>
        </Row>
      )}

      <Card style={{ marginBottom: 16 }}>
        <Space>
          <span>生成器类型：</span>
          <Select
            allowClear
            placeholder="全部类型"
            style={{ width: 160 }}
            value={filterType}
            onChange={(val) => { setFilterType(val); setPage(1) }}
            options={generatorTypeOptions}
          />
          <span>状态：</span>
          <Select
            allowClear
            placeholder="全部状态"
            style={{ width: 120 }}
            value={filterStatus}
            onChange={(val) => { setFilterStatus(val); setPage(1) }}
            options={[
              { value: 'completed', label: '已完成' },
              { value: 'failed', label: '失败' },
              { value: 'running', label: '进行中' },
            ]}
          />
        </Space>
      </Card>

      <Card>
        <Table
          dataSource={listData?.items || []}
          columns={columns}
          rowKey="id"
          loading={loading}
          size="small"
          scroll={{ x: 'max-content' }}
          locale={{ emptyText: <Empty description="暂无历史记录" /> }}
          rowSelection={rowSelection}
          pagination={{
            current: page,
            pageSize: pageSize,
            total: listData?.total || 0,
            showSizeChanger: true,
            showQuickJumper: true,
            pageSizeOptions: ['10', '20', '50', '100', '200'],
            onChange: (p, ps) => { setPage(p); setPageSize(ps) },
            showTotal: (total) => `共 ${total} 条`,
          }}
        />
      </Card>

      <Modal
        title="历史记录详情"
        open={detailModalOpen}
        onCancel={() => { setDetailModalOpen(false); setDetailData(null) }}
        footer={null}
        width={800}
      >
        {detailLoading ? (
          <div style={{ textAlign: 'center', padding: '24px' }}>加载中...</div>
        ) : detailData ? (
          <div>
            <Descriptions column={2} bordered size="small" style={{ marginBottom: 16 }}>
              <Descriptions.Item label="ID">{detailData.id}</Descriptions.Item>
              <Descriptions.Item label="生成器类型">{detailData.generator_type}</Descriptions.Item>
              <Descriptions.Item label="生成数量">{detailData.count}</Descriptions.Item>
              <Descriptions.Item label="状态">{getStatusTag(detailData.status)}</Descriptions.Item>
              <Descriptions.Item label="耗时">{formatDuration(detailData.duration_ms)}</Descriptions.Item>
              <Descriptions.Item label="客户端 IP">{detailData.client_ip || '-'}</Descriptions.Item>
              <Descriptions.Item label="生成时间">{new Date(detailData.created_at).toLocaleString('zh-CN')}</Descriptions.Item>
              <Descriptions.Item label="完成时间">
                {detailData.completed_at ? new Date(detailData.completed_at).toLocaleString('zh-CN') : '-'}
              </Descriptions.Item>
              {detailData.error_msg && (
                <Descriptions.Item label="错误信息" span={2}>
                  <span style={{ color: '#cf1322' }}>{detailData.error_msg}</span>
                </Descriptions.Item>
              )}
            </Descriptions>

            {detailData.result_data && detailData.result_data.length > 0 && (
              <div>
                <Title level={5}>数据预览（前 {detailData.result_data.length} 条）</Title>
                <Table
                  dataSource={detailData.result_data.map((item, idx) => ({ ...item, _idx: idx + 1 }))}
                  columns={[
                    ...Object.keys(detailData.result_data[0] || {}).map(key => ({
                      title: key,
                      dataIndex: key,
                      key,
                      ellipsis: true,
                    })),
                  ]}
                  rowKey="_idx"
                  size="small"
                  scroll={{ x: 'max-content', y: 300 }}
                  pagination={false}
                />
              </div>
            )}
          </div>
        ) : null}
      </Modal>
    </div>
  )
}

export default History