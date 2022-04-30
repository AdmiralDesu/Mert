opts = {
        'format': 'bestaudio/best',
        'forcefilename': 'True',
        'outtmpl': './music/%(title)s-%(id)s.%(ext)s',
        'no-remove-chapters': 'True',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',

            },

        ]
    }
