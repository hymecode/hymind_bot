# Media kontenti (filmlar, multfilmlar, animelar) shu yopiq guruh/kanalda saqlanadi.
# movies / cartoons: har bir element {chat_id, message_id, title}
# anime: har bir anime {title, episodes: [{chat_id, message_id, title}, ...]}
#
# Yangi ID olish uchun: guruhga xabar tashlang -> o'sha xabarga reply qilib /get_id
# yozing, bot sizga tayyor dict qatorini beradi - shuni pastga qo'shsangiz bo'ladi.

UZB_MEDIA = {
    "movies": [
        # Oddiy film (qismsiz)
        {"chat_id": -1003863295329, "message_id": 1, "title": "bosma! film yoq baribir"},
        
        # Qismlari bo'lgan film (Marvel guruhi)
        {
            "title": "Temir Odam [1,2,3]",
            "episodes": [
                {"chat_id": -1003863295329, "message_id": 102, "title": "[1] Temir Odam 1 (2008)"},
                {"chat_id": -1003863295329, "message_id": 104, "title": "[2] Temir Odam 2 (2010)"},
                {"chat_id": -1003863295329, "message_id": 106, "title": "[3] Temir Odam 3 (2013)"},
            ]
        },
        
        # Yana yangi film qo'shish uchun shu yerda davom eting (masalan Spiderman)
        {
            "title": "O'rgimchak odam [1,2,3,4]",
            "episodes": [
                {"chat_id": -1003863295329, "message_id": 108, "title": "[1] Uyga qaytish (2017)"},
                {"chat_id": -1003863295329, "message_id": 110, "title": "[2] Uydan uzoqda (2019)"},
                {"chat_id": -1003863295329, "message_id": 112, "title": "[3] Uyga yo'l yo'q (2021)"},
                {"chat_id": -1003863295329, "message_id": 114, "title": "[4] Yangi kun (2026)"},
            ]
        },
        {
            "title": "Men Grutman [1,2,3,4,5]",
            "episodes": [
                {"chat_id": -1003863295329, "message_id": 116, "title": "Men Grutman 1"},
                {"chat_id": -1003863295329, "message_id": 118, "title": "Men Grutman 2"},
                {"chat_id": -1003863295329, "message_id": 120, "title": "Men Grutman 3"},
                {"chat_id": -1003863295329, "message_id": 122, "title": "Men Grutman 4"},
                {"chat_id": -1003863295329, "message_id": 124, "title": "Men Grutman 5"},
            ]
        },
        {
            "title": "Kapitan Amerika [1,2,3,4,5]",
            "episodes": [
                {"chat_id": -1003863295329, "message_id": 116, "title": "[1] Birinchi Qasoskor (2011)"},
                {"chat_id": -1003863295329, "message_id": 118, "title": "[2] Qishki Askar (2014)"},
                {"chat_id": -1003863295329, "message_id": 120, "title": "[3] Fuqarolik Urushi (2016)"},
                {"chat_id": -1003863295329, "message_id": 122, "title": "[4] Jasur Yangi Dunyo (2025)"},
            ]
        },
    ],

    "cartoons": [
        {"chat_id": -1003863295329, "message_id": 2, "title": "Multfilm nomi 1"},
    ],

    "anime": [
        {
            "title": "Anime nomi 1",
            "episodes": [
                {"chat_id": -1003863295329, "message_id": 2, "title": "1-qism"},
                {"chat_id": -1003863295329, "message_id": 2, "title": "2-qism"},
            ]
        },
    ],
}








ENG_MEDIA = {
    "movies": [
        {"chat_id": -1003863295329, "message_id": 2, "title": "Movie name 1"},
        {
            "title": "Marvel",
            "episodes": [
                {"chat_id": -1003863295329, "message_id": 102, "title": "Iron Man (2008)"},
                {"chat_id": -1003863295329, "message_id": 104, "title": "Iron Man (2011)"},
            ]
        },
    ],
    "cartoons": [
        {"chat_id": -1003863295329, "message_id": 2, "title": "Cartoon name 1"},
    ],
    "anime": [
        {
            "title": "Anime name 1",
            "episodes": [
                {"chat_id": -1003863295329, "message_id": 2, "title": "Episode 1"},
                {"chat_id": -1003863295329, "message_id": 2, "title": "Episode 2"},
            ]
        },
    ],
}