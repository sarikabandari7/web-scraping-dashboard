import streamlit as st
import pandas as pd

from scraper import scrape_books


st.set_page_config(
    page_title="Web Scraping Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Web Scraping Dashboard")
st.write("Book data scraped from the web")


# Scrape button
if st.button("🔄 Scrape Data"):

    data = scrape_books()

    if data:
        st.session_state["books"] = data
        st.success("Data scraped successfully!")

    else:
        st.error("Failed to scrape data.")


# Check if data is available
if "books" in st.session_state:

    df = pd.DataFrame(st.session_state["books"])

    # Convert price to number
    df["price"] = (
        df["price"]
        .str.extract(r"(\d+\.\d+)")[0]
        .astype(float)
    )

    # Search
    search = st.text_input("🔍 Search books")

    if search:
        df = df[
            df["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # Maximum price
    max_price = st.slider(
        "💰 Maximum Price",
        min_value=0.0,
        max_value=float(df["price"].max()),
        value=float(df["price"].max())
    )

    df = df[df["price"] <= max_price]

    # Sort
    sort_order = st.selectbox(
        "↕️ Sort by Price",
        ["Low to High", "High to Low"]
    )

    if sort_order == "Low to High":
        df = df.sort_values("price", ascending=True)
    else:
        df = df.sort_values("price", ascending=False)

    # Statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Total Books",
            len(df)
        )

    with col2:
        if len(df) > 0:
            st.metric(
                "💰 Average Price",
                f"£{df['price'].mean():.2f}"
            )
        else:
            st.metric(
                "💰 Average Price",
                "£0.00"
            )

    with col3:
        if len(df) > 0:
            st.metric(
                "💵 Maximum Price",
                f"£{df['price'].max():.2f}"
            )
        else:
            st.metric(
                "💵 Maximum Price",
                "£0.00"
            )

    # Price chart
    st.subheader("📊 Book Prices")

    if len(df) > 0:
        chart_data = df.set_index("title")["price"]
        st.bar_chart(chart_data)

    # Book data
    st.subheader("📚 Book Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    # Download CSV
    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="books_data.csv",
        mime="text/csv"
    )