import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Spin, ConfigProvider } from 'antd';
import './App.css';

// 懒加载页面组件
const Home = React.lazy(() => import('./pages/Home'));
const ChatPage = React.lazy(() => import('./pages/ChatPage'));

function App() {
  return (
    <ConfigProvider>
      <Router>
        <Suspense fallback={<div className="flex justify-center items-center h-screen"><Spin size="large" /></div>}>
          <Routes>
            <Route path="/" element={<Navigate to="/home" replace />} />
            <Route path="/home" element={<Home />} />
            <Route path="/chat/:type" element={<ChatPage />} />
            <Route path="*" element={<Navigate to="/home" replace />} />
          </Routes>
        </Suspense>
      </Router>
    </ConfigProvider>
  );
}

export default App;
