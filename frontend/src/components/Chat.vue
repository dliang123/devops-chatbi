<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
}

const messages = ref<Message[]>([{
  id: 1,
  text: "Hello! How can I help you today?",
  sender: 'bot'
}]);
const newMessage = ref('');
const messageId = ref(2);

const sendMessage = async () => {
  if (newMessage.value.trim() === '') return;

  const userMessage: Message = {
    id: messageId.value++,
    text: newMessage.value,
    sender: 'user',
  };
  messages.value.push(userMessage);
  const userQuestion = newMessage.value;
  newMessage.value = '';

  try {
    const response = await axios.post(import.meta.env.VITE_API_URL, { message: userQuestion });
    const botMessage: Message = {
      id: messageId.value++,
      text: response.data.response,
      sender: 'bot',
    };
    messages.value.push(botMessage);
  } catch (error) {
    console.error('Error sending message:', error);
    const errorMessage: Message = {
      id: messageId.value++,
      text: 'Sorry, something went wrong. Please try again later.',
      sender: 'bot',
    };
    messages.value.push(errorMessage);
  }
};
</script>

<template>
  <div class="chat-container">
    <div class="messages-display">
      <div v-for="message in messages" :key="message.id" :class="['message', message.sender]">
        <p>{{ message.text }}</p>
      </div>
    </div>
    <div class="message-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="Type your message..."
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}

.messages-display {
  flex-grow: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.message {
  margin-bottom: 10px;
  padding: 8px 12px;
  border-radius: 15px;
  max-width: 70%;
}

.message.user {
  background-color: #e0f7fa;
  align-self: flex-end;
  margin-left: auto;
  text-align: right;
}

.message.bot {
  background-color: #e3f2fd;
  align-self: flex-start;
  margin-right: auto;
  text-align: left;
}

.message p {
  margin: 0;
  line-height: 1.4;
}

.message-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #eee;
  background-color: #fff;
}

.message-input input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  margin-right: 10px;
  font-size: 16px;
}

.message-input input:focus {
  outline: none;
  border-color: #007bff;
}

.message-input button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.2s;
}

.message-input button:hover {
  background-color: #0056b3;
}
</style>
