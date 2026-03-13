from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Automated Incident Response",
        "version": "1.0.0"
    }), 200

if __name__ == "__main__":
    app.run()