import React from 'react'
import { Progress } from 'antd'

interface ProgressBarProps {
  percent: number
  status?: 'normal' | 'active' | 'success' | 'exception'
  showInfo?: boolean
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  percent,
  status = 'active',
  showInfo = true,
}) => {
  return <Progress percent={percent} status={status} showInfo={showInfo} />
}

export default ProgressBar
