from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

MODEL = "gpt-5.6-luna"


def generate_answer(question, context):
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "You are an engineering document assistant. "
                    "Answer questions using only the provided document context. "
                    "If the context does not contain enough information, "
                    "say that the information is not available in the provided document. "
                    "Do not invent technical facts. "
                    "Cite the relevant page numbers using the exact format [Page X]. "
                    "Only cite page numbers that appear in the provided context. "
                    "Do not invent or guess page numbers."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Document context:\n{context}"
                )
            }
        ]
    )

    return response.output_text