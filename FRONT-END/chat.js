/**
 * 🎯 CHAT WIDGET INTEGRADO COM BACKEND - VERSÃO CORRIGIDA
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
        
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            // Desenvolvimento local
            return 'http://localhost:8000';
        } else if (hostname.includes('replit') || hostname.includes('repl.co')) {
            // Ambiente Replit - usar URL local do backend
            return 'http://localhost:8000';
        } else {
            // Produção ou outros ambientes
            return 'http://localhost:8000';
        }
    }

    init() {
        this.createChatInterface();
        this.attachEventListeners();
        console.log('🚀 Chat Widget inicializado | Backend:', this.backendUrl);
    }

    createChatInterface() {
        // Criar launcher button
        const launcher = document.createElement('div');
        launcher.className = 'chat-launcher';
        launcher.innerHTML = `
            <div class="chat-launcher-text">
                Fale com nosso assistente e seja direcionado a um advogado em minutos.
            </div>
            <div class="chat-launcher-icon">⚖️</div>
        `;
        document.body.appendChild(launcher);

        // Criar container do chat
        const chatRoot = document.createElement('div');
        chatRoot.id = 'chat-root';
        chatRoot.innerHTML = `
            <div class="chat-container">
                <div class="chat-header">
                    💼 Chat Advocacia — Escritório m.lima
                    <button class="chat-close-btn">×</button>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                </div>
                
                <div class="messages" id="chat-messages">
                    <div class="message bot">
                        <div class="bubble">
                            Conectando com nosso sistema...
                        </div>
                    </div>
                </div>
                
                <div class="input-area">
                    <input type="text" id="chat-input" placeholder="Digite sua mensagem..." disabled>
                    <button id="chat-send" disabled>Enviar</button>
                </div>
            </div>
        `;
        document.body.appendChild(chatRoot);
    }

    attachEventListeners() {
        // Botão launcher
        const launcher = document.querySelector('.chat-launcher');
        if (launcher) {
            launcher.addEventListener('click', () => this.toggleChat());
        }

        // Botão fechar
        const closeBtn = document.querySelector('.chat-close-btn');
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
        const chatRoot = document.getElementById('chat-root');
        const launcher = document.querySelector('.chat-launcher');
        
        if (chatRoot && launcher) {
            chatRoot.classList.add('active');
            launcher.style.display = 'none';
            this.isOpen = true;

            // Inicializar conversa se ainda não foi iniciada
            if (!this.sessionId) {
                await this.startConversation();
            }
        }
    }

    closeChat() {
        const chatRoot = document.getElementById('chat-root');
        const launcher = document.querySelector('.chat-launcher');
        
        if (chatRoot && launcher) {
            chatRoot.classList.remove('active');
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

        // Mostrar indicador de digitação
        this.showTypingIndicator();

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

            // Remover indicador de digitação
            this.hideTypingIndicator();

            // Mostrar resposta do bot
            this.addBotMessage(data.response);

            // Atualizar barra de progresso
            this.updateProgress();

            // Verificar se precisa coletar telefone
            if (this.flowCompleted && !this.phoneCollected) {
                setTimeout(() => {
                    this.showPhoneCollection();
                }, 1000);
            }

        } catch (error) {
            console.error('❌ Erro ao enviar mensagem:', error);
            this.hideTypingIndicator();
            this.addBotMessage('Desculpe, ocorreu um erro. Tente novamente.');
        } finally {
            this.enableInput();
        }
    }

    showPhoneCollection() {
        const messagesContainer = document.getElementById('chat-messages');
        
        const phoneDiv = document.createElement('div');
        phoneDiv.className = 'message bot phone-collection';
        phoneDiv.innerHTML = `
            <div class="bubble">
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
            this.updateProgress();

            console.log('✅ Telefone enviado com sucesso');

        } catch (error) {
            console.error('❌ Erro ao enviar telefone:', error);
            alert('Erro ao enviar telefone. Tente novamente.');
        }
    }

    addUserMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.innerHTML = `
            <div class="bubble">
                ${this.escapeHtml(message)}
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addBotMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        messageDiv.innerHTML = `
            <div class="bubble">
                ${this.formatBotMessage(message)}
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-message';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                Digitando<span></span><span></span><span></span>
            </div>
        `;

        messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingMessage = document.querySelector('.typing-message');
        if (typingMessage) {
            typingMessage.remove();
        }
    }

    updateProgress() {
        const progressFill = document.querySelector('.progress-fill');
        if (progressFill) {
            let progress = 0;
            
            if (this.messageCount >= 1) progress = 20;
            if (this.messageCount >= 2) progress = 40;
            if (this.messageCount >= 3) progress = 60;
            if (this.messageCount >= 4) progress = 80;
            if (this.flowCompleted && this.phoneCollected) progress = 100;
            
            progressFill.style.width = `${progress}%`;
        }
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