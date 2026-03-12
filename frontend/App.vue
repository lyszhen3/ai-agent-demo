<template>
  <div id="app">
    <div class="chat-container">
      <h1>AI Agent Chat</h1>
      
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          :class="['message', message.role]"
        >
          <div class="message-content">
            <strong>{{ message.role === 'user' ? '你' : 'AI' }}:</strong>
            <p>{{ message.content }}</p>
          </div>
        </div>
        
        <div v-if="loading" class="message ai">
          <div class="message-content">
            <strong>AI:</strong>
            <p>正在思考...</p>
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <input 
          v-model="inputMessage"
          @keyup.enter="sendMessage"
          placeholder="输入消息..."
          :disabled="loading"
        />
        <button @click="sendMessage" :disabled="loading || !inputMessage.trim()">
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick } from 'vue'

export default {
  name: 'ChatApp',
  setup() {
    const messages = ref([])
    const inputMessage = ref('')
    const loading = ref(false)
    const messagesContainer = ref(null)

    const scrollToBottom = async () => {
      await nextTick()
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    const sendMessage = async () => {
      if (!inputMessage.value.trim() || loading.value) return

      const userMessage = inputMessage.value.trim()
      messages.value.push({
        role: 'user',
        content: userMessage
      })

      inputMessage.value = ''
      loading.value = true

      try {
        const response = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: userMessage,
            conversation_id: 'default'
          })
        })

        if (!response.ok) {
          throw new Error('请求失败')
        }

        const data = await response.json()
        messages.value.push({
          role: 'ai',
          content: data.response
        })
      } catch (error) {
        messages.value.push({
          role: 'ai',
          content: `错误：${error.message}`
        })
      } finally {
        loading.value = false
        await scrollToBottom()
      }
    }

    return {
      messages,
      inputMessage,
      loading,
      messagesContainer,
      sendMessage
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

#app {
  width: 100%;
  max-width: 800px;
  height: 90vh;
}

.chat-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

h1 {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  text-align: center;
  margin: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  display: flex;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  justify-content: flex-end;
}

.message.ai {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.ai .message-content {
  background: #f0f0f0;
  color: #333;
  border-bottom-left-radius: 4px;
}

.message-content strong {
  display: block;
  margin-bottom: 5px;
  font-size: 0.9em;
  opacity: 0.8;
}

.message-content p {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background: #fafafa;
}

.chat-input input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.chat-input input:focus {
  border-color: #667eea;
}

.chat-input input:disabled {
  background: #f0f0f0;
  cursor: not-allowed;
}

.chat-input button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.chat-input button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.chat-input button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
