import React, { useState, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Input, Button, message, Upload, Typography, Avatar, Divider, Tooltip } from 'antd';
import { SendOutlined, FileImageOutlined, AudioOutlined, FileTextOutlined, MessageOutlined } from '@ant-design/icons';

const { TextArea } = Input;
const { Text } = Typography;

type ChatType = 'text' | 'image' | 'audio' | 'pdf';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  content_blocks?: Array<{ type: string; content: string }>;
  timestamp: string;
  references?: Array<{ id: number; text: string; source: string; page: number }>;
}

interface ContentBlock {
  type: 'text' | 'image' | 'audio';
  content: string;
}

const ChatPage: React.FC = () => {
  const { type = 'text' } = useParams<{ type: ChatType }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [pdfName, setPdfName] = useState<string>('');
  const chatEndRef = useRef<HTMLDivElement>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const getTitleByType = (chatType: ChatType): string => {
    switch (chatType) {
      case 'text': return '智能问答';
      case 'image': return '图片分析';
      case 'audio': return '音频转写';
      case 'pdf': return 'PDF解析';
      default: return '智能问答';
    }
  };

  const getTypeColor = (chatType: ChatType): string => {
    switch (chatType) {
      case 'text': return 'from-blue-600 to-indigo-700';
      case 'image': return 'from-green-600 to-teal-700';
      case 'audio': return 'from-purple-600 to-violet-700';
      case 'pdf': return 'from-orange-600 to-amber-700';
      default: return 'from-blue-600 to-indigo-700';
    }
  };

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  const handleFileUpload = async (file: File) => {
    setUploading(true);
    try {
      if (type === 'image' && !file.type.startsWith('image/')) {
        message.error('请上传图片文件');
        setUploading(false);
        return false;
      }
      if (type === 'audio' && !file.type.startsWith('audio/')) {
        message.error('请上传音频文件');
        setUploading(false);
        return false;
      }
      if (type === 'pdf' && file.type !== 'application/pdf') {
        message.error('请上传PDF文件');
        setUploading(false);
        return false;
      }

      setUploadedFile(file);
      
      if (type === 'image') {
        setImageUrl(URL.createObjectURL(file));
        message.success('图片上传成功');
      } else if (type === 'audio') {
        setAudioUrl(URL.createObjectURL(file));
        message.success('音频上传成功');
      } else if (type === 'pdf') {
        setPdfName(file.name);
        message.success('PDF上传成功');
      }
      
      setUploading(false);
      return false;
    } catch (error) {
      message.error('文件上传失败');
      setUploading(false);
      return false;
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() && !uploadedFile) {
      message.warning('请输入消息或上传文件');
      return;
    }

    setLoading(true);
    
    const contentBlocks: ContentBlock[] = [{ type: 'text', content: inputValue }];
    
    if (imageUrl) {
      contentBlocks.push({ type: 'image', content: imageUrl });
    }
    
    if (audioUrl) {
      contentBlocks.push({ type: 'audio', content: audioUrl });
    }

    const userMessage: Message = {
      role: 'user',
      content: inputValue,
      content_blocks: contentBlocks,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    try {
      const formData = new FormData();
      formData.append('content_blocks', JSON.stringify(contentBlocks));
      formData.append('history', JSON.stringify(messages));
      
      if (uploadedFile) {
        if (type === 'image') {
          formData.append('image_file', uploadedFile);
        } else if (type === 'audio') {
          formData.append('audio_file', uploadedFile);
        } else if (type === 'pdf') {
          formData.append('pdf_file', uploadedFile);
        }
      }

      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('请求失败');
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法读取响应');
      }

      let assistantContent = '';
      let references: Array<{ id: number; text: string; source: string; page: number }> = [];

      const processStream = async () => {
        const { done, value } = await reader.read();
        
        if (done) {
          setLoading(false);
          setUploadedFile(null);
          setImageUrl(null);
          setAudioUrl(null);
          setPdfName('');
          return;
        }

        const chunk = new TextDecoder('utf-8').decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6);
            if (dataStr === '[DONE]') {
              break;
            }
            try {
              const data = JSON.parse(dataStr);
              if (data.type === 'content_delta') {
                assistantContent += data.content;
                updateAssistantMessage(assistantContent, references);
              } else if (data.type === 'message_complete') {
                assistantContent = data.full_content;
                references = data.references || [];
                updateAssistantMessage(assistantContent, references);
              } else if (data.type === 'error') {
                message.error(`错误: ${data.error}`);
                setLoading(false);
              }
            } catch (error) {
              console.error('解析流式数据失败:', error);
            }
          }
        }

        processStream();
      };

      processStream();
    } catch (error) {
      message.error('发送消息失败');
      setLoading(false);
    }
  };

  const updateAssistantMessage = (content: string, references: Array<{ id: number; text: string; source: string; page: number }>) => {
    setMessages(prev => {
      const newMessages = [...prev];
      // 找到最后一个 assistant 消息
      const assistantMessageIndex = [...newMessages].reverse().findIndex(msg => msg.role === 'assistant');
      const actualIndex = assistantMessageIndex !== -1 ? newMessages.length - 1 - assistantMessageIndex : -1;
      
      if (actualIndex !== -1) {
        // 更新现有消息
        newMessages[actualIndex] = {
          role: 'assistant',
          content,
          timestamp: newMessages[actualIndex].timestamp, // 保持原始时间戳
          references,
        };
      } else {
        // 添加新消息
        newMessages.push({
          role: 'assistant',
          content,
          timestamp: new Date().toISOString(),
          references,
        });
      }
      
      return newMessages;
    });
  };

  const renderMessageContent = (message: Message) => {
    if (message.role === 'user') {
      return (
        <div className="space-y-3">
          {message.content_blocks?.map((block, index) => {
            if (block.type === 'text' && block.content) {
              return <div key={index} className="text-gray-800">{block.content}</div>;
            } else if (block.type === 'image') {
              return (
                <div key={index} className="mt-3 rounded-lg overflow-hidden shadow-md transition-all duration-300 hover:shadow-lg">
                  <img 
                    src={block.content} 
                    alt="User uploaded" 
                    className="max-w-full max-h-80 rounded-lg object-cover"
                  />
                </div>
              );
            } else if (block.type === 'audio') {
              return (
                <div key={index} className="mt-3 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-sm">
                  <audio controls className="w-full h-12">
                    <source src={block.content} type="audio/*" />
                    您的浏览器不支持音频播放。
                  </audio>
                </div>
              );
            }
            return null;
          })}
          {type === 'pdf' && pdfName && (
            <div className="mt-3 p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg shadow-sm">
              <FileTextOutlined className="mr-2 text-orange-600" />
              <Text className="text-orange-800 font-medium">{pdfName}</Text>
            </div>
          )}
        </div>
      );
    } else {
      return (
        <div className="space-y-3">
          <div className="text-gray-800 leading-relaxed">{message.content}</div>
          {message.references && message.references.length > 0 && (
            <div className="mt-3 pt-3 border-t border-purple-100">
              <Text type="secondary" className="text-sm font-medium">引用来源：</Text>
              <div className="mt-2 space-y-2">
                {message.references.map(ref => (
                  <div key={ref.id} className="text-sm bg-purple-50 p-2 rounded-lg border border-purple-100">
                    <div className="font-medium text-purple-800 mb-1">[{ref.id}] {ref.text}</div>
                    {ref.page && <Text type="secondary" className="text-xs"> (第{ref.page}页)</Text>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }
  };

  const uploadProps = {
    accept: type === 'image' ? 'image/*' : type === 'audio' ? 'audio/*' : '.pdf',
    showUploadList: false,
    beforeUpload: handleFileUpload,
    loading: uploading,
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-indigo-50 to-purple-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <Card 
          className="shadow-xl rounded-xl overflow-hidden transition-all duration-300 hover:shadow-2xl"
          style={{ 
            borderRadius: '20px',
          }}
        >
          <div className={`bg-gradient-to-r ${getTypeColor(type)} text-white p-6`}>
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-full bg-white/20">
                <MessageOutlined className="text-white text-xl" />
              </div>
              <Typography.Title level={4} className="text-white mb-0 font-bold">
                {getTitleByType(type)}
              </Typography.Title>
            </div>
          </div>
          
          <div className="p-6 h-[650px] overflow-y-auto bg-white">
            <div className="space-y-8">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center py-20">
                  <div className="p-6 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 mb-6">
                    <MessageOutlined className="text-indigo-500 text-4xl" />
                  </div>
                  <Typography.Title level={5} className="text-gray-700 mb-3">
                    开始对话
                  </Typography.Title>
                  <Text className="text-gray-500 max-w-md">
                    {type === 'text' ? '输入您的问题，AI 将为您提供智能回答' : 
                     type === 'image' ? '上传图片并描述您的问题，AI 将根据图片内容进行分析' :
                     type === 'audio' ? '上传音频文件，AI 将进行转写并回答相关问题' :
                     '上传PDF文档，AI 将基于文档内容回答您的问题'}
                  </Text>
                </div>
              ) : (
                messages.map((message, index) => (
                  <div 
                    key={index} 
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
                  >
                    <div className={`flex items-start space-x-3 max-w-[85%] ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                      <Avatar 
                        size={40} 
                        className={`shadow-md ${message.role === 'user' ? 'bg-gradient-to-r from-blue-500 to-indigo-600' : 'bg-gradient-to-r from-purple-500 to-pink-600'}`}
                      >
                        {message.role === 'user' ? '我' : 'AI'}
                      </Avatar>
                      <div className={`
                        ${message.role === 'user' ? 
                          'bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-900 rounded-tl-3xl rounded-tr-xl rounded-bl-3xl' : 
                          'bg-gradient-to-r from-purple-50 to-pink-50 text-purple-900 rounded-tl-xl rounded-tr-3xl rounded-br-3xl'}
                        p-4 shadow-sm transition-all duration-300 hover:shadow-md
                      `}>
                        {renderMessageContent(message)}
                        <div className="mt-2 text-xs text-gray-500 font-medium">
                          {new Date(message.timestamp).toLocaleTimeString('zh-CN', { 
                            hour: '2-digit', 
                            minute: '2-digit',
                            second: '2-digit'
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              )}
              {loading && (
                <div className="flex justify-start">
                  <div className="flex items-start space-x-3 max-w-[85%]">
                    <Avatar size={40} className="bg-gradient-to-r from-purple-500 to-pink-600">AI</Avatar>
                    <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-tl-xl rounded-tr-3xl rounded-br-3xl shadow-sm">
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></div>
                        <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
          </div>
          
          <Divider className="m-0" />
          
          <div className="p-6 bg-white">
            {type !== 'text' && (
              <div className="mb-6">
                <Upload {...uploadProps}>
                  <Tooltip title={type === 'image' ? '上传图片' : type === 'audio' ? '上传音频' : '上传PDF'}>
                    <Button 
                      loading={uploading} 
                      icon={type === 'image' ? <FileImageOutlined /> : type === 'audio' ? <AudioOutlined /> : <FileTextOutlined />}
                      className={`bg-gradient-to-r ${getTypeColor(type)} text-white hover:opacity-90 transition-all duration-300`}
                    >
                      {type === 'image' ? '上传图片' : type === 'audio' ? '上传音频' : '上传PDF'}
                    </Button>
                  </Tooltip>
                </Upload>
                {uploadedFile && (
                  <div className="mt-3 p-3 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg shadow-sm">
                    <Text className="text-green-800 font-medium">已上传: {uploadedFile.name}</Text>
                  </div>
                )}
              </div>
            )}
            
            <div className="flex space-x-3">
              <TextArea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={`请输入${type === 'text' ? '问题' : type === 'image' ? '关于图片的问题' : type === 'audio' ? '关于音频的问题' : '关于PDF的问题'}`}
                rows={4}
                className="flex-1 rounded-xl shadow-sm border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-300"
                showCount
                maxLength={1000}
              />
              <Tooltip title="发送消息">
                <Button 
                  type="primary" 
                  icon={<SendOutlined />} 
                  onClick={handleSendMessage}
                  loading={loading}
                  className={`align-self-end p-4 rounded-xl bg-gradient-to-r ${getTypeColor(type)} text-white hover:opacity-90 transition-all duration-300 shadow-md hover:shadow-lg`}
                  size="large"
                />
              </Tooltip>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ChatPage;