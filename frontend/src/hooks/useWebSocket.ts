import { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';

const WS_URL = import.meta.env.VITE_API_URL?.replace('http', 'ws') || 'ws://localhost:8000';

export const useWebSocket = (sessionId: string, customerId: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    // Create WebSocket connection
    const socket = io(WS_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    socketRef.current = socket;

    socket.on('connect', () => {
      console.log('✓ WebSocket connected');
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('✗ WebSocket disconnected');
      setIsConnected(false);
    });

    socket.on('message', (data: any) => {
      setLastMessage(data);
    });

    socket.on('error', (error: any) => {
      console.error('WebSocket error:', error);
    });

    return () => {
      socket.disconnect();
    };
  }, [sessionId, customerId]);

  const sendMessage = (message: string) => {
    if (socketRef.current && isConnected) {
      socketRef.current.emit('chat', {
        message,
        session_id: sessionId,
        customer_id: customerId,
      });
    }
  };

  return {
    isConnected,
    sendMessage,
    lastMessage,
  };
};
