import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import sys
import onnxruntime as ort



def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://careers.nike.com/quality-systems-engineer/job/R-65289")
    submit_button = st.button("Submit")

    if submit_button:
        with st.spinner("Processing..."):
            try:
                st.write("🔍 Loading and cleaning URL...")
                loader = WebBaseLoader([url_input])
                text = loader.load().pop().page_content
                data = clean_text(text)


                st.write("📂 Loading portfolio...")
                portfolio.load_portfolio()

                st.write("🧠 Extracting jobs from LLM...")
                jobs = llm.extract_jobs(data)
                st.write(f"✅ Jobs extracted: {len(jobs)}")

                for i, job in enumerate(jobs):
                    try:

                        skills = job.get('skills', [])

                        if not skills:
                            st.warning("⚠️ No skills found.")
                            continue

                        links = portfolio.query_links(skills)

                        if not links or not links[0]:
                            st.warning("⚠️ No relevant portfolio links.")
                            continue

                        email = llm.write_mail(job, links[0])
                        st.code(email, language='markdown')

                    except Exception as inner_e:
                        st.error(f"🚨 Error in processing job {i + 1}: {inner_e}")
                        continue

            except Exception as e:
                st.error(f"❌ Fatal Error in App: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)