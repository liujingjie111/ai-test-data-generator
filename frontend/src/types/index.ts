export interface TemplateField {
  type: string
  label: string
  required: boolean
  options?: Record<string, unknown>
}

export interface Template {
  id: number
  name: string
  description: string
  fields: TemplateField[]
  createdAt: string
  updatedAt: string
  created_at: string
  updated_at: string
}

export type GeneratorType = 'personal' | 'enterprise' | 'address' | 'finance' | 'product' | 'other'

export interface GeneratedItem {
  data: unknown
}

export interface GeneratorResult {
  count: number
  data: GeneratedItem[]
}

export interface AIResult {
  prompt: string
  count: number
  data: Record<string, unknown>[]
}

export interface ApiKey {
  id: number
  key: string
  name: string
  isActive: boolean
  is_active: boolean
  createdAt: string
  created_at: string
  expiresAt?: string
  expires_at?: string
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  message?: string
}
