# Geometric Magazine — Opportunities Bot

Automatický bot, ktorý každý pondelok ráno prehľadá overené umelecké platformy, vyfiltruje relevantné príležitosti pre geometrických, abstraktných a konceptuálnych umelcov a pošle HTML email digest.

## Čo bot robí

1. Prehľadá RSS feedy (e-flux, Rhizome, Art Rabbit) a web stránky (Res Artis, TransArtists, CuratorSpace, ArtDeadline, ArtConnect, Arebyte)
2. Každú príležitosť ohodnotí podľa relevantnosti (1–10 bodov) pomocou tier systému kľúčových slov
3. Odfiltruje príležitosti s deadlineom kratším ako 35 dní
4. Zoradí podľa score a pošle HTML email s prehľadnými kartičkami
5. Uloží týždenný digest ako markdown do `/digests/`

## Nastavenie (GitHub Secrets)

Idi na: **Settings → Secrets and variables → Actions → New repository secret**

| Secret name          | Hodnota                                  |
|----------------------|------------------------------------------|
| `GMAIL_USER`         | tvoja Gmail adresa (napr. simon@gmail.com) |
| `GMAIL_APP_PASSWORD` | 16-znakové App Password z Google Account |
| `EMAIL_TO`           | kam posielať digest (napr. simon@gmail.com) |

### Ako získať Gmail App Password

1. Zapni 2-faktorové overenie na Google Account
2. Choď na [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Vytvor nové App Password → vyber "Mail" + "Other (Custom)" → napíš "GeometricBot"
4. Skopíruj 16-znakový kód — to je tvoj `GMAIL_APP_PASSWORD`

## Spustenie

### Manuálne (GitHub Actions UI)
`Actions → Weekly Opportunities Bot → Run workflow`

### Automaticky
Každý pondelok o 07:00 UTC (09:00 SK v lete).

### Lokálne (testovanie)
```bash
pip install -r requirements.txt
export GMAIL_USER="tvoj@gmail.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
export EMAIL_TO="tvoj@gmail.com"
python main.py
```

## Štruktúra projektu

```
opportunities-bot/
├── main.py              # Entry point — orchestruje všetko
├── config.py            # Zdroje a nastavenia (MIN_SCORE, zdroje...)
├── filter.py            # Scoring systém + tier klasifikácia
├── emailer.py           # HTML email builder + Gmail sender
├── requirements.txt     # Python závislosti
├── scrapers/
│   ├── rss.py           # feedparser RSS scraper
│   └── web.py           # requests + BeautifulSoup scraper
├── .github/
│   └── workflows/
│       └── weekly.yml   # GitHub Actions cron workflow
└── digests/             # Ukladajú sa týždenné markdown súbory
```

## Tier systém

| Tier   | Score | Kľúčové slová                                      |
|--------|-------|-----------------------------------------------------|
| Tier 1 | +3    | geometric, op art, constructivism, generative art…  |
| Tier 2 | +2    | abstract, installation, digital art, mural…         |
| Tier 3 | +1    | painting, residency, grant, prize…                  |
| Exclude| auto  | figurative, portrait, realism, photography only…    |

Minimálny score pre zaradenie do digestu: **4 body**.
