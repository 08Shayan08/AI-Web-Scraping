import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter the URL of the website you want to scrape")
if st.button("Scrape"):
    st.write(f"Scraping {url}...")
    result=scrape_website(url)
    body_content=extract_body_content(result)
    cleaned_content=clean_body_content(body_content)

    st.session_state.dom_content=cleaned_content
    with st.expander("DOM Content"):
        st.text_area("DOM content", cleaned_content,height=300)

if "dom_content" in st.session_state:
    parse_description=st.text_area("Enter the parse description")
    if st.button("Parse"):
       if parse_description:
        st.write("Parsing...")
        dom_chunks=split_dom_content(st.session_state.dom_content)
        result=parse_with_ollama(dom_chunks,parse_description)
        st.write(result)

