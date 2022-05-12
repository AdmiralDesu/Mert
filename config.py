audio_opts = {
    'format': 'bestaudio/best',
    'forcefilename': 'True',
    'outtmpl': './music/from_youtube/%(id)s.%(ext)s',
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',

        },

    ]
}

video_opts = {
    'forcefilename': 'True',
    'outtmpl': './video/%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'
    }]

}
