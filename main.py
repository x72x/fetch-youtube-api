import subprocess
import json
import youtube_search

from flask import Flask, request, Response

app = Flask(__name__)

def fetch_link(
        link: str,
        format: str
) -> str:
    return subprocess.check_output(
        "yt-dlp -g -f {format} {link}".format(
            format="bestaudio[ext=m4a]" if format == "audio" else "b",
            link=link
        )
    ).decode().strip()

def fetch(
        link: str
) -> str:
    return json.dumps(
        json.loads(
            subprocess.check_output("yt-dlp -J {link}".format(
                    link=link
                )
            )
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

@app.route("/fetch_link", methods=["GET", "POST"])
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
        return Response(
            fetch_link(
                link=link,
                format=format or "audio"
            ),
            status=200,
            mimetype="text/plain",
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
    
@app.route("/")
def _():
    return ":)"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80,
        debug=True
    )
