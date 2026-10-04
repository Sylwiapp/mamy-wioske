AREAS = [
    {
        "id": "podgorze",
        "label": "Podgórze",
        "city": "Kraków",
        "lat": 50.0415,
        "lng": 19.9493,
        "zoom": 14,
        "demo": True,
        "subs": [
            {"id": "stare-podgorze", "label": "Stare Podgórze", "lat": 50.0415, "lng": 19.9493, "zoom": 15},
            {"id": "plaszow", "label": "Płaszów", "lat": 50.0442, "lng": 19.9724, "zoom": 15},
            {"id": "zablocie", "label": "Zabłocie", "lat": 50.0476, "lng": 19.9678, "zoom": 15},
            {"id": "krzemionki", "label": "Krzemionki", "lat": 50.0368, "lng": 19.9448, "zoom": 15},
        ],
    },
    {
        "id": "debniki",
        "label": "Dębniki",
        "city": "Kraków",
        "lat": 50.044,
        "lng": 19.926,
        "zoom": 13,
        "subs": [
            {"id": "ludwinow", "label": "Ludwinów", "lat": 50.0448, "lng": 19.9315, "zoom": 15},
            {"id": "ruczaj", "label": "Ruczaj", "lat": 50.0335, "lng": 19.9062, "zoom": 15},
            {"id": "tyniec", "label": "Tyniec", "lat": 50.0198, "lng": 19.8295, "zoom": 14},
        ],
    },
    {
        "id": "stare-miasto",
        "label": "Stare Miasto",
        "city": "Kraków",
        "lat": 50.062,
        "lng": 19.937,
        "zoom": 14,
        "subs": [],
    },
    {
        "id": "krowodrza",
        "label": "Krowodrza",
        "city": "Kraków",
        "lat": 50.076,
        "lng": 19.916,
        "zoom": 14,
        "subs": [],
    },
    {
        "id": "grzegorzki",
        "label": "Grzegórzki",
        "city": "Kraków",
        "lat": 50.061,
        "lng": 19.97,
        "zoom": 14,
        "subs": [],
    },
    {
        "id": "nowa-huta",
        "label": "Nowa Huta",
        "city": "Kraków",
        "lat": 50.072,
        "lng": 20.037,
        "zoom": 13,
        "subs": [
            {"id": "nh-centrum", "label": "Centrum Nowej Huty", "lat": 50.0724, "lng": 20.0376, "zoom": 15},
            {"id": "czyzyny", "label": "Czyżyny", "lat": 50.0702, "lng": 19.9994, "zoom": 15},
        ],
    },
]

PARENT_SEEDS = [
    {
        "id": "ania",
        "name": "Ania",
        "gender": "dziewczynka",
        "age_band": "6-12m",
        "want": "spacer",
        "seeking": ["spacerek", "kawa", "piknik"],
        "window": "16:00–17:30",
        "bio": "Szukam kogoś na powolny spacer z wózkiem. Lubię kawę na wynos i ciszę w parku.",
        "district_id": "podgorze",
        "area_id": "stare-podgorze",
        "east": 120,
        "north": 80,
    },
    {
        "id": "kasia",
        "name": "Kasia",
        "gender": "chlopiec",
        "age_band": "2-3",
        "want": "pogadac",
        "seeking": ["narzekac", "patenty", "ploteczki"],
        "window": "po południu",
        "bio": "Chętnie pogadam o sennych nocach i żłobku. Mogę usiąść na ławce przy placu zabaw.",
        "district_id": "podgorze",
        "area_id": "stare-podgorze",
        "east": -90,
        "north": 40,
    },
    {
        "id": "ola",
        "name": "Ola",
        "gender": "bliznieta",
        "age_band": "0-6m",
        "want": "spacer",
        "seeking": ["spacerek", "wyjsci", "kawa"],
        "window": "krótko, do 17:00",
        "bio": "Dwa wózki, zero pośpiechu. Szukam osoby, która też wychodzi na krótko.",
        "district_id": "podgorze",
        "area_id": "plaszow",
        "east": 70,
        "north": -40,
    },
    {
        "id": "magda",
        "name": "Magda",
        "gender": "dziewczynka",
        "age_band": "6-12m",
        "want": "pogadac",
        "seeking": ["ploteczki", "kawa", "jedzenie"],
        "window": "elastycznie",
        "bio": "Nowa w okolicy — chcę poznać sąsiadki i sąsiadów z dziećmi, nawet na 20 minut.",
        "district_id": "podgorze",
        "area_id": "zablocie",
        "east": -60,
        "north": 50,
    },
    {
        "id": "zuza",
        "name": "Zuza",
        "gender": "chlopiec",
        "age_band": "1-2",
        "want": "spacer",
        "seeking": ["spacerek", "piknik", "jedzenie"],
        "window": "15:00–16:30",
        "bio": "Mogę na rundkę wokół osiedla. Lubię małe grupy, bez pośpiechu.",
        "district_id": "podgorze",
        "area_id": "krzemionki",
        "east": 40,
        "north": 90,
    },
    {
        "id": "asia",
        "name": "Asia",
        "gender": "dziewczynka",
        "age_band": "6-8",
        "want": "dom",
        "seeking": ["joga", "piknik", "patenty"],
        "window": "",
        "bio": "Dziś zostaję w domu, ale chętnie dołączę do wydarzenia w weekend.",
        "district_id": "podgorze",
        "area_id": "plaszow",
        "east": -30,
        "north": 70,
    },
    {
        "id": "ewa",
        "name": "Ewa",
        "gender": "chlopiec",
        "age_band": "0-6m",
        "want": "pogadac",
        "seeking": ["narzekac", "patenty", "kawa"],
        "window": "gdy maluch śpi",
        "bio": "Świeżo po porodzie. Szukam spokojnej rozmowy, bez presji wracania do formy.",
        "district_id": "podgorze",
        "area_id": "stare-podgorze",
        "east": 480,
        "north": 420,
    },
    {
        "id": "bartek",
        "name": "Bartek",
        "gender": "chlopiec",
        "age_band": "9-12",
        "want": "pogadac",
        "seeking": ["jedzenie", "piknik", "kawa"],
        "window": "po szkole",
        "bio": "Tata. Szukam innych ojców na boisko albo wspólną kawę, gdy dzieci grają.",
        "district_id": "podgorze",
        "area_id": "plaszow",
        "east": 110,
        "north": -70,
    },
    {
        "id": "nina",
        "name": "Nina",
        "gender": "dziewczynka",
        "age_band": "13-17",
        "want": "dom",
        "seeking": ["nie-o-dzieciach", "kawa", "joga"],
        "window": "wieczorami",
        "bio": "Córka w liceum, ja wracam do ludzi. Chętnie na wystawę albo spokojną kawę w okolicy.",
        "district_id": "podgorze",
        "area_id": "zablocie",
        "east": 80,
        "north": 20,
    },
    {
        "id": "iga",
        "name": "Iga",
        "gender": "chlopiec",
        "age_band": "3-5",
        "want": "spacer",
        "seeking": ["piknik", "spacerek", "ploteczki"],
        "window": "po przedszkolu",
        "bio": "Plac zabaw i krótkie rundki. Szukam kogoś na stałe, nie jednorazowo.",
        "district_id": "debniki",
        "area_id": "ruczaj",
        "east": 50,
        "north": -30,
    },
    {
        "id": "tomek",
        "name": "Tomek",
        "gender": "dziewczynka",
        "age_band": "6-8",
        "want": "pogadac",
        "seeking": ["nie-o-dzieciach", "joga", "wyjsci"],
        "window": "weekendy",
        "bio": "Tata. Lubię boisko, herbatę i rozmowę bez recenzowania wychowania.",
        "district_id": "nowa-huta",
        "area_id": "nh-centrum",
        "east": -40,
        "north": 60,
    },
]

EVENT_SEEDS = [
    {
        "id": "kawa",
        "title": "Kawa na trawie",
        "kind": "inicjatywa",
        "when": "Dziś, 16:30",
        "place": "Skwer przy bloku",
        "east": 220,
        "north": 160,
        "spots": 6,
        "horizon": "dzis",
        "art": "park",
        "photo": "/static/img/draw/kawa.svg",
        "blurb": "Termosy, kocyki, wózki. Przyjdź nawet na kwadrans.",
        "category": "inicjatywa",
    },
    {
        "id": "wymiana",
        "title": "Wymiana ubranek 62–86",
        "kind": "inicjatywa",
        "when": "Jutro, 11:00",
        "place": "Klatka schodowa / podwórko",
        "east": -500,
        "north": 80,
        "spots": 10,
        "horizon": "tydzien",
        "art": "swap",
        "photo": "/static/img/draw/wymiana.svg",
        "blurb": "Przynieś 3 rzeczy, zabierz 3. Bez sprzedaży.",
        "category": "inicjatywa",
    },
    {
        "id": "spacerek",
        "title": "Poranny korowód wózków",
        "kind": "wydarzenie",
        "when": "Sobota, 9:30",
        "place": "Brama osiedla → park",
        "east": 900,
        "north": -200,
        "spots": 12,
        "horizon": "tydzien",
        "art": "park",
        "photo": "/static/img/draw/spacerek.svg",
        "blurb": "Wspólny spacer 40 min. Tempo niemowlęce, zero rywalizacji.",
        "category": "ruch",
    },
    {
        "id": "biblioteka",
        "title": "Czytanie dla maluchów",
        "kind": "wydarzenie",
        "when": "Niedziela, 12:00",
        "place": "Biblioteka osiedlowa",
        "east": 2800,
        "north": 700,
        "spots": 15,
        "horizon": "tydzien",
        "art": "dk",
        "photo": "/static/img/draw/biblioteka.svg",
        "blurb": "Krótka bajka i kącik dla opiekunów. Można karmić.",
        "category": "inicjatywa",
    },
]

HAPPENING_SEEDS = [
    {
        "id": "dk-joga",
        "title": "Joga z wózkiem",
        "source": "Dom Kultury Podgórze",
        "category": "ruch",
        "audience": "mamy",
        "when": "Wtorek, 10:00",
        "place": "Sala lustrzana, DK Podgórze",
        "east": 650,
        "north": 420,
        "blurb": "Łagodna praktyka, niemowlę w wózku obok maty. Nie trzeba rezerwować stałego miejsca.",
        "horizon": "tydzien",
        "art": "dk",
        "photo": "/static/img/draw/dk-joga.svg",
        "free": False,
    },
    {
        "id": "dk-glina",
        "title": "Ceramika dla mam i maluchów",
        "source": "Dom Kultury Podgórze",
        "category": "warsztat",
        "audience": "mamy",
        "when": "Środa, 11:30",
        "place": "Pracownia gliny",
        "east": 1800,
        "north": -900,
        "blurb": "Brudzimy ręce, dzieci obok na macie. Glina i fartuchy są na miejscu.",
        "horizon": "tydzien",
        "art": "dk",
        "photo": "/static/img/draw/dk-glina.svg",
        "free": False,
    },
    {
        "id": "tata-klub",
        "title": "Klub tata i dziecko",
        "source": "Biblioteka Kraków — Podgórze",
        "category": "ruch",
        "audience": "taty",
        "when": "Sobota, 10:00",
        "place": "Czytelnia dziecięca",
        "east": -700,
        "north": 1100,
        "blurb": "Godzina bajek, klocków i kawy dla ojców. Wózki wjeżdżają.",
        "horizon": "tydzien",
        "art": "people",
        "photo": "/static/img/draw/tata-klub.svg",
    },
    {
        "id": "chusta",
        "title": "Warsztat chustonoszenia",
        "source": "Fundacja Blisko",
        "category": "warsztat",
        "audience": "wszyscy",
        "when": "Niedziela, 12:00",
        "place": "Świetlica osiedlowa",
        "east": 400,
        "north": -600,
        "blurb": "Jak związać chustę na spacer. Można przyjść z partnerem i niemowlęciem.",
        "horizon": "tydzien",
        "art": "people",
        "photo": "/static/img/draw/chusta.svg",
    },
    {
        "id": "lalki",
        "title": "Teatrzyk dla najmłodszych",
        "source": "Teatr Groteska",
        "category": "inicjatywa",
        "audience": "wszyscy",
        "when": "Niedziela, 11:00",
        "place": "Mała scena",
        "east": 2400,
        "north": 1600,
        "blurb": "25 minut, światło przyciemnione łagodnie. Karmienie w ostatnim rzędzie OK.",
        "horizon": "tydzien",
        "art": "dk",
        "photo": "/static/img/draw/lalki.svg",
        "free": False,
    },
    {
        "id": "sensoryka",
        "title": "Zajęcia sensoryczne 6–18 mies.",
        "source": "Dom Kultury Zakrzówek",
        "category": "ruch",
        "audience": "wszyscy",
        "when": "Czwartek, 9:30",
        "place": "Sala ruchowa",
        "east": -2200,
        "north": 300,
        "blurb": "Kasza, tkaniny, dźwięki. Jeden opiekun na dziecko. Można przyjść w skarpetkach.",
        "horizon": "tydzien",
        "art": "park",
        "photo": "/static/img/draw/sensoryka.svg",
        "free": False,
    },
    {
        "id": "tato-warsztat",
        "title": "Tata w warsztacie: naprawiamy wózki",
        "source": "Hackerspace Rodziców",
        "category": "warsztat",
        "audience": "taty",
        "when": "Piątek, 18:00",
        "place": "Garaż społeczny",
        "east": 900,
        "north": 2100,
        "blurb": "Smar, kółka, regulacja. Weź swój wózek albo przyjdź popatrzeć.",
        "horizon": "tydzien",
        "art": "swap",
        "photo": "/static/img/draw/tato-warsztat.svg",
    },
    {
        "id": "kawiarenka",
        "title": "Kawiarenka dla mam karmiących",
        "source": "Dom Kultury Podgórze",
        "category": "inicjatywa",
        "audience": "mamy",
        "when": "Piątek, 10:30",
        "place": "Hol DK, strefa cicha",
        "east": 320,
        "north": 80,
        "blurb": "Bez programu. Kanapa, woda, ktoś do pogadania. Noworodki mile widziane.",
        "horizon": "tydzien",
        "art": "dk",
        "photo": "/static/img/draw/kawiarenka.svg",
    },
    {
        "id": "cafe-lipa",
        "title": "Poranek w bawialni",
        "source": "Kawiarnia Pod Lipą",
        "category": "inicjatywa",
        "audience": "wszyscy",
        "when": "Dziś, 10:00–12:00",
        "place": "Kawiarnia Pod Lipą",
        "east": 80,
        "north": 40,
        "blurb": "Zapraszamy was na kawę. Dla maluchów kącik z drewnianymi zabawkami, dla opiekunów stolik bez pośpiechu. Wózek wjeżdża, przewijak jest.",
        "horizon": "dzis",
        "art": "dk",
        "photo": "/static/img/draw/cafe-lipa.svg",
        "sponsored": True,
        "sponsor": "Kawiarnia Pod Lipą",
        "perk": "Kawa dla opiekuna · kącik zabaw · wstęp wolny",
        "free": True,
    },
    {
        "id": "cafe-brunch",
        "title": "Weekendowy brunch na wózki",
        "source": "Kawiarnia Ziarenko",
        "category": "inicjatywa",
        "audience": "wszyscy",
        "when": "Sobota, 10:30",
        "place": "Kawiarnia Ziarenko",
        "east": 60,
        "north": -20,
        "blurb": "Długi stół, jajecznica i kącik z piankami. Rezerwacja niepotrzebna — kawiarnia otwiera salę specjalnie dla wioski.",
        "horizon": "tydzien",
        "art": "dk",
        "photo": "/static/img/draw/cafe-brunch.svg",
        "sponsored": True,
        "sponsor": "Kawiarnia Ziarenko",
        "perk": "Brunch · bawialnia z tyłu · miejsca na wózki",
        "free": False,
    },
]

CATEGORY_LABEL = {
    "ruch": "Ruch",
    "warsztat": "Warsztat",
    "inicjatywa": "Inicjatywa",
    "spacer": "Ruch",
    "spotkanie": "Inicjatywa",
    "zajecia": "Ruch",
    "spektakl": "Inicjatywa",
    "kolko": "Ruch",
    "kółko": "Ruch",
    "wymiana": "Inicjatywa",
    "kawiarnia": "Inicjatywa",
    "dom-kultury": "Warsztat",
    "osiedle": "Inicjatywa",
    "wydarzenie": "Inicjatywa",
    "sponsor": "Inicjatywa",
}

AUDIENCE_LABEL = {
    "mamy": "Dla mam",
    "taty": "Dla tat",
    "wszyscy": "Dla opiekunów",
}

WANT_LABEL = {
    "spacer": "Chce na spacer",
    "pogadac": "Chce pogadać",
    "dom": "Zostaje w domu",
}

SWAP_SEEDS = [
    {
        "id": "swap-body",
        "title": "Paczka body 62–68, prawie nowe",
        "who": "Ania",
        "kind": "oddaje",
        "platform": "vinted",
        "url": "https://www.vinted.pl",
        "note": "5 sztuk, bawełna. Odbiorę przy wózku na podwórku albo wyślę z Vinted.",
        "photo": "/static/img/photos/swap-body.jpg",
        "east": 160,
        "north": 200,
    },
    {
        "id": "swap-chusta",
        "title": "Chusta kółkowa, rozmiar 6",
        "who": "Kasia",
        "kind": "oddaje",
        "platform": "facebook",
        "url": "https://www.facebook.com",
        "note": "Ogłoszenie z grupy osiedlowej. Oddam za słoiki albo za nic.",
        "photo": "/static/img/photos/swap-chusta.jpg",
        "east": -380,
        "north": 70,
    },
    {
        "id": "swap-fotelik",
        "title": "Fotelik 0–13 kg, baza Isofix",
        "who": "Ola",
        "kind": "link",
        "platform": "olx",
        "url": "https://www.olx.pl",
        "note": "Nie mój, ale sprawdziłam ogłoszenie — sprzedająca z naszej klatki.",
        "photo": "/static/img/photos/swap-fotelik.jpg",
        "east": 740,
        "north": -280,
    },
    {
        "id": "swap-nosidlo",
        "title": "Szukam nosidełka do 15 kg",
        "who": "Ewa",
        "kind": "szuka",
        "platform": "osiedle",
        "url": "",
        "note": "Może ktoś z wioski odkłada po starszaku. Odbiór lokalny.",
        "photo": "/static/img/photos/swap-nosidlo.jpg",
        "east": -60,
        "north": 480,
    },
    {
        "id": "swap-sloiki",
        "title": "Oddam słoiki i butelki po kaszkach",
        "who": "Magda",
        "kind": "oddaje",
        "platform": "osiedle",
        "url": "",
        "note": "Czyste, do przetworów albo zabaw sensorycznych. Pod klatką 3.",
        "photo": "/static/img/photos/swap-sloiki.jpg",
        "east": -900,
        "north": 500,
    },
]

PLACE_SEEDS = [
    {
        "id": "kawa-przewijak",
        "name": "Kawa i cisza",
        "kind": "miejsce",
        "verified": True,
        "tag": "kawiarnia",
        "note": "Przewijak, wejście z wózkiem, nikt nie patrzy krzywo na karmienie.",
        "by": "3 mamy z wioski",
        "photo": "/static/img/photos/place-kawa.jpg",
        "east": 260,
        "north": 140,
    },
    {
        "id": "pediatra",
        "name": "Lek. Marta Wilk",
        "kind": "usluga",
        "verified": True,
        "tag": "pediatra",
        "note": "Nie pędzi. Można wejść z wózkiem. Termin zwykle w 2–3 dni.",
        "by": "Ania, Kasia",
        "photo": "/static/img/photos/place-pediatra.jpg",
        "east": -240,
        "north": 360,
    },
    {
        "id": "hania",
        "name": "Hania — opiekunka",
        "kind": "opiekunka",
        "verified": True,
        "tag": "opiekunka",
        "note": "Wieczory i weekendy. Dwoje własnych dzieci, polecana przez sąsiadki.",
        "by": "5 opinii wioski",
        "photo": "/static/img/photos/place-hania.jpg",
        "east": 520,
        "north": -120,
    },
    {
        "id": "fizjo",
        "name": "Pracownia dna miednicy",
        "kind": "usluga",
        "verified": True,
        "tag": "fizjoterapia",
        "note": "Po porodzie, bez pośpiechu. Gabinet na parterze.",
        "by": "Ewa",
        "photo": "/static/img/photos/place-fizjo.jpg",
        "east": 1100,
        "north": 200,
    },
    {
        "id": "wozki",
        "name": "Używane wózki i foteliki",
        "kind": "miejsce",
        "verified": False,
        "tag": "sklep",
        "note": "Można przymierzyć wózek z dzieckiem. Nie jest to sieć.",
        "by": "Ola",
        "photo": "/static/img/photos/place-wozki.jpg",
        "east": -600,
        "north": -400,
    },
    {
        "id": "zlobek",
        "name": "Żłobek Kamienny Domek",
        "kind": "miejsce",
        "verified": True,
        "tag": "żłobek",
        "note": "Mała grupa, wejście z wózkiem, adaptacja bez łez na siłę.",
        "by": "2 tatusiów z klubu",
        "photo": "/static/img/photos/place-zlobek.jpg",
        "east": 200,
        "north": 700,
    },
]

PLATFORM_LABEL = {
    "vinted": "Vinted",
    "olx": "OLX",
    "facebook": "Grupa FB",
    "osiedle": "Osiedle",
}

KIND_SWAP_LABEL = {
    "oddaje": "Oddaje",
    "szuka": "Szuka",
    "link": "Link",
}

PLACE_KIND_LABEL = {
    "miejsce": "Miejsce",
    "usluga": "Usługa",
    "opiekunka": "Opiekunka",
}

DEFAULT_PROFILE = {
    "name": "Sylwia",
    "district": "Podgórze, Kraków",
    "district_id": "podgorze",
    "area_id": "stare-podgorze",
    "kids": [{"gender": "dziewczynka", "age_band": "6-12m"}],
    "interests": [],
    "seeking": ["spacerek", "kawa"],
    "availability": "spacer",
    "window": "16:00–18:00",
    "quiet": False,
    "onboarded": True,
    "email": "",
    "verified": False,
    "about": "Szukam spokojnej wioski: ktoś na wózek i pogawędkę, bez presji.",
}

NOTICE_SEEDS = [
    {
        "id": "n-walk",
        "kind": "walk",
        "title": "Ania wychodzi na spacer",
        "body": "Koło 16:30 przy skwerze. Może dołączysz z wózkiem?",
        "at": "16:05",
        "parent_id": "ania",
    },
    {
        "id": "n-kawa",
        "kind": "event",
        "title": "Dziś kawa na trawie",
        "body": "Sąsiadki z osiedla spotykają się o 16:30. Zostało jeszcze miejsce.",
        "at": "15:40",
        "happening_id": "kawa",
    },
    {
        "id": "n-cafe",
        "kind": "sponsor",
        "title": "Kawiarnia Pod Lipą zaprasza",
        "body": "Poranek w bawialni — kawa dla Ciebie, kącik dla malucha. Dziś 10:00.",
        "at": "9:10",
        "happening_id": "cafe-lipa",
    },
]

THREAD_SEEDS = [
    {"parent_id": "ania", "sender": "ania", "text": "Hej, wychodzę z wózkiem koło 16:30 przy skwerze. Idziesz?", "at": "16:12"},
    {"parent_id": "kasia", "sender": "kasia", "text": "Dzięki za radę o żłobku. Jak u Ciebie sen?", "at": "14:48"},
    {"parent_id": "magda", "sender": "magda", "text": "Cześć! Jestem nowa w okolicy — może kawa w weekend?", "at": "11:20"},
]

CHAT_REPLIES = {
    "ania": "Super. Będę przy skwerze, zielony wózek.",
    "kasia": "U nas dziś lepiej, dzięki że pytasz.",
    "magda": "Jasne, daj znać która kawiarnia Ci bliżej.",
    "ola": "Mogę na krótko, dwa wózki, ale chętnie.",
    "ewa": "Jeśli maluch zaśnie — napiszę.",
    "zuza": "Pasuje mi rundka po osiedlu.",
    "bartek": "Po szkole mogę wpaść na kwadrans.",
}

AGE_BAND_LABEL = {
    "0-6m": "0–6 mies.",
    "6-12m": "6–12 mies.",
    "1-2": "1–2 lata",
    "2-3": "2–3 lata",
    "3-5": "3–5 lat",
    "6-8": "6–8 lat",
    "9-12": "9–12 lat",
    "13-17": "13–17 lat",
}

GENDER_LABEL = {
    "dziewczynka": "Dziewczynka",
    "chlopiec": "Chłopiec",
    "bliznieta": "Bliźnięta",
    "dziecko": "Dziecko",
}

AGE_BAND_ORDER = ["0-6m", "6-12m", "1-2", "2-3", "3-5", "6-8", "9-12", "13-17"]
AGE_BAND_ALIASES = {
    "0-3m": "0-6m",
    "3-6m": "0-6m",
}


def public_kid(gender: str, age_band: str) -> str:
    band = AGE_BAND_ALIASES.get(age_band, age_band)
    return f"{GENDER_LABEL.get(gender, 'Dziecko')} · {AGE_BAND_LABEL.get(band, 'wiek niepodany')}"


def normalize_kids(kids) -> list[dict]:
    out = []
    for item in kids or []:
        if not isinstance(item, dict):
            continue
        band = item.get("age_band") or "6-12m"
        out.append(
            {
                "gender": item.get("gender") or "dziecko",
                "age_band": AGE_BAND_ALIASES.get(band, band),
            }
        )
    return out or [dict(kid) for kid in DEFAULT_PROFILE["kids"]]


def bands_close(band: str, mine: list[str]) -> bool:
    if not mine:
        return True
    band = AGE_BAND_ALIASES.get(band, band)
    try:
        idx = AGE_BAND_ORDER.index(band)
    except ValueError:
        return False
    for other in mine:
        other = AGE_BAND_ALIASES.get(other, other)
        try:
            if abs(idx - AGE_BAND_ORDER.index(other)) <= 1:
                return True
        except ValueError:
            continue
    return False


SEEKING_LABEL = {
    "wyjsci": "Wyjść i nie zwariować",
    "kawa": "Wypić kawę zanim wystygnie",
    "narzekac": "Ponarzekać",
    "patenty": "Wymienić się patentami",
    "ploteczki": "Ploteczki",
    "spacerek": "Spacerek",
    "jedzenie": "Wspólne jedzenie",
    "joga": "Joga",
    "piknik": "Piknik",
    "nie-o-dzieciach": "Pogadanki nie o dzieciach",
}

SEEKING_LEGACY = {
    "spacer": "spacerek",
    "pogadac": "narzekac",
    "zabawa": "piknik",
    "wydarzenia": "joga",
    "wymiana": "patenty",
    "sen": "narzekac",
    "karmienie": "patenty",
    "tata": "wyjsci",
    "zlobek": "patenty",
    "kawka": "kawa",
    "pomoc": "wyjsci",
    "nowi": "ploteczki",
    "cisza": "nie-o-dzieciach",
}


def normalize_seeking(ids=None):
    out = []
    seen = set()
    for sid in ids or []:
        nid = SEEKING_LEGACY.get(sid, sid)
        if nid in SEEKING_LABEL and nid not in seen:
            seen.add(nid)
            out.append(nid)
    return out

INTEREST_LABEL = {
    "kawa": "Kawa",
    "ksiazki": "Książki",
    "film": "Film i seriale",
    "kuchnia": "Gotowanie",
    "ogrod": "Rośliny",
    "sport": "Ruch i sport",
    "muzyka": "Muzyka",
    "recznosc": "Rękodzieło",
    "podroze": "Podróże",
    "zwierzeta": "Zwierzęta",
    "spacery": "Długie spacery",
}

SEED_AREA = {
    "ania": ("podgorze", "stare-podgorze"),
    "kasia": ("podgorze", "stare-podgorze"),
    "ola": ("podgorze", "plaszow"),
    "magda": ("podgorze", "zablocie"),
    "zuza": ("podgorze", "krzemionki"),
    "asia": ("podgorze", "plaszow"),
    "ewa": ("podgorze", "stare-podgorze"),
    "bartek": ("podgorze", "plaszow"),
    "nina": ("podgorze", "zablocie"),
    "iga": ("debniki", "ruczaj"),
    "tomek": ("nowa-huta", "nh-centrum"),
    "kawa": ("podgorze", "stare-podgorze"),
    "wymiana": ("podgorze", "stare-podgorze"),
    "spacerek": ("podgorze", "krzemionki"),
    "biblioteka": ("podgorze", "plaszow"),
    "dk-joga": ("podgorze", "stare-podgorze"),
    "dk-glina": ("podgorze", "stare-podgorze"),
    "tata-klub": ("podgorze", "plaszow"),
    "chusta": ("podgorze", "zablocie"),
    "lalki": ("podgorze", "stare-podgorze"),
    "sensoryka": ("podgorze", "krzemionki"),
    "tato-warsztat": ("podgorze", "zablocie"),
    "kawiarenka": ("podgorze", "stare-podgorze"),
    "cafe-lipa": ("podgorze", "stare-podgorze"),
    "cafe-brunch": ("podgorze", "zablocie"),
    "swap-body": ("podgorze", "stare-podgorze"),
    "swap-chusta": ("podgorze", "stare-podgorze"),
    "swap-fotelik": ("podgorze", "plaszow"),
    "swap-nosidlo": ("podgorze", "stare-podgorze"),
    "swap-sloiki": ("podgorze", "zablocie"),
    "kawa-przewijak": ("podgorze", "stare-podgorze"),
    "pediatra": ("podgorze", "stare-podgorze"),
    "hania": ("podgorze", "zablocie"),
    "fizjo": ("podgorze", "plaszow"),
    "wozki": ("podgorze", "krzemionki"),
    "zlobek": ("podgorze", "plaszow"),
}


def area_table() -> dict:
    table = {}
    for district in AREAS:
        table[district["id"]] = {
            **district,
            "district_id": district["id"],
            "kind": "district",
        }
        for sub in district.get("subs") or []:
            table[sub["id"]] = {
                **sub,
                "district_id": district["id"],
                "district_label": district["label"],
                "city": district["city"],
                "kind": "sub",
            }
    return table


def area_of(area_id: str | None, district_id: str | None = None) -> dict:
    table = area_table()
    if area_id and area_id in table:
        return table[area_id]
    if district_id and district_id in table:
        return table[district_id]
    return table["podgorze"]


def seed_area(seed_id: str, seed: dict | None = None) -> tuple[str, str]:
    if seed:
        district_id = seed.get("district_id")
        area_id = seed.get("area_id")
        if district_id and area_id:
            return district_id, area_id
    return SEED_AREA.get(seed_id, ("podgorze", "stare-podgorze"))


def item_in_scope(district_id: str, area_id: str | None, item_district: str, item_area: str) -> bool:
    if item_district != district_id:
        return False
    if not area_id or area_id == district_id:
        return True
    return item_area == area_id


def area_label(area_id: str, district_id: str) -> str:
    node = area_of(area_id, district_id)
    return node.get("label") or "Wioska"


def area_phrase(district_id: str, area_id: str | None = None) -> str:
    node = area_of(area_id or district_id, district_id)
    city = node.get("city") or "Kraków"
    if node.get("kind") == "sub":
        return f"{node['label']}, {node.get('district_label') or 'Kraków'}"
    return f"{node.get('label') or 'Wioska'}, {city}"
