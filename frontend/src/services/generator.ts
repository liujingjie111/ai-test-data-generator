import api from './api'
import type { GeneratorResult } from '../types'

export const generateData = (
  generatorType: string,
  count: number,
  params?: Record<string, unknown>,
): Promise<GeneratorResult> => {
  return api.post('/generate', {
    generator_type: generatorType,
    count,
    params,
  })
}

export const exportData = (
  generatorType: string,
  count: number,
  format: string,
): Promise<Blob> => {
  return api.post(`/generate/${generatorType}/export?format=${format}`, { count }, {
    responseType: 'blob',
  })
}