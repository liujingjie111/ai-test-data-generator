import api from './api'
import type { ApiKey } from '../types'

export interface CreateApiKeyRequest {
  name: string
  expires_at?: string
}

export const getApiKeys = (): Promise<ApiKey[]> => {
  return api.get('/api-keys')
}

export const createApiKey = (data: CreateApiKeyRequest): Promise<ApiKey> => {
  return api.post('/api-keys', data)
}

export const deleteApiKey = (id: number): Promise<void> => {
  return api.delete(`/api-keys/${id}`)
}
