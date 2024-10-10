from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Optional: Run the app in debug mode for development
if __name__ == '__main__':
    app.run(debug=True)