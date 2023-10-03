import json
import youtube_search
import yt_dlp
import requests
import io

from flask import Flask, request, Response, send_file
from random import randint

app = Flask(__name__)

def fetch_link(
        link: str,
        format: str
) -> str:
    return yt_dlp.YoutubeDL({"format": "bestaudio[ext=m4a]" if format == "audio" else "best"}).extract_info(
        url=link,
        download=False
    )["url"]

def fetch(
        link: str
) -> str:
    return json.dumps(
        yt_dlp.YoutubeDL().extract_info(
            url=link,
            download=False
        ),
        ensure_ascii=False,
        indent=4
    )

def search(
        query: str
) -> str:
    return json.dumps(
        youtube_search.YoutubeSearch(query, max_results=10).to_dict(),
        ensure_ascii=False,
        indent=4
    )

@app.route("/search", methods=["GET", "POST"])
def search_rule():
    if request.method == "GET":
        query = request.args.get("q")
    elif request.method == "POST":
        query = request.form.get("q")
    else:
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': 'Invalid method'
                }
            ),
            status=400,
            mimetype="application/json"
        )
    
    if query is None:
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': 'query is required'
                }
            ),
            status=400,
            mimetype="application/json"
        )
    
    return Response(
        search(query=query),
        status=200,
        mimetype="application/json"
    )

@app.route("/fetch", methods=["GET", "POST"])
def fetch_rule():
    if request.method == "GET":
        link = request.args.get("link")
    elif request.method == "POST":
        link = request.form.get("link")
    else:
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': 'Invalid method'
                }
            ),
            status=400,
            mimetype="application/json"
        )
    
    if link is None:
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': 'link is required'
                }
            ),
            status=400,
            mimetype="application/json"
        )

    try:
        return Response(
            fetch(
                link=link
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': str(e)
                }
            ),
            status=400,
            mimetype="application/json"
        )

@app.route("/stream", methods=["GET", "POST"])
def fetch_link_rule():
    if request.method == "GET":
        link = request.args.get("link")
        format = request.args.get("format")
    elif request.method == "POST":
        link = request.form.get("link")
        format = request.form.get("format")
    else:
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': 'Invalid method'
                }
            ),
            status=400,
            mimetype="application/json"
        )
    
    if link is None:
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': 'link is required'
                }
            ),
            status=400,
            mimetype="application/json"
        )
    
    try:
        _ = fetch_link(link=link, format=format or "audio")
        res = requests.get(_)
        file = io.BytesIO()
        file.write(res.content)
        file.name = f"{randint(100000, 9999999)}.m4a" if format == "audio" else f"{randint(100000, 9999999)}.mp4"
        return send_file(file.name)
    except Exception as e:
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': str(e)
                }
            ),
            status=400,
            mimetype="application/json"
        )
    
@app.route("/")
def _():
    return Response(
            ":)",
            status=200,
            mimetype="text/plain",
        )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80,
        debug=True
    )
