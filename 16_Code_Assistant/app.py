import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    "Content-Type": "application/json",
}

history = []

def get_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)
    data = {
        "model" : "llama3.2:latest",
        "prompt": final_prompt,
        'stream': False,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response = response.text
        data = json.loads(response)
        actual_response = data["response"]
        return actual_response
    else:
        return "Error"
    


interface = gr.Interface(
    fn=get_response,
    inputs=gr.Textbox(lines=4, label="Enter your prompt here"),
    outputs="text",
    title="Code Assistant",
    description="A simple code assistant that helps you write code.",
    article="<p>This is a simple code assistant that helps you write code. It uses the <a href='https://github.com/emma-ai/emma'>Emma LLM</a> to generate code.</p>",
)


interface.launch()