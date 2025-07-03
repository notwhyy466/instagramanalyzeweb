import cv2
import re
import random
from ai_responses import get_response

def detect_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(image_path)
    if img is None:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces) > 0

def suggest_username(username):
    base = re.sub(r'[^a-zA-Z]', '', username.lower())
    if len(base) > 8:
        base = base[:8]
    options = [f"{base}.id", f"{base}_me", f"{base}.logi", f"{base}gram"]
    return options

def tone(roast, heal, mode):
    return roast if mode == "roasting" else heal

def detect_ig_personality(data, has_face):
    posts = data['posts']
    bio = data['bio'].lower()
    username = data['username'].lower()
    following = data['followees']
    followers = data['followers']

    personalities = [
        "🛒 Tipe kamu: 'Jiwa Dagang' – akun ini punya DNA bisnis dan orientasi jualan.",
        "🧢 Tipe kamu: 'Akun Cadangan' – sepi, misterius, dan tidak teridentifikasi.",
        "🤪 Tipe kamu: 'Receh Banget' – bio dan vibes kamu penuh kejenakaan!",
        "🔥 Tipe kamu: 'Aktif & Ambisius' – akunmu aktif, jelas, dan penuh energi positif.",
        "🎨 Tipe kamu: 'Estetik Misterius' – sedikit postingan, tapi estetik dan berkarakter.",
        "😴 Tipe kamu: 'Silent Viewer' – kamu suka scroll, tapi enggan muncul ke permukaan.",
        "👤 Tipe kamu belum terdeteksi, tapi potensimu besar. Bentuk branding-mu sekarang!"
    ]

    if "shop" in username or "jual" in bio:
        return personalities[0]
    if posts == 0 and not has_face and len(bio) < 5:
        return personalities[1]
    if "meme" in bio or "receh" in bio or "lawak" in bio:
        return personalities[2]
    if posts > 10 and has_face and len(bio) > 10:
        return personalities[3]
    if posts < 5 and not has_face:
        return personalities[4]
    if posts == 0 and following > followers:
        return personalities[5]

    return personalities[6]

def analyze_profile(profile_data, image_path, mode="roasting"):
    insight = []

    bio = profile_data['bio']
    username = profile_data['username']
    clean_bio = bio.strip()

    has_face = detect_face(image_path)
    if has_face:
        insight.append(tone("✅ Wajah terlihat di foto profil.", "✅ Wajah kamu tampak jelas, ini bagus untuk membangun koneksi.", mode))
    else:
        insight.append(get_response("pp_tidak_terlihat", mode))

    if profile_data['posts'] == 0:
        insight.append(get_response("feed_kosong", mode))
    else:
        insight.append(tone(f"✅ Terdapat {profile_data['posts']} postingan.", f"✅ Kamu sudah mulai aktif membagikan konten.", mode))

    if profile_data['followers'] == 0 and profile_data['followees'] == 0:
        insight.append(tone("❌ Akun ini sepi banget, bahkan IG-nya sendiri nggak follow.", "⚠️ Masih butuh interaksi, coba ikuti beberapa teman dulu.", mode))
    else:
        if profile_data['followees'] > profile_data['followers'] * 1.5:
            insight.append(get_response("rasio_follow", mode))
        else:
            insight.append(tone("✅ Rasio followers-following kamu udah keren.", "✅ Keseimbangan followers dan following kamu sudah bagus.", mode))

    if len(clean_bio) == 0:
        insight.append(get_response("bio_kosong", mode))
    elif len(clean_bio) < 10:
        insight.append(tone("⚠️ Bio terlalu singkat, kayak chat doi yang cuma 'ok'.", "⚠️ Bio kamu singkat banget, coba tambahkan sedikit lagi biar makin menarik.", mode))
    else:
        insight.append(tone("✅ Bio cukup informatif.", "✅ Bio kamu udah menggambarkan dirimu dengan baik.", mode))

    if profile_data.get('is_verified'):
        insight.append(tone("✅ Centang biru terdeteksi, siapakah kamu sebenarnya?", "✅ Kamu sudah terverifikasi, ini meningkatkan kepercayaan publik.", mode))
    else:
        insight.append(tone("❌ Belum centang biru, tenang bukan berarti kamu nggak keren.", "⚠️ Akun belum terverifikasi, tapi kamu tetap punya potensi kok.", mode))

    score = 0
    if has_face:
        score += 3
    if profile_data['posts'] > 1:
        score += 2
    if profile_data['followees'] <= profile_data['followers'] * 1.5:
        score += 2
    if len(clean_bio) >= 3:
        score += 1

    alay_keywords = ['123', 'abc', '__', 'xx', 'zzz', 'anjay', 'ganteng', 'cantik']
    is_alay = any(kw in username.lower() for kw in alay_keywords)
    is_too_long = len(username) > 15
    if not is_alay and not is_too_long:
        score += 2
        insight.append(tone("✅ Username clean dan profesional.", "✅ Username kamu terlihat singkat dan enak dibaca.", mode))
    else:
        insight.append(get_response("username_alay", mode))
        suggestions = suggest_username(username)
        insight.append(tone(f"Coba: {', '.join(suggestions)}", f"Rekomendasi: {', '.join(suggestions)}", mode))

    suspicious = 0
    if profile_data['posts'] == 0:
        suspicious += 1
    if profile_data['followees'] > profile_data['followers'] * 1.5:
        suspicious += 1
    if not has_face:
        suspicious += 1
    if len(clean_bio) < 5:
        suspicious += 1

    if suspicious >= 2:
        insight.append(tone("❗ Akun ini mencurigakan, bisa jadi akun fake/fess.", "⚠️ Profil kamu perlu dilengkapi supaya terlihat lebih meyakinkan.", mode))
    else:
        insight.append(tone("✅ Akun ini terlihat asli dan aktif.", "✅ Akunmu tampak terpercaya dan asli.", mode))

    if profile_data['posts'] < 3:
        insight.append(tone("❌ Feed masih sepi, ini IG atau tempat tinggal alien?", "⚠️ Feed kamu masih kosong, yuk mulai upload konten yang kamu suka.", mode))
    else:
        insight.append(tone("✅ Feed kamu cukup aktif, tinggal ditingkatkan aja.", "✅ Feed kamu sudah aktif, tinggal jaga konsistensinya.", mode))

    branding = "🧑‍💼 Personal"
    if any(word in username.lower() or word in bio.lower() for word in ["shop", "store", "official", "cv", "pt", "logistik", "cargo", "jualan"]):
        branding = "🛍️ Bisnis"
    elif any(word in bio.lower() for word in ["photography", "influencer", "travel", "gym", "fit", "content"]):
        branding = "📸 Kreator"

    insight.append(tone(f"AI Deteksi Branding: {branding}", f"Jenis akunmu terdeteksi sebagai: {branding}", mode))
    

    if score >= 8:
        insight.append(tone("✅ Akun ini sangat layak di-follow.", "✅ Akunmu terlihat menarik dan terpercaya untuk diikuti.", mode))
    elif score >= 5:
        insight.append(tone("⚠️ Akun ini cukup oke, tapi masih bisa ditingkatkan.", "⚠️ Kamu sudah di jalur yang baik, tinggal ditingkatkan sedikit lagi.", mode))
    else:
        insight.append(tone("🚫 Belum layak di-follow, upgrade dulu ya.", "🚫 Masih perlu perbaikan agar akunmu lebih menarik dan kredibel.", mode))

    dna_traits = []
    if any(word in username.lower() or word in bio.lower() for word in ["store", "shop", "jualan", "olshop"]):
        dna_traits.append("🛒 40% Jualan")
    if any(word in bio.lower() for word in ["galau", "rindu", "sendiri", "move on"]):
        dna_traits.append("😢 30% Galau")
    if any(word in bio.lower() for word in ["aesthetic", "filter", "preset", "feed"]):
        dna_traits.append("🎨 30% Estetik")
    if any(word in bio.lower() for word in ["funny", "meme", "lawak", "receh"]):
        dna_traits.append("🤣 25% Lawak")
    if any(word in bio.lower() for word in ["kuliah", "mahasiswa", "belajar"]):
        dna_traits.append("📚 20% Akademis")

    if dna_traits:
        insight.append(tone("🧬 IG DNA kamu: " + ', '.join(dna_traits), "🧬 Komposisi kepribadian akunmu: " + ', '.join(dna_traits), mode))
    else:
        insight.append(tone("🧬 IG kamu masih netral, bisa kamu bentuk sesuai branding-mu.", "🧬 IG kamu fleksibel, tinggal kamu arahkan sesuai passion-mu.", mode))
    
    insight.append(f"⭐ Rating akun kamu: {min(score, 10)} / 10")
    
    personality = detect_ig_personality(profile_data, has_face)
    insight.append(personality)
    
    return {'insight': insight}
