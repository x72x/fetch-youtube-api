<p align="center">
    <a href="https://github.com/x72x/fetch-youtube-api">
        <img src="https://lh3.googleusercontent.com/3zkP2SYe7yYoKKe47bsNe44yTgb4Ukh__rBbwXwgkjNRe4PykGG409ozBxzxkrubV7zHKjfxq6y9ShogWtMBMPyB3jiNps91LoNH8A=s500" alt="fetch-youtube-api" width="256">
    </a>
    <br>
    <b>
      YouTube Stuff API
    </b>
    <br>
</p>

# How to use ?
## Fetch stream url:
---
- Parameters: link , format ( optional, default to audio )
- `http://127.0.0.1/stream?link=https://youtu.be/xxxxxx`
- Response: STREAM url of audio/video

## Fetch video info:
---
- Parameters: link
- `http://127.0.0.1/fetch?link=https://youtu.be/xxxxxx`
- Response: All video data with multiple formats in json
```json
{
    "id": "e-ORhEE9VVg",
    "title": "Taylor Swift - Blank Space",
    "formats": [
        {
            "format_id": "616",
            "format_index": null,
            "url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1696391289/ei/GYwcZaajB4-IW9iDkeAB/ip....index.m3u8",
            "manifest_url": "https://manifest.googlevideo.com/api/manifest/hls_variant/expire/1696391289/ei/GYwcZaajB4-IW9iDkeAB/ip.....index.m3u8",
            "tbr": 4723.599,
            "ext": "mp4",
            "fps": 24.0,
            "protocol": "m3u8_native",
            "preference": null,
            "quality": 9,
            "has_drm": false,
            "width": 1920,
            "height": 1080,
            "vcodec": "vp09.00.40.08",
            "acodec": "none",
            "dynamic_range": "SDR",
            "source_preference": 99,
            "format_note": "Premium",
            "resolution": "1920x1080",
            "aspect_ratio": 1.78,
            "video_ext": "mp4",
            "audio_ext": "none",
            "abr": 0,
            "vbr": 4723.599,
            "format": "616 - 1920x1080 (Premium)"
        }
    ],
    "thumbnails": [
        {
            "url": "https://i.ytimg.com/vi/e-ORhEE9VVg/maxresdefault.jpg",
            "height": 1080,
            "width": 1920,
            "preference": -1,
            "id": "40",
            "resolution": "1920x1080"
        },
    ],
    "thumbnail": "https://i.ytimg.com/vi/e-ORhEE9VVg/maxresdefault.jpg",
    "description": "",
    "channel_id": "UCANLZYMidaCbLQFWXBC95Jg",
    "channel_url": "https://www.youtube.com/channel/UCANLZYMidaCbLQFWXBC95Jg",
    "duration": 272,
    "categories": [
        "Music"
    ],
    "subtitles": {
        "en-nP7-2PuUl7o": [
            {
                "ext": "json3",
                "url": "https://www.youtube.com/api/timedtext?v=e-ORhEE9VVg&ei=GIwcZY_8C6m5mLAP98ag-Ak&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1696394888&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Copi%2Cxoaf&signature=CE85A6EFBBF5F98EC2BED18D5BE13260948B7EF8.976502AF19DA0EAFCA27726EA7678B98B7385CB4&key=yt8&lang=en&name=en&fmt=json3",
                "name": "English - en"
            },
        ]
    },
    "comment_count": 635000,
    "channel": "Taylor Swift",
    "channel_follower_count": 54300000,
    "channel_is_verified": true,
    "uploader": "Taylor Swift",
}
```
- And too many details .. :)

## YouTube search:
---
- Parameters: q ( query )
- `http://127.0.0.1/search?q=Blank+Space`
- Response: Array of results
```json
[
    {
        "id": "e-ORhEE9VVg",
        "thumbnails": [
            "https://i.ytimg.com/vi/e-ORhEE9VVg/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLC7LLziwR69qyxJPrp91dqJE8K_3A",
            "https://i.ytimg.com/vi/e-ORhEE9VVg/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLAi4Oi5FjsX69xGpTO9vn1ILcye3A"
        ],
        "title": "Taylor Swift - Blank Space",
        "channel": "Taylor Swift",
        "duration": "4:33",
        "views": "3,266,488,618 views",
        "publish_time": "8 years ago",
        "url_suffix": "/watch?v=e-ORhEE9VVg&pp=ygULQmxhbmsgU3BhY2U%3D"
    },
    {
        "id": "nAQ_1lTDvPQ",
        "thumbnails": [
            "https://i.ytimg.com/vi/nAQ_1lTDvPQ/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDEFmkis8iQqGK-bSUFhNIiO5ZWdA",
            "https://i.ytimg.com/vi/nAQ_1lTDvPQ/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDvLZqWrBW4C-JsAyIp3fB68EFAcA"
        ],
        "title": "Taylor Swift - Blank Space (Lyrics)",
        "channel": "Vibe Music",
        "duration": "3:52",
        "views": "5,287,558 views",
        "publish_time": "3 months ago",
        "url_suffix": "/watch?v=nAQ_1lTDvPQ&pp=ygULQmxhbmsgU3BhY2U%3D"
    },
]
```

# Get help ?
## Telegram Community
---
- [Support group](https://telegram.me/PyhonProjectsChat)
- [Updates channel](https://telegram.me/Y88F8)
