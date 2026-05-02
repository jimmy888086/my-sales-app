st.markdown("""
<style>
    /* 使用系统原生字体，不加载外部资源 */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, Helvetica, Arial, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 动态弥散光背景 */
    .stApp {
        background: #0a0a0f;
        position: relative;
        overflow: hidden;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background:
            radial-gradient(ellipse at 20% 50%, rgba(236, 72, 153, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 50%);
        animation: bgShift 20s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }

    @keyframes bgShift {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(2%, -1%) rotate(1deg); }
        66% { transform: translate(-1%, 1%) rotate(-1deg); }
    }

    /* Bento Box 主容器 */
    .bento-container {
        position: relative;
        z-index: 1;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 20px;
        max-width: 1100px;
        margin: 0 auto;
        padding: 20px;
    }

    /* 液态玻璃卡片 - 降低 blur 使用 */
    .glass-bento {
        background: rgba(20, 20, 35, 0.7);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-radius: 28px;
        padding: 32px 28px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .glass-bento::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
    }

    .glass-bento:hover {
        border-color: rgba(255, 255, 255, 0.12);
        box-shadow:
            0 12px 48px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.06);
        transform: translateY(-2px);
    }

    /* 电光粉渐变标题 - 不使用背景裁切，改用纯色渐变文字 */
    .hero-title {
        font-size: clamp(28px, 5vw, 40px);
        font-weight: 800;
        background: linear-gradient(135deg, #f472b6 0%, #ec4899 25%, #a855f7 50%, #6366f1 75%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientFlow 6s ease infinite;
        letter-spacing: -1px;
        line-height: 1.2;
        color: transparent; /* 回退确保渐变生效 */
    }

    @keyframes gradientFlow {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(15deg); }
    }

    .hero-subtitle {
        font-size: clamp(12px, 1.5vw, 14px);
        color: rgba(255, 255, 255, 0.3);
        font-weight: 500;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* 领奖台 */
    .podium-2026 {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 16px;
        flex-wrap: wrap;
        padding: 10px 0;
    }

    .podium-card-2026 {
        flex: 1 1 110px;
        max-width: 140px;
        border-radius: 20px;
        padding: 24px 14px 18px;
        text-align: center;
        position: relative;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
    }

    .podium-card-2026:hover {
        transform: translateY(-10px);
    }

    .podium-champion {
        background: linear-gradient(180deg, rgba(251, 191, 36, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 1.5px solid rgba(251, 191, 36, 0.4);
        box-shadow: 0 8px 40px rgba(251, 191, 36, 0.2);
        padding-top: 32px;
        padding-bottom: 28px;
        z-index: 3;
    }

    .podium-runnerup {
        background: linear-gradient(180deg, rgba(192, 192, 192, 0.15) 0%, rgba(148, 163, 184, 0.1) 100%);
        border: 1.5px solid rgba(192, 192, 192, 0.25);
        z-index: 2;
    }

    .podium-third {
        background: linear-gradient(180deg, rgba(205, 127, 50, 0.15) 0%, rgba(180, 83, 9, 0.1) 100%);
        border: 1.5px solid rgba(205, 127, 50, 0.25);
        z-index: 1;
    }

    .crown-glow {
        font-size: 36px;
        filter: drop-shadow(0 0 15px rgba(251, 191, 36, 0.9));
        animation: crownFloat 3s ease-in-out infinite;
    }

    @keyframes crownFloat {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-10px) scale(1.1); }
    }

    .rank-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        font-weight: 800;
        font-size: 16px;
        color: white;
        margin-bottom: 12px;
    }

    .podium-champion .rank-circle {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        box-shadow: 0 0 30px rgba(251, 191, 36, 0.6);
    }

    .podium-runnerup .rank-circle {
        background: linear-gradient(135deg, #cbd5e1, #94a3b8);
        box-shadow: 0 0 20px rgba(148, 163, 184, 0.3);
    }

    .podium-third .rank-circle {
        background: linear-gradient(135deg, #cd7f32, #a0522d);
        box-shadow: 0 0 20px rgba(205, 127, 50, 0.3);
    }

    .podium-name {
        display: block;
        font-size: clamp(13px, 2vw, 16px);
        font-weight: 700;
        color: white;
        margin: 8px 0 6px;
        letter-spacing: 0.5px;
    }

    .podium-number {
        display: block;
        font-size: clamp(22px, 3.5vw, 30px);
        font-weight: 900;
        color: rgba(255, 255, 255, 0.95);
    }

    .podium-label {
        display: block;
        font-size: 11px;
        color: rgba(255, 255, 255, 0.35);
        font-weight: 500;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* 输入框液态风格 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        color: white !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ec4899 !important;
        box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.15), 0 0 30px rgba(236, 72, 153, 0.08) !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.2) !important;
    }

    /* Streamlit 按钮 */
    .stButton > button {
        width: 100% !important;
        border-radius: 16px !important;
        height: 52px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
    }

    /* 响应式 */
    @media (max-width: 768px) {
        .bento-container {
            grid-template-columns: 1fr;
            padding: 12px;
            gap: 14px;
        }
        .glass-bento {
            padding: 24px 18px;
            border-radius: 22px;
        }
        .podium-2026 {
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }
        .podium-card-2026 {
            max-width: 220px;
            width: 85%;
        }
    }

    @media (max-width: 480px) {
        .hero-title {
            font-size: 24px;
        }
        .glass-bento {
            padding: 20px 14px;
            border-radius: 18px;
        }
    }
</style>
""", unsafe_allow_html=True)
