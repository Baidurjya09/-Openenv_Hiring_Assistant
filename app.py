"""
Simple web interface for HuggingFace Space
Keeps the container running and displays results
"""
from flask import Flask, render_template_string
import subprocess
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Hiring Assistant - OpenEnv</title>
    <style>
        body { font-family: monospace; padding: 20px; background: #1e1e1e; color: #d4d4d4; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #4ec9b0; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #1e3a1e; border: 1px solid #4ec9b0; }
        .info { background: #1e2a3a; border: 1px solid #569cd6; }
        pre { background: #252526; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .score { color: #4ec9b0; font-weight: bold; }
        button { background: #0e639c; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #1177bb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Hiring Assistant - OpenEnv Environment</h1>
        
        <div class="status success">
            <strong>✅ Status:</strong> Deployed and Running
        </div>
        
        <div class="status info">
            <strong>📊 Model:</strong> {{ model }}<br>
            <strong>🎯 Tasks:</strong> 6 (Easy, Medium, Hard, Management, Marketing, Business)
        </div>
        
        <h2>Latest Test Results</h2>
        <pre>{{ output }}</pre>
        
        <form method="post" action="/">
            <button type="submit">🔄 Run Tests Again</button>
        </form>
        
        <h2>About</h2>
        <p>This OpenEnv environment evaluates AI agents on technical recruiting tasks. The agent must read job descriptions, review candidate resumes, and select the best-fit candidates based on skills and experience.</p>
        
        <p><strong>Scoring:</strong> F1 metric (0.0 to 1.0), where 1.0 = perfect selection</p>
    </div>
</body>
</html>
"""

def run_inference():
    """Run the inference script and capture output"""
    try:
        result = subprocess.run(
            ["python", "inference.py"],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error running inference: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        output = run_inference()
    else:
        # Run once on startup
        output = run_inference()
    
    model = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    
    return render_template_string(HTML_TEMPLATE, output=output, model=model)

if __name__ == "__main__":
    from flask import request
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
