# ================= GURUH VA TOPIC ID'LAR (BIR MARTA YOZAMIZ) =================

# Guruh ID'si (hammasida bir xil)
ch = -1004324672328

# Har bir topic uchun o'z raqamini yozing (botdan olgan raqamingizni shu yerga qo'ying)
# Masalan: Uzb Movie uchun bot sizga 23, Eng Movie uchun 24 deb bergan bo'lsa:
UZB_MOVIE = 2     # Uzb Movie
ENG_MOVIE = 24     # Eng Movie
UZB_CARTOON = 25   # Uzb Cartoon
ENG_CARTOON = 26   # Eng Cartoon
UZB_ANIME = 27     # Uzb Anime
ENG_ANIME = 28     # Eng Anime

# ================= KONTENT RO'YXATI =================

UZB_MEDIA = {
    "movies": [
        # Oddiy film (qismsiz)
        {"chat_id": ch, "message_thread_id": UZB_MOVIE, "message_id": 1, "title": "bosma! film yoq baribir"},
        
        # Qismlari bo'lgan film (Marvel guruhi)
        {
            "title": "Temir Odam [1,2,3]",
            "episodes": [
                {"chat_id": ch, "message_thread_id": UZB_MOVIE, "message_id": 25, "title": "[1] Temir Odam 1 (2008)"},
                {"chat_id": ch, "message_thread_id": UZB_MOVIE, "message_id": 27, "title": "[2] Temir Odam 2 (2010)"},
                {"chat_id": ch, "message_thread_id": UZB_MOVIE, "message_id": 29, "title": "[3] Temir Odam 3 (2013)"},
            ]
        },
        
        # O'rgimchak odam
        {
            "title": "O'rgimchak odam [1,2,3,4]",
            "episodes": [
                {"chat_id": ch, "message_thread_id": UZB_MOVIE, "message_id": 39, "title": "[1] Uyga qaytish (2017)"},
                {"chat_id": ch, "message_thread_id": UZB_MOVIE, "message_id": 40, "title": "[2] Uydan uzoqda (2019)"},
                {"chat_id": ch, "message_thread_id": UZB_MOVIE, "message_id": 41, "title": "[3] Uyga yo'l yo'q (2021)"},
                {"chat_id": ch, "message_thread_id": UZB_MOVIE, "message_id": 42, "title": "[4] Yangi kun (2026)"},
            ]
        },
        # ... qolgan kinolar ham shu tarzda davom etadi
    ],
    "cartoons": [
        {"chat_id": ch, "message_thread_id": UZB_CARTOON, "message_id": 2, "title": "Multfilm nomi 1"},
    ],
    "anime": [
        {
            "title": "Anime nomi 1",
            "episodes": [
                {"chat_id": ch, "message_thread_id": UZB_ANIME, "message_id": 2, "title": "1-qism"},
                {"chat_id": ch, "message_thread_id": UZB_ANIME, "message_id": 4, "title": "2-qism"},
            ]
        },
    ],
}

ENG_MEDIA = {
    "movies": [
        {"chat_id": ch, "message_thread_id": ENG_MOVIE, "message_id": 200, "title": "Movie name 1"},
        {
            "title": "Marvel",
            "episodes": [
                {"chat_id": ch, "message_thread_id": ENG_MOVIE, "message_id": 202, "title": "Iron Man (2008)"},
                {"chat_id": ch, "message_thread_id": ENG_MOVIE, "message_id": 204, "title": "Iron Man (2011)"},
            ]
        },
    ],
    "cartoons": [
        {"chat_id": ch, "message_thread_id": ENG_CARTOON, "message_id": 2, "title": "Cartoon name 1"},
    ],
    "anime": [
        {
            "title": "Anime name 1",
            "episodes": [
                {"chat_id": ch, "message_thread_id": ENG_ANIME, "message_id": 2, "title": "Episode 1"},
                {"chat_id": ch, "message_thread_id": ENG_ANIME, "message_id": 4, "title": "Episode 2"},
            ]
        },
    ],
}