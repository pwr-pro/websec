# Pystebin
---
## Aplikacja Webowa

---

## użyte technologie

| Kategoria         | Technologia    |
| ----------------- | -------------- |
| Język             | Python         |
| Baza Danych       | PostgreSQL     |
| CI/CD             | GitHub Actions |
| Skaner podatności | Grype          |
| Chmura            | OpenStack      |
| IaC               | Terraform      |


---

# PYSTEBIN
---
## Pastebin w Pythonie

---

## Funkcjonalność

- Logowanie poprzez GitHub OAuth2.0
- Wszystkie strony statycznie generowane (0 JS)

---

## Elementy
- Web Server: ASGI - Uvicorn
- Framework - FastAPI
- Walidacja typów - Pydantic
- Template language - Jinja2
- CSS framework 😎 - Picocss


---

## Baza danych
### PostgreSQL 
---
### Najlepsza baza danych


---

## CI/CD

- Repozytorium hostowane na GitHub'ie więc GitHub Actions \
(+ za darmo)
- Przy komitach automatycznie buduje kontener i wysyła go na repozytorium githuba (ghcr.io)
- W międzyczasie skanuje kontener z pomocą skanera podatności Grype

---

# OpenStack
---
## OpenSource'owa chmura
(+ za darmo)

---

### Postawiono w sumie 4 maszyny
- Load balancer z programem caddy
- 2 instancje aplikacji
- Baza danych PostgreSQL

---

Schemat architektury \
<img src="./img/diagram.png" height=800>

---

Diagram z Horizon (WebUI OpenStacka) \
<img src="./img/horizon.png" height=800>


---

# Problemy i ulepszenia

1. Łatwy dostęp do sekretów
    ```sh
    $ openstack --os-cloud cluster \
        server show pystebin-database \
        -f json | jq -r '.user_data' | base64 -d
    ```

2. Dane przechowywane są na maszynie z bazą danych oraz load balancerem

---

# Dziękujemy za uwagę