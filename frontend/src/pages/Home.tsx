import React from 'react'
import { Card, Row, Col, Typography, Button, Space } from 'antd'
import { useNavigate } from 'react-router-dom'
import {
  ThunderboltOutlined,
  FileTextOutlined,
  RobotOutlined,
  ExportOutlined,
} from '@ant-design/icons'

const { Title, Paragraph } = Typography

interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
  link: string
}

const features: FeatureCardProps[] = [
  {
    icon: <ThunderboltOutlined />,
    title: '内置生成器',
    description: '20+种预设数据类型，快速生成各类测试数据',
    link: '/generator',
  },
  {
    icon: <FileTextOutlined />,
    title: '自定义模板',
    description: '灵活定义模板，满足复杂数据结构需求',
    link: '/templates',
  },
  {
    icon: <RobotOutlined />,
    title: 'AI智能生成',
    description: '自然语言描述需求，AI自动生成测试数据',
    link: '/ai-generator',
  },
  {
    icon: <ExportOutlined />,
    title: '批量导出',
    description: '支持 JSON、CSV、Excel、SQL 多种格式导出',
    link: '/generator',
  },
]

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, link }) => {
  const navigate = useNavigate()

  return (
    <Card
      hoverable
      onClick={() => navigate(link)}
      style={{ height: '100%' }}
    >
      <Card.Meta
        avatar={
          <div style={{ fontSize: '32px', color: '#1677ff' }}>
            {icon}
          </div>
        }
        title={<Title level={5}>{title}</Title>}
        description={description}
      />
    </Card>
  )
}

const Home: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div>
      <div style={{ textAlign: 'center', marginBottom: 64 }}>
        <Title>智能测试数据生成平台</Title>
        <Paragraph style={{ fontSize: 16, color: '#666' }}>
          快速生成高质量的测试数据，提升测试效率
        </Paragraph>
        <Space>
          <Button
            type="primary"
            size="large"
            icon={<ThunderboltOutlined />}
            onClick={() => navigate('/generator')}
          >
            立即生成
          </Button>
          <Button
            size="large"
            icon={<RobotOutlined />}
            onClick={() => navigate('/ai-generator')}
          >
            AI生成
          </Button>
        </Space>
      </div>

      <Row gutter={[24, 24]}>
        {features.map((feature, index) => (
          <Col xs={24} sm={12} lg={6} key={index}>
            <FeatureCard {...feature} />
          </Col>
        ))}
      </Row>
    </div>
  )
}

export default Home
