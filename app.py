
import streamlit as st
import pandas as pd
from backend import PropertyChatbot

# Page configuration
st.set_page_config(
    page_title="NoBrokerage Property Chat",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS (same as before)
st.markdown("""
<style>
    .main { background-color: #f5f7fa; }
    .stChatMessage { background-color: white !important; border-radius: 10px; padding: 15px; margin: 10px 0; color: #000000 !important; }
    .stChatMessage[data-testid="user-message"] { background-color: #E3F2FD !important; }
    .stChatMessage[data-testid="assistant-message"] { background-color: #F5F5F5 !important; }
    .property-card { background: white !important; border-radius: 12px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; color: #1a1a1a !important; border: 1px solid #e0e0e0; }
    .property-card:hover { transform: translateY(-5px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .property-title { font-size: 20px; font-weight: bold; color: #1a1a1a !important; margin-bottom: 10px; }
    .property-price { font-size: 24px; font-weight: bold; color: #FF6B35 !important; margin: 10px 0; }
    .property-detail { display: inline-block; background: #f0f0f0 !important; padding: 5px 12px; border-radius: 20px; margin: 5px 5px 5px 0; font-size: 14px; color: #333333 !important; }
    .status-ready { background: #4CAF50 !important; color: white !important; }
    .status-construction { background: #FF9800 !important; color: white !important; }
    .cta-link { background: #FF6B35 !important; color: white !important; padding: 8px 16px; border-radius: 8px; text-decoration: none; display: inline-block; margin-top: 10px; font-size: 14px; }
    .cta-link:hover { background: #E85D2A !important; }
    h1 { color: #FF6B35 !important; text-align: center; font-weight: 700 !important; margin-bottom: 10px !important; }
    .subtitle { text-align: center; color: #2C3E50 !important; margin-bottom: 30px; font-size: 18px; }
    .developer-credit { text-align: center; color: #666 !important; font-size: 14px; margin-top: 10px; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white !important; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; }
    .stChatMessage p { color: #000000 !important; }
    .stButton button { background-color: #FF6B35 !important; color: white !important; border-radius: 8px; padding: 8px 16px; border: none; }
    .stButton button:hover { background-color: #E85D2A !important; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = PropertyChatbot(
            'project.csv',
            'ProjectAddress.csv',
            'ProjectConfiguration.csv',
            'ProjectConfigurationVariant.csv'
        )
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Header
st.title("🏠 NoBrokerage Property Search")
st.markdown('<p class="subtitle">Find your dream property with AI-powered natural language search</p>', unsafe_allow_html=True)
st.markdown('<div class="developer-credit">💻 Developed by <strong>Shivansh Shrivastava</strong> | shrivastavashivansh498@gmail.com</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("💡 Example Queries")
    st.markdown("""
    **Try asking:**
    - 3BHK flat in Mumbai under 5 Cr
    - 2BHK ready to move in Pune
    - Properties in Gurukripa project
    - 1BHK in Chembur under 2 Cr
    - 4BHK between 3 Cr and 7 Cr
    """)

    st.divider()
    st.header("📊 Database Stats")
    if "chatbot" in st.session_state:
        df = st.session_state.chatbot.df
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Properties", len(df))
        with col2:
            st.metric("Cities", "2")
        st.info("🏙️ Mumbai & Pune")

    st.divider()
    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Shivansh Shrivastava**")
    st.markdown("📧 shrivastavashivansh498@gmail.com")
    st.markdown("🎓 AI Engineer Intern")
    st.markdown("🏢 NoBrokerage.com")

def display_properties(df):
    """Display property cards using ONLY CSV data."""
    if df.empty:
        st.info("No properties found matching your criteria.")
        return

    for idx, row in df.iterrows():
        # Format price
        price = row['price_inr']
        if price >= 10000000:
            price_str = f"₹{price/10000000:.2f} Cr"
        else:
            price_str = f"₹{price/100000:.2f} L"

        # Status
        status = str(row.get('status', 'N/A'))
        status_class = "status-ready" if "READY" in status else "status-construction"
        status_display = status.replace("_", " ").title()

        # Property details FROM CSV
        prop_name = str(row.get('name', 'Property'))
        bhk_type = str(row.get('bhk', 'N/A'))
        locality = str(row.get('locality', 'Unknown'))
        city_name = "Mumbai" if row.get('city') == "cmf50r5a00000vcj0k1iuocuu" else "Pune"
        slug = str(row.get('slug', prop_name.lower().replace(' ', '-')))

        # Property card - NO hardcoded amenities
        card_html = f"""
        <div class="property-card">
            <div class="property-title">🏢 {prop_name}</div>
            <div class="property-price">{price_str}</div>
            <div style="margin: 15px 0;">
                <span class="property-detail"><strong>{bhk_type}</strong></span>
                <span class="property-detail {status_class}">{status_display}</span>
                <span class="property-detail">📍 {city_name} - {locality}</span>
            </div>
            <a href="/project/{slug}" class="cta-link">
                🔗 View Full Details
            </a>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "properties" in message and message["properties"] is not None:
            display_properties(message["properties"])

# Chat input
if prompt := st.chat_input("Ask about properties... (e.g., '3BHK in Mumbai under 5 Cr')"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching properties..."):
            try:
                summary, results, filters = st.session_state.chatbot.process_query(prompt)
                st.markdown(summary)

                with st.expander("🔍 Filters Applied"):
                    st.json(filters)

                if not results.empty:
                    st.success(f"✅ Found {len(results)} matching properties!")

                display_properties(results)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": summary,
                    "properties": results
                })

            except Exception as e:
                error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "properties": None
                })

# Welcome message
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("""
        👋 **Welcome to NoBrokerage Property Search!**

        I'm your AI property assistant. I can help you find properties based on:

        🏙️ **Location:** Mumbai, Pune
        🏠 **BHK:** 1BHK, 2BHK, 3BHK, 4BHK
        💰 **Budget:** "under 5 Cr", "between 1 Cr and 3 Cr"
        🏗️ **Status:** Ready to move, Under construction
        🏢 **Project Name:** Search by specific projects

        **Try these queries:**
        - `3BHK in Mumbai under 5 Cr`
        - `Properties in Gurukripa project`
        - `2BHK ready to move in Pune`

        Just type your query below! 👇
        """)
