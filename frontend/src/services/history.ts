import api from './api'

export interface HistoryItem {
  id: number
  generator_type: string
  count: number
  status: string
  error_msg?: string
  client_ip?: string
  created_at: string
  completed_at?: string
  duration_ms?: number
}

export interface HistoryDetail {
  id: number
  generator_type: string
  count: number
  status: string
  params?: Record<string, unknown>
  result_data?: Array<Record<string, unknown>>
  error_msg?: string
  client_ip?: string
  created_at: string
  completed_at?: string
  duration_ms?: number
}

export interface HistoryStats {
  total_count: number
  total_generated: number
  completed_count: number
  failed_count: number
}

export interface HistoryListResponse {
  items: HistoryItem[]
  total: number
  skip: number
  limit: number
}

export interface HistoryQueryParams {
  skip?: number
  limit?: number
  generator_type?: string
  status?: string
  date_from?: string
  date_to?: string
}

export interface BatchDeleteRequest {
  ids: number[]
}

export const getHistoryList = (params: HistoryQueryParams) =>
  api.get('/history', { params }) as Promise<HistoryListResponse>

export const getHistoryDetail = (id: number) =>
  api.get(`/history/${id}`) as Promise<HistoryDetail>

export const deleteHistory = (id: number) =>
  api.delete(`/history/${id}`)

export const batchDeleteHistory = (req: BatchDeleteRequest) =>
  api.post('/history/batch-delete', req)

export const getHistoryStats = () =>
  api.get('/history/stats') as Promise<HistoryStats>