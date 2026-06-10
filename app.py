
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    print("Received request.")
    print("Headers:", dict(request.headers))
    print("JSON body:", request.json)

    token = None
    if request.json:
        token = request.json.get("access_token")

    # If we got an access token, let's test it against Microsoft Graph
    if token:
        print("Testing Microsoft Graph token...")

        graph_resp = requests.get(
            "https://graph.microsoft.com/v1.0/sites?search=*",
            headers={"Authorization": f"Bearer {token}"},
        )

        print("Graph status:", graph_resp.status_code)
        print("Graph response text:", graph_resp.text)

        return jsonify({
            "status": "received_token",
            "graph_status": graph_resp.status_code,
            "graph_text": graph_resp.text
        })

    # No token — just respond normally
    return jsonify({"status": "ok", "message": "No token received"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
