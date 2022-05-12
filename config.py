audio_opts = {
        'format': 'bestaudio/best',
        'forcefilename': 'True',
        'outtmpl': './music/from_youtube/%(title)s-%(id)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',

            },

        ]
    }

video_opts = {
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mkv'
    }]

}
