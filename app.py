"""
OpenEnv-compliant Flask server with web interface
Provides both API endpoints for validation and a web UI
"""
from flask import Flask, request, jsonify, render_template_string
import subprocess
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from env.hiring_env import HiringEnv
from models.schemas import Action

app = Flask(__name__)

# Global environment instance
env_instance = None

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
            <strong>🎯 Tasks:</strong> 6 (Easy, Medium, Hard, Management, Marketing, Business)<br>
            <strong>🔗 API:</strong> /reset (POST), /step (POST), /state (GET)
        </div>
        
        <h2>Latest Test Results</h2>
        <pre>{{ output }}</pre>
        
        <form method="post" action="/">
            <button type="submit">🔄 Run Tests Again</button>
        </form>
        
        <h2>About</h2>
        <p>This OpenEnv environment evaluates AI agents on technical recruiting tasks. The agent must read job descriptions, review candidate resumes, and select the best-fit candidates based on skills and experience.</p>
        
        <p><strong>Scoring:</strong> F1 metric (0.0 to 1.0), where 1.0 = perfect selection</p>
        
        <h2>API Endpoints</h2>
        <pre>POST /reset?difficulty=easy
POST /step (body: {"selected_candidates": ["id1", "id2"]})
GET  /state</pre>
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

# ------------------------------------------------------------------
# OpenEnv API Endpoints
# ------------------------------------------------------------------

@app.route("/reset", methods=["POST"])
def reset():
    """Reset the environment and return initial observation"""
    global env_instance
    
    try:
        # Get difficulty from query params or default to 'easy'
        difficulty = request.args.get("difficulty", "easy")
        
        # Create new environment instance
        env_instance = HiringEnv(difficulty=difficulty)
        observation = env_instance.reset()
        
        # Return observation as JSON
        return jsonify({
            "observation": {
                "job_description": observation.job_description,
                "resumes": observation.resumes,
                "task_id": observation.task_id,
                "difficulty": observation.difficulty
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/step", methods=["POST"])
def step():
    """Execute one step in the environment"""
    global env_instance
    
    if env_instance is None:
        return jsonify({"error": "Environment not initialized. Call /reset first."}), 400
    
    try:
        # Parse action from request body
        data = request.get_json()
        if not data or "selected_candidates" not in data:
            return jsonify({"error": "Missing 'selected_candidates' in request body"}), 400
        
        action = Action(selected_candidates=data["selected_candidates"])
        
        # Execute step
        result = env_instance.step(action)
        
        # Return result as JSON
        return jsonify({
            "observation": {
                "job_description": result.observation.job_description,
                "resumes": result.observation.resumes,
                "task_id": result.observation.task_id,
                "difficulty": result.observation.difficulty
            },
            "reward": result.reward.score,
            "done": result.done,
            "info": result.info
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/state", methods=["GET"])
def state():
    """Get current environment state"""
    global env_instance
    
    if env_instance is None:
        return jsonify({"error": "Environment not initialized. Call /reset first."}), 400
    
    try:
        current_state = env_instance.state()
        return jsonify(current_state), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------------
# Web Interface
# ------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    """Web interface for viewing test results"""
    if request.method == "POST":
        output = run_inference()
    else:
        # Run once on startup
        output = run_inference()
    
    model = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    
    return render_template_string(HTML_TEMPLATE, output=output, model=model)

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
