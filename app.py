import streamlit as st
import chromadb
from database import KnowledgeBase
from pathlib import Path
import os
from datetime import datetime
import importlib

# Local module imports
import collector
import processor
import analyst
import database

# Force reload local modules to prevent AttributeError from Streamlit caching
importlib.reload(collector)
importlib.reload(processor)
importlib.reload(analyst)
importlib.reload(database)

from collector import PaperCollector
from processor import PaperProcessor
from analyst import ResearchAnalyst
from database import KnowledgeBase

# Page config
st.set_page_config(
    page_title="AI Research Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    .stApp {
        background: transparent;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 255, 0.5);
    }
    
    h1, h2, h3 {
        color: #00f2fe !important;
        font-weight: 600;
    }
    
    .stSidebar {
        background-color: rgba(0, 0, 0, 0.5) !important;
    }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background: #00f2fe;
        color: #0f0c29;
    }
    </style>
    """, unsafe_allow_html=True)

# App Title
st.title("🚀 AI Automated Research Hub")
st.markdown("Hệ thống tự động nghiên cứu và cập nhật tri thức AI - Chạy bằng **Ollama**")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.header("Dashboard")
    menu = st.radio("Chức năng", ["Tổng quan kho tri thức", "Báo cáo nghiên cứu mới", "Tìm kiếm thông minh", "Vòng lặp Nghiên cứu Đa Agent", "Chế độ AI Tự Tiến Hóa", "Chat với Bộ não AI"])
    st.divider()
    st.info("Hệ thống đang hoạt động độc lập và bảo mật cục bộ.")

# Initialize KB
@st.cache_resource
def get_kb():
    return KnowledgeBase()

kb = get_kb()

if menu == "Tổng quan kho tri thức":
    st.subheader("📚 Thư viện bài báo đã phân tích")
    
    # Fetch all data from ChromaDB
    data = kb.collection.get()
    
    if not data['ids']:
        st.warning("Kho tri thức hiện đang trống. Hãy chạy `main.py` để thu thập dữ liệu.")
    else:
        for i in range(len(data['ids'])):
            meta = data['metadatas'][i]
            with st.container():
                st.markdown(f"""
                <div class="glass-card">
                    <span class="status-badge">New Paper</span>
                    <h3>{meta['title']}</h3>
                    <p style="color: #ccc;"><b>Tác giả:</b> {meta['authors']}</p>
                    <hr style="border-color: rgba(255,255,255,0.1)">
                    <div style="font-size: 0.95rem;">
                        {meta['analysis'].replace('\n', '<br>')}
                    </div>
                    <br>
                    <a href="{meta['url']}" target="_blank" style="color: #00f2fe; text-decoration: none;">🔗 Xem bản gốc (arXiv)</a>
                </div>
                """, unsafe_allow_html=True)

elif menu == "Báo cáo nghiên cứu mới":
    st.subheader("📊 Báo cáo xu hướng & Ý tưởng đột phá")
    
    report_files = sorted(list(Path("data").glob("report_*.md")), reverse=True)
    
    if not report_files:
        st.info("Chưa có báo cáo nào được tạo. Hệ thống sẽ tự động tạo báo cáo sau mỗi chu kỳ nghiên cứu.")
    else:
        selected_report = st.selectbox("Chọn báo cáo", [f.name for f in report_files])
        with open(Path("data") / selected_report, "r", encoding="utf-8") as f:
            content = f.read()
        
        st.markdown(f"""
        <div class="glass-card">
            {content}
        </div>
        """, unsafe_allow_html=True)

elif menu == "Tìm kiếm thông minh":
    st.subheader("🔍 Truy vấn tri thức AI")
    query = st.text_input("Nhập chủ đề bạn quan tâm (ví dụ: 'Large Language Models', 'Computer Vision improvements')...")
    
    if query:
        results = kb.search_similar(query, n_results=3)
        if results['ids']:
            st.write(f"Tìm thấy {len(results['ids'])} kết quả liên quan:")
            for i in range(len(results['ids'][0])):
                meta = results['metadatas'][0][i]
                with st.expander(f"📄 {meta['title']}"):
                    st.markdown(meta['analysis'])
                    st.write(f"[Link arXiv]({meta['url']})")
        else:
            st.write("Không tìm thấy kết quả phù hợp.")

elif menu == "Vòng lặp Nghiên cứu Đa Agent":
    st.subheader("🔄 Multi-Agent Deep Research Loop")
    st.markdown("Quy trình: **User Topic** ➔ **AI 1 (Researcher)** ➔ **AI 2 (Architect)** ➔ **Upgraded Research**")
    
    seed_topic = st.text_input("Nhập chủ đề hoặc ý tưởng sơ khai của bạn:", placeholder="Ví dụ: AI trong y tế, Tối ưu hóa LLM...")
    
    if st.button("Bắt đầu chu trình nghiên cứu chuyên sâu"):
        if not seed_topic:
            st.error("Vui lòng nhập chủ đề!")
        else:
            with st.status("🤖 AI Agents đang làm việc...", expanded=True) as status:
                collector = PaperCollector()
                processor = PaperProcessor()
                analyst = ResearchAnalyst()
                
                # --- AI 1: RESEARCHER ---
                st.write("🕵️ **AI 1 (Researcher)**: Đang tìm kiếm bài báo liên quan...")
                papers = collector.search_papers(query=seed_topic, max_results=3)
                
                findings = []
                for p in papers:
                    st.write(f"  - Đang đọc: *{p['title']}*")
                    pdf_path = collector.download_pdf(p)
                    if pdf_path:
                        text = processor.extract_text_from_pdf(pdf_path)
                        if text:
                            analysis = processor.summarize_paper(text, p)
                            findings.append(analysis)
                
                if not findings:
                    st.error("AI 1 không tìm thấy tài liệu phù hợp.")
                    status.update(label="Thất bại", state="error")
                else:
                    # --- AI 2: ARCHITECT ---
                    st.write("🏗️ **AI 2 (Architect)**: Đang phản biện và nâng cấp chủ đề...")
                    upgraded_report = analyst.refine_and_upgrade_topic(seed_topic, findings)
                    
                    st.divider()
                    st.markdown("### 🏆 KẾT QUẢ NGHIÊN CỨU CHUYÊN SÂU")
                    st.markdown(upgraded_report)
                    
                    # Store in logs/reports
                    report_path = Path("data") / f"deep_research_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                    with open(report_path, "w", encoding="utf-8") as f:
                        f.write(f"# Báo cáo Nghiên cứu Đa Agent\n\nChủ đề gốc: {seed_topic}\n\n{upgraded_report}")
                    
                    status.update(label="Hoàn tất chu trình!", state="complete")

elif menu == "Chế độ AI Tự Tiến Hóa":
    st.subheader("🌌 Autonomous AI Evolution Mode")
    st.markdown("Trong chế độ này, AI sẽ tự đặt câu hỏi, tự tìm kiếm và tự nâng cấp tri thức mà không cần sự can thiệp của con người.")
    
    if "auto_evolve_running" not in st.session_state:
        st.session_state.auto_evolve_running = False
        st.session_state.evolve_history = []

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Bắt đầu Tự tiến hóa", disabled=st.session_state.auto_evolve_running):
            st.session_state.auto_evolve_running = True
    with col2:
        if st.button("🛑 Dừng lại"):
            st.session_state.auto_evolve_running = False

    if st.session_state.auto_evolve_running:
        with st.status("♾️ AI đang tự tiến hóa...") as status:
            analyst = ResearchAnalyst()
            collector = PaperCollector()
            processor = PaperProcessor()
            
            # Step 1: Self-initiation
            st.write("🧠 **AI Initiator**: Đang suy ngẫm về các biên giới AI mới...")
            history = "\n".join(st.session_state.evolve_history[-3:]) # Last 3 steps for context
            quest = analyst.generate_autonomous_quest(history)
            
            st.markdown(f"**Nhiệm vụ tự đặt ra:**\n{quest}")
            
            # Extract query (simple heuristic)
            query = quest.split("Search Query:")[-1].strip() if "Search Query:" in quest else quest.split("\n")[-1]
            
            # Step 2: Research
            st.write(f"🕵️ **AI Researcher**: Đang thực thi nhiệm vụ: *{query}*")
            papers = collector.search_papers(query=query, max_results=2)
            
            findings = []
            for p in papers:
                st.write(f"  - Đang nạp tri thức từ: *{p['title']}*")
                pdf_path = collector.download_pdf(p)
                if pdf_path:
                    text = processor.extract_text_from_pdf(pdf_path)
                    if text:
                        analysis = processor.summarize_paper(text, p)
                        findings.append(analysis)
                        kb.add_paper(p['id'], text, p, analysis)
            
            # Step 3: Integrate and Evolve
            if findings:
                st.write("🏗️ **AI Architect**: Đang tích hợp tri thức và nâng cấp hệ thống...")
                evolution_result = analyst.refine_and_upgrade_topic(quest, findings)
                st.session_state.evolve_history.append(evolution_result)
                st.markdown(evolution_result)
                
                # Save report
                report_path = Path("data") / f"evolution_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(f"# Nhật ký Tự tiến hóa AI\n\n{evolution_result}")
            
            status.update(label="Vòng lặp hoàn tất. Đang chuẩn bị bước tiếp theo...", state="complete")
            st.rerun() # Continue the loop

    # Show History
    if st.session_state.evolve_history:
        st.divider()
        st.markdown("### 📜 Lịch sử tiến hóa")
        for idx, step in enumerate(reversed(st.session_state.evolve_history)):
            with st.expander(f"Bước tiến hóa {len(st.session_state.evolve_history) - idx}"):
                st.markdown(step)

elif menu == "Chat với Bộ não AI":
    st.subheader("💬 Chat với Bộ não AI")
    st.markdown("Hỏi bất cứ điều gì về AI, tôi sẽ trả lời dựa trên kho tri thức mà tôi đã tự nghiên cứu.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Bạn muốn hỏi gì về AI?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("🧠 Đang lục lại trí nhớ..."):
            # 1. Retrieve context
            results = kb.search_similar(prompt, n_results=3)
            context_docs = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    doc = results['documents'][0][i]
                    meta = results['metadatas'][0][i]
                    context_docs.append(f"Từ bài báo '{meta['title']}':\n{meta['analysis']}\nNội dung: {doc[:1000]}")
            
            # 2. Generate response using Analyst
            analyst = ResearchAnalyst()
            response = analyst.chat_with_brain(prompt, context_docs)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
