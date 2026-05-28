from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

API = "https://tbox-share-list-v2.subhodas5673.workers.dev/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}


def extract_surl(url):

    match = re.search(r'/s/([A-Za-z0-9_-]+)', url)

    if not match:
        raise Exception("Invalid Terabox URL")

    surl = match.group(1)

    # remove first 1 if exists
    if surl.startswith("1"):
        surl = surl[1:]

    return surl


@app.route("/")
def home():

    return """
    <html>
    <head>
        <title>Terabox API</title>

        <style>

            body{
                background:#111;
                color:white;
                font-family:Arial;
                padding:40px;
            }

            input{
                width:80%;
                padding:12px;
                border:none;
                border-radius:8px;
                margin-bottom:10px;
            }

            button{
                padding:12px 20px;
                border:none;
                border-radius:8px;
                background:#00b894;
                color:white;
                cursor:pointer;
            }

            pre{
                background:#222;
                padding:20px;
                border-radius:10px;
                overflow:auto;
                white-space:pre-wrap;
                word-wrap:break-word;
            }

            .copy-btn{
                margin-top:10px;
                background:#0984e3;
            }

        </style>
    </head>

    <body>

        <h1>Terabox API</h1>

        <input type="text" id="url" placeholder="Paste Terabox URL">

        <button onclick="fetchData()">Fetch</button>

        <button class="copy-btn" onclick="copyData()">Copy JSON</button>

        <pre id="result"></pre>

        <script>

            async function fetchData(){

                const url = document.getElementById("url").value;

                const res = await fetch(`/tera?url=${encodeURIComponent(url)}`);

                const data = await res.json();

                document.getElementById("result").textContent =
                    JSON.stringify(data, null, 2);
            }

            function copyData(){

                const text =
                    document.getElementById("result").textContent;

                navigator.clipboard.writeText(text);

                alert("Copied");
            }

        </script>

    </body>
    </html>
    """


@app.route("/tera")
def tera():

    url = request.args.get("url")

    if not url:
        return jsonify({
            "error": "Missing url parameter"
        }), 400

    try:

        surl = extract_surl(url)

        payload = {
            "domain": "terabox.com",
            "surl": surl,
            "root": 1,
            "page": 1
        }

        response = requests.post(
            API,
            json=payload,
            headers=HEADERS,
            timeout=30
        )

        return jsonify(response.json())

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
