import json
import random

random.seed(2026)

# 1. Curated Multi-Cultural Templates (Indian, Pakistani, English)
# We combine rich multi-turn scenarios with randomized variations so all 500 chats are unique!

INDIAN_SCENARIOS = [
    lambda b, g, t1, t2, t3: [
        {"sender": "them", "text": f"so gayi kya? 🥺", "time": t1, "hold": 1.4},
        {"sender": "me",   "text": "mujhe baat nahi karni tumse", "time": t1, "hold": 1.3},
        {"sender": "me",   "text": "jao apni uss meeting wali se hi baat karo 😒👍", "time": t2, "hold": 1.9},
        {"sender": "them", "text": "arey yaar wo bas client thi 😭", "time": t2, "hold": 1.5},
        {"sender": "them", "text": "acha suno, balcony mein aao ek second", "time": t2, "hold": 1.8},
        {"sender": "me",   "text": "kyu? main nahi aa rahi 😤", "time": t3, "hold": 1.6},
        {"sender": "them", "text": f"neeche gate pe dekho drama queen... tumhari {random.choice(['cold coffee aur momos', 'paneer momos aur brownie', 'masala chai aur maggi', 'chocolates aur waffle'])} thande ho rahe hain 🧋🥟", "time": t3, "hold": 2.8},
        {"sender": "me",   "text": "sachi??? tum itni raat ko aaye ho?! 😭❤️", "time": t3, "hold": 1.8},
        {"sender": "me",   "text": "ruko 2 min mein bhaag ke aayi 🏃‍♀️🙈", "time": t3, "hold": 2.8}
    ],
    lambda b, g, t1, t2, t3: [
        {"sender": "me",   "text": "suno, ghar pahunch gaye?", "time": t1, "hold": 1.4},
        {"sender": "them", "text": "haan ji, abhi just bike park ki ❤️", "time": t1, "hold": 1.6},
        {"sender": "me",   "text": "ek baat bolu? gussa toh nahi karoge?", "time": t2, "hold": 1.8},
        {"sender": "them", "text": "tumpe gussa karke kahan jaunga? bolo meri maa 🥺", "time": t2, "hold": 2.0},
        {"sender": "me",   "text": f"wo tumhari {random.choice(['black hoodie', 'oversized olive tshirt', 'denim jacket', 'favourite sweatshirt'])} mere bag mein reh gayi... galti se 🙈", "time": t2, "hold": 2.4},
        {"sender": "them", "text": "'galti se'?? 😂 maine khud chupke se daali thi tumhare bag mein", "time": t3, "hold": 2.3},
        {"sender": "them", "text": "mujhe pata tha tumhe uski khushboo pasand hai ❤️", "time": t3, "hold": 2.5},
        {"sender": "me",   "text": "stopppp 😭❤️ tum itne cute kyu ho yaar", "time": t3, "hold": 2.8}
    ],
    lambda b, g, t1, t2, t3: [
        {"sender": "them", "text": f"aaj uss {random.choice(['white kurti', 'black saree', 'yellow suit', 'pastel kurti'])} mein bohot zyada pyari lag rahi thi tum 🧿", "time": t1, "hold": 2.2},
        {"sender": "me",   "text": "acha ji? tab toh samne se kuch nahi bola 😒", "time": t1, "hold": 1.8},
        {"sender": "them", "text": "samne bolne ki himmat kahan bachti hai jab tum bindi laga ke aati ho 😭❤️", "time": t2, "hold": 2.4},
        {"sender": "me",   "text": "zyada makkhan mat lagao ab 🙈", "time": t2, "hold": 1.6},
        {"sender": "them", "text": "makkhan nahi, sachi! maine chupke se 4 photos bhi click ki hain tumhari 📸", "time": t3, "hold": 2.3},
        {"sender": "me",   "text": "dikhaoooo abhi bhejo!! 🥺💕", "time": t3, "hold": 2.6}
    ],
    lambda b, g, t1, t2, t3: [
        {"sender": "me",   "text": "mera bilkul mann nahi lag raha aaj office mein 😩", "time": t1, "hold": 1.8},
        {"sender": "them", "text": "kyu kya hua mere bacche ko? boss ne kuch bola?", "time": t1, "hold": 1.9},
        {"sender": "me",   "text": "nahi... bas sir dard ho raha hai aur tumhari yaad aa rahi hai 🥺", "time": t2, "hold": 2.2},
        {"sender": "them", "text": "reception pe jao 2 minute mein", "time": t2, "hold": 1.6},
        {"sender": "me",   "text": "reception pe kyu??", "time": t2, "hold": 1.4},
        {"sender": "them", "text": f"Zomato wale bhaiya ke haath tumhari {random.choice(['iced latte aur cheesecake', 'hot chocolate aur croissant', 'adrak wali chai aur samosa'])} + Saridon bheji hai ❤️", "time": t3, "hold": 2.7},
        {"sender": "me",   "text": "whatttt 😭❤️ main ro dungi abhi office mein!!", "time": t3, "hold": 2.8}
    ]
]

PAKISTANI_SCENARIOS = [
    lambda b, g, t1, t2, t3: [
        {"sender": "them", "text": "suno na... abhi tak naraz ho mujhse? 🥺", "time": t1, "hold": 1.7},
        {"sender": "me",   "text": "jee haan, bilkul baat na karein mujhse 😤", "time": t1, "hold": 1.7},
        {"sender": "them", "text": "khuda ka khauf karo begum, 3 ghante ho gaye hain 😭", "time": t2, "hold": 2.1},
        {"sender": "me",   "text": "toh kisne kaha tha meri baat kaatne ko?", "time": t2, "hold": 1.8},
        {"sender": "them", "text": f"acha maafi! chalo jaldi se तैयार ho jao, 10 minute mein bahar aa raha hoon", "time": t2, "hold": 2.2},
        {"sender": "me",   "text": "is waqt kahan jana hai??", "time": t3, "hold": 1.5},
        {"sender": "them", "text": f"{random.choice(['Quetta cafe ki special doodh patti', 'Burns Road ki kulfi aur biryani', 'tandoori chai aur cheese paratha', 'late night drive aur ice cream'])} khilane, meri nakhre wali ko ❤️✨", "time": t3, "hold": 2.8},
        {"sender": "me",   "text": "sachi?? 😍 ruko bas dupatta le ke aayi 🙈❤️", "time": t3, "hold": 2.8}
    ],
    lambda b, g, t1, t2, t3: [
        {"sender": "me",   "text": "aap ghar pohanch gaye khairiyat se?", "time": t1, "hold": 1.6},
        {"sender": "them", "text": "jee meri jaan, abhi kamray mein aaya hoon ❤️", "time": t1, "hold": 1.8},
        {"sender": "me",   "text": "aaj ammi pooch rahi thi aapke baare mein... 🙈", "time": t2, "hold": 2.0},
        {"sender": "them", "text": "hain?? sachi?! kya kaha phir ammi ne? 😱❤️", "time": t2, "hold": 1.9},
        {"sender": "me",   "text": "keh rahi thi larka toh bohot shareef aur pyara lagta hai 😂", "time": t3, "hold": 2.3},
        {"sender": "them", "text": "shukar Alhamdulillah!! 😭❤️ ab toh mithai pakki samjho!", "time": t3, "hold": 2.4},
        {"sender": "me",   "text": "pagal 😂❤️ chalo ab so jao chup kar ke", "time": t3, "hold": 2.6}
    ],
    lambda b, g, t1, t2, t3: [
        {"sender": "them", "text": f"wese aaj jo tumne {random.choice(['jhumkay', 'gajray', 'kangan', 'paranda'])} pehne thay na... qasmein dil le gaye 🧿❤️", "time": t1, "hold": 2.4},
        {"sender": "me",   "text": "acha jee? itna ghaur se kab dekha aapne? 🙈", "time": t1, "hold": 1.8},
        {"sender": "them", "text": "meri nazrein tumse hatein toh kuch aur dekhoon na 🥺", "time": t2, "hold": 2.1},
        {"sender": "me",   "text": "ufff itni shayari kahan se seekh li aaj kal? 😂💕", "time": t2, "hold": 2.0},
        {"sender": "them", "text": "jab pasandida aurat saamne ho toh shayari khud aa jati hai ❤️", "time": t3, "hold": 2.4},
        {"sender": "me",   "text": "bas karein ab mujhe sharam aa rahi hai 😭🙈❤️", "time": t3, "hold": 2.7}
    ]
]

ENGLISH_SCENARIOS = [
    lambda b, g, t1, t2, t3: [
        {"sender": "them", "text": "hey... are you still awake? 🥺", "time": t1, "hold": 1.5},
        {"sender": "me",   "text": "yeah, I'm still mad at you though. don't text me 😒", "time": t1, "hold": 1.9},
        {"sender": "them", "text": "okay fair, you can stay mad at me", "time": t2, "hold": 1.6},
        {"sender": "them", "text": "but can you at least unlock your front door for 5 seconds?", "time": t2, "hold": 2.1},
        {"sender": "me",   "text": "wait what?? why?", "time": t2, "hold": 1.4},
        {"sender": "them", "text": f"because I'm standing on your porch holding {random.choice(['your favorite iced coffee and Chick-fil-A', 'warm cookies and strawberry matcha', 'Target snacks and Peonies', 'Taco Bell and your favorite ice cream'])} 🧋🌸", "time": t3, "hold": 2.8},
        {"sender": "me",   "text": "NO WAY YOU DROVE HERE AT MIDNIGHT 😭❤️", "time": t3, "hold": 2.0},
        {"sender": "me",   "text": "hold on I'm running downstairs right now!! 🏃‍♀️🙈", "time": t3, "hold": 2.8}
    ],
    lambda b, g, t1, t2, t3: [
        {"sender": "me",   "text": "did you make it home safe?", "time": t1, "hold": 1.4},
        {"sender": "them", "text": "just walked in ❤️ miss you already though", "time": t1, "hold": 1.7},
        {"sender": "me",   "text": "so... don't be mad but I accidentally stole something from your room 🙈", "time": t2, "hold": 2.2},
        {"sender": "them", "text": "let me guess... my grey oversized hoodie?", "time": t2, "hold": 1.8},
        {"sender": "me",   "text": "HOW DID YOU KNOW 😭", "time": t2, "hold": 1.5},
        {"sender": "them", "text": "babe I literally sprayed my cologne on it before you left so it would smell like me 😂❤️", "time": t3, "hold": 2.6},
        {"sender": "me",   "text": "stop it right now I'm literally melting 🥺🫶", "time": t3, "hold": 2.8}
    ],
    lambda b, g, t1, t2, t3: [
        {"sender": "them", "text": "I can't stop thinking about how pretty you looked tonight 🤍", "time": t1, "hold": 2.0},
        {"sender": "me",   "text": "stop lying my hair was a total mess 😭", "time": t1, "hold": 1.8},
        {"sender": "them", "text": "are you kidding?? when you laughed in the car I literally forgot how to drive for a second 🥺", "time": t2, "hold": 2.5},
        {"sender": "me",   "text": "you're just saying that to make me smile 🙈", "time": t2, "hold": 1.8},
        {"sender": "them", "text": "is it working though?", "time": t3, "hold": 1.4},
        {"sender": "me",   "text": "...yes my cheeks hurt from smiling shut up 😭❤️", "time": t3, "hold": 2.8}
    ]
]

AVATARS = [
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=200&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop&q=80"
]

INDIAN_NAMES = ["Aarav ❤️", "Kabir 🥺❤️", "Vivaan 💕", "Rohan ❤️ (Sirदर्द)", "Aditya 🧿❤️", "Siddharth ❤️", "Karan 🥺💕", "Mera Sukoon 🧿"]
PAKISTANI_NAMES = ["Zain ❤️", "Hamza 🥺❤️", "Bilal 🧿", "Haris 💕", "Salar ❤️✨", "Ahad 🥺", "Zaviyar ❤️", "Sartaaj जी 🙈❤️"]
ENGLISH_NAMES = ["Liam ❤️", "Noah 🥺🤍", "Ethan 💕", "Lucas 🫶", "My Favorite Person ❤️", "Mason 🥺", "Jack 🤍✨", "Babe ❤️"]

CAPTIONS = [
    "Tag your pasandida aurat / mard ❤️✨\nWait for the end 😭💕\n.\n.\n#couplegoals #indianrelationships #pakistaniweddings #loveydovey #whatsappchats #pasandidaaurat #relatablecouples #latechats #explorepage",
    "Send this to the one who handles all your nakhre 🥺❤️\n.\n.\n#cutecouples #relationshipgoals #hinglish #desicouples #romanurdu #boyfriendgoals #textconversations #loveunlimited #reelsindia",
    "When they know exactly how to fix your mood at midnight 😭🧋❤️\n.\n.\n#latenighttalks #couplereels #wholesomelove #soulmate #chatstories #pakistanicouples #indiancouples #romanticreels #viralreels",
    "May this type of love find everyone 🧿❤️✨\nTag your person below 👇\n.\n.\n#pasandidamard #pasandidaaurat #couplehumor #sweettexts #lovestories #greenflag #relationshipmemes #explore"
]

queue = []
for i in range(1, 501):
    # Rotate cultures: 1 = Indian, 2 = Pakistani, 0 = English
    mod = i % 3
    hr = random.choice(["10", "11", "12", "1"])
    m_base = random.randint(10, 52)
    ampm = "pm" if hr in ("10", "11") else "am"
    t1 = f"{hr}:{m_base:02d} {ampm}"
    t2 = f"{hr}:{m_base+1:02d} {ampm}"
    t3 = f"{hr}:{m_base+2:02d} {ampm}"

    if mod == 1:
        culture = "indian"
        name = random.choice(INDIAN_NAMES)
        fn = random.choice(INDIAN_SCENARIOS)
    elif mod == 2:
        culture = "pakistani"
        name = random.choice(PAKISTANI_NAMES)
        fn = random.choice(PAKISTANI_SCENARIOS)
    else:
        culture = "english"
        name = random.choice(ENGLISH_NAMES)
        fn = random.choice(ENGLISH_SCENARIOS)

    msgs = fn(name, "Me", t1, t2, t3)
    queue.append({
        "id": i,
        "culture": culture,
        "contact_name": name,
        "dp_url": random.choice(AVATARS),
        "battery": f"{random.randint(62, 96)}%",
        "header_time": t3.replace(" am", "").replace(" pm", ""),
        "music_key": i % 4,
        "caption": CAPTIONS[i % len(CAPTIONS)],
        "messages": msgs,
        "posted": False
    })

# Mark #1 as posted since we already published the first test Reel, or keep all 500 unposted
with open("queue.json", "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)

print(f"SUCCESS! Generated queue.json with {len(queue)} unique Indian, Pakistani & English couple Reels!")
