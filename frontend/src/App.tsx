import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import Layout from './components/Layout'
import Home from './pages/Home'
import Generator from './pages/Generator'
import Templates from './pages/Templates'
import AIGenerator from './pages/AIGenerator'
import APIDocs from './pages/APIDocs'
import ApiKeys from './pages/ApiKeys'
import History from './pages/History'

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/generator" element={<Generator />} />
            <Route path="/generator/:templateId" element={<Generator />} />
            <Route path="/templates" element={<Templates />} />
            <Route path="/templates/new" element={<Generator />} />
            <Route path="/templates/:templateId" element={<Generator />} />
            <Route path="/ai-generator" element={<AIGenerator />} />
            <Route path="/api-keys" element={<ApiKeys />} />
            <Route path="/history" element={<History />} />
            <Route path="/api-docs" element={<APIDocs />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </ConfigProvider>
  )
}

export default App
