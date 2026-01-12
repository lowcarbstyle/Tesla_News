import streamlit as st
import feedparser
import datetime

# Page Configuration
st.set_page_config(
    page_title="テスラ関連ニュース収集ダッシュボード",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Card Design (lowcarb.style clone)
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #f4f5f7;
        font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
        color: #333333;
    }
    
    /* Card Container */
    a.card-link {
        text-decoration: none;
        color: inherit !important;
        display: block;
    }
    
    .card {
        background-color: #ffffff;
        border-radius: 4px;
        padding: 24px;
        margin-bottom: 20px;
        border-bottom: 1px solid #e0e0e0;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out, opacity 0.3s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .card:hover {
        opacity: 0.85;
        background-color: #fafafa;
        cursor: pointer;
    }

    .card-date {
        font-size: 11px;
        color: #888888;
        margin-bottom: 6px;
        display: block;
    }

    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #333333;
        margin-bottom: 10px;
        line-height: 1.6;
    }

    .card-summary {
        font-size: 14px;
        color: #555555;
        line-height: 1.6;
        margin-bottom: 15px;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .read-more {
        display: inline-block;
        background-color: #333333; /* Dark gray accent */
        color: #ffffff !important;
        padding: 6px 14px;
        border-radius: 2px;
        font-size: 11px;
        font-weight: 600;
        text-decoration: none;
        transition: background-color 0.2s;
    }
    /* Hide Streamlit components branding if possible */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide Sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    section[data-testid="stSidebar"] > div {
        height: 100px;
        width: 100px;
        position: relative;
        top: -100px;
    }
    /* Hide the top left button to expand sidebar */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    button[kind="header"] {
        display: none !important;
    }
    
    /* Search Widget Styling */
    /* Label Styling */
    label[data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #333333 !important;
    }
    
    /* Input Box Styling */
    input[type="text"] {
        border: 2px solid #555555 !important;
        background-color: #ffffff !important;
        border-radius: 4px !important;
        padding: 10px !important;
        color: #333333 !important;
    }
    input[type="text"]:focus {
        border-color: #e31937 !important; /* Tesla Red-ish for focus */
        box-shadow: 0 0 5px rgba(227, 25, 55, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Application Title
# st.title("⚡ テスラ関連ニュース収集ダッシュボード")
# st.markdown("Google ニュース RSS からの最新情報")

# Search Settings (Moved from Sidebar)
search_query = st.text_input("テスラニュース検索", value="テスラモデルYスタンダード")

# 1. Fetch Data
# Compatibility for different Streamlit versions
if hasattr(st, "cache_data"):
    cache_decorator = st.cache_data
elif hasattr(st, "experimental_memo"):
    cache_decorator = st.experimental_memo
else:
    cache_decorator = st.cache

@cache_decorator(ttl=300)
def fetch_news(query):
    # Encode query for URL
    encoded_query = query.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)
    return feed.entries

# Main Logic
if search_query:
    with st.spinner(f"'{search_query}' のニュースを取得中..."):
        news_entries = fetch_news(search_query)

    if news_entries:
        # st.write(f"{len(news_entries)} 件の記事が見つかりました。")
        
        # 3. Display as Cards
        # Compatibility for columns
        if hasattr(st, "columns"):
            cols = st.columns(3)
        elif hasattr(st, "beta_columns"):
            cols = st.beta_columns(3)
        else:
            cols = None

        for idx, entry in enumerate(news_entries):
            if cols:
                col = cols[idx % 3]
                context = col
            else:
                context = st.container() if hasattr(st, "container") else st
            
            # Extract Data
            
            # Extract Data
            title = entry.get('title', 'タイトルなし')
            link = entry.get('link', '#')
            published = entry.get('published', '日付なし')
            # Try to format date cleaner if possible, otherwise use raw
            try:
                # date_parsed is a time.struct_time
                if hasattr(entry, 'published_parsed'):
                     dt = datetime.datetime.fromtimestamp(datetime.datetime(*entry.published_parsed[:6]).timestamp())
                     published = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass

            # Summary often contains HTML, we strip it or truncate for the card
            # summary = entry.get('summary', '')
            # For this dashboard, we might render simple text.
            # Google News RSS summary is often just a snippet.
            # Using clean text might be safer or just raw HTML if trusted.
            # We'll use a clean version for safety/layout.
            summary = entry.get('description', '')  # Google often puts it in description
            
            # Render Card HTML
            # Wrap entire card in an anchor tag for clickability
            card_html = f"""
            <a href="{link}" target="_blank" class="card-link">
                <div class="card">
                    <div class="card-date">{published}</div>
                    <div class="card-title">{title}</div>
                    <div class="card-summary">{summary}</div>
                    <div style="margin-top: 10px;">
                        <span class="read-more">記事を読む</span>
                    </div>
                </div>
            </a>
            """
            
            with context:
                st.markdown(card_html, unsafe_allow_html=True)
                
    else:
        st.warning(f"'{search_query}' のニュースは見つかりませんでした。")
else:
    st.info("検索キーワードを入力してください。")

