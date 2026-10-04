# mamy wioskę

Aplikacja do budowania **lokalnej wspólnoty rodziców**: kto jest blisko na spacer, co się dzieje w okolicy, czym się wymienić i które miejsca są polecone.

Interfejs jest w telefonie (jeden ekran), po polsku. Wejście od razu do przeglądania — bez rejestracji na starcie.

## Zasady produktu

- **Dziecko:** w profilach widać tylko płeć/typ i przedział wieku. Bez imienia dziecka, zdjęcia dziecka, szkoły i adresu domu.
- **Miejsce:** bez GPS na żywo, pinezek i nazw ulic. Odległość jest przybliżona (tuż obok, 500 m, 1 km…). Mapa na Poznaj to uproszczona ilustracja, nie prawdziwa mapa.
- **Nazwa** zawsze małą literą: *mamy wioskę*.

## Zakładki

- **Poznaj** — osoby w zasięgu (500 m–10 km, start 1 km). Filtry: *Chciałabym* i wiek dzieci. Serduszko oznacza osobę (w karcie: *Znam*). Brak filtra po serduszkach.
- **Wydarzenia** — kiedy / rodzaj (ruch, warsztat, inicjatywa) / wstęp (darmowe, płatne). Można dołączyć i dodać własne hasło.
- **Wymiana** — oddaje / szuka / link (Vinted, OLX, grupa FB, osiedle).
- **Miejsca** — miejsca, usługi, opieka. *Sprawdzone* = polecone. Wpisy dodane przez użytkowniczkę są od razu polecone; wpisy z góry — dopiero po *Polecamy*.
- **Wiadomości** — czat 1:1, bez imion dzieci.
- **Ja** (góra) — imię, o sobie, dzieci (płeć + wiek), czego szukam w wiosce. Dzwonek: krótkie powiadomienia.

## Uruchomienie lokalne

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Otwórz http://127.0.0.1:8000

## Kod i hosting

- GitHub: https://github.com/Sylwiapp/mamy-wioske
- Na żywo (Render): https://mamy-wioske.onrender.com

Aplikacja to **FastAPI + SQLite**, więc GitHub Pages jej nie uruchomi. Render buduje Web Service z `render.yaml` (`uvicorn app:app --host 0.0.0.0 --port $PORT`). Darmowy plan bywa zimny — pierwsze otwarcie może chwilę poczekać.

Nowy serwis: https://render.com/deploy?repo=https://github.com/Sylwiapp/mamy-wioske

## Gdzie zmieniać treści

| Co | Plik |
| --- | --- |
| osoby, wydarzenia, wymiana, miejsca, etykiety | `seed.py` |
| dystans i sformułowania „ok. 1 km” | `geo.py` |
| API, SQLite, polecanie miejsc | `app.py` |
| wygląd | `static/style.css` |
| zakładki, filtry, serduszka | `static/app.js` |
| struktura ekranów | `static/index.html` |
