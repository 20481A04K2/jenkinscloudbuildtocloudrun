from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Hello from Cloud Run deployed via jenkins!"

if __name__ == '__main__':
    # Cloud Run expects the app to listen on port 8080 and 0.0.0.0
    app.run(host='0.0.0.0', port=8080)
