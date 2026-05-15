import * as XLSX from 'xlsx'

/**
 * 导出数据为 JSON 格式
 * @param data 要导出的数据数组
 * @param filename 文件名
 */
export function exportToJSON(
  data: Record<string, unknown>[],
  filename: string,
): void {
  const jsonStr = JSON.stringify(data, null, 2)
  const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8;' })
  triggerDownload(blob, filename)
}

/**
 * 导出数据为 CSV 格式（Excel 兼容）
 * @param data 要导出的数据数组
 * @param filename 文件名
 */
export function exportToCSV(
  data: Record<string, unknown>[],
  filename: string,
): void {
  if (!data || data.length === 0) return

  const headers = Object.keys(data[0])
  const csvRows: string[] = []

  csvRows.push(headers.map(escapeCSVField).join(','))

  for (const row of data) {
    const values = headers.map((header) => {
      const val = row[header]
      if (val === null || val === undefined) return ''
      return escapeCSVField(String(val))
    })
    csvRows.push(values.join(','))
  }

  const csvContent = '\ufeff' + csvRows.join('\r\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  triggerDownload(blob, filename)
}

/**
 * 转义 CSV 字段，确保 Excel 兼容性
 * @param field CSV 字段值
 * @returns 转义后的字段值
 */
function escapeCSVField(field: string): string {
  if (field.includes(',') || field.includes('"') || field.includes('\n') || field.includes('\r')) {
    return `"${field.replace(/"/g, '""')}"`
  }
  return field
}

/**
 * 导出数据为 Excel (XLSX) 格式
 * @param data 要导出的数据数组
 * @param filename 文件名
 */
export function exportToExcel(
  data: Record<string, unknown>[],
  filename: string,
): void {
  if (!data || data.length === 0) return

  const worksheet = XLSX.utils.json_to_sheet(data)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')

  const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
  const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8;' })
  triggerDownload(blob, filename)
}

/**
 * 导出数据为 SQL 格式（包含表结构定义）
 * @param data 要导出的数据数组
 * @param tableName 表名
 * @param filename 文件名
 */
export function exportToSQL(
  data: Record<string, unknown>[],
  tableName: string,
  filename: string,
): void {
  if (!data || data.length === 0) return

  const headers = Object.keys(data[0])
  const statements: string[] = []

  statements.push('-- 自动生成的 SQL 数据导出文件')
  statements.push(`-- 导出时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`)
  statements.push('')

  statements.push(`-- 创建表结构`)
  const columnDefs = headers.map((col) => {
    const sampleVal = data[0][col]
    let columnType = 'TEXT'
    if (typeof sampleVal === 'number') {
      columnType = Number.isInteger(sampleVal) ? 'INTEGER' : 'REAL'
    }
    return `  ${col} ${columnType}`
  })
  statements.push(`CREATE TABLE IF NOT EXISTS ${tableName} (`)
  statements.push(columnDefs.join(',\n'))
  statements.push(');')
  statements.push('')

  statements.push('-- 插入数据')
  for (const row of data) {
    const columns = headers.join(', ')
    const values = headers.map((col) => {
      const val = row[col]
      if (val === null || val === undefined) return 'NULL'
      if (typeof val === 'number') return String(val)
      const escaped = String(val).replace(/'/g, "''")
      return `'${escaped}'`
    })
    statements.push(`INSERT INTO ${tableName} (${columns}) VALUES (${values.join(', ')});`)
  }

  statements.push('')
  statements.push('-- 数据导出完成')

  const sqlContent = statements.join('\n')
  const blob = new Blob([sqlContent], { type: 'text/plain;charset=utf-8;' })
  triggerDownload(blob, filename)
}

/**
 * 触发浏览器下载
 * @param blob 要下载的 Blob 对象
 * @param filename 文件名
 */
function triggerDownload(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
