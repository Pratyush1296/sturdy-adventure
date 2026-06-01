import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
API_KEY = "a4ee47b7-f53f-4b36-a3a9-88ad85805d25"
API_URL = "https://eventregistry.org/api/v1/article/getArticles"

st.set_page_config(
    page_title="Tesla News Dashboard",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Tesla News Dashboard")
st.caption("Fetch today's Tesla-related news articles from Event Registry")

# -----------------------------
# Fetch Articles Function
# -----------------------------
def fetch_articles(keyword="Tesla Inc"):
    payload = {
        "action": "getArticles",
        "keyword": keyword,
        "sourceLocationUri": [
            "http://en.wikipedia.org/wiki/United_States",
            "http://en.wikipedia.org/wiki/Canada",
            "http://en.wikipedia.org/wiki/United_Kingdom"
        ],
        "ignoreSourceGroupUri": "paywall/paywalled_sources",
        "articlesPage": 1,
        "articlesCount": 100,
        "articlesSortBy": "date",
        "articlesSortByAsc": False,
        "dataType": ["news", "pr"],
        "forceMaxDataTimeWindow": 1,  # Last 24 hours
        "resultType": "articles",
        "apiKey": API_KEY
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(
            f"API Error: {response.status_code}\n{response.text}"
        )
        return None


# -----------------------------
# UI
# -----------------------------
keyword = st.text_input(
    "Search Keyword",
    value="Tesla Inc"
)

if st.button("Fetch News"):
    with st.spinner("Fetching articles..."):
        data = fetch_articles(keyword)

    if data:
        articles = data.get("articles", {}).get("results", [])

        if not articles:
            st.warning("No articles found.")
        else:
            st.success(f"Found {len(articles)} articles")

            rows = []

            for article in articles:
                rows.append({
                    "Title": article.get("title", ""),
                    "Source": article.get("source", {}).get("title", ""),
                    "Published": article.get("dateTime", ""),
                    "URL": article.get("url", "")
                })

            df = pd.DataFrame(rows)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.markdown("---")
            st.subheader("Article Details")

            for article in articles:
                title = article.get("title", "No Title")
                source = article.get("source", {}).get("title", "Unknown")
                published = article.get("dateTime", "")
                url = article.get("url", "")

                with st.expander(title):
                    st.write(f"**Source:** {source}")
                    st.write(f"**Published:** {published}")

                    body = article.get("body", "")
                    if body:
                        st.write(body[:1000] + "...")

                    if url:
                        st.markdown(f"[Read Full Article]({url})")

