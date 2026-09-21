<!DOCTYPE html>
<html lang="ko" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Socrates AI Tutor - 개인 맞춤형 AI 튜터링</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#f0f9ff',
                            100: '#e0f2fe',
                            500: '#0284c7',
                            600: '#0284c7',
                            700: '#0369a1',
                            900: '#0c4a6e',
                        }
                    }
                }
            }
        }
    </script>
    
    <!-- FontAwesome Icons CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Marked.js Markdown Parser -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
    <!-- Highlight.js for Code Highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>

    <!-- Custom CSS Styles -->
    <style>
        /* Custom Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }
        .dark ::-webkit-scrollbar-thumb {
            background: #475569;
        }
        
        /* Markdown Content Styling */
        .markdown-body pre {
            background-color: #1e293b;
            color: #f8fafc;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .markdown-body code:not(pre code) {
            background-color: rgba(148, 163, 184, 0.2);
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.875em;
        }
        .markdown-body p {
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }
        .markdown-body ul, .markdown-body ol {
            margin-left: 1.25rem;
            margin-bottom: 0.5rem;
        }
        .markdown-body ul { list-style-type: disc; }
        .markdown-body ol { list-style-type: decimal; }
    </style>
</head>
<body class="h-full bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-100 flex flex-col font-sans transition-colors duration-200">

    <!-- Header Navigation Bar -->
    <header class="h-16 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 px-4 flex items-center justify-between z-10 shrink-0">
        <div class="flex items-center gap-3">
            <button id="toggle-sidebar-btn" class="md:hidden text-slate-600 dark:text-slate-300 p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg">
                <i class="fa-solid fa-bars text-lg"></i>
            </button>
            <div class="flex items-center gap-2">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-md">
                    <i class="fa-solid fa-graduation-cap text-lg"></i>
                </div>
                <span class="font-bold text-lg bg-gradient-to-r from-sky-600 to-indigo-600 dark:from-sky-400 dark:to-indigo-400 bg-clip-text text-transparent">Socrates AI</span>
            </div>
        </div>

        <!-- Subject Selector & Control Buttons -->
        <div class="flex items-center gap-2 md:gap-4">
            <!-- Active Subject Dropdown -->
            <div class="relative">
                <select id="subject-selector" class="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-sm font-medium py-2 px-3 pr-8 rounded-lg border-none focus:ring-2 focus:ring-sky-500 cursor-pointer">
                    <option value="coding">💻 프로그래밍 / 코딩</option>
                    <option value="math">📐 수학 (Math)</option>
                    <option value="language">🗣️ 외국어 (Language)</option>
                    <option value="science">🔬 과학 (Science)</option>
                    <option value="history">📜 역사 (History)</option>
                    <option value="general">🧠 일반 / 기타 (General)</option>
                </select>
            </div>

            <!-- Dark / Light Mode Toggle Button -->
            <button id="theme-toggle-btn" class="p-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors" title="다크/라이트 모드">
                <i class="fa-solid fa-moon text-lg dark:hidden"></i>
                <i class="fa-solid fa-sun text-lg hidden dark:block text-amber-400"></i>
            </button>

            <!-- API Key & Settings Button -->
            <button id="open-settings-btn" class="p-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors relative" title="설정">
                <i class="fa-solid fa-gear text-lg"></i>
                <span id="api-key-badge" class="absolute top-1 right-1 w-2.5 h-2.5 bg-red-500 rounded-full"></span>
            </button>
        </div>
    </header>

    <!-- Main Three-Pane Layout Container -->
    <div class="flex-1 flex overflow-hidden relative">
        
        <!-- LEFT SIDEBAR: History & Subjects -->
        <aside id="left-sidebar" class="absolute md:relative inset-y-0 left-0 w-64 bg-white dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800 z-20 transform -translate-x-full md:translate-x-0 transition-transform duration-200 ease-in-out flex flex-col shrink-0">
            <div class="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                <h2 class="font-semibold text-slate-700 dark:text-slate-200 text-sm uppercase tracking-wider">학습 공간</h2>
                <button id="new-chat-btn" class="text-xs bg-sky-500 hover:bg-sky-600 text-white font-medium px-2.5 py-1.5 rounded-lg flex items-center gap-1.5 shadow-sm transition-all">
                    <i class="fa-solid fa-plus"></i> 새 질문
                </button>
            </div>
            
            <!-- Chat Sessions List -->
            <div class="flex-1 overflow-y-auto p-3 space-y-1" id="chat-history-list">
                <!-- Dynamically Rendered History Items -->
            </div>

            <!-- Sidebar Footer -->
            <div class="p-3 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400 flex justify-between items-center">
                <span>학습 모드: 소크라테스식</span>
                <i class="fa-solid fa-lightbulb text-amber-500"></i>
            </div>
        </aside>

        <!-- CENTER PANEL: Interactive AI Chat Area -->
        <main class="flex-1 flex flex-col min-w-0 bg-slate-50 dark:bg-slate-900 relative">
            
            <!-- Chat Control Bar -->
            <div class="px-4 py-2 bg-white/80 dark:bg-slate-950/80 backdrop-blur border-b border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span id="current-subject-label" class="font-medium text-slate-700 dark:text-slate-300">프로그래밍 모드</span>
                </div>
                <div class="flex gap-2">
                    <button id="generate-summary-btn" class="hover:text-sky-500 flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded transition-colors">
                        <i class="fa-solid fa-wand-magic-sparkles text-sky-500"></i> 개념 요약
                    </button>
                    <button id="generate-quiz-btn" class="hover:text-indigo-500 flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded transition-colors">
                        <i class="fa-solid fa-clipboard-question text-indigo-500"></i> 퀴즈 생성
                    </button>
                </div>
            </div>

            <!-- Messages Conversation Display -->
            <div id="messages-container" class="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
                <!-- Initial Welcome Screen -->
                <div id="welcome-screen" class="h-full flex flex-col items-center justify-center text-center p-6 max-w-lg mx-auto">
                    <div class="w-16 h-16 rounded-full bg-sky-100 dark:bg-sky-950 flex items-center justify-center text-sky-500 text-2xl mb-4 shadow-inner">
                        <i class="fa-solid fa-brain"></i>
                    </div>
                    <h1 class="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-2">안녕하세요! AI 튜터입니다.</h1>
                    <p class="text-sm text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
                        정답을 그대로 알려주는 대신, 스스로 답을 찾아갈 수 있도록 질문을 던지며 돕습니다. 무엇이 궁금하신가요?
                    </p>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full text-left text-xs">
                        <button onclick="app.sendPreset('Python에서 리스트와 튜플의 차이점은 무엇인가요?')" class="p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-sky-500 dark:hover:border-sky-500 transition-all shadow-sm">
                            <span class="font-semibold block text-slate-700 dark:text-slate-200 mb-1">💻 코딩</span>
                            리스트와 튜플의 차이점 설명해줘
                        </button>
                        <button onclick="app.sendPreset('미적분학에서 도함수의 직관적인 의미가 궁금해요.')" class="p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-sky-500 dark:hover:border-sky-500 transition-all shadow-sm">
                            <span class="font-semibold block text-slate-700 dark:text-slate-200 mb-1">📐 수학</span>
                            도함수의 직관적인 개념이 뭐야?
                        </button>
                        <button onclick="app.sendPreset('영어 시제 중에서 Present Perfect(현재완료)의 용법을 쉽게 이해하고 싶어요.')" class="p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-sky-500 dark:hover:border-sky-500 transition-all shadow-sm">
                            <span class="font-semibold block text-slate-700 dark:text-slate-200 mb-1">🗣️ 언어</span>
                            현재완료 시제 구분법 알려줘
                        </button>
                        <button onclick="app.sendPreset('광합성 과정에서 빛이 왜 필요한지 단계별로 알고 싶어요.')" class="p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-sky-500 dark:hover:border-sky-500 transition-all shadow-sm">
                            <span class="font-semibold block text-slate-700 dark:text-slate-200 mb-1">🔬 과학</span>
                            식물이 광합성을 하는 원리 설명해줘
                        </button>
                    </div>
                </div>
            </div>

            <!-- Bottom User Prompt Input Bar -->
            <div class="p-3 md:p-4 bg-white dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800 shrink-0">
                <form id="chat-form" class="max-w-4xl mx-auto flex items-end gap-2 bg-slate-100 dark:bg-slate-800/80 rounded-2xl p-2 border border-transparent focus-within:border-sky-500 dark:focus-within:border-sky-500 transition-all">
                    <textarea id="user-input" rows="1" placeholder="배우고 싶은 개념이나 질문을 입력하세요... (Shift+Enter 줄바꿈)" class="flex-1 bg-transparent border-none outline-none resize-none p-2 text-sm max-h-32 text-slate-800 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500"></textarea>
                    <button type="submit" id="send-btn" class="w-10 h-10 rounded-xl bg-sky-500 hover:bg-sky-600 text-white flex items-center justify-center shrink-0 disabled:opacity-50 transition-all shadow-md">
                        <i class="fa-solid fa-paper-plane text-sm"></i>
                    </button>
                </form>
            </div>
        </main>

        <!-- RIGHT SIDEBAR / PANEL: Summaries, Quizzes & Notes -->
        <aside id="right-panel" class="w-80 bg-white dark:bg-slate-950 border-l border-slate-200 dark:border-slate-800 flex flex-col shrink-0 hidden lg:flex">
            <!-- Tabs Header -->
            <div class="flex border-b border-slate-200 dark:border-slate-800">
                <button data-tab="summary" class="panel-tab flex-1 py-3 text-xs font-semibold text-center text-sky-600 dark:text-sky-400 border-b-2 border-sky-500 transition-all">
                    <i class="fa-solid fa-list-check mb-1 block text-sm"></i> 개념 요약
                </button>
                <button data-tab="quiz" class="panel-tab flex-1 py-3 text-xs font-semibold text-center text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-all">
                    <i class="fa-solid fa-graduation-cap mb-1 block text-sm"></i> AI 퀴즈
                </button>
                <button data-tab="notes" class="panel-tab flex-1 py-3 text-xs font-semibold text-center text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-all">
                    <i class="fa-solid fa-bookmark mb-1 block text-sm"></i> 학습 노트
                </button>
            </div>

            <!-- Tab Contents -->
            <div class="flex-1 overflow-y-auto p-4">
                <!-- Summary Tab Content -->
                <div id="tab-summary" class="tab-content space-y-3">
                    <div class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed mb-3">
                        대화 내용을 바탕으로 핵심 개념을 자동 추출합니다.
                    </div>
                    <div id="summary-cards-container" class="space-y-3">
                        <div class="text-center py-8 text-slate-400 text-xs">
                            <i class="fa-regular fa-lightbulb text-2xl mb-2 block"></i>
                            상단의 '개념 요약' 버튼을 눌러 요약 카드를 생성하세요.
                        </div>
                    </div>
                </div>

                <!-- Quiz Tab Content -->
                <div id="tab-quiz" class="tab-content hidden space-y-4">
                    <div class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                        현재 대화 내용 기반으로 3개의 맞춤형 테스트 문제를 생성합니다.
                    </div>
                    <div id="quiz-container" class="space-y-4">
                        <div class="text-center py-8 text-slate-400 text-xs">
                            <i class="fa-solid fa-clipboard-question text-2xl mb-2 block"></i>
                            '퀴즈 생성' 버튼을 눌러 학습을 평가하세요.
                        </div>
                    </div>
                </div>

                <!-- Notes Tab Content -->
                <div id="tab-notes" class="tab-content hidden space-y-3">
                    <div id="saved-notes-container" class="space-y-3">
                        <div class="text-center py-8 text-slate-400 text-xs">
                            <i class="fa-regular fa-bookmark text-2xl mb-2 block"></i>
                            저장된 학습 노트가 없습니다.
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    </div>

    <!-- API Key Settings Modal -->
    <div id="settings-modal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 shadow-xl transform transition-all">
            <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-lg text-slate-800 dark:text-slate-100 flex items-center gap-2">
                    <i class="fa-solid fa-key text-sky-500"></i> Gemini API 키 설정
                </h3>
                <button id="close-settings-btn" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mb-4 leading-relaxed">
                구글 Gemini API 키를 입력하세요. 입력된 키는 서버로 전송되지 않으며, 사용자 브라우저의 LocalStorage에만 안전하게 보관됩니다.
            </p>
            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">API Key</label>
                    <input type="password" id="api-key-input" placeholder="AIzaSy..." class="w-full bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-800 dark:text-slate-100 outline-none focus:ring-2 focus:ring-sky-500">
                </div>
                <div class="flex items-center justify-between text-xs">
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" class="text-sky-500 hover:underline flex items-center gap-1">
                        API 키 발급받기 <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                </div>
                <div class="flex justify-end gap-2 pt-2">
                    <button id="save-settings-btn" class="bg-sky-500 hover:bg-sky-600 text-white font-medium text-sm px-4 py-2 rounded-xl transition-all shadow-md">
                        저장하기
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast Notification Container -->
    <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none"></div>

    <script>
        /**
         * Socrates AI Tutor Application Core Script
         * Manages state, API calls, TTS, UI interactions, and storage.
         */
        class AITutorApp {
            constructor() {
                // Application State
                this.apiKey = localStorage.getItem('socrates_gemini_key') || '';
                this.theme = localStorage.getItem('socrates_theme') || 'light';
                this.currentSubject = 'coding';
                this.chats = JSON.parse(localStorage.getItem('socrates_chats') || '[]');
                this.activeChatId = null;
                this.notes = JSON.parse(localStorage.getItem('socrates_notes') || '[]');
                this.isGenerating = false;

                // Model Constants
                this.MODEL_NAME = 'gemini-3-flash-preview';

                // Subject Prompts Configuration
                this.subjectPrompts = {
                    coding: "당신은 세계적인 수석 소프트웨어 엔지니어이자 소크라테스식 코딩 튜터입니다.",
                    math: "당신은 친절하고 명확한 수학 튜터입니다. 직관적인 개념 이해를 돕습니다.",
                    language: "당신은 언어학 전공 교정이자 자연스러운 외국어 학습을 돕는 튜터입니다.",
                    science: "당신은 탐구 중심의 호기심을 유발하는 원리 중심 과학 튜터입니다.",
                    history: "당신은 역사의 인과관계와 맥락을 흥미롭게 이야기해주는 역사 튜터입니다.",
                    general: "당신은 모든 분야의 학습을 자발적으로 돕는 지능형 학습 페이스메이커입니다."
                };

                // Initialize App Component
                this.initApp();
            }

            initApp() {
                this.applyTheme(this.theme);
                this.bindEvents();
                this.updateApiKeyBadge();
                this.renderHistoryList();
                this.renderSavedNotes();
                
                // Initialize Marked Library
                marked.setOptions({
                    highlight: function(code, lang) {
                        const language = hljs.getLanguage(lang) ? lang : 'plaintext';
                        return hljs.highlight(code, { language }).value;
                    },
                    langPrefix: 'hljs language-'
                });

                // Auto Key Prompt on First Load
                if (!this.apiKey) {
                    setTimeout(() => this.toggleModal('settings-modal', true), 500);
                }
            }

            /* --- Event Binding --- */
            bindEvents() {
                // Theme Switcher
                document.getElementById('theme-toggle-btn').addEventListener('click', () => {
                    this.theme = this.theme === 'light' ? 'dark' : 'light';
                    this.applyTheme(this.theme);
                });

                // Settings Modal Triggers
                document.getElementById('open-settings-btn').addEventListener('click', () => this.toggleModal('settings-modal', true));
                document.getElementById('close-settings-btn').addEventListener('click', () => this.toggleModal('settings-modal', false));
                document.getElementById('save-settings-btn').addEventListener('click', () => this.saveApiKey());

                // Subject Selection Change
                document.getElementById('subject-selector').addEventListener('change', (e) => {
                    this.currentSubject = e.target.value;
                    const labels = { coding: '프로그래밍 모드', math: '수학 모드', language: '외국어 모드', science: '과학 모드', history: '역사 모드', general: '일반 학습 모드' };
                    document.getElementById('current-subject-label').textContent = labels[this.currentSubject];
                    this.showToast(`${labels[this.currentSubject]}로 변경되었습니다.`, 'info');
                });

                // Chat Form Submission
                const form = document.getElementById('chat-form');
                const textarea = document.getElementById('user-input');

                textarea.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        form.dispatchEvent(new Event('submit'));
                    }
                });

                form.addEventListener('submit', (e) => {
                    e.preventDefault();
                    this.handleUserSubmit();
                });

                // New Chat Button
                document.getElementById('new-chat-btn').addEventListener('click', () => this.createNewChat());

                // Right Panel Auxiliary Generators
                document.getElementById('generate-summary-btn').addEventListener('click', () => this.generateSummaryCards());
                document.getElementById('generate-quiz-btn').addEventListener('click', () => this.generateQuiz());

                // Right Sidebar Tabs
                document.querySelectorAll('.panel-tab').forEach(tab => {
                    tab.addEventListener('click', (e) => {
                        const target = e.currentTarget.getAttribute('data-tab');
                        this.switchRightTab(target);
                    });
                });

                // Mobile Sidebar Toggle Button
                document.getElementById('toggle-sidebar-btn').addEventListener('click', () => {
                    const sidebar = document.getElementById('left-sidebar');
                    sidebar.classList.toggle('-translate-x-full');
                });
            }

            /* --- Theme & UI Helpers --- */
            applyTheme(theme) {
                if (theme === 'dark') {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
                localStorage.setItem('socrates_theme', theme);
            }

            toggleModal(id, show) {
                const modal = document.getElementById(id);
                if (show) modal.classList.remove('hidden');
                else modal.classList.add('hidden');
            }

            showToast(message, type = 'info') {
                const container = document.getElementById('toast-container');
                const toast = document.createElement('div');
                const colors = {
                    info: 'bg-slate-800 text-white',
                    success: 'bg-emerald-600 text-white',
                    error: 'bg-red-600 text-white'
                };
                
                toast.className = `pointer-events-auto flex items-center gap-2 px-4 py-3 rounded-xl text-xs font-medium shadow-lg transition-all transform translate-y-2 opacity-0 ${colors[type]}`;
                toast.innerHTML = `<span>${message}</span>`;
                
                container.appendChild(toast);
                
                requestAnimationFrame(() => {
                    toast.classList.remove('translate-y-2', 'opacity-0');
                });

                setTimeout(() => {
                    toast.classList.add('opacity-0', 'translate-y-2');
                    setTimeout(() => toast.remove(), 300);
                }, 3000);
            }

            updateApiKeyBadge() {
                const badge = document.getElementById('api-key-badge');
                if (this.apiKey) {
                    badge.classList.remove('bg-red-500');
                    badge.classList.add('bg-emerald-500');
                } else {
                    badge.classList.remove('bg-emerald-500');
                    badge.classList.add('bg-red-500');
                }
            }

            saveApiKey() {
                const val = document.getElementById('api-key-input').value.trim();
                if (!val) {
                    this.showToast('올바른 API 키를 입력하세요.', 'error');
                    return;
                }
                this.apiKey = val;
                localStorage.setItem('socrates_gemini_key', val);
                this.updateApiKeyBadge();
                this.toggleModal('settings-modal', false);
                this.showToast('API 키가 성공적으로 저장되었습니다.', 'success');
            }

            switchRightTab(tabName) {
                document.querySelectorAll('.panel-tab').forEach(btn => {
                    if (btn.getAttribute('data-tab') === tabName) {
                        btn.classList.add('text-sky-600', 'dark:text-sky-400', 'border-b-2', 'border-sky-500');
                        btn.classList.remove('text-slate-500', 'dark:text-slate-400');
                    } else {
                        btn.classList.remove('text-sky-600', 'dark:text-sky-400', 'border-b-2', 'border-sky-500');
                        btn.classList.add('text-slate-500', 'dark:text-slate-400');
                    }
                });

                document.querySelectorAll('.tab-content').forEach(content => {
                    if (content.id === `tab-${tabName}`) {
                        content.classList.remove('hidden');
                    } else {
                        content.classList.add('hidden');
                    }
                });
            }

            /* --- Chat Session Management --- */
            createNewChat() {
                const newChat = {
                    id: Date.now().toString(),
                    title: '새로운 학습 대화',
                    subject: this.currentSubject,
                    messages: []
                };
                this.chats.unshift(newChat);
                this.activeChatId = newChat.id;
                this.saveChats();
                this.renderHistoryList();
                this.renderActiveChat();
            }

            saveChats() {
                localStorage.setItem('socrates_chats', JSON.stringify(this.chats));
            }

            getActiveChat() {
                return this.chats.find(c => c.id === this.activeChatId);
            }

            renderHistoryList() {
                const container = document.getElementById('chat-history-list');
                container.innerHTML = '';

                if (this.chats.length === 0) {
                    container.innerHTML = `<div class="text-xs text-center text-slate-400 py-4">대화 기록이 없습니다.</div>`;
                    return;
                }

                this.chats.forEach(chat => {
                    const isActive = chat.id === this.activeChatId;
                    const item = document.createElement('div');
                    item.className = `group flex items-center justify-between p-2.5 rounded-xl cursor-pointer text-xs transition-all ${
                        isActive ? 'bg-sky-50 dark:bg-sky-950/50 text-sky-600 dark:text-sky-400 font-semibold' : 'hover:bg-slate-100 dark:hover:bg-slate-900 text-slate-600 dark:text-slate-400'
                    }`;
                    
                    item.innerHTML = `
                        <div class="flex items-center gap-2 overflow-hidden flex-1" onclick="app.selectChat('${chat.id}')">
                            <i class="fa-regular fa-message shrink-0"></i>
                            <span class="truncate">${chat.title}</span>
                        </div>
                        <button onclick="app.deleteChat('${chat.id}', event)" class="opacity-0 group-hover:opacity-100 p-1 hover:text-red-500 transition-opacity">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    `;
                    container.appendChild(item);
                });
            }

            selectChat(chatId) {
                this.activeChatId = chatId;
                this.renderHistoryList();
                this.renderActiveChat();
            }

            deleteChat(chatId, e) {
                e.stopPropagation();
                this.chats = this.chats.filter(c => c.id !== chatId);
                if (this.activeChatId === chatId) {
                    this.activeChatId = this.chats.length > 0 ? this.chats[0].id : null;
                }
                this.saveChats();
                this.renderHistoryList();
                this.renderActiveChat();
                this.showToast('대화가 삭제되었습니다.', 'info');
            }

            renderActiveChat() {
                const container = document.getElementById('messages-container');
                const chat = this.getActiveChat();

                if (!chat || chat.messages.length === 0) {
                    container.innerHTML = document.getElementById('welcome-screen').outerHTML;
                    return;
                }

                container.innerHTML = '';
                chat.messages.forEach((msg, idx) => {
                    this.appendMessageUI(msg.role, msg.text, idx);
                });
                container.scrollTop = container.scrollHeight;
            }

            /* --- Chat UI & Interaction --- */
            sendPreset(text) {
                document.getElementById('user-input').value = text;
                document.getElementById('chat-form').dispatchEvent(new Event('submit'));
            }

            async handleUserSubmit() {
                if (this.isGenerating) return;

                if (!this.apiKey) {
                    this.showToast('Gemini API 키를 등록해야 합니다.', 'error');
                    this.toggleModal('settings-modal', true);
                    return;
                }

                const textarea = document.getElementById('user-input');
                const userText = textarea.value.trim();
                if (!userText) return;

                textarea.value = '';
                textarea.style.height = 'auto';

                // Ensure active chat session
                if (!this.activeChatId) {
                    const newChat = {
                        id: Date.now().toString(),
                        title: userText.substring(0, 20) + '...',
                        subject: this.currentSubject,
                        messages: []
                    };
                    this.chats.unshift(newChat);
                    this.activeChatId = newChat.id;
                }

                const activeChat = this.getActiveChat();
                if (activeChat.messages.length === 0) {
                    activeChat.title = userText.substring(0, 18) + '...';
                }

                // Add User Message
                activeChat.messages.push({ role: 'user', text: userText });
                this.saveChats();
                this.renderHistoryList();
                this.renderActiveChat();

                // Generate AI Response
                await this.requestAIResponse(userText);
            }

            appendMessageUI(role, text, index) {
                const container = document.getElementById('messages-container');
                const isUser = role === 'user';

                const wrapper = document.createElement('div');
                wrapper.className = `flex gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'} mb-4`;

                const avatar = document.createElement('div');
                avatar.className = `w-8 h-8 rounded-xl flex items-center justify-center shrink-0 text-xs text-white shadow-sm ${
                    isUser ? 'bg-slate-700 dark:bg-slate-600' : 'bg-sky-500'
                }`;
                avatar.innerHTML = isUser ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

                const body = document.createElement('div');
                body.className = `flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[85%]`;

                const bubble = document.createElement('div');
                bubble.className = `p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
                    isUser 
                        ? 'bg-sky-500 text-white rounded-tr-none' 
                        : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-slate-700/80 rounded-tl-none markdown-body'
                }`;

                if (isUser) {
                    bubble.textContent = text;
                } else {
                    bubble.innerHTML = marked.parse(text);
                }

                body.appendChild(bubble);

                // Add Action Buttons for AI responses
                if (!isUser) {
                    const actions = document.createElement('div');
                    actions.className = 'flex items-center gap-3 mt-1.5 px-1 text-[11px] text-slate-400 dark:text-slate-500';
                    actions.innerHTML = `
                        <button onclick="app.speakText(\`${this.escapeQuote(text)}\`)" class="hover:text-sky-500 transition-colors flex items-center gap-1">
                            <i class="fa-solid fa-volume-high"></i> 음성 듣기
                        </button>
                        <button onclick="app.saveToNotes(\`${this.escapeQuote(text)}\`)" class="hover:text-sky-500 transition-colors flex items-center gap-1">
                            <i class="fa-regular fa-bookmark"></i> 노트 저장
                        </button>
                    `;
                    body.appendChild(actions);
                }

                wrapper.appendChild(avatar);
                wrapper.appendChild(body);
                container.appendChild(wrapper);

                container.scrollTop = container.scrollHeight;
            }

            escapeQuote(text) {
                return text.replace(/`/g, '\\`').replace(/"/g, '&quot;').replace(/\n/g, ' ');
            }

            /* --- Gemini API Integration --- */
            async requestAIResponse(userQuery) {
                this.isGenerating = true;
                this.showLoadingIndicator();

                const systemInstruction = `
${this.subjectPrompts[this.currentSubject]}

[중요 튜터링 지침 - 소크라테스 대화식 연출]
1. 정답이나 공식, 코드를 바로 모두 알려주지 마세요.
2. 학습자가 스스로 생각할 수 있도록 유도하는 1~2개의 질문이나 작은 힌트를 먼저 제공하세요.
3. 친절하고 격려하는 한국어 어조를 유지하세요.
4. 핵심 문맥에 맞춰 가볍고 명확하게 설명하세요.
                `;

                const activeChat = this.getActiveChat();
                const contentsPayload = activeChat.messages.map(m => ({
                    role: m.role === 'user' ? 'user' : 'model',
                    parts: [{ text: m.text }]
                }));

                try {
                    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${this.MODEL_NAME}:generateContent?key=${this.apiKey}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: contentsPayload,
                            systemInstruction: { parts: [{ text: systemInstruction }] }
                        })
                    });

                    const data = await response.json();
                    this.removeLoadingIndicator();

                    if (data.error) {
                        throw new Error(data.error.message || 'API 오류 발생');
                    }

                    const aiReply = data.candidates?.[0]?.content?.parts?.[0]?.text || '답변을 생성할 수 없습니다.';
                    
                    activeChat.messages.push({ role: 'model', text: aiReply });
                    this.saveChats();
                    this.renderActiveChat();

                } catch (err) {
                    this.removeLoadingIndicator();
                    this.showToast(`오류: ${err.message}`, 'error');
                } finally {
                    this.isGenerating = false;
                }
            }

            showLoadingIndicator() {
                const container = document.getElementById('messages-container');
                const indicator = document.createElement('div');
                indicator.id = 'ai-loading';
                indicator.className = 'flex gap-3 max-w-3xl mr-auto mb-4';
                indicator.innerHTML = `
                    <div class="w-8 h-8 rounded-xl bg-sky-500 flex items-center justify-center shrink-0 text-xs text-white">
                        <i class="fa-solid fa-robot"></i>
                    </div>
                    <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 p-4 rounded-2xl rounded-tl-none flex items-center gap-2">
                        <div class="w-2 h-2 rounded-full bg-sky-500 animate-bounce"></div>
                        <div class="w-2 h-2 rounded-full bg-sky-500 animate-bounce [animation-delay:-0.15s]"></div>
                        <div class="w-2 h-2 rounded-full bg-sky-500 animate-bounce [animation-delay:-0.3s]"></div>
                    </div>
                `;
                container.appendChild(indicator);
                container.scrollTop = container.scrollHeight;
            }

            removeLoadingIndicator() {
                const el = document.getElementById('ai-loading');
                if (el) el.remove();
            }

            /* --- Auxiliary Features: TTS, Summary, Quiz, Notes --- */
            speakText(text) {
                if (!('speechSynthesis' in window)) {
                    this.showToast('이 브라우저는 음성 합성을 지원하지 않습니다.', 'error');
                    return;
                }

                window.speechSynthesis.cancel(); // Clear existing queue

                // Clean Markdown syntax for cleaner speech
                const cleanText = text.replace(/[#*`_~]/g, '');

                const utterance = new SpeechSynthesisUtterance(cleanText);
                utterance.lang = 'ko-KR';
                utterance.rate = 1.0;

                window.speechSynthesis.speak(utterance);
                this.showToast('음성 재생을 시작합니다.', 'info');
            }

            async generateSummaryCards() {
                const activeChat = this.getActiveChat();
                if (!activeChat || activeChat.messages.length === 0) {
                    this.showToast('요약할 대화 내용이 없습니다.', 'error');
                    return;
                }

                this.switchRightTab('summary');
                const container = document.getElementById('summary-cards-container');
                container.innerHTML = `<div class="text-center py-8 text-sky-500 text-xs"><i class="fa-solid fa-spinner fa-spin text-xl mb-2 block"></i>개념 요약 카드 생성 중...</div>`;

                const conversationContext = activeChat.messages.map(m => `${m.role}: ${m.text}`).join('\n');
                const prompt = `다음 대화 내용에서 핵심 공부 개념 2~3개를 요약 카드로 정리해줘. JSON 포맷으로 출력해줘.\n대화 내용:\n${conversationContext}`;

                try {
                    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${this.MODEL_NAME}:generateContent?key=${this.apiKey}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{ parts: [{ text: prompt }] }],
                            generationConfig: {
                                responseMimeType: "application/json",
                                responseSchema: {
                                    type: "ARRAY",
                                    items: {
                                        type: "OBJECT",
                                        properties: {
                                            title: { type: "STRING" },
                                            description: { type: "STRING" },
                                            keyTakeaway: { type: "STRING" }
                                        },
                                        required: ["title", "description", "keyTakeaway"]
                                    }
                                }
                            }
                        })
                    });

                    const result = await response.json();
                    const cardsData = JSON.parse(result.candidates[0].content.parts[0].text);

                    container.innerHTML = '';
                    cardsData.forEach(card => {
                        const cardEl = document.createElement('div');
                        cardEl.className = 'bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl shadow-sm space-y-2';
                        cardEl.innerHTML = `
                            <h4 class="font-bold text-xs text-sky-600 dark:text-sky-400 flex items-center justify-between">
                                <span>📌 ${card.title}</span>
                                <button onclick="app.saveToNotes('**${card.title}**\\n${card.description}\\n*핵심*: ${card.keyTakeaway}')" class="text-slate-400 hover:text-sky-500">
                                    <i class="fa-regular fa-bookmark"></i>
                                </button>
                            </h4>
                            <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">${card.description}</p>
                            <div class="text-[11px] bg-white dark:bg-slate-800 p-2 rounded-lg text-slate-500 dark:text-slate-400 border border-slate-100 dark:border-slate-700/50">
                                💡 <span class="font-medium">Point:</span> ${card.keyTakeaway}
                            </div>
                        `;
                        container.appendChild(cardEl);
                    });

                } catch (err) {
                    container.innerHTML = `<div class="text-center py-8 text-red-500 text-xs">요약 생성 실패: ${err.message}</div>`;
                }
            }

            async generateQuiz() {
                const activeChat = this.getActiveChat();
                if (!activeChat || activeChat.messages.length === 0) {
                    this.showToast('퀴즈를 생성할 대화 내용이 없습니다.', 'error');
                    return;
                }

                this.switchRightTab('quiz');
                const container = document.getElementById('quiz-container');
                container.innerHTML = `<div class="text-center py-8 text-indigo-500 text-xs"><i class="fa-solid fa-spinner fa-spin text-xl mb-2 block"></i>맞춤형 퀴즈 3문항 생성 중...</div>`;

                const conversationContext = activeChat.messages.map(m => `${m.role}: ${m.text}`).join('\n');
                const prompt = `대화 내용을 바탕으로 학습 이해도를 측정할 4지선다형 퀴즈 3개를 만들어줘. JSON 배열 형태로 답해줘.\n대화 내용:\n${conversationContext}`;

                try {
                    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${this.MODEL_NAME}:generateContent?key=${this.apiKey}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{ parts: [{ text: prompt }] }],
                            generationConfig: {
                                responseMimeType: "application/json",
                                responseSchema: {
                                    type: "ARRAY",
                                    items: {
                                        type: "OBJECT",
                                        properties: {
                                            question: { type: "STRING" },
                                            options: { type: "ARRAY", items: { type: "STRING" } },
                                            answerIndex: { type: "INTEGER" },
                                            explanation: { type: "STRING" }
                                        },
                                        required: ["question", "options", "answerIndex", "explanation"]
                                    }
                                }
                            }
                        })
                    });

                    const result = await response.json();
                    const quizzes = JSON.parse(result.candidates[0].content.parts[0].text);

                    container.innerHTML = '';
                    quizzes.forEach((q, qIdx) => {
                        const qEl = document.createElement('div');
                        qEl.className = 'bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl space-y-3';
                        
                        let optionsHTML = q.options.map((opt, oIdx) => `
                            <button onclick="app.checkAnswer(${qIdx}, ${oIdx}, ${q.answerIndex}, '${this.escapeQuote(q.explanation)}')" 
                                id="quiz-opt-${qIdx}-${oIdx}" 
                                class="w-full text-left p-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs hover:border-sky-500 transition-all">
                                ${oIdx + 1}. ${opt}
                            </button>
                        `).join('');

                        qEl.innerHTML = `
                            <div class="font-bold text-xs text-slate-800 dark:text-slate-100">Q${qIdx + 1}. ${q.question}</div>
                            <div class="space-y-1.5" id="quiz-options-${qIdx}">${optionsHTML}</div>
                            <div id="quiz-exp-${qIdx}" class="hidden text-[11px] p-2 bg-sky-50 dark:bg-sky-950/40 text-sky-700 dark:text-sky-300 rounded-lg"></div>
                        `;
                        container.appendChild(qEl);
                    });

                } catch (err) {
                    container.innerHTML = `<div class="text-center py-8 text-red-500 text-xs">퀴즈 생성 실패: ${err.message}</div>`;
                }
            }

            checkAnswer(qIdx, selectedIdx, correctIdx, explanation) {
                const optionsContainer = document.getElementById(`quiz-options-${qIdx}`);
                const expContainer = document.getElementById(`quiz-exp-${qIdx}`);
                
                const buttons = optionsContainer.querySelectorAll('button');
                buttons.forEach((btn, idx) => {
                    btn.disabled = true;
                    if (idx === correctIdx) {
                        btn.classList.add('bg-emerald-500', 'text-white', 'border-emerald-500');
                    } else if (idx === selectedIdx) {
                        btn.classList.add('bg-red-500', 'text-white', 'border-red-500');
                    }
                });

                expContainer.classList.remove('hidden');
                expContainer.innerHTML = `<strong>${selectedIdx === correctIdx ? '정답입니다! 🎉' : '아쉽네요. 😅'}</strong><br>${explanation}`;
            }

            saveToNotes(content) {
                const note = {
                    id: Date.now().toString(),
                    date: new Date().toLocaleDateString('ko-KR'),
                    content: content
                };
                this.notes.unshift(note);
                localStorage.setItem('socrates_notes', JSON.stringify(this.notes));
                this.renderSavedNotes();
                this.showToast('학습 노트에 저장되었습니다.', 'success');
            }

            renderSavedNotes() {
                const container = document.getElementById('saved-notes-container');
                container.innerHTML = '';

                if (this.notes.length === 0) {
                    container.innerHTML = `<div class="text-center py-8 text-slate-400 text-xs"><i class="fa-regular fa-bookmark text-2xl mb-2 block"></i>저장된 학습 노트가 없습니다.</div>`;
                    return;
                }

                this.notes.forEach(note => {
                    const noteEl = document.createElement('div');
                    noteEl.className = 'bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-3 rounded-xl space-y-2 relative group';
                    noteEl.innerHTML = `
                        <div class="flex justify-between items-center text-[10px] text-slate-400">
                            <span>${note.date}</span>
                            <button onclick="app.deleteNote('${note.id}')" class="text-slate-400 hover:text-red-500">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        </div>
                        <div class="text-xs text-slate-700 dark:text-slate-300 markdown-body">${marked.parse(note.content)}</div>
                    `;
                    container.appendChild(noteEl);
                });
            }

            deleteNote(id) {
                this.notes = this.notes.filter(n => n.id !== id);
                localStorage.setItem('socrates_notes', JSON.stringify(this.notes));
                this.renderSavedNotes();
                this.showToast('노트가 삭제되었습니다.', 'info');
            }
        }

        // Initialize App Instance on Window Load
        let app;
        window.addEventListener('DOMContentLoaded', () => {
            app = new AITutorApp();
        });
    </script>
</body>
</html>
