import streamlit as st
import chromadb
from database import KnowledgeBase
from pathlib import Path
import os
from datetime import datetime

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
    menu = st.radio("Chức năng", ["Tổng quan kho tri thức", "Báo cáo nghiên cứu mới", "Tìm kiếm thông minh"])
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

# Footer
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
