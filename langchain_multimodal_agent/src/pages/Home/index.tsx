import React from 'react';
import { Card, Row, Col, Typography, Button, Space, Divider } from 'antd';
import { MessageOutlined, PictureOutlined, AudioOutlined, FileTextOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;

const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: '智能问答',
      description: '与大模型进行纯文本对话，获取智能回答',
      icon: <MessageOutlined className="text-white text-4xl" />,
      path: '/chat/text',
      color: 'blue',
      gradient: 'from-blue-500 to-blue-700',
      bgColor: 'bg-blue-50',
      hoverColor: 'hover:from-blue-600 hover:to-blue-800',
    },
    {
      title: '图片分析',
      description: '上传图片，大模型根据图片内容进行分析回答',
      icon: <PictureOutlined className="text-white text-4xl" />,
      path: '/chat/image',
      color: 'green',
      gradient: 'from-green-500 to-green-700',
      bgColor: 'bg-green-50',
      hoverColor: 'hover:from-green-600 hover:to-green-800',
    },
    {
      title: '音频转写',
      description: '上传音频，大模型进行转写并回答相关问题',
      icon: <AudioOutlined className="text-white text-4xl" />,
      path: '/chat/audio',
      color: 'purple',
      gradient: 'from-purple-500 to-purple-700',
      bgColor: 'bg-purple-50',
      hoverColor: 'hover:from-purple-600 hover:to-purple-800',
    },
    {
      title: 'PDF解析',
      description: '上传PDF文档，大模型基于文档内容回答问题',
      icon: <FileTextOutlined className="text-white text-4xl" />,
      path: '/chat/pdf',
      color: 'orange',
      gradient: 'from-orange-500 to-orange-700',
      bgColor: 'bg-orange-50',
      hoverColor: 'hover:from-orange-600 hover:to-orange-800',
    },
  ];

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-20">
          <div className="inline-block p-3 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 mb-6">
            <MessageOutlined className="text-white text-5xl" />
          </div>
          <Title level={1} className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 mb-6">
            多模态大模型RAG系统
          </Title>
          <Paragraph className="text-xl text-gray-700 max-w-3xl mx-auto leading-relaxed">
            基于先进的大语言模型，支持文本、图片、音频和PDF文档的智能分析与问答，为您提供全方位的AI助手服务
          </Paragraph>
          <Divider className="my-10 max-w-2xl mx-auto" />
        </div>

        <Row gutter={[24, 24]} className="justify-center">
          {features.map((feature, index) => (
            <Col key={index} xs={24} sm={12} md={6}>
              <Card
                hoverable
                className={`h-full border-0 shadow-xl transition-all duration-400 hover:shadow-2xl hover:-translate-y-2 transform-gpu`}
                style={{ 
                  borderRadius: '20px',
                  overflow: 'hidden',
                }}
              >
                <div className="flex flex-col items-center text-center p-8">
                  <div className={`p-6 rounded-full bg-gradient-to-r ${feature.gradient} mb-6 shadow-lg transition-all duration-300 hover:scale-110`}>
                    {feature.icon}
                  </div>
                  <h3 className={`text-2xl font-bold mb-3 text-${feature.color}-700`}>{feature.title}</h3>
                  <p className="text-gray-600 mb-8 leading-relaxed">{feature.description}</p>
                  <Button
                    type="primary"
                    size="large"
                    onClick={() => handleNavigate(feature.path)}
                    className={`bg-gradient-to-r ${feature.gradient} ${feature.hoverColor} text-white px-8 py-3 rounded-full shadow-md transition-all duration-300 hover:shadow-lg hover:scale-105`}
                  >
                    开始使用
                  </Button>
                </div>
              </Card>
            </Col>
          ))}
        </Row>

        <div className="mt-24 text-center">
          <Card className="max-w-4xl mx-auto shadow-xl rounded-2xl overflow-hidden border-0">
            <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-10">
              <Typography>
                <Title level={4} className="text-2xl font-bold text-gray-800 mb-8">系统特点</Title>
                <Space orientation="vertical" size="large" style={{ display: 'block' }}>
                  <Paragraph className="text-lg text-gray-700 leading-relaxed">
                    <span className="inline-block p-2 mr-3 rounded-full bg-blue-100 text-blue-600 font-bold">01</span>
                    <strong>流式输出</strong>：答案实时生成，逐步展示，提升交互体验
                  </Paragraph>
                  <Paragraph className="text-lg text-gray-700 leading-relaxed">
                    <span className="inline-block p-2 mr-3 rounded-full bg-green-100 text-green-600 font-bold">02</span>
                    <strong>多模态支持</strong>：整合文本、图像、音频、文档等多种信息源
                  </Paragraph>
                  <Paragraph className="text-lg text-gray-700 leading-relaxed">
                    <span className="inline-block p-2 mr-3 rounded-full bg-purple-100 text-purple-600 font-bold">03</span>
                    <strong>智能分析</strong>：基于先进的大语言模型，提供准确的分析和回答
                  </Paragraph>
                  <Paragraph className="text-lg text-gray-700 leading-relaxed">
                    <span className="inline-block p-2 mr-3 rounded-full bg-orange-100 text-orange-600 font-bold">04</span>
                    <strong>引用溯源</strong>：PDF文档问答中提供内容引用，确保回答的可靠性
                  </Paragraph>
                </Space>
              </Typography>
            </div>
          </Card>
        </div>

        <div className="mt-20 text-center">
          <Button
            type="primary"
            size="large"
            onClick={() => handleNavigate('/chat/text')}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-10 py-3 rounded-full shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
          >
            立即开始对话
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Home;