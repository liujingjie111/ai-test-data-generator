import React, { useState } from 'react'
import { Layout, Menu, Typography } from 'antd'
import {
  HomeOutlined,
  SettingOutlined,
  FileTextOutlined,
  RobotOutlined,
  ApiOutlined,
  KeyOutlined,
  HistoryOutlined,
} from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'
import type { MenuProps } from 'antd'

const { Sider, Content, Header } = Layout
const { Title } = Typography

interface LayoutProps {
  children: React.ReactNode
}

const LayoutComponent: React.FC<LayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  const getSelectedMenuKey = (): string => {
    const path = location.pathname
    const match = path.match(/^\/generator\/\d+$/)
    if (match) {
      return '/templates'
    }
    return path
  }

  const menuItems: MenuProps['items'] = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '首页',
    },
    {
      key: '/generator',
      icon: <SettingOutlined />,
      label: '内置生成器',
    },
    {
      key: '/templates',
      icon: <FileTextOutlined />,
      label: '模板管理',
    },
    {
      key: '/ai-generator',
      icon: <RobotOutlined />,
      label: 'AI生成',
    },
    {
      key: '/api-keys',
      icon: <KeyOutlined />,
      label: 'API密钥',
    },
    {
      key: '/api-docs',
      icon: <ApiOutlined />,
      label: 'API文档',
    },
    {
      key: '/history',
      icon: <HistoryOutlined />,
      label: '历史记录',
    },
  ]

  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    navigate(key)
  }

  return (
    <Layout style={{ height: '100vh', overflow: 'hidden' }}>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={setCollapsed}
        style={{ overflow: 'auto', height: '100vh', position: 'sticky', top: 0, left: 0 }}
      >
        <div style={{ padding: '16px', textAlign: 'center' }}>
          <Title level={4} style={{ color: '#fff', margin: 0 }}>
            智能测试数据生成
          </Title>
        </div>
        <Menu
          theme="dark"
          selectedKeys={[getSelectedMenuKey()]}
          mode="inline"
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Sider>
      <Layout style={{ overflow: 'auto' }}>
        <Header style={{ background: '#fff', padding: '0 24px' }}>
          <Title level={3} style={{ margin: 0, lineHeight: '64px' }}>
            智能测试数据生成平台
          </Title>
        </Header>
        <Content style={{ margin: '16px', padding: 24, background: '#fff' }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  )
}

export default LayoutComponent
