from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm(config):
    model = config["llm"]["model"]
    api_key = config["llm"]["api_key"]

    return ChatGoogleGenerativeAI(model=model, api_key=api_key)

def generate_reply(post_text, config):
    llm = get_llm(config)
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Write a short, natural, and non-spammy Reddit reply "
        "to this post (max 3 sentences). Avoid marketing tone. \n\nPost:\n{post}"
    )
    chain = prompt | llm
    return chain.invoke({"post": post_text}).content
