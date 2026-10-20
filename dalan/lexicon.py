"""Bilingual tourism lexicon: Cebuano (ceb) and Tagalog (tl) lemmas mapped to English concept tokens.

Each entry: lemma -> (language, [English gloss tokens]). Gloss tokens are chosen to match the vocabulary used
in the knowledge base so that projected queries land on the right entries. Lemmas are base forms; affixed
forms (makapalit, gipalit, bumili) are reduced to these by dalan.normalize.

Extend this list from real user logs. Keep glosses short (1 to 3 tokens) to avoid query drift.
"""

LEXICON = {
    # question words and function words
    "unsa": ("ceb", ["what"]), "unsaon": ("ceb", ["how"]), "giunsa": ("ceb", ["how"]),
    "asa": ("ceb", ["where"]), "diin": ("ceb", ["where"]), "kinsa": ("ceb", ["who"]),
    "pila": ("ceb", ["how", "much", "price"]), "kanusa": ("ceb", ["when"]), "ngano": ("ceb", ["why"]),
    "naa": ("ceb", ["there"]), "wala": ("ceb", ["none"]), "gikan": ("ceb", ["from"]),
    "padulong": ("ceb", ["to", "going"]), "paingon": ("ceb", ["to", "going"]), "diri": ("ceb", ["here"]),
    "didto": ("ceb", ["there"]), "duol": ("ceb", ["near"]), "layo": ("ceb", ["far"]),
    "paano": ("tl", ["how"]), "saan": ("tl", ["where"]), "magkano": ("tl", ["how", "much", "price"]),
    "kailan": ("tl", ["when"]), "ano": ("tl", ["what"]), "mayroon": ("tl", ["there"]), "meron": ("tl", ["there"]),
    "papunta": ("tl", ["to", "going"]), "galing": ("tl", ["from"]), "malapit": ("tl", ["near"]),
    "ilang": ("tl", ["how", "many"]),
    # movement and travel
    "adto": ("ceb", ["go"]), "anha": ("ceb", ["go"]), "biyahe": ("ceb", ["travel", "trip"]),
    "suroy": ("ceb", ["tour", "visit", "trip"]), "lakaw": ("ceb", ["trip", "travel"]),
    "sakay": ("ceb", ["ride", "transport"]), "sakyanan": ("ceb", ["transport", "ride"]),
    "punta": ("tl", ["go"]), "pasyal": ("tl", ["visit", "tour"]), "pasyalan": ("tl", ["destinations", "places", "visit"]),
    "puntahan": ("tl", ["destinations", "places", "visit"]), "sasakyan": ("tl", ["transport", "ride"]),
    "uli": ("ceb", ["return", "home"]), "balik": ("ceb", ["return"]),
    "pamasahe": ("ceb", ["fare", "price"]), "plete": ("ceb", ["fare", "price"]),
    "dyip": ("ceb", ["jeepney"]), "dyipni": ("ceb", ["jeepney"]), "traysikol": ("ceb", ["tricycle", "ride"]),
    "barko": ("ceb", ["ferry", "boat"]), "bangka": ("ceb", ["boat", "island", "hopping"]),
    "lantsa": ("tl", ["ferry", "boat"]), "pantalan": ("ceb", ["port", "ferry"]), "pier": ("ceb", ["port", "ferry"]),
    "eroplano": ("ceb", ["plane", "flight", "airport"]), "erport": ("ceb", ["airport"]),
    "dalan": ("ceb", ["road", "route"]), "daan": ("tl", ["road", "route"]),
    # places and nature
    "syudad": ("ceb", ["city"]), "siyudad": ("ceb", ["city"]), "dakbayan": ("ceb", ["city"]),
    "lungsod": ("ceb", ["town", "city"]), "lugar": ("ceb", ["places", "place"]), "dapit": ("ceb", ["place", "places"]),
    "baybayon": ("ceb", ["beach"]), "dagat": ("ceb", ["sea", "beach", "snorkel"]), "isla": ("ceb", ["island"]),
    "pulo": ("ceb", ["island"]), "bukid": ("ceb", ["mountain", "hike"]), "bundok": ("tl", ["mountain", "hike"]),
    "talon": ("tl", ["falls"]), "busay": ("ceb", ["falls"]), "suba": ("ceb", ["river"]), "langub": ("ceb", ["cave"]),
    "kweba": ("ceb", ["cave"]), "lanaw": ("ceb", ["lake"]), "lawa": ("tl", ["lake"]),
    "amihanan": ("ceb", ["north"]), "habagatan": ("ceb", ["south"]), "hilaga": ("tl", ["north"]), "timog": ("tl", ["south"]),
    "simbahan": ("ceb", ["church"]), "kapilya": ("ceb", ["church"]), "merkado": ("ceb", ["market"]),
    "palengke": ("tl", ["market"]), "tindahan": ("ceb", ["store", "shopping"]), "terminal": ("ceb", ["terminal", "bus"]),
    "ospital": ("ceb", ["hospital"]), "pulis": ("ceb", ["police"]),
    # descriptors
    "taas": ("ceb", ["highest", "high"]), "pinakataas": ("ceb", ["highest"]), "mataas": ("tl", ["highest", "high"]),
    "pinakamataas": ("tl", ["highest"]), "nindot": ("ceb", ["best", "beautiful"]), "tan-aw": ("ceb", ["view", "watch"]), "baylo": ("ceb", ["exchange"]), "maayo": ("ceb", ["good", "best"]),
    "maganda": ("tl", ["best", "beautiful"]), "bantog": ("ceb", ["famous", "known"]), "sikat": ("tl", ["famous", "known"]),
    "ilado": ("ceb", ["famous", "known"]), "kilala": ("tl", ["famous", "known"]),
    "luwas": ("ceb", ["safe", "safety"]), "ligtas": ("tl", ["safe", "safety"]), "delikado": ("ceb", ["safety", "danger"]),
    "mahal": ("ceb", ["expensive", "cost"]), "barato": ("ceb", ["cheap", "budget"]), "mura": ("ceb", ["cheap", "budget"]),
    "lami": ("ceb", ["delicious", "food"]), "masarap": ("tl", ["delicious", "food"]),
    "init": ("ceb", ["hot", "weather"]), "tugnaw": ("ceb", ["cold", "weather"]),
    # time and weather
    "adlaw": ("ceb", ["day", "days"]), "araw": ("tl", ["day", "days"]), "buntag": ("ceb", ["morning"]),
    "gabii": ("ceb", ["night"]), "bulan": ("ceb", ["month"]), "buwan": ("tl", ["month"]),
    "panahon": ("ceb", ["season", "weather", "time"]), "ting": ("ceb", ["season"]),
    "ulan": ("ceb", ["rainy", "rain", "weather"]), "bagyo": ("ceb", ["typhoon", "storm"]),
    "tulo": ("ceb", ["3", "three"]), "tatlo": ("tl", ["3", "three"]), "duha": ("ceb", ["2", "two"]),
    # money and needs
    "kwarta": ("ceb", ["money", "cash"]), "kuwarta": ("ceb", ["money", "cash"]), "pera": ("tl", ["money", "cash"]),
    "bayad": ("ceb", ["fee", "price", "pay"]), "bayaran": ("tl", ["fee", "pay"]), "presyo": ("ceb", ["price", "cost"]),
    "gasto": ("ceb", ["budget", "cost"]), "gastos": ("tl", ["budget", "cost"]), "badyet": ("ceb", ["budget"]),
    "tabang": ("ceb", ["help", "emergency"]), "tulong": ("tl", ["help", "emergency"]), "nawala": ("ceb", ["lost"]),
    "numero": ("ceb", ["number"]), "kinahanglan": ("ceb", ["need"]), "kailangan": ("tl", ["need"]),
    "sinina": ("ceb", ["dress", "clothes"]), "damit": ("tl", ["dress", "clothes"]), "sanina": ("ceb", ["dress", "clothes"]),
    "pinulongan": ("ceb", ["language"]), "sinultihan": ("ceb", ["language"]), "wika": ("tl", ["language"]),
    "sulti": ("ceb", ["speak", "say"]), "istorya": ("ceb", ["speak"]), "salita": ("tl", ["speak", "word"]),
    "linggo": ("ceb", ["week", "sunday"]), "pista": ("ceb", ["festival", "fiesta"]), "kapistahan": ("tl", ["festival", "fiesta"]),
    "plano": ("ceb", ["plan", "itinerary"]), "iskedyul": ("ceb", ["schedule", "itinerary"]),
    # buying and products
    "palit": ("ceb", ["buy"]), "pamalit": ("ceb", ["buy", "shopping"]), "bili": ("tl", ["buy"]),
    "dala": ("ceb", ["bring", "bring home"]), "dad": ("ceb", ["bring"]), "dalhin": ("tl", ["bring"]),
    "regalo": ("ceb", ["gift", "pasalubong"]), "produkto": ("ceb", ["products", "local products"]),
    "lokal": ("ceb", ["local"]), "pagkaon": ("ceb", ["food", "eat"]), "kaon": ("ceb", ["eat", "food"]),
    "pagkain": ("tl", ["food", "eat"]), "kain": ("tl", ["eat", "food"]), "pamahaw": ("ceb", ["breakfast"]),
    "isda": ("ceb", ["fish"]), "buwad": ("ceb", ["dried fish", "danggit"]), "tuyo": ("tl", ["dried fish", "danggit"]),
    "uga": ("ceb", ["dried"]), "pinauga": ("ceb", ["dried"]), "pinatuyo": ("tl", ["dried"]),
    "itlog": ("ceb", ["egg", "eggs"]), "manok": ("ceb", ["chicken", "poultry"]),
    "mangga": ("ceb", ["mango", "mangoes"]), "prutas": ("ceb", ["fruit"]), "bunga": ("ceb", ["fruit"]),
    "utanon": ("ceb", ["vegetables", "vegetable"]), "gulay": ("tl", ["vegetables", "vegetable"]),
    "baboy": ("ceb", ["pork"]), "litson": ("ceb", ["lechon", "roast pig"]), "tsitsaron": ("ceb", ["chicharon"]),
    "mais": ("ceb", ["corn"]), "bugas": ("ceb", ["rice"]), "kan-on": ("ceb", ["rice"]), "kanon": ("ceb", ["rice"]),
    "tsokolate": ("ceb", ["chocolate", "tablea"]), "kakaw": ("ceb", ["cacao", "tablea"]),
    "bulak": ("ceb", ["flower", "flowers"]), "bulaklak": ("tl", ["flower", "flowers"]),
    "habol": ("ceb", ["weaving", "hablon"]), "gitara": ("ceb", ["guitar"]), "lusong": ("ceb", ["dive"]),
    "mag-uuma": ("ceb", ["farm", "farmers"]), "uma": ("ceb", ["farm"]), "umahan": ("ceb", ["farm"]),
    "sakahan": ("tl", ["farm"]), "magsasaka": ("tl", ["farm", "farmers"]),
    "gamay": ("ceb", ["small", "local"]),
    # wildlife and activities
    "iho": ("ceb", ["shark"]), "pating": ("tl", ["shark"]), "tiburon": ("ceb", ["shark"]),
    "pawikan": ("ceb", ["turtle"]), "bao": ("ceb", ["turtle"]), "sardinas": ("ceb", ["sardine", "sardines"]),
    "tamban": ("ceb", ["sardine", "sardines"]), "langoy": ("ceb", ["swim", "snorkel"]), "languy": ("ceb", ["swim"]),
    "lumangoy": ("tl", ["swim"]), "katkat": ("ceb", ["hike", "trek"]), "akyat": ("tl", ["hike", "trek"]),
    "ambak": ("ceb", ["jump", "cliff"]),
    "sugbo": ("ceb", ["cebu"]), "sugbu": ("ceb", ["cebu"]), "pwede": ("tl", []), "puede": ("ceb", []),
    "makaadto": ("ceb", ["go"]), "pwedeng": ("tl", []),
    # greetings
    "maayong": ("ceb", ["hello", "good"]), "kumusta": ("ceb", ["hello"]), "kamusta": ("ceb", ["hello"]),
    "umaga": ("tl", ["morning"]), "gabi": ("tl", ["night"]), "tanawin": ("tl", ["view", "viewpoint"]), "salamat": ("ceb", ["thank"]),
}

# Clitic and contracted forms common in chat Cebuano/Tagalog -> expansion
CONTRACTIONS = {
    "unsay": "unsa ang", "asay": "asa ang", "pilay": "pila ang", "kinsay": "kinsa ang", "naay": "naa ang",
    "asang": "asa ang", "unsang": "unsa ang", "pilang": "pila ang", "diay": "", "man": "", "ba": "",
    "og": "ug", "nga": "", "ang": "", "ug": "", "sa": "", "si": "", "ni": "", "ko": "", "mo": "", "ka": "",
    "ta": "", "kami": "", "mi": "", "nako": "", "akong": "", "imong": "", "ang mga": "", "mga": "",
    "ng": "", "na": "", "po": "", "lang": "", "pa": "", "ba't": "bakit", "pano": "paano", "san": "san",
    "nasaan": "saan", "asan": "asa", "hain": "asa", "aha": "asa", "ngadto": "padulong",
}

PREFIXES = ["makapag", "makapa", "makig", "maka", "magpa", "mag", "nag", "nang", "mang", "man", "pag", "gipa",
            "gi", "ma", "na", "mo", "ni", "ka", "pa", "i", "pinaka"]
SUFFIXES = ["anan", "hanan", "han", "hon", "ng", "an", "on", "in", "a"]
