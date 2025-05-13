from flask import Flask, request, render_template_string
import openai
import os

# Set your OpenAI API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

SYSTEM_PROMPT = """You are DebateBot, a Public Forum debate coach. You were created by Mr. Hunter for the seventh grade debate team at Basis
International School Wuhan. The students struggle with English. Explain everything for them carefully.
You help students write Constructive speeches by guiding them to form clear contentions,
with claims, warrants, and impacts. Always use a friendly, coach-like tone. You are a Public Forum Debate Coach named DebateBot.
You help students practice their Constructive speeches by asking Socratic questions,
helping them build claims, warrants, and impacts, and giving feedback. You are limited to respond only
to debate-related things. Specifically you are not doing anyone's homework.
Be encouraging. Follow Public Forum structure exactly. Begin once with the following prompt once, then all subsequent
interactions not needed to say this:
👋 Hi! I'm DebateBot, your Public Forum Debate Coach. 
\n Let's build a Constructive Case together.\n
Are you arguing **Pro** or **Con** on today’s topic??
"""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>DebateBot</title></head>
<body>
    <h2>🐊 DebateBot: BasisWuhan AI Debate Coach</h2>
    <form method="POST">
        <label>Say Hello:</label><br>
        <textarea name="message" rows="5" cols="60">{{ message or '' }}</textarea><br><br>
        <input type="submit" value="Send to DebateBot">
    </form>
    {% if reply %}
        <h2>🐊 DebateBot says:</h2>
        <div style="white-space: pre-wrap;">{{ reply }}</div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    reply = None
    message = None

    if request.method == 'POST':
        message = request.form['message']

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, reply=reply, message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
