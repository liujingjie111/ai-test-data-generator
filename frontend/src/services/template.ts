import api from './api'
import type { Template } from '../types'

export const getTemplates = (): Promise<Template[]> => {
  return api.get('/templates')
}

export const getTemplate = (id: number): Promise<Template> => {
  return api.get(`/templates/${id}`)
}

export const createTemplate = (data: Omit<Template, 'id' | 'createdAt' | 'updatedAt'>): Promise<Template> => {
  return api.post('/templates', data)
}

export const updateTemplate = (
  id: number,
  data: Partial<Omit<Template, 'id' | 'createdAt' | 'updatedAt'>>,
): Promise<Template> => {
  return api.put(`/templates/${id}`, data)
}

export const deleteTemplate = (id: number): Promise<void> => {
  return api.delete(`/templates/${id}`)
}

export const copyTemplate = (id: number): Promise<Template> => {
  return api.post(`/templates/${id}/copy`)
}
