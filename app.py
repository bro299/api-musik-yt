from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_music():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'skip_download': True,
            'writethumbnail': True,
            'outtmpl': '%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if 'entries' in info_dict:
                info_dict = info_dict['entries'][0]

            title = info_dict.get('title', 'No title')
            thumbnail = info_dict.get('thumbnail', 'No thumbnail')
            download_url = info_dict.get('url', 'No URL')

            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'download_url': download_url
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
