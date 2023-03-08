[![Build Status](https://travis-ci.org/OPI-PIB/navoica-enroll-web.svg?branch=master)](https://travis-ci.org/OPI-PIB/navoica-enroll-web)

# Formularz Rejestacyjny Navoica

Do działania systemu wymagane są: 

* Zaintalowany Docker i Docker Compose
* Dostęp do użytkowania dockera przez użytkownika bez 'sudo'
* Otwarte porty 80 i 443. Certyfikat SSL zostanie pobrany automatycznie zgodnie z wybraną domeną. **Jeżeli oba porty nie są dostępne** albo aplikacja działa za reverse-proxy, load balancer itp. można skorzystać z portu 81 i ustawić aplikację wg własnych preferencji.
* Git

Zalecamy, aby adres URL formularza, dla poczucia bezpieczeństwa użytkowników, zawierał w sobie hasło "navoica", np. navoica.domenauczelni.edu.pl.

## Wersja automatyczna instalacji:

Pobierz aktualny kod z repozytorium:

    git clone https://github.com/OPI-PIB/navoica-enroll-web.git

Ustaw zmienne środowiskowe:

    export ENROLL_DOMAIN=domena.pl

    export ENROLL_EMAIL=adres_do_kontaktu@domena.pl
    
[Opcjonalnie] zapisze je do `~/.bashrc` do pożniejszego wykorzystania
    
Przejdź do katalogu:

    cd navoica-enroll-web/

Uruchom komende:

    make setup
    
Ostatnim krokiem instalacji będzie ustawienie hasła dla użytkownika `admin`.

Formularz powinien zostać już zainstalowany poprawny i dostępny online. Przejdź do sekcji `Konfiguracja Oauth2`


## Konfiguracja Oauth2 do komunikacji z navoica.pl

Przechodzimy do panelu administratora (adres może się różnić od wartości `DJANGO_ADMIN_URL`):

    https://enroll-test.navoica.pl/admin/

Uzupełniamy informacje o domenie zgodnie z `DOMAIN`

    https://enroll-test.navoica.pl/admin/sites/site/1/change/

Dodajemy wartości OAUTH2 otrzymane od administratora z navoica.pl, provider EDX

    https://enroll-test.navoica.pl/admin/socialaccount/socialapp/
    
    
## Aktywacja integracji z navoica.pl 

Przechodzimy do panelu twórcy na stronie studio.navoica.pl i wybieramy kurs do edycji. 

    Ustawienia -> Ustawienia zaawansowane -> 
    
Wypełniamy następujące pola:

    Adres rejestracji zdalnej //nasz adres https://ENROLL_DOMAIN/
i

    Aktywuj zdalną rejestrację na kurs // ustawiamy na TRUE


## Podmiana plików PDF ze zgodami w formularzu

Dodaj odpowiednie pliki do katalogu: `./external_static`

Edytuj zmienne środowiskowe ( lub je dodaj ) w pliku `.envs./production/.django `
    
"Wzór oświadczenia...":

    STATEMENT1_PDF=nazwa_pliku.pdf
    STATEMENT1_EN_PDF=nazwa_pliku.pdf #wersja angielska
    
"Przetwarzanie informacji":

    STATEMENT2_PDF=nazwa_pliku2.pdf
    STATEMENT2_EN_PDF=nazwa_pliku.pdf #wersja angielska
    
Zrestartuj aplikacje

    make stop && make start

## Export danych do pliku CSV

Proszę zalogować się do panelu administatora i przejść do sekcji:

    Użytkownicy -> Rejestracje na kurs 
    
Następnie wybrać rekordy i wybrać z listy Akcję: "Export selected objects as csv file"


## Aktualizacja formularza do najnowszej wersji

Przed aktualizacją zalecamy backup bazy danych:

    docker-compose -f production.yml exec postgres backup

Aby aktualizować formularz do najnowszej wersji należy wykonać komende 

    make update

Powyższa operacja wykona się poprawnie jedynie w momencie jeżeli źródło *navoica-enroll-web* zostało sklonowane poprzez *git clone ...* jeżeli natomiast pobrało się paczkę .zip i rozpakowało należy wykonać najpierw:

    git init
    git remote add origin https://github.com/OPI-PIB/navoica-enroll-web.git
    git reset origin/master 
    make update

---------------
---------------


## Wersja ręczna instalacji:

Przejdź do katalogu .envs i skopiuj domyślne ustawienia:


    cd .envs/
    mv .production_example/ .production



Edytuj wg potrzeby. Przykładowe wartości poniżej:

   `.production/.django`

    DJANGO_SECRET_KEY=8zqaTVpMGbAJ6mKdTsdfSDASswwdSfGSZlzAdIpzTYbDXfKw53HVdRCM8n

    DJANGO_ADMIN_URL=admin/

    DJANGO_ALLOWED_HOSTS=enroll.navoica.pl

    DOMAIN=enroll.navoica.pl

    NAVOICA_URL=https://draft.navoica.pl

    CERTBOT_EMAIL=enroll@example.com
    
    EMAIL=enroll@example.com


### Budowanie i uruchamianie Dockera

    docker-compose -f production.yml build

    docker-compose -f production.yml up -d

Po uruchomieniu uruchamiamy migracje danych i tworzymy własnego użytkownika admina

    docker-compose -f production.yml exec django python manage.py migrate

    docker-compose -f production.yml exec django python manage.py createsuperuser


### Dodanie nazwy formularza:

FORM_ORGANIZER_NAME=

np. organizator kursu/szkolenia

FORM_ORGANIZER_NAME=Uniwersytet Kardynała Stefana Wyszyńskiego w Warszawie


### ---- FRONTEND ---- 

## Automatyczne generowanie/aktualizowanie css z scss

npm run compile:css:watch

## Testowanie kodu

npm run lint

## Testowanie kodu scss

npm run lint:styles

## Testowanie kodu javascript

npm run lint:scripts

## Testy lokalne javascript

npm test

