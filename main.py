import json
import youtube_search
import yt_dlp
import telebot
import os

from flask import Flask, request, Response

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

@app.route("/tg", methods=["POST", "GET"])
def send_to_telegram():
    if request.method == "GET":
        link = request.args.get("link")
        format = request.args.get("format")
        chat_id = request.args.get("chat_id")
        msg_id = request.args.get("msg_id")
        token = request.args.get("token")
    elif request.method == "POST":
        link = request.form.get("link")
        format = request.form.get("format")
        chat_id = request.form.get("chat_id")
        msg_id = request.form.get("msg_id")
        token = request.form.get("token")
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
    
    if (link is None) or (chat_id is None) or (token is None):
        return Response(
            json.dumps(
                {
                    'error': True,
                    'message': 'link, chat_id and token required'
                }
            ),
            status=400,
            mimetype="application/json"
        )
    
    try:
        bot = telebot.TeleBot(token=token)
        yt = yt_dlp.YoutubeDL({"format": "bestaudio[ext=m4a]" if (format is None) or (format == "audio") else "best"})
        info = yt.extract_info(link, download=False)
        if int(info['duration']) > 1505:
            return Response(
                json.dumps(
                    {
                        'error': True,
                        'message': 'duration limit is 25M'
                    }
                ),
                status=400,
                mimetype="application/json"
            )
        else:
            info = yt.extract_info(link, download=True)
            file_name = yt.prepare_filename(info)
            with open(file_name, "rb") as f:
                if (format is None) or (format == "audio"):
                    message = bot.send_audio(
                        chat_id=chat_id,
                        audio=f,
                        title=info['title'],
                        duration=int(info['duration']),
                        performer=info['channel'],
                        reply_to_message_id=msg_id
                    )
                else:
                    message = bot.send_video(
                        chat_id=chat_id,
                        video=f,
                        duration=int(info['duration']),
                        reply_to_message_id=msg_id
                    )
            os.remove(file_name)
            dic = message.__dict__
            for i in dic:
                if not dic[i]:
                    del dic[i]
            return Response(
                json.dumps(
                    dic,
                    ensure_ascii=False,
                    indent=4
                ),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        try:
            os.remove(file_name)
        except:
            pass
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
