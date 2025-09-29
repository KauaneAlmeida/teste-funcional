/**
 * 🎯 CHAT WIDGET INTEGRADO COM BACKEND
 * 
 * Conecta diretamente com o backend Python FastAPI
 * Gerencia fluxo conversacional completo
 */

class ChatWidget {
    constructor() {
        this.isOpen = false;
        this.sessionId = null;
        this.messageCount = 0;
        this.flowCompleted = false;
        this.phoneCollected = false;
        this.currentStep = '';
        
        // 🔧 CONFIGURAÇÃO DO BACKEND
        this.backendUrl = this.detectBackendUrl();
        
        this.init();
    }

    detectBackendUrl() {
        // Detectar URL do backend baseado no ambiente
        const hostname = window.location.hostname;
        
        if (hostname.includes('replit') || hostname.includes('repl.co')) {
            // Ambiente Replit
            return 'https://law-firm-backend-936902782519-936902782519.us-central1.run.app';
        } else if (hostname === 'localhost' || hostname === '127.0.0.1') {
            // Desenvolvimento local
            return 'http://localhost:8000';
        } else {
            // Produção - usar a URL do backend configurada
            return 'https://law-firm-backend-936902782519-936902782519.us-central1.run.app';
        }
    }

    init() {
        this.createChatInterface();
        this.attachEventListeners();
        console.log('🚀 Chat Widget inicializado | Backend:', this.backendUrl);
    }

    createChatInterface() {
        // Criar container do chat
        const chatContainer = document.createElement('div');
        chatContainer.id = 'chat-widget';
        chatContainer.className = 'chat-widget';
        chatContainer.innerHTML = `
            <div class="chat-header">
                <div class="chat-header-info">
                    <div class="chat-avatar">⚖️</div>
                    <div class="chat-title">
                        <h4>m.lima Advogados</h4>
                        <span class="chat-status">Online</span>
                    </div>
                </div>
                <button class="chat-close" id="chat-close">×</button>
            </div>
            
            <div class="chat-messages" id="chat-messages">
                <div class="message bot-message">
                    <div class="message-content">
                        <p>Conectando com nosso sistema...</p>
                    </div>
                </div>
            </div>
            
            <div class="chat-input-container">
                <div class="chat-input-wrapper">
                    <input type="text" id="chat-input" placeholder="Digite sua mensagem..." disabled>
                    <button id="chat-send" disabled>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(chatContainer);
    }

    attachEventListeners() {
        // Botão launcher
        const launcher = document.getElementById('chat-launcher');
        if (launcher) {
            launcher.addEventListener('click', () => this.toggleChat());
        }

        // Botão fechar
        const closeBtn = document.getElementById('chat-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeChat());
        }

        // Input e envio
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send');

        if (input && sendBtn) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !input.disabled) {
                    this.sendMessage();
                }
            });

            sendBtn.addEventListener('click', () => {
                if (!sendBtn.disabled) {
                    this.sendMessage();
                }
            });
        }
    }

    async toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            await this.openChat();
        }
    }

    async openChat() {
        const chatWidget = document.getElementById('chat-widget');
        const launcher = document.getElementById('chat-launcher');
        
        if (chatWidget && launcher) {
            chatWidget.classList.add('open');
            launcher.style.display = 'none';
            this.isOpen = true;

            // Inicializar conversa se ainda não foi iniciada
            if (!this.sessionId) {
                await this.startConversation();
            }
        }
    }

    closeChat() {
        const chatWidget = document.getElementById('chat-widget');
        const launcher = document.getElementById('chat-launcher');
        
        if (chatWidget && launcher) {
            chatWidget.classList.remove('open');
            launcher.style.display = 'flex';
            this.isOpen = false;
        }
    }

    async startConversation() {
        try {
            console.log('🚀 Iniciando conversa com backend...');
            
            const response = await fetch(`${this.backendUrl}/api/v1/conversation/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            this.sessionId = data.session_id;
            this.messageCount = data.message_count || 0;
            this.flowCompleted = data.flow_completed || false;
            this.phoneCollected = data.phone_collected || false;

            console.log('✅ Conversa iniciada | Session:', this.sessionId);

            // Mostrar mensagem inicial
            this.clearMessages();
            this.addBotMessage(data.response);
            this.enableInput();

        } catch (error) {
            console.error('❌ Erro ao iniciar conversa:', error);
            this.clearMessages();
            this.addBotMessage('Desculpe, ocorreu um erro ao conectar. Tente novamente em alguns instantes.');
            this.enableInput();
        }
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message || !this.sessionId) return;

        // Adicionar mensagem do usuário
        this.addUserMessage(message);
        input.value = '';
        this.disableInput();

        try {
            console.log('📤 Enviando mensagem:', message);

            const response = await fetch(`${this.backendUrl}/api/v1/conversation/respond`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Atualizar estado
            this.messageCount = data.message_count || this.messageCount + 1;
            this.flowCompleted = data.flow_completed || false;
            this.phoneCollected = data.phone_collected || false;
            this.currentStep = data.current_step || '';

            console.log('✅ Resposta recebida | Step:', this.currentStep, '| Completed:', this.flowCompleted);

            // Mostrar resposta do bot
            this.addBotMessage(data.response);

            // Verificar se precisa coletar telefone
            if (this.flowCompleted && !this.phoneCollected) {
                setTimeout(() => {
                    this.showPhoneCollection();
                }, 1000);
            }

        } catch (error) {
            console.error('❌ Erro ao enviar mensagem:', error);
            this.addBotMessage('Desculpe, ocorreu um erro. Tente novamente.');
        } finally {
            this.enableInput();
        }
    }

    showPhoneCollection() {
        const messagesContainer = document.getElementById('chat-messages');
        
        const phoneDiv = document.createElement('div');
        phoneDiv.className = 'message bot-message phone-collection';
        phoneDiv.innerHTML = `
            <div class="message-content">
                <p>Para finalizar, preciso do seu WhatsApp com DDD:</p>
                <div class="phone-input-container">
                    <input type="tel" id="phone-input" placeholder="11999999999" maxlength="11">
                    <button id="phone-submit">Enviar</button>
                </div>
            </div>
        `;

        messagesContainer.appendChild(phoneDiv);
        this.scrollToBottom();

        // Event listeners para coleta de telefone
        const phoneInput = document.getElementById('phone-input');
        const phoneSubmit = document.getElementById('phone-submit');

        if (phoneInput && phoneSubmit) {
            phoneInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.submitPhone();
                }
            });

            phoneSubmit.addEventListener('click', () => {
                this.submitPhone();
            });

            phoneInput.focus();
        }
    }

    async submitPhone() {
        const phoneInput = document.getElementById('phone-input');
        const phone = phoneInput.value.trim();

        if (!phone || phone.length < 10) {
            alert('Por favor, digite um número válido com DDD (ex: 11999999999)');
            return;
        }

        try {
            console.log('📱 Enviando telefone:', phone);

            const response = await fetch(`${this.backendUrl}/api/v1/conversation/submit-phone`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    phone_number: phone,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Remover interface de coleta de telefone
            const phoneCollection = document.querySelector('.phone-collection');
            if (phoneCollection) {
                phoneCollection.remove();
            }

            // Mostrar mensagem de confirmação
            this.addBotMessage(data.message);
            this.phoneCollected = true;

            console.log('✅ Telefone enviado com sucesso');

        } catch (error) {
            console.error('❌ Erro ao enviar telefone:', error);
            alert('Erro ao enviar telefone. Tente novamente.');
        }
    }

    addUserMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${this.escapeHtml(message)}</p>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addBotMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${this.formatBotMessage(message)}</p>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatBotMessage(message) {
        // Converter quebras de linha e formatação básica
        return this.escapeHtml(message)
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    clearMessages() {
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            messagesContainer.innerHTML = '';
        }
    }

    enableInput() {
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send');
        
        if (input && sendBtn) {
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        }
    }

    disableInput() {
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send');
        
        if (input && sendBtn) {
            input.disabled = true;
            sendBtn.disabled = true;
        }
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
}

// 🚀 INICIALIZAR CHAT QUANDO DOM ESTIVER PRONTO
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎯 Inicializando Chat Widget...');
    window.chatWidget = new ChatWidget();
});

// Fallback para casos onde DOMContentLoaded já passou
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (!window.chatWidget) {
            console.log('🎯 Inicializando Chat Widget (fallback)...');
            window.chatWidget = new ChatWidget();
        }
    });
} else {
    if (!window.chatWidget) {
        console.log('🎯 Inicializando Chat Widget (imediato)...');
        window.chatWidget = new ChatWidget();
    }
}