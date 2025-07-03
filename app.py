from flask import Flask, render_template, request
import instaloader
import requests
import os
from collections import deque
from time import time
from ai_analysis import analyze_bio_sentiment
from smart_analysis import analyze_profile

app = Flask(__name__)

leaderboard = deque(maxlen=5)

def format_number(n):
    return "{:,}".format(n).replace(",", ".")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        mode = request.form.get('mode', 'roasting')

        try:
            L = instaloader.Instaloader()
            profile = instaloader.Profile.from_username(L.context, username)
            img_url = profile.profile_pic_url
            img_path = os.path.join("static", f"{username}.jpg")
            with open(img_path, 'wb') as f:
                f.write(requests.get(img_url).content)

            info = {
                'username': profile.username,
                'full_name': profile.full_name,
                'followers': format_number(profile.followers),
                'followees': format_number(profile.followees),
                'posts': format_number(profile.mediacount),
                'followers_raw': profile.followers,
                'followees_raw': profile.followees,
                'posts_raw': profile.mediacount,
                'bio': profile.biography,
                'is_verified': profile.is_verified,
                'profile_pic_url': f"/static/{username}.jpg"
            }

            sentiment = analyze_bio_sentiment(profile.biography)
            profile_analysis = analyze_profile({
                'username': profile.username,
                'bio': profile.biography,
                'followers': profile.followers,
                'followees': profile.followees,
                'posts': profile.mediacount,
                'is_verified': profile.is_verified
            }, img_path, mode)

            # Ambil skor dan update leaderboard tanpa duplikat
            score_line = next((line for line in profile_analysis['insight'] if '⭐ Rating akun kamu:' in line), None)
            score = int(score_line.split(':')[-1].strip().split('/')[0]) if score_line else 0

            for entry in list(leaderboard):
                if entry['username'] == username:
                    leaderboard.remove(entry)
                    break

            leaderboard.appendleft({
                'username': username,
                'score': score,
                'profile_pic': info['profile_pic_url'],
                'time': time()
            })


            sorted_leaderboard = sorted(leaderboard, key=lambda x: (-x['score'], x['time']))


            return render_template('result.html', info=info, sentiment=sentiment,
                       profile_analysis=profile_analysis, leaderboard=sorted_leaderboard, mode=mode)


        except instaloader.exceptions.ProfileNotExistsException:
            return render_template('index.html', error=f"❌ Tidak menemukan username <strong>{username}</strong> di Instagram.")
        except Exception as e:
            return render_template('index.html', error=f"❌ Gagal mengambil data: {e}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)