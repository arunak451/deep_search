// ============================================
// DEEPDIG — XPLORE IT CORP PREMIUM APP.JS
// ============================================

// Global State
let currentResearchData = null;

// DOM Elements
const searchSection = document.getElementById('search-section');
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const selectSection = document.getElementById('results-select-section');
const resultsList = document.getElementById('search-results-list');
const cancelSearchBtn = document.getElementById('cancel-search-btn');
const progressSection = document.getElementById('progress-section');
const reportSection = document.getElementById('report-section');
const newSearchBtn = document.getElementById('new-search-btn');

// Chat DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

let chatHistory = [];

// ============ PARTICLES ============
const particleContainer = document.getElementById('bgParticles');
const particleColors = ['#6c5ce7', '#00cec9', '#fd79a8', '#0984e3', '#00b894', '#a29bfe'];

function createParticles() {
    if (!particleContainer) return;
    for (let i = 0; i < 35; i++) {
        const p = document.createElement('div');
        p.classList.add('particle');
        const size = Math.random() * 5 + 2;
        const color = particleColors[Math.floor(Math.random() * particleColors.length)];
        p.style.cssText = `width:${size}px;height:${size}px;background:${color};left:${Math.random()*100}%;animation-duration:${Math.random()*18+14}s;animation-delay:${Math.random()*8}s;`;
        particleContainer.appendChild(p);
    }
}
createParticles();

// ============ NAVBAR ============
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 40) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
});

// Mobile menu
const mobileToggle = document.getElementById('mobileToggle');
const mobileOverlay = document.getElementById('mobileOverlay');
const mobileClose = document.getElementById('mobileClose');

if (mobileToggle) mobileToggle.addEventListener('click', () => { mobileOverlay.classList.add('active'); document.body.style.overflow = 'hidden'; });
if (mobileClose) mobileClose.addEventListener('click', () => { mobileOverlay.classList.remove('active'); document.body.style.overflow = ''; });
document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', () => { mobileOverlay.classList.remove('active'); document.body.style.overflow = ''; });
});

// ============ FAB ============
const fabMain = document.getElementById('fabMain');
const fabContainer = document.getElementById('fabContainer');
if (fabMain) {
    fabMain.addEventListener('click', () => { fabContainer.classList.toggle('active'); fabMain.classList.toggle('active'); });
}
document.addEventListener('click', (e) => {
    if (fabContainer && !fabContainer.contains(e.target)) { fabContainer.classList.remove('active'); fabMain.classList.remove('active'); }
});

// FAB actions
const fabActions = {
    'fabWhatsApp': () => window.open('https://wa.me/919047020807?text=Hi%20Xplore%20IT%20Corp!', '_blank'),
    'fabCall': () => window.open('tel:+919047020807'),
    'fabEmail': () => window.open('mailto:info@xploreitcorp.com'),
    'fabSearch': () => { scrollToSearch(); }
};
Object.entries(fabActions).forEach(([id, fn]) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', fn);
});

// ============ SCROLL HELPERS ============
function scrollToSearch() {
    const el = document.getElementById('search-section');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(() => searchInput.focus(), 500);
}

function scrollToFeatures() {
    const el = document.getElementById('features-section');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function scrollToChannels() {
    const el = document.getElementById('channels-section');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Hero & Nav button actions
const scrollActions = {
    'heroStartBtn': scrollToSearch,
    'btnStartResearch': scrollToSearch,
    'mobileStartBtn': () => { mobileOverlay.classList.remove('active'); document.body.style.overflow = ''; scrollToSearch(); },
    'ctaStart': scrollToSearch,
    'navFeatures': scrollToFeatures,
    'navChannels': scrollToChannels,
    'btnBackTop': () => window.scrollTo({ top: 0, behavior: 'smooth' }),
    'navHome': () => window.scrollTo({ top: 0, behavior: 'smooth' }),
};
Object.entries(scrollActions).forEach(([id, fn]) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', fn);
});

// ============ TOAST SYSTEM ============
function showToast(message, icon = 'info-circle', type = 'info') {
    const colors = { info: 'linear-gradient(135deg,#6c5ce7,#0984e3)', success: 'linear-gradient(135deg,#00b894,#00cec9)', warning: 'linear-gradient(135deg,#f39c12,#e84393)' };
    const toast = document.createElement('div');
    toast.style.cssText = `position:fixed;top:80px;right:24px;background:${colors[type]};color:white;padding:14px 24px;border-radius:12px;font-family:'Outfit',sans-serif;font-size:0.88rem;font-weight:500;display:flex;align-items:center;gap:10px;z-index:10000;box-shadow:0 8px 30px rgba(0,0,0,0.4);transform:translateX(120%);transition:transform 0.4s cubic-bezier(0.34,1.56,0.64,1);max-width:380px;`;
    toast.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
    document.body.appendChild(toast);
    requestAnimationFrame(() => { toast.style.transform = 'translateX(0)'; });
    setTimeout(() => { toast.style.transform = 'translateX(120%)'; setTimeout(() => toast.remove(), 400); }, 3000);
}

// ============ TOAST BUTTON HANDLERS ============
const toastButtons = {
    'heroWatchBtn': ['Demo video coming soon! 🎬', 'play-circle', 'info'],
    'heroApiBtn': ['API documentation coming soon! 🔌', 'code', 'info'],
    'btnDocs': ['Documentation coming soon! 📖', 'book', 'info'],
    'btnHistory': ['Search history coming soon! 📜', 'history', 'info'],
    'btnBookmarks': ['Bookmarks coming soon! 🔖', 'bookmark', 'info'],
    'btnSettings': ['Settings panel coming soon! ⚙️', 'cog', 'info'],
    'btnVoice': ['Voice search coming soon! 🎤', 'microphone', 'info'],
    'ctaBulk': ['Bulk research feature coming soon! 📋', 'list', 'info'],
    'ctaApi': ['API access coming soon! 🔌', 'plug', 'info'],
    'ctaPricing': ['Pricing details coming soon! 💰', 'tags', 'info'],
    'btnAllChannels': ['All 6 channels active by default! ✅', 'check-circle', 'success'],
    'btnCustomize': ['Channel customization coming soon! 🎛️', 'sliders-h', 'info'],
    'btnShareReport': ['Report sharing coming soon! 📤', 'share-alt', 'info'],
    'btnPrintReport': ['Print feature coming soon! 🖨️', 'print', 'info'],
    'btnResearchAll': ['Batch research coming soon! 🔄', 'layer-group', 'info'],
    'btnRefreshResults': ['Results refreshed! ✅', 'sync-alt', 'success'],
    'btnFilterResults': ['Filter coming soon! 🔍', 'filter', 'info'],
    'btnClearChat': ['Chat cleared! ✅', 'eraser', 'success'],
    'btnExportChat': ['Chat export coming soon! 📥', 'download', 'info'],
    'btnFullscreen': ['Fullscreen coming soon! 🖥️', 'expand', 'info'],
    'btnAttach': ['Attachments coming soon! 📎', 'paperclip', 'info'],
    'btnEmoji': ['Emoji picker coming soon! 😊', 'smile', 'info'],
    'navAbout': ['About Xplore IT Corp 🏢', 'info-circle', 'info'],
    'btnPrivacy': ['Privacy policy coming soon!', 'shield-alt', 'info'],
    'btnTerms': ['Terms of service coming soon!', 'file-contract', 'info'],
    'btnSupport': ['Support: info@xploreitcorp.com 📧', 'headset', 'info'],
};
Object.entries(toastButtons).forEach(([id, args]) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', (e) => { e.preventDefault(); showToast(...args); });
});

// Feature card buttons
['btnLearnGoogle', 'btnLearnMaps', 'btnLearnLinkedIn', 'btnLearnYT', 'btnLearnNews', 'btnLearnScrape'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', () => scrollToSearch());
});

// ============ CHANNEL TOGGLE ============
document.querySelectorAll('.btn-channel').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.classList.toggle('active');
        const ch = btn.dataset.ch;
        const isActive = btn.classList.contains('active');
        showToast(`${ch.charAt(0).toUpperCase() + ch.slice(1)} channel ${isActive ? 'enabled' : 'disabled'}`, isActive ? 'check-circle' : 'times-circle', isActive ? 'success' : 'warning');
    });
});

// ============ SUGGESTION BUTTONS ============
document.querySelectorAll('.btn-suggestion').forEach(btn => {
    btn.addEventListener('click', () => {
        searchInput.value = btn.dataset.query;
        searchInput.focus();
        showToast(`Query set: ${btn.dataset.query}`, 'search', 'success');
    });
});

// ============ CHIP BUTTONS ============
document.querySelectorAll('.btn-chip').forEach(btn => {
    btn.addEventListener('click', () => {
        const category = btn.textContent.trim();
        searchInput.value = '';
        searchInput.placeholder = `Search for a ${category}...`;
        scrollToSearch();
        showToast(`Category: ${category} selected`, 'tag', 'success');
    });
});

// ============ QUICK QUESTION BUTTONS ============
document.querySelectorAll('.btn-quick-q').forEach(btn => {
    btn.addEventListener('click', () => {
        const q = btn.dataset.q;
        if (chatInput && currentResearchData) {
            chatInput.value = q;
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
});

// ============ CLEAR CHAT ============
const btnClearChat = document.getElementById('btnClearChat');
if (btnClearChat) {
    btnClearChat.addEventListener('click', () => {
        if (chatMessages) chatMessages.innerHTML = '';
        chatHistory = [];
    });
}

// ============ CANCEL RESEARCH ============
const btnCancelResearch = document.getElementById('btnCancelResearch');
if (btnCancelResearch) {
    btnCancelResearch.addEventListener('click', () => {
        progressSection.classList.add('hidden');
        searchSection.classList.remove('hidden');
        document.getElementById('hero-section').style.display = '';
        document.getElementById('features-section').style.display = '';
        document.querySelector('.cta-banner').style.display = '';
        document.getElementById('channels-section').style.display = '';
        showToast('Research cancelled', 'times-circle', 'warning');
    });
}

// ============ RIPPLE EFFECT ============
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        ripple.style.cssText = `position:absolute;width:${size}px;height:${size}px;left:${e.clientX-rect.left-size/2}px;top:${e.clientY-rect.top-size/2}px;background:rgba(255,255,255,0.12);border-radius:50%;transform:scale(0);animation:ripple 0.6s ease forwards;pointer-events:none;z-index:10;`;
        this.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });
});
const rippleStyle = document.createElement('style');
rippleStyle.textContent = '@keyframes ripple { to { transform: scale(4); opacity: 0; } }';
document.head.appendChild(rippleStyle);

// ============ SCROLL REVEAL ============
const revealEls = document.querySelectorAll('.feature-card, .cta-banner, .channels-showcase, .glass-card');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.08 });
revealEls.forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = `opacity 0.5s ease ${(i % 6) * 0.08}s, transform 0.5s ease ${(i % 6) * 0.08}s`;
    revealObserver.observe(el);
});

// ============ TILT EFFECT ============
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;
        card.style.transform = `perspective(600px) rotateX(${(y-0.5)*6}deg) rotateY(${(x-0.5)*-6}deg) translateY(-6px)`;
    });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; });
});

// ============================================
// CORE RESEARCH FUNCTIONALITY (preserved)
// ============================================

// Hide extra sections during research flow
function showResearchUI() {
    document.getElementById('hero-section').style.display = 'none';
    document.getElementById('features-section').style.display = 'none';
    document.querySelector('.cta-banner').style.display = 'none';
    document.getElementById('channels-section').style.display = 'none';
}

function showHomeUI() {
    document.getElementById('hero-section').style.display = '';
    document.getElementById('features-section').style.display = '';
    document.querySelector('.cta-banner').style.display = '';
    document.getElementById('channels-section').style.display = '';
}

// Form Submit
searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;

    try {
        setBtnLoading(true);
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();

        if (data.results && data.results.length > 0) {
            renderSearchResults(data.results);
            searchSection.classList.add('hidden');
            showResearchUI();
            selectSection.classList.remove('hidden');
        } else {
            showToast('No search results found. Try a different query.', 'exclamation-triangle', 'warning');
        }
    } catch (err) {
        console.error(err);
        showToast('Search failed. Check API key configuration.', 'times-circle', 'warning');
    } finally {
        setBtnLoading(false);
    }
});

cancelSearchBtn.addEventListener('click', () => {
    selectSection.classList.add('hidden');
    searchSection.classList.remove('hidden');
    showHomeUI();
});

function renderSearchResults(results) {
    resultsList.innerHTML = '';
    results.forEach(item => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
            <div class="result-info">
                <h4>${escapeHtml(item.title)}</h4>
                <p>${escapeHtml(item.snippet)}</p>
            </div>
            <span class="result-domain">${escapeHtml(extractDomain(item.link))}</span>
        `;
        card.addEventListener('click', () => startDeepResearch(item));
        resultsList.appendChild(card);
    });
}

async function startDeepResearch(item) {
    selectSection.classList.add('hidden');
    progressSection.classList.remove('hidden');
    resetProgress();

    const steps = [
        { id: 'step-search', delay: 2000 },
        { id: 'step-maps', delay: 2500 },
        { id: 'step-linkedin', delay: 2000 },
        { id: 'step-youtube', delay: 2000 },
        { id: 'step-news', delay: 2000 },
        { id: 'step-scrape', delay: 3000 },
        { id: 'step-placement', delay: 2000 },
        { id: 'step-ai', delay: 3000 }
    ];

    let currentStepIdx = 0;
    function runNextStep() {
        if (currentStepIdx < steps.length) {
            const step = steps[currentStepIdx];
            updateStepStatus(step.id, 'active');
            setTimeout(() => {
                const element = document.getElementById(step.id);
                if (element && element.classList.contains('active')) {
                    updateStepStatus(step.id, 'completed');
                    currentStepIdx++;
                    runNextStep();
                }
            }, step.delay);
        }
    }
    runNextStep();

    try {
        const startTime = Date.now();
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: item.title, link: item.link })
        });

        if (!response.ok) throw new Error('Research request failed');
        const data = await response.json();
        currentResearchData = data;

        const elapsed = Date.now() - startTime;
        if (elapsed < 4000) await sleep(4000 - elapsed);

        steps.forEach(s => updateStepStatus(s.id, 'completed'));
        await sleep(600);

        progressSection.classList.add('hidden');
        renderResearchReport(data);
        initChatbot(data);
        reportSection.classList.remove('hidden');
        showToast('Research completed successfully! 🎉', 'check-circle', 'success');
    } catch (err) {
        console.error(err);
        showToast('Deep research failed. Check server logs.', 'exclamation-triangle', 'warning');
        progressSection.classList.add('hidden');
        searchSection.classList.remove('hidden');
        showHomeUI();
    }
}

function resetProgress() {
    const ids = ['step-search', 'step-maps', 'step-linkedin', 'step-youtube', 'step-news', 'step-scrape', 'step-placement', 'step-ai'];
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.className = 'check-item';
            el.querySelector('.check-status').innerHTML = '<i class="far fa-circle text-muted"></i>';
        }
    });
}

function updateStepStatus(id, status) {
    const el = document.getElementById(id);
    if (!el) return;
    const statusEl = el.querySelector('.check-status');
    if (!statusEl) return;
    
    if (status === 'active') {
        el.className = 'check-item active';
        statusEl.innerHTML = '<i class="fas fa-spinner fa-spin text-primary"></i>';
    } else if (status === 'completed') {
        el.className = 'check-item completed';
        statusEl.innerHTML = '<i class="fas fa-check-circle text-success"></i>';
    }
}

function renderResearchReport(data) {
    document.getElementById('report-title').innerText = data.title;
    const maps = data.maps_data || {};
    const linkedin = data.linkedin_data || {};
    document.getElementById('badge-rating').innerHTML = `<i class="fas fa-star"></i> ${maps.rating && maps.rating !== 'N/A' ? maps.rating + '/5' : 'N/A'}`;
    document.getElementById('badge-founded').innerHTML = `<i class="fas fa-calendar"></i> ${linkedin.founded_year && linkedin.founded_year !== 'N/A' ? 'Founded: ' + linkedin.founded_year : 'Founded: N/A'}`;
    document.getElementById('badge-industry').innerHTML = `<i class="fas fa-industry"></i> ${linkedin.industry_type && linkedin.industry_type !== 'N/A' ? linkedin.industry_type : 'Industry: N/A'}`;
}

// Export
document.querySelectorAll('.btn-export').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        if (!currentResearchData) return;
        const format = e.currentTarget.getAttribute('data-format');
        if (!format) return;
        const originalText = e.currentTarget.innerHTML;
        e.currentTarget.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Exporting...';

        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    format, title: currentResearchData.title,
                    ai_report: currentResearchData.ai_report,
                    contact_data: currentResearchData.contact_data,
                    news_data: currentResearchData.news_data,
                    youtube_data: currentResearchData.youtube_data,
                    raw_data_string: currentResearchData.raw_data_string
                })
            });
            if (!response.ok) throw new Error('Export failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const disposition = response.headers.get('Content-Disposition');
            let filename = `DeepDig_${sanitize(currentResearchData.title)}.${format}`;
            if (disposition && disposition.includes('filename=')) filename = disposition.split('filename=')[1].replace(/"/g, '');
            const a = document.createElement('a'); a.href = url; a.download = filename;
            document.body.appendChild(a); a.click(); a.remove(); window.URL.revokeObjectURL(url);
            showToast(`${format.toUpperCase()} exported successfully!`, 'check-circle', 'success');
        } catch (err) {
            console.error(err);
            showToast('Export failed. Check server.', 'times-circle', 'warning');
        } finally {
            e.currentTarget.innerHTML = originalText;
        }
    });
});

// New Search
newSearchBtn.addEventListener('click', () => {
    reportSection.classList.add('hidden');
    searchSection.classList.remove('hidden');
    showHomeUI();
    searchInput.value = '';
    currentResearchData = null;
    chatHistory = [];
});

// Helpers
function setBtnLoading(isLoading) {
    const btn = document.getElementById('search-btn');
    if (isLoading) { btn.disabled = true; btn.querySelector('span').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...'; }
    else { btn.disabled = false; btn.querySelector('span').innerHTML = '<i class="fas fa-bolt"></i> Dig Deep'; }
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

function extractDomain(url) {
    if (!url) return 'N/A';
    try { return new URL(url).hostname; } catch(e) { return url; }
}

function sanitize(name) { return name.replace(/[^a-zA-Z0-9_\-]/g, '_').substring(0, 30); }
function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

function parseSimpleMarkdown(markdown) {
    if (!markdown) return '';
    let html = '';
    const lines = markdown.split('\n');
    let insideList = false;
    lines.forEach(line => {
        let t = line.trim();
        t = t.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        if (t.startsWith('### ')) { if (insideList) { html += '</ul>'; insideList = false; } html += `<h3>${t.replace('### ', '')}</h3>`; }
        else if (t.startsWith('## ') || /^\d+\. /.test(t)) { if (insideList) { html += '</ul>'; insideList = false; } html += `<h2>${t.startsWith('## ') ? t.replace('## ', '') : t}</h2>`; }
        else if (t.startsWith('* ') || t.startsWith('- ')) { if (!insideList) { html += '<ul>'; insideList = true; } html += `<li>${t.substring(2)}</li>`; }
        else { if (insideList) { html += '</ul>'; insideList = false; } if (t) html += `<p>${t}</p>`; else html += '<br>'; }
    });
    if (insideList) html += '</ul>';
    return html;
}

// ============ CHATBOT ============
function initChatbot(data) {
    chatHistory = [];
    chatMessages.innerHTML = '';
    appendChatMessage('assistant', `Hello! I've analyzed all the information about <strong>${escapeHtml(data.title)}</strong>. Ask me anything about this entity!`);
    setTimeout(() => chatInput.focus(), 100);
}

function appendChatMessage(role, content) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${role}`;
    msgDiv.innerHTML = role === 'system' ? content : parseSimpleMarkdown(content);
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = chatInput.value.trim();
    if (!question || !currentResearchData) return;
    chatInput.value = '';
    appendChatMessage('user', question);

    const loaderId = 'chat-loader-' + Date.now();
    const loaderDiv = document.createElement('div');
    loaderDiv.className = 'chat-msg assistant research-status';
    loaderDiv.id = loaderId;
    loaderDiv.innerHTML = `<div class="research-indicator"><div class="research-spinner"></div><div class="research-text"><span class="research-label">🔍 Searching & analyzing...</span><span class="research-sub">Performing live deep research for your question</span></div></div>`;
    chatMessages.appendChild(loaderDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: currentResearchData.title, raw_data_string: currentResearchData.raw_data_string, question, history: chatHistory })
        });
        const loader = document.getElementById(loaderId);
        if (loader) loader.remove();
        if (!response.ok) throw new Error('Chat failed');
        const data = await response.json();
        appendChatMessage('assistant', data.answer);
        chatHistory.push({ role: 'user', content: question });
        chatHistory.push({ role: 'assistant', content: data.answer });
    } catch (err) {
        console.error(err);
        const loader = document.getElementById(loaderId);
        if (loader) loader.remove();
        appendChatMessage('system', '⚠️ Failed to connect to chat assistant. Please try again.');
    }
});

console.log('%c🚀 DeepDig by Xplore IT Corp — Loaded!', 'color: #6c5ce7; font-size: 14px; font-weight: bold;');
