# Media kontenti (filmlar, multfilmlar, animelar) shu yopiq guruh/kanalda saqlanadi.
# movies / cartoons: har bir element {chat_id, message_thread_id, message_id, title}
# anime: har bir anime {title, episodes: [{chat_id, message_thread_id, message_id, title}, ...]}
#
# Yangi ID olish uchun: guruhga xabar tashlang -> bot sizga Chat ID, Message ID va Topic ID (thread_id) ni qaytaradi
# O'sha qiymatlarni quyidagi `None` o'rniga yozing.

UZB_MEDIA = {
    "movies": [
        # Oddiy film (qismsiz)
        {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "bosma! film yoq baribir"},
        
        # Qismlari bo'lgan film (Marvel guruhi)
        {
            "title": "Temir Odam [1,2,3]",
            "episodes": [
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[1] Temir Odam 1 (2008)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[2] Temir Odam 2 (2010)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[3] Temir Odam 3 (2013)"},
            ]
        },
        
        # Yana yangi film qo'shish uchun shu yerda davom eting (masalan Spiderman)
        {
            "title": "O'rgimchak odam [1,2,3,4]",
            "episodes": [
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[1] Uyga qaytish (2017)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[2] Uydan uzoqda (2019)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[3] Uyga yo'l yo'q (2021)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[4] Yangi kun (2026)"},
            ]
        },
        {
            "title": "Men Grutman [1,2,3,4,5]",
            "episodes": [
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Men Grutman 1"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Men Grutman 2"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Men Grutman 3"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Men Grutman 4"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Men Grutman 5"},
            ]
        },
        {
            "title": "Kapitan Amerika [1,2,3,4,5]",
            "episodes": [
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[1] Birinchi Qasoskor (2011)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[2] Qishki Askar (2014)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[3] Fuqarolik Urushi (2016)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "[4] Jasur Yangi Dunyo (2025)"},
            ]
        },
    ],

    "cartoons": [
        {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Multfilm nomi 1"},
    ],

    "anime": [
        {
            "title": "Anime nomi 1",
            "episodes": [
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "1-qism"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "2-qism"},
            ]
        },
    ],
}

ENG_MEDIA = {
    "movies": [
        {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Movie name 1"},
        {
            "title": "Marvel",
            "episodes": [
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Iron Man (2008)"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Iron Man (2011)"},
            ]
        },
    ],
    "cartoons": [
        {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Cartoon name 1"},
    ],
    "anime": [
        {
            "title": "Anime name 1",
            "episodes": [
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Episode 1"},
                {"chat_id": -1004324672328, "message_thread_id": None, "message_id": None, "title": "Episode 2"},
            ]
        },
    ],
}