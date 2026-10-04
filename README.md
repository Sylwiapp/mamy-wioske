# mamy wioskę

Aplikacja do budowania lokalnej wspólnoty rodziców: kto jest blisko na spacer, co się dzieje w okolicy, czym się wymienić i które miejsca są sprawdzone.

Stack: **Python (FastAPI)** + mapa OpenStreetMap. Interfejs jest przytłumiony, jak aplikacja, nie jak krzykliwa strona.

## Uruchomienie

```powershell
cd C:\Users\sylwi\Projects\mamy-wioske
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload
```

Otwórz http://127.0.0.1:8000.

## Hosting

Kod: https://github.com/Sylwiapp/mamy-wioske

Aplikacja potrzebuje Pythona (FastAPI + SQLite), więc **GitHub Pages jej nie uruchomi**. Publiczną wersję stawia Render z tego repo: Web Service, start `uvicorn app:app --host 0.0.0.0 --port $PORT`.

Jednym kliknięciem: https://render.com/deploy?repo=https://github.com/Sylwiapp/mamy-wioske

## Zakładki

- **Wioska** — osoby w zasięgu, filtr spacer / pogadać, krótka wiadomość
- **Poznaj** — zbiór z domów kultury, warsztatów dla mam i tat, plus hasła z osiedla
- **Wymiana** — rzeczy lokalnie, też jako link z Vinted / OLX / grupy FB
- **Miejsca** — pinezki: kawiarnie, usługi, opiekunki polecane przez wioskę

## Jak rozszerzyć

| Chcesz zmienić | Plik |
| --- | --- |
| mamy, wydarzenia, ogłoszenia, miejsca | `seed.py` |
| dystans | `geo.py` |
| API i SQLite | `app.py` |
| wygląd | `static/style.css` |
| mapa i zakładki | `static/app.js` |
