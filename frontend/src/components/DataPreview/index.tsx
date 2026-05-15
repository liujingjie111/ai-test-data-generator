import React from 'react'
import { Table, Button, Space } from 'antd'
import { DownloadOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'

interface DataPreviewProps {
  dataSource: Record<string, unknown>[]
  columns: ColumnsType<Record<string, unknown>>
  loading: boolean
  onExport?: (format: string) => void
}

const DataPreview: React.FC<DataPreviewProps> = ({
  dataSource,
  columns,
  loading,
  onExport,
}) => {
  return (
    <div>
      {onExport && (
        <Space style={{ marginBottom: 16 }}>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => onExport('json')}
          >
            导出 JSON
          </Button>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => onExport('csv')}
          >
            导出 CSV
          </Button>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => onExport('excel')}
          >
            导出 Excel
          </Button>
        </Space>
      )}
      <Table
        columns={columns}
        dataSource={dataSource}
        loading={loading}
        rowKey={(_, index) => String(index)}
        pagination={{ pageSize: 10, showSizeChanger: true }}
        scroll={{ x: 'max-content' }}
      />
    </div>
  )
}

export default DataPreview
