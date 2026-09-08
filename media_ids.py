# Media kontenti (filmlar, multfilmlar, animelar) shu yopiq guruh/kanalda saqlanadi.
# movies / cartoons: har bir element {chat_id, message_id, title}
# anime: har bir anime {title, episodes: [{chat_id, message_id, title}, ...]}
#
# Yangi ID olish uchun: guruhga xabar tashlang -> o'sha xabarga reply qilib /get_id
# yozing, bot sizga tayyor dict qatorini beradi - shuni pastga qo'shsangiz bo'ladi.

UZB_MEDIA = {
    "movies": [
        {"chat_id": -1003863295329, "message_id": 104, "title": "Film nomi 1"},
        {
            "title": "Temir odam",
            "Temir odam": [
                {"chat_id": -1003863295329, "message_id": 102, "title": "Temir Odam (2008)"},
                {"chat_id": -1003863295329, "message_id": 104, "title": "Temir Odam (2011)"},
            ],
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
                {"chat_id": -1003863295329, "message_id": 2, "title": "3-qism"},
            ],
        },
        {
            "title": "Anime nomi 2",
            "episodes": [
                {"chat_id": -1003863295329, "message_id": 2, "title": "1-qism"},
                {"chat_id": -1003863295329, "message_id": 2, "title": "2-qism"},
            ],
        },
    ],






}

ENG_MEDIA = {
    "movies": [
        {"chat_id": -1003863295329, "message_id": 2, "title": "Movie name 1"},
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
            ],
        },
    ],
}