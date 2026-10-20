"""Builds kb.json, the single knowledge base shared by the web prototype and the local-LLM backend.

Edit the entries here, run `python build_kb.py`, and both front end and backend pick up the change.
Prices and schedules are approximate (2025-2026) and flagged for verification.
"""
import json

VERIFIED = "2026-10"

E = []  # Q&A entries


def add(id, region, cat, title, keywords, questions, answer):
    E.append(dict(id=id, region=region, category=cat, title=title,
                  keywords=keywords, questions=questions, answer=answer.strip()))


# ---------------------------------------------------------------- GENERAL
add("greet", "general", "Basics", "Greeting",
    ["hello", "hi", "hey", "maayong", "kumusta", "good morning", "good day", "start"],
    ["Hi", "Maayong buntag", "Hello, who are you?"],
    """
Maayong adlaw! I'm Sugbo Guide, your Cebu travel helper.
Ask me about North Cebu (Bantayan, Malapascua, Camotes), South Cebu (Oslob, Moalboal, Kawasan, Osmeña Peak, Simala), the city, getting around, or local products and pasalubong.
""")

add("best-time", "general", "Basics", "Best time to visit",
    ["best", "time", "season", "month", "weather", "rainy", "dry", "summer", "when"],
    ["When is the best time to visit Cebu?", "What is the weather like?"],
    """
Dry season, roughly December to May, is the easiest time to visit. March to May is hottest and best for beaches and island hopping.
June to November is the rainy and typhoon season. Trips still run, but ferries and boat tours get cancelled when a storm signal is raised.
Expect big crowds and higher prices during Sinulog (January), Holy Week, and Christmas.
""")

add("typhoon", "general", "Safety", "Typhoons and cancelled ferries",
    ["typhoon", "storm", "signal", "bagyo", "cancelled", "cancel", "ferry", "suspended", "pagasa", "coast guard"],
    ["Are ferries cancelled during a typhoon?", "What if there is a storm signal?"],
    """
When PAGASA raises a Tropical Cyclone Wind Signal, the Philippine Coast Guard usually suspends sea trips for small boats and sometimes ferries.
Check PAGASA and the Coast Guard (PCG Central Visayas) pages before leaving for Bantayan, Malapascua, Camotes, or Sumilon.
Keep a buffer day before your flight if your itinerary includes an island.
""")

add("airport", "metro", "Getting around", "Airport to the city",
    ["airport", "mactan", "mcia", "arrival", "city", "taxi", "grab", "mybus", "transfer"],
    ["How do I get from the airport to Cebu City?", "Is there a bus from Mactan airport?"],
    """
Mactan-Cebu International Airport (MCIA) is on Mactan Island, Lapu-Lapu City.
Options to the city:
- MyBus airport route to SM City Cebu and other stops. Cheapest, about PHP 50 to 100 (verify current fare).
- Yellow airport taxi or white metered taxi. Ask the driver to use the meter.
- Grab car. Pick up at the designated Grab area.
Travel time to Cebu City is 30 minutes to over an hour depending on traffic. Use the CCLEX bridge route for the south part of the city.
""")

add("getting-around", "metro", "Getting around", "Getting around Metro Cebu",
    ["jeepney", "jeep", "transport", "commute", "taxi", "grab", "habal", "angkas", "move it", "mybus", "around", "ride"],
    ["How do I get around Cebu City?", "How do jeepneys work?"],
    """
- Jeepneys: cheapest. Route codes (like 01K, 04L, 13C) are on the side and front. Base fare is around PHP 13 to 15. Pass the fare forward and say "Lugar lang" to get off.
- Taxi: metered. Make sure the meter is on.
- Grab: car rides through the Grab app. Motorcycle taxis like Angkas and Move It also operate.
- MyBus: air-conditioned buses linking the airport, SM City, SM Seaside, and Il Corso.
Traffic is heavy from 7 to 9 am and 5 to 8 pm, so plan around it.
""")

add("bus-terminals", "general", "Getting around", "North and South bus terminals",
    ["bus", "terminal", "ceres", "north", "south", "province", "provincial"],
    ["Where do I take a bus to the province?", "Which bus terminal for Oslob?"],
    """
- Cebu South Bus Terminal (N. Bacalso Ave., Cebu City): buses to Carcar, Simala/Sibonga, Argao, Dalaguete, Oslob, Moalboal, Badian, Santander.
- Cebu North Bus Terminal (near SM City Cebu, Mandaue side): buses to Danao, Bogo, Hagnaya (for Bantayan), Maya (for Malapascua).
Ceres is the main operator. Air-conditioned buses cost a bit more but are worth it for long trips. Last trips usually leave in the late afternoon, so check before planning a return.
""")

add("money", "general", "Basics", "Money, ATMs, and cash",
    ["money", "atm", "cash", "card", "peso", "exchange", "gcash", "pay", "credit"],
    ["Can I use my card?", "Are there ATMs in Bantayan?", "Where can I exchange money?"],
    """
The currency is the Philippine peso (PHP).
Cards and GCash work in malls, hotels, and big restaurants in the city. In provincial towns, islands, markets, and on boats, bring cash.
ATMs exist in Bantayan (Santa Fe and Bantayan town), Moalboal, and Oslob town proper, but they run out of cash on weekends and holidays. Withdraw in the city first.
Money changers in SM, Ayala, and Robinsons malls usually give better rates than the airport.
""")

add("sim", "general", "Basics", "SIM cards and internet",
    ["sim", "internet", "data", "wifi", "globe", "smart", "dito", "signal", "load", "esim"],
    ["Where can I buy a SIM card?", "Is there mobile data in the islands?"],
    """
Buy a Globe, Smart, or DITO SIM at the airport or any mall. Bring your passport because SIM registration is required. Some carriers also sell eSIMs.
Signal is good in the city and town centers but weak on some beaches, mountain trails, and small islands. Download offline maps before you go.
""")

add("safety", "general", "Safety", "Safety and emergency numbers",
    ["safe", "safety", "emergency", "police", "hospital", "911", "help", "lost", "scam", "doctor"],
    ["Is Cebu safe?", "What is the emergency number?", "Where is the nearest hospital?"],
    """
Cebu is generally friendly and safe for tourists. Use normal city precautions: watch your phone and bag in crowded places like Colon and Carbon Market, and use metered taxis or Grab at night.
Emergency hotline: 911 (nationwide).
Major hospitals in the city include Chong Hua, Cebu Doctors' University Hospital, Perpetual Succour, and Vicente Sotto Memorial Medical Center.
If you lose something on a ride, Grab trips can be traced in the app.
""")

add("dress-code", "general", "Culture", "Church dress code and etiquette",
    ["dress", "code", "church", "shorts", "sleeveless", "etiquette", "respect", "culture", "shrine"],
    ["Is there a dress code for churches?", "Can I wear shorts in Simala?"],
    """
Churches and shrines, especially Simala Shrine and the Basilica del Santo Niño, expect modest clothing: no shorts, sleeveless tops, or short skirts. Simala lends wraps at the entrance if needed.
Keep quiet during Mass and ask before photographing people praying.
Filipinos value politeness. A smile and "Salamat" (thank you) go a long way.
""")

add("phrases", "general", "Culture", "Useful Cebuano phrases",
    ["cebuano", "bisaya", "language", "phrase", "speak", "translate", "say", "word", "english"],
    ["What language do they speak in Cebu?", "Teach me some Bisaya phrases"],
    """
People speak Cebuano (Bisaya). English is widely understood.
- Maayong buntag / hapon / gabii: Good morning / afternoon / evening
- Salamat: Thank you
- Pila ni?: How much is this?
- Asa ang ...?: Where is ...?
- Lugar lang: Please stop here (jeepney)
- Palihug: Please
- Lami!: Delicious!
- Wala ko kasabot: I don't understand
""")

add("sinulog", "metro", "Events", "Sinulog Festival",
    ["sinulog", "festival", "january", "santo nino", "parade", "fiesta", "event"],
    ["When is Sinulog?", "What is the Sinulog Festival?"],
    """
Sinulog is Cebu City's biggest festival, honoring the Santo Niño. The grand parade is held on the third Sunday of January, with novena Masses and events through the weeks before.
Book hotels months ahead, expect road closures, and keep valuables close in the crowds.
Other big fiestas: Kadaugan sa Mactan (April, Lapu-Lapu City) and many town fiestas through the year.
""")

add("itinerary-3d", "general", "Planning", "Sample 3-day itinerary",
    ["itinerary", "plan", "days", "3", "three", "schedule", "trip", "first", "time", "suggest", "recommend"],
    ["What is a good 3-day itinerary?", "I have 3 days in Cebu, where should I go?"],
    """
A popular 3-day plan:
- Day 1, City: Magellan's Cross, Basilica del Santo Niño, Fort San Pedro, Taoist Temple, Temple of Leah, sunset at Tops.
- Day 2, South loop: leave around 4 am for Oslob, then Tumalog Falls, then Kawasan Falls or canyoneering in Badian. Stay in Moalboal.
- Day 3, Moalboal: sardine run and turtles at Panagsama Beach, Pescador Island hopping, then back to the city.
If you prefer white sand and a slower pace, swap Days 2 and 3 for Bantayan Island in the north.
""")

add("budget", "general", "Planning", "Daily budget",
    ["budget", "cost", "expensive", "cheap", "how much", "money", "daily", "backpacker"],
    ["How much should I budget per day?", "Is Cebu expensive?"],
    """
Rough daily budgets per person (2026, verify locally):
- Backpacker: PHP 1,500 to 2,500 (hostel, buses, local food)
- Mid-range: PHP 3,500 to 6,000 (hotel, some private transport, tours)
- Comfort: PHP 8,000 and up (resorts, private van)
Add tour fees separately, like whale shark watching, canyoneering, and island hopping.
""")

add("food", "general", "Food", "What to eat in Cebu",
    ["eat", "food", "dish", "try", "restaurant", "local", "delicacy", "lami"],
    ["What food should I try in Cebu?", "What is Cebu famous for food?"],
    """
Must-try Cebuano food:
- Lechon: Cebu roast pig, flavored inside so it needs no sauce.
- Puso: rice cooked in woven coconut leaves.
- Sutukil: choose fresh seafood, then have it grilled (sugba), in soup (tuwa), or raw in vinegar (kilaw).
- Ngohiong: Cebuano spring roll.
- Siomai sa Tisa and tuslob buwa (Pasil) for street food.
- Sikwate (thick hot chocolate) with puto maya for breakfast.
Ask me about pasalubong to bring home, too.
""")

add("fallback", "general", "Basics", "Fallback", [], [], """
I'm not sure about that one yet. Try asking about a place (Oslob, Bantayan, Moalboal), a topic (ferries, budget, safety), or local products (dried mangoes, danggit, chicharon).
""")

# ---------------------------------------------------------------- METRO
add("city-heritage", "metro", "Attractions", "Cebu City heritage sites",
    ["magellan", "cross", "basilica", "santo nino", "fort san pedro", "heritage", "history", "colon", "museum", "city", "downtown", "parian", "casa gorordo", "yap"],
    ["What can I see in Cebu City?", "Where is Magellan's Cross?", "Historical places in Cebu City"],
    """
The heritage area downtown is walkable in half a day:
- Magellan's Cross and the Basilica Minore del Santo Niño, the oldest Catholic church in the country.
- Fort San Pedro, a Spanish-era fort by the port.
- Colon Street, the oldest street in the Philippines.
- Parian District: Yap-San Diego Ancestral House, Casa Gorordo Museum, Heritage of Cebu Monument.
Go in the morning to beat the heat, and dress modestly for the Basilica.
""")

add("city-uplands", "metro", "Attractions", "Busay uplands: Temple of Leah, Tops, Sirao",
    ["temple of leah", "tops", "sirao", "flower", "garden", "busay", "view", "sunset", "taoist", "mountain", "lahug"],
    ["What is the Temple of Leah?", "Where can I see the city view?", "Sirao flower garden"],
    """
The Busay and Sirao highlands are 30 to 45 minutes from Lahug:
- Temple of Leah: a Roman-style temple built as a love monument, with a good view.
- Sirao Flower Garden: celosia flower farm, sometimes called the Little Amsterdam of Cebu.
- Tops Lookout: best city view at sunset.
- Taoist Temple in Beverly Hills, Lahug.
Hire a taxi, Grab, or habal-habal for a half-day loop since jeepneys don't cover all stops.
""")

add("mactan", "metro", "Attractions", "Mactan Island beaches and Lapu-Lapu Shrine",
    ["mactan", "lapu-lapu", "lapu lapu", "shrine", "beach", "resort", "island hopping", "nalusuan", "hilutungan", "olango"],
    ["What can I do in Mactan?", "Island hopping near the city", "Where is the Lapu-Lapu shrine?"],
    """
- Mactan Shrine (Liberty Shrine): the Lapu-Lapu monument marking the 1521 battle.
- Beach resorts along Maribago and Punta Engaño. Many offer day passes.
- Island hopping to Nalusuan, Hilutungan, and Pandanon for snorkeling. Boats leave from Mactan, about half a day.
- Olango Island Wildlife Sanctuary for migratory birds (best around September to March).
- Guitar workshops in Abuno and Maribago, where Mactan's handmade guitars are made.
""")

# ---------------------------------------------------------------- NORTH
add("north-overview", "north", "Overview", "North Cebu overview",
    ["north", "northern", "amihanan", "overview", "where", "places", "visit", "destinations"],
    ["What are the places to visit in North Cebu?", "What's in northern Cebu?"],
    """
North Cebu is quieter, with white-sand islands and fresh seafood:
- Bantayan Island: powdery beaches, Kota Beach, Virgin Island, dried fish and eggs.
- Malapascua Island: thresher shark diving at dawn.
- Camotes Islands: Lake Danao, caves, and calm coves.
- Along the way: Danao, Sogod, Bogo City, San Remigio, and Medellin.
Buses leave from the Cebu North Bus Terminal. Plan at least two days for any island.
""")

add("bantayan", "north", "Islands", "Bantayan Island",
    ["bantayan", "santa fe", "sta fe", "hagnaya", "kota", "virgin island", "ogtong", "madridejos", "white sand"],
    ["How do I get to Bantayan Island?", "What to do in Bantayan?", "Is Bantayan worth it?"],
    """
Getting there: bus from Cebu North Bus Terminal to Hagnaya Port, San Remigio (about 3 to 4 hours), then ferry to Santa Fe (about 1 hour). Several ferry trips run daily until late afternoon.
What to do:
- Swim at Kota Beach, Sugar Beach, and Paradise Beach.
- Ogtong Cave pool in Santa Fe.
- Island hop to Virgin Island and Hilantagaan.
- Rent a motorbike and loop to Bantayan town and Madridejos (old church, Kota Park).
Buy dried fish and eggs before you leave. Holy Week is very crowded, so book early.
""")

add("malapascua", "north", "Islands", "Malapascua Island",
    ["malapascua", "thresher", "shark", "monad", "shoal", "maya", "daanbantayan", "dive", "diving", "kalanggaman"],
    ["How do I get to Malapascua?", "Can I see thresher sharks?", "Diving in Malapascua"],
    """
Getting there: bus from Cebu North Bus Terminal to Maya Port, Daanbantayan (about 4 to 5 hours), then a boat to Malapascua (about 30 to 45 minutes).
Highlights:
- Thresher shark dives at Monad Shoal, at dawn. You need Open Water certification, and Advanced is recommended for the depth.
- Bounty Beach and Langob Beach for swimming.
- Day trip to Kalanggaman Island (Leyte side) with its long sandbar.
Bring cash and arrive at Maya port before mid-afternoon.
""")

add("camotes", "north", "Islands", "Camotes Islands",
    ["camotes", "danao", "lake danao", "consuelo", "timubo", "cave", "santiago", "mangodlong", "pacijan", "poro", "busay falls"],
    ["How do I go to Camotes?", "What to see in Camotes Islands?"],
    """
Getting there: bus or van to Danao City Port (about 1 to 1.5 hours from the city), then ferry to Consuelo, Camotes (about 2 hours).
Highlights:
- Lake Danao, the guitar-shaped lake, with bamboo rafts.
- Timubo Cave and Bukilat Cave.
- Santiago Bay and Mangodlong beaches.
- Busay Falls.
Rent a motorbike or habal-habal with a driver for a day tour.
""")

add("north-towns", "north", "Attractions", "Towns along the north road",
    ["sogod", "bogo", "medellin", "san remigio", "danao", "carmen", "catmon", "tabuelan", "liloan", "compostela", "road trip"],
    ["What stops are there on the way north?", "Road trip North Cebu"],
    """
Good stops on a North Cebu road trip:
- Liloan: Liloan lighthouse and Titay's rosquillos.
- Danao City: port to Camotes, and a lively public market.
- Carmen and Catmon: mountain views and roadside fruit stands.
- Sogod and Borbon: quiet beach resorts.
- Bogo City: the main hub of the far north.
- San Remigio: resorts and Hagnaya Port to Bantayan.
Roadside stalls sell fresh fruit, puto, and budbud. Stopping to buy helps small farmers directly.
""")

# ---------------------------------------------------------------- SOUTH
add("south-overview", "south", "Overview", "South Cebu overview",
    ["south", "southern", "habagatan", "overview", "where", "places", "visit", "destinations"],
    ["What are the places to visit in South Cebu?", "What's in southern Cebu?"],
    """
South Cebu packs the classic adventures:
- Oslob: whale sharks, Tumalog Falls, Sumilon Island.
- Badian: Kawasan Falls and canyoneering.
- Moalboal: sardine run, turtles, Pescador Island.
- Dalaguete and Badian: Osmeña Peak, the highest point in Cebu.
- Sibonga: Simala Shrine.
- Carcar, Argao, and Boljoon: heritage churches and food.
Buses leave from the Cebu South Bus Terminal. A loop takes 2 to 3 days.
""")

add("oslob", "south", "Attractions", "Oslob whale sharks",
    ["oslob", "whale", "shark", "butanding", "tan-awan", "tanawan", "snorkel"],
    ["How do I see the whale sharks in Oslob?", "How much is Oslob whale shark watching?", "Is Oslob ethical?"],
    """
Getting there: bus from Cebu South Bus Terminal to Tan-awan, Oslob (about 3 to 4 hours). Leave by 4 or 5 am since viewing ends around noon.
Fees: roughly PHP 500 for locals and PHP 1,000 for foreigners for snorkeling (verify current rates).
Rules: keep your distance, no touching, no sunscreen in the water, no flash.
Note: the sharks are hand-fed, which marine biologists criticize because it changes their behavior. If you prefer wild encounters, consider Malapascua (thresher sharks) or Moalboal (turtles and sardines) instead.
Combine with Tumalog Falls and Sumilon Island the same day.
""")

add("tumalog-sumilon", "south", "Attractions", "Tumalog Falls and Sumilon Island",
    ["tumalog", "falls", "sumilon", "sandbar", "oslob", "bluewater"],
    ["Where is Tumalog Falls?", "How to go to Sumilon Island?"],
    """
- Tumalog Falls: a curtain-like waterfall about 10 minutes from the whale shark area. Take a habal-habal down the steep road.
- Sumilon Island: a marine sanctuary with a shifting sandbar, reached by boat from Bancogon, Oslob. Day trips are possible.
Both pair well with the morning whale shark visit.
""")

add("kawasan", "south", "Attractions", "Kawasan Falls and canyoneering",
    ["kawasan", "canyoneering", "badian", "alegria", "falls", "jump", "cliff", "matutinao", "adventure"],
    ["How do I go to Kawasan Falls?", "How much is canyoneering?", "Is canyoneering safe?"],
    """
Kawasan Falls is in Matutinao, Badian, about 3 hours by bus from the South Bus Terminal.
Canyoneering usually starts in Alegria or upstream Badian and ends at Kawasan. It takes 3 to 5 hours of river trekking, swimming, and jumps (all jumps are optional).
Packages run roughly PHP 1,500 to 3,500 per person with guide, helmet, life vest, and transport (verify).
Bring aqua shoes, a waterproof phone pouch, and go with an accredited guide. Avoid it after heavy rain.
""")

add("moalboal", "south", "Attractions", "Moalboal sardine run and Pescador",
    ["moalboal", "sardine", "sardines", "run", "turtle", "pescador", "panagsama", "white beach", "dive", "snorkel"],
    ["What to do in Moalboal?", "Where can I see the sardine run?", "How to go to Moalboal?"],
    """
Getting there: bus from Cebu South Bus Terminal via Barili (about 3 hours).
Highlights:
- Sardine run: millions of sardines right off Panagsama Beach, reachable by snorkeling from shore.
- Sea turtles along the reef wall.
- Pescador Island: island hopping and diving.
- White Beach (Basdaku) for swimming.
Moalboal is a good base for Kawasan and has many dive shops and budget stays.
""")

add("osmena-peak", "south", "Attractions", "Osmeña Peak",
    ["osmena", "osmeña", "peak", "hike", "highest", "mountain", "dalaguete", "trek", "sunrise"],
    ["How do I go to Osmeña Peak?", "What is the highest mountain in Cebu?"],
    """
Osmeña Peak (about 1,000 meters) is the highest point in Cebu, in Mantalongon, Dalaguete.
Take a bus to Dalaguete, then a habal-habal up to the jump-off. The hike to the summit is only about 20 to 30 minutes.
Go for sunrise for the best view of the jagged hills. It gets cool up there, so bring a light jacket.
You can trek across to Kawasan Falls in Badian (about 3 to 4 hours downhill) with a guide.
""")

add("simala", "south", "Attractions", "Simala Shrine",
    ["simala", "shrine", "castle", "church", "sibonga", "lindogon", "monastery", "pilgrimage", "miracle"],
    ["How to go to Simala Shrine?", "What is Simala?"],
    """
The Monastery of the Holy Eucharist (Simala Shrine) in Lindogon, Sibonga is a castle-like church known for devotees' prayers and testimonies.
Getting there: bus from Cebu South Bus Terminal to the Simala junction in Sibonga, then a habal-habal or tricycle up (about 1.5 to 2 hours total).
Strict dress code: no shorts or sleeveless tops. Weekends are crowded.
""")

add("south-heritage", "south", "Attractions", "Carcar, Argao, and Boljoon heritage",
    ["carcar", "argao", "boljoon", "heritage", "church", "old", "spanish", "ancestral", "rotunda", "dalaguete", "alcoy", "samboan", "aguinid"],
    ["Old churches in South Cebu", "What to see in Carcar?", "What is in Argao?"],
    """
- Carcar City: heritage houses, St. Catherine of Alexandria Church, and the famous chicharon at the public market.
- Argao: Spanish-era church and plaza, torta, and hablon handwoven fabric.
- Dalaguete: the vegetable basket and summer capital of Cebu, gateway to Osmeña Peak.
- Boljoon: the Patrocinio de Maria church, one of the best-preserved in the country, with a museum.
- Alcoy: Tingko Beach. Samboan: Aguinid Falls.
These are easy stops on the way to or from Oslob.
""")

add("dumaguete-bohol", "south", "Getting around", "Crossing to Dumaguete or Bohol",
    ["dumaguete", "negros", "bohol", "santander", "liloan port", "sibulan", "ferry", "cross", "tagbilaran", "oceanjet"],
    ["How do I go from Cebu to Dumaguete?", "Ferry to Bohol"],
    """
- To Dumaguete: bus to Liloan Port, Santander (southern tip), then a short ferry to Sibulan, Negros Oriental (about 20 to 30 minutes).
- To Bohol: fast craft from Pier 1 in Cebu City to Tagbilaran (about 2 hours). Book OceanJet or SuperCat in advance on weekends.
""")

# ---------------------------------------------------------------- PRODUCTS (catalog + Q&A)
P = []  # product catalog


def product(id, name, kind, origin, region, desc, where, price, tip, keywords, questions):
    P.append(dict(id=id, name=name, kind=kind, origin=origin, region=region,
                  description=desc, where_to_buy=where, price_range=price, tip=tip))
    answer = f"""
{name}: {desc}
Origin: {origin}.
Where to buy: {where}
Typical price: {price} (approximate, check with the seller).
Tip: {tip}
"""
    add("p-" + id, "products", "Local products", name, keywords, questions, answer)


product("dried-mangoes", "Cebu dried mangoes", "Processed fruit",
        "Made from Carabao mangoes processed in Metro Cebu", "metro",
        "Sweet, chewy dried Carabao mango slices. Cebu's best-known pasalubong.",
        "Pasalubong centers, malls, the airport, and factory outlets in Mandaue.",
        "PHP 100 to 200 per 100 g pack",
        "Buy local brands from Cebu processors to support mango growers. Check the expiry date.",
        ["mango", "mangoes", "dried mango", "mangga", "pasalubong", "fruit"],
        ["Where can I buy dried mangoes?", "Are Cebu mangoes the best?"])

product("danggit", "Danggit and dried fish", "Seafood",
        "Coastal towns, especially Bantayan Island and Daanbantayan", "north",
        "Sun-dried rabbitfish (danggit), plus dried squid (pusit) and other dried fish. Fried crispy for breakfast with rice and vinegar.",
        "Taboan Market (Cebu City) has the widest selection. On Bantayan, buy straight from processors near the port.",
        "PHP 600 to 1,200 per kilo for danggit, depending on grade",
        "Ask for boneless or unsalted (lamayo-style) if you prefer. Ask the seller to vacuum-seal for flights.",
        ["danggit", "dried fish", "buwad", "pusit", "squid", "taboan", "fish"],
        ["Where can I buy danggit?", "What is Taboan market?"])

product("bantayan-eggs", "Bantayan eggs and poultry", "Agriculture",
        "Bantayan Island, the egg basket of the Visayas", "north",
        "Bantayan's poultry farms supply eggs to much of the Visayas. Look for salted eggs and fresh trays.",
        "Markets in Bantayan town and Santa Fe, and roadside stalls on the island.",
        "Local market prices per tray",
        "Good to buy for your stay. Fresh eggs travel poorly, so choose salted eggs if taking them home.",
        ["egg", "eggs", "poultry", "chicken", "bantayan egg", "itlog"],
        ["What is Bantayan known for?", "Where do eggs in Cebu come from?"])

product("chicharon", "Carcar chicharon", "Food",
        "Carcar City, South Cebu", "south",
        "Crispy pork crackling, including the famous 'with laman' (with meat) and bituka (intestine) versions.",
        "Carcar Public Market near the rotunda. Also sold in pasalubong shops in the city.",
        "PHP 150 to 300 per pack",
        "Buy on the way back from the south so it stays crisp. Pair it with spiced vinegar.",
        ["chicharon", "chicharron", "carcar", "pork", "crackling", "snack"],
        ["Where is the best chicharon?", "What is Carcar famous for?"])

product("lechon", "Cebu lechon", "Food",
        "Talisay City and Carcar City, South Cebu", "south",
        "Whole roast pig stuffed with lemongrass, garlic, and spices. Famous for crispy skin and flavor that needs no sauce.",
        "Lechon houses in Talisay and Carcar, and well-known shops in Cebu City. Order by the kilo or whole.",
        "PHP 800 to 1,000 per kilo; whole lechon from about PHP 7,000",
        "Order a day ahead for a whole pig. Some shops vacuum-pack lechon for travel.",
        ["lechon", "roast pig", "litson", "talisay", "baboy"],
        ["Where is the best lechon in Cebu?", "Can I bring lechon on the plane?"])

product("rosquillos", "Rosquillos", "Pastry",
        "Liloan, North Metro Cebu", "north",
        "Crisp, flower-shaped cookies first made in Liloan, the original from Titay's.",
        "Titay's in Liloan and pasalubong shops across Metro Cebu.",
        "PHP 80 to 150 per pack",
        "Visit the original Titay's on the way north to Danao or Bantayan.",
        ["rosquillos", "liloan", "titay", "cookie", "biscuit"],
        ["What is rosquillos?", "Where can I buy rosquillos?"])

product("otap", "Otap", "Pastry",
        "Metro Cebu bakeries", "metro",
        "Flaky, oval puff pastry with sugar. A classic Cebu pasalubong that pairs well with coffee or sikwate.",
        "Pasalubong centers, supermarkets, and bakeries in Cebu City and Mandaue.",
        "PHP 80 to 150 per pack",
        "It crumbles easily, so pack it on top of your bag.",
        ["otap", "pastry", "biscuit", "flaky"],
        ["What is otap?"])

product("torta", "Argao torta", "Pastry",
        "Argao, South Cebu", "south",
        "Soft, sweet cake traditionally made with tuba (coconut wine) and pork lard, baked in a mold.",
        "Argao public market and home bakeries along the highway.",
        "PHP 20 to 40 per piece",
        "Best eaten within a few days. Great with sikwate.",
        ["torta", "argao", "cake", "tuba", "bread"],
        ["What is Argao torta?", "What can I buy in Argao?"])

product("hablon", "Argao hablon", "Handicraft",
        "Argao, South Cebu", "south",
        "Handwoven fabric made on wooden looms by local weavers, turned into scarves, bags, and table runners.",
        "Weaving centers and shops in Argao.",
        "PHP 200 to 1,500 depending on the item",
        "Buying direct from weavers keeps the tradition alive. Ask for a weaving demonstration.",
        ["hablon", "weaving", "woven", "fabric", "textile", "handicraft", "craft", "souvenir"],
        ["What handicrafts are made in Cebu?", "What is hablon?"])

product("mantalongon-veg", "Mantalongon highland vegetables", "Agriculture",
        "Mantalongon, Dalaguete, the vegetable basket of Cebu", "south",
        "Cool-climate vegetables like cabbage, carrots, bell pepper, and lettuce grown in the Dalaguete highlands.",
        "Mantalongon public market (busiest early morning) and roadside stalls on the way to Osmeña Peak.",
        "Farm-gate prices, usually cheaper than city markets",
        "Visit the Mantalongon market at dawn before hiking Osmeña Peak. Farmers sell directly here.",
        ["vegetables", "vegetable", "gulay", "mantalongon", "dalaguete", "highland", "farm", "cabbage", "carrots"],
        ["Where do vegetables in Cebu come from?", "Is there a farmers market in Cebu?"])

product("sirao-flowers", "Sirao celosia flowers", "Agri-tourism",
        "Sirao, Cebu City highlands", "metro",
        "Flower farms growing celosia and other cut flowers, also open to visitors as photo gardens.",
        "Flower farms in Sirao and Busay.",
        "Entrance about PHP 100 to 150; flowers by the bundle",
        "Go early morning for cooler weather and better light.",
        ["flower", "flowers", "sirao", "celosia", "garden", "agri", "agritourism", "farm tour"],
        ["Are there farm tours near Cebu City?", "Where is the flower farm?"])

product("guitars", "Mactan guitars", "Handicraft",
        "Abuno and Maribago, Lapu-Lapu City", "metro",
        "Handcrafted guitars and ukuleles from family workshops using local and imported woods.",
        "Workshops and showrooms in Abuno and Maribago, Mactan.",
        "Ukuleles from about PHP 1,500; guitars from about PHP 4,000",
        "Ask for a workshop tour. Workshops can pack instruments for flights.",
        ["guitar", "ukulele", "instrument", "music", "abuno", "maribago"],
        ["Where can I buy a guitar in Cebu?"])

product("puso-masi", "Puso, masi, and budbud", "Food",
        "Made across Cebu, sold in every town market", "general",
        "Puso is rice in woven coconut leaves. Masi is a sticky rice ball with peanut and sugar. Budbud is sticky rice wrapped in banana leaf.",
        "Town public markets, carenderias, and roadside stalls.",
        "PHP 5 to 30 per piece",
        "Masi and budbud make cheap road-trip snacks. Buy from local vendors along the highways.",
        ["puso", "masi", "budbud", "rice cake", "kakanin", "hanging rice", "snack"],
        ["What is puso?", "What snacks are local?"])

product("sikwate-tablea", "Tablea and sikwate", "Agriculture",
        "Made from cacao grown in Cebu and nearby Visayas uplands", "general",
        "Pure ground cacao tablets (tablea) used to make sikwate, the thick Cebuano hot chocolate.",
        "Public markets, Carbon Market, and pasalubong shops.",
        "PHP 100 to 250 per pack",
        "Ask for locally grown cacao to support small farmers. Breakfast of sikwate and puto maya is a Cebu classic.",
        ["tablea", "sikwate", "cacao", "chocolate", "cocoa", "puto maya", "breakfast"],
        ["Where can I buy tablea?", "What is sikwate?"])

product("seaweed", "Guso and seaweed", "Seafood",
        "Coastal farms around Cebu and nearby islands", "general",
        "Fresh seaweed (guso, lato) eaten as salad with vinegar and tomatoes. Seaweed farming supports many coastal families.",
        "Coastal town markets, Carbon Market, and seafood restaurants.",
        "PHP 20 to 60 per serving",
        "Eat it fresh at a sutukil place. It doesn't travel well.",
        ["seaweed", "guso", "lato", "salad", "sea grapes"],
        ["What is guso?"])

product("corn", "Corn and bugas mais", "Agriculture",
        "Upland and northern farming towns", "general",
        "Cebu has a strong corn tradition. Corn grits (bugas mais) are eaten like rice, and boiled corn is sold along the highways.",
        "Town public markets and roadside stalls.",
        "Local market prices",
        "Try a meal with bugas mais at a local carenderia for a true Cebuano experience.",
        ["corn", "mais", "bugas mais", "grits", "maize"],
        ["Do Cebuanos eat corn rice?"])

product("banana-chips", "Banana chips and fruit snacks", "Processed fruit",
        "Small processors across Cebu", "general",
        "Sweet, crunchy banana chips and other dried fruit snacks from local cooperatives.",
        "Pasalubong centers, supermarkets, and cooperative stores.",
        "PHP 50 to 150 per pack",
        "Look for cooperative or barangay-made labels to support local producers.",
        ["banana chips", "banana", "saging", "chips"],
        ["What fruit snacks can I bring home?"])

add("pasalubong", "products", "Local products", "Pasalubong guide",
    ["pasalubong", "souvenir", "buy", "bring home", "gift", "shopping", "products", "local products", "market"],
    ["What pasalubong should I buy?", "What are Cebu's local products?", "What can I bring home from Cebu?"],
    """
Top pasalubong and local products from Cebu:
- Food: dried mangoes, danggit and dried squid, Carcar chicharon, otap, rosquillos, Argao torta, tablea.
- Fresh from farms: Mantalongon vegetables, Bantayan eggs, highway fruits.
- Crafts: Argao hablon weaving, Mactan guitars and ukuleles.
Where to shop: Taboan Market for dried fish, Carbon Market for produce, pasalubong centers in the city, and town markets on your route.
Buying directly in the towns helps the farmers and makers most. Tap a product in the Pasalubong tab for details.
""")

add("markets", "metro", "Local products", "Carbon and Taboan markets",
    ["carbon", "taboan", "market", "public market", "wet market", "palengke", "tiangge"],
    ["Where is Carbon Market?", "What can I buy in Taboan?"],
    """
- Carbon Market (downtown Cebu City): the oldest and largest farmers' market, with fruits, vegetables, flowers, and native goods. The redeveloped section is cleaner and easier to walk.
- Taboan Market (near Pasil): the dried fish market, with danggit, pusit, and more.
Go in the morning, bring small bills, and keep your phone secure in crowds.
""")

add("cargo-food", "products", "Local products", "Bringing food on flights",
    ["flight", "plane", "airport", "baggage", "check in", "carry on", "bring", "allowed", "customs", "pack"],
    ["Can I bring danggit on the plane?", "Can I take lechon home?"],
    """
Dried goods (mangoes, danggit, chicharon, otap) are fine in checked baggage when sealed. Ask sellers to vacuum-seal dried fish so it doesn't smell.
Lechon is allowed if packed well. Many shops offer travel boxes.
For international flights, check your destination's customs rules. Many countries restrict meat, fresh produce, and eggs.
""")

kb = dict(name="Sugbo Guide Cebu KB", verified=VERIFIED, entries=E, products=P)
with open("kb.json", "w", encoding="utf-8") as f:
    json.dump(kb, f, ensure_ascii=False, indent=1)
print(len(E), "entries,", len(P), "products")
