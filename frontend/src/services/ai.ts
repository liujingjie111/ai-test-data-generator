import api from './api'
import type { AIResult } from '../types'

export const generateWithAI = (
  prompt: string,
  count: number,
): Promise<AIResult> => {
  return api.post('/ai/generate', { prompt, count })
}
