import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import urllib.parse
import base64


def set_background(image_path):
    """
    Sets a custom background image for the Streamlit app from a local file.
    :param image_path: Path to the image file.
    """
    with open(image_path, "rb") as image_file:
        bin_str = base64.b64encode(image_file.read()).decode()
        page_bg_img = f"""
        <style>
        .stApp {{
          background-image: url("data:image/png;base64,{bin_str}");
          background-size: cover;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)


def generate_mailto_link(email_link, subject, body):
    """
    Generates a mailto link for composing emails.
    """
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body)
    mailto_link = f"mailto:{email_link}?subject={encoded_subject}&body={encoded_body}"
    return mailto_link


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("🚀 Job Posting Mail Generator")
    url_input = st.text_input("Enter a URL:")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            for job in jobs:
                skills = job.get("skills", [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language="markdown")
                email_link = "shashankshende3110@gmail.com"
                subject = "Applying for job role"
                mailto_link = generate_mailto_link(email_link, subject, email)

                # Create a clickable highlighted "Compose in Gmail" text link
                st.markdown(
                    f'<a href="{mailto_link}" target="_blank" style="color: #FF4B4B; font-weight: bold; text-decoration: underline;">Compose an Email</a>',
                    unsafe_allow_html=True,
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(page_title="Email Generator", page_icon="🚀")

    set_background(
        "D:/.projects/GEN  AI projects/Restaurant_Name_Genrator/Email_genrator_tool/resources/c3uhsgo1vx541.jpg"
    )
    create_streamlit_app(chain, portfolio, clean_text)
