from flask import Flask, render_template, request
from pypdf import PdfReader
import subprocess


app = Flask(__name__)



contract_text = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    global contract_text
    file = request.files["pdf"]
    reader = PdfReader(file)
    contract_text = ""

    for page in reader.pages:
        contract_text += page.extract_text()

    return render_template("chat.html")
@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]

    prompt = f"""
    You are a virtual legal assistant for small businesses.
    Answer only legal and contract related questions.

    Document:
    {contract_text}

    Question:
    {question}

    Answer in simple language.
    """

    result = subprocess.run(
        ["ollama", "run", "phi3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    answer = result.stdout

    return render_template("chat.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
