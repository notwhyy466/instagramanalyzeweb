# Kumpulan jawaban AI dalam gaya Roasting dan Healing untuk setiap aspek analisis IG
# Digunakan oleh smart_analysis.py untuk menghasilkan respon acak dan lebih variatif

import random

def get_response(aspek, mode="roasting"):
    RESPONSES = {
        "pp_tidak_terlihat": {
            "roasting": [
                "❌ Foto profilmu gelap, ini IG atau CCTV gang?",
                "❌ Mukamu kemana? Ini akun manusia atau ninja?",
                "❌ No face detected. Akun ini lebih misterius dari isi chat dia.",
                "❌ Gak ada wajahnya. Ini akun IG atau kartu keluarga?",
                "❌ PP kamu nihil. Bahkan alien pun lebih jelas mukanya."
            ],
            "healing": [
                "⚠️ Belum ada wajah di PP, coba tampilkan biar lebih mudah dikenali.",
                "⚠️ Foto wajah bikin akunmu terasa lebih personal dan connectable.",
                "⚠️ Gak apa-apa belum pasang wajah, tapi lebih baik ditambahkan kalau siap.",
                "⚠️ Wajah kamu adalah identitas, ayo tampilkan versi terbaikmu.",
                "⚠️ Yuk tampilkan foto wajah agar akunmu lebih akrab dan dipercaya."
            ]
        },
        "bio_kosong": {
            "roasting": [
                "❌ Bio kosong, kayak hati dia pas ghosting kamu.",
                "❌ Isi bio dong, ini IG bukan Google Form kosong.",
                "❌ Bio-nya nihil. Bahkan buku harian anak SD lebih informatif.",
                "❌ Kosong banget, bahkan file .txt aja masih ada isinya.",
                "❌ Bio kamu diam seribu bahasa. Malu atau nggak niat?"
            ],
            "healing": [
                "⚠️ Bio kamu masih kosong, yuk isi dengan hal menarik tentang dirimu.",
                "⚠️ Coba tambahkan sedikit tentang dirimu agar akunmu lebih menonjol.",
                "⚠️ Bio adalah kesan pertama. Tulis satu kalimat aja dulu nggak apa-apa kok.",
                "⚠️ Yuk mulai dari satu kata yang menggambarkan kamu.",
                "⚠️ Bio bisa bantu orang mengenalmu. Tulis dengan jujur dan singkat."
            ]
        },
        "feed_kosong": {
            "roasting": [
                "❌ Feed-nya kosong. Ini IG atau tempat persembunyian?",
                "❌ Belum posting apapun. Jangan-jangan ini akun pengintai diam-diam?",
                "❌ Kosong melompong. Cuma terlihat jejak kamu ngintip doang.",
                "❌ Feed kamu kayak rumah kosong — sunyi dan spooky.",
                "❌ Gak ada postingan. Bahkan IG baru aja udah punya reels."
            ],
            "healing": [
                "⚠️ Belum ada postingan, tapi gak apa-apa. Mulai aja dari 1 foto favorit kamu.",
                "⚠️ Yuk mulai berbagi momen seru kamu di feed!",
                "⚠️ Feed kosong itu peluang. Kamu bisa mulai bangun branding dari sekarang.",
                "⚠️ Jangan takut posting, semua kreator juga mulai dari 0.",
                "⚠️ Unggah momen kecilmu, itu bisa jadi awal yang besar."
            ]
        },
        "username_alay": {
            "roasting": [
                "❌ Username alay banget. Ini IG atau kode nuklir?",
                "❌ Susah dibaca, susah diingat. Branding-nya gagal dari username.",
                "❌ Username kayak nama akun prank tahun 2012.",
                "❌ Penuh angka dan simbol. Username atau password?",
                "❌ Username kamu ribet banget. Ini akun IG atau sandi WiFi?"
            ],
            "healing": [
                "⚠️ Username kamu bisa disingkat supaya lebih clean.",
                "⚠️ Coba ganti ke nama yang lebih profesional dan mudah dibaca.",
                "⚠️ Username bagus itu kunci personal branding loh.",
                "⚠️ Bikin username yang gampang diingat biar orang mudah cari kamu.",
                "⚠️ Coba pikirin nama yang ringkas dan sesuai niche kamu."
            ]
        },
        "rasio_follow": {
            "roasting": [
                "⚠️ Following kamu kebanyakan, ini follow akun atau jadi stalker?",
                "⚠️ Jumlah following bikin IG kamu keliatan needy banget.",
                "⚠️ Rasio gak seimbang. IG kamu lebih butuh dari chat mantan.",
                "⚠️ Following segunung, followers secuil. Kayak neraca miring.",
                "⚠️ Nampak haus atensi. Yuk diatur follow-nya."
            ],
            "healing": [
                "⚠️ Coba seimbangkan followers dan following untuk terlihat lebih kredibel.",
                "⚠️ Perhatikan proporsi following agar branding kamu makin kuat.",
                "⚠️ Yuk pelan-pelan kurangi akun yang gak perlu kamu ikuti.",
                "⚠️ Rasio yang seimbang bikin akun kamu lebih profesional.",
                "⚠️ Ikuti akun yang benar-benar relevan sama tujuanmu."
            ]
        }
    }
    return random.choice(RESPONSES.get(aspek, {}).get(mode, ["(tidak ada respon)"]))
