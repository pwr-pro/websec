# Instalacja

## Tworzenie aplikacji GitHub OAuth2.0

Instrukcja znajduje się na strone https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app

Należy stworzyć aplikację oraz zapisać `client secret` oraz `client id`



## Ręcznie
Należy stworzyć środowisko wirtualne z pythonem oraz zainstalować program 
```shell
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app
```
Następnie podać wymagane zmienne jak w przykładowym [`pystebin.toml`](/pystebin-example.toml) lub poprzez zmienne środowiskowe jak w [`docker-compose.yml`](/docker-compose.yml)
> Program szuka pliku konfiguracyjnego w /etc/pystebin.toml

```
curl -fsSL https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app | sudo tee -a /etc/pystebin.toml
```

Pamiętaj o podaniu własnych sekretów


Następnie należy włączyć program i połączyć się z aplikacją na podanym adresie oraz porcie
```shell
(venv) $ pystebin
```

## Docker Compose

Należy podać wymagane zmienne (tekst z <> naokoło) w podanym [docker-compose.yml](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app) 

następnie wystarczy jedynie wystartować docker compose

```shell
$ docker compose up
```


## Terraform

Do odtworzenia infrastruktury niezbędnę będą

- chmura OpenStack (w prosty sposób można stworzyć ją lokalnie z pomocą projektu [devstack](https://docs.openstack.org/devstack/latest/))
- clouds.yaml lub openrc.sh z dostępnymi danymi potrzebnymi do zalogowania się do chmury
- zewnętrzna sieć o nazwie `public`
- flavor maszyny wirtualnej o nazwie `m1.small` - lub zmienić w data.ft

Poniższe dane należy podać jako argumenty

```toml
cloud = "<clouds.yaml>"

container_tag        = "@sha:<sha>" # lub ":latest"
github_client_id     = "<github-client-id>"
github_client_secret = "<github-client-secret>"

app_auth_secret   = "<jwt-signing-secret>"
database_password = "<database-password>"
```

następnie wykonać komendę

```sh
$ terraform apply
```
