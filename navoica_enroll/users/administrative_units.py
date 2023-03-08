from django.utils.translation import ugettext_lazy as _
from slugify import slugify

units_raw = """ aleksandrowski
 augustowski
 bartoszycki
 bełchatowski
 będziński
 bialski
Biała Podlaska
 białobrzeski
 białogardzki
 białostocki
Białystok
 bielski
 bielski
Bielsko-Biała
 bieruńsko-lędziński
 bieszczadzki
 biłgorajski
 bocheński
 bolesławiecki
 braniewski
 brodnicki
 brzeski
 brzeski
 brzeziński
 brzozowski
 buski
 bydgoski
Bydgoszcz
Bytom
 bytowski
Chełm
 chełmiński
 chełmski
 chodzieski
 chojnicki
Chorzów
 choszczeński
 chrzanowski
 ciechanowski
 cieszyński
 czarnkowsko-trzcianecki
Częstochowa
 częstochowski
 człuchowski
Dąbrowa Górnicza
 dąbrowski
 dębicki
 drawski
 działdowski
 dzierżoniowski
Elbląg
 elbląski
 ełcki
 garwoliński
Gdańsk
 gdański
Gdynia
 giżycki
Gliwice
 gliwicki
 głogowski
 głubczycki
 gnieźnieński
 goleniowski
 golubsko-dobrzyński
 gołdapski
 gorlicki
 gorzowski
Gorzów Wielkopolski
 gostyniński
 gostyński
 górowski
 grajewski
 grodziski
 grodziski
 grójecki
Grudziądz
 grudziądzki
 gryficki
 gryfiński
 hajnowski
 hrubieszowski
 iławski
 inowrocławski
 janowski
 jarociński
 jarosławski
 jasielski
Jastrzębie-Zdrój
 jaworski
Jaworzno
Jelenia Góra
 jędrzejowski
 kaliski
Kalisz
 kamiennogórski
 kamieński
 karkonoski
 kartuski
Katowice
 kazimierski
 kędzierzyńsko-kozielski
 kępiński
 kętrzyński
Kielce
 kielecki
 kluczborski
 kłobucki
 kłodzki
 kolbuszowski
 kolneński
 kolski
 kołobrzeski
 konecki
Konin
 koniński
Koszalin
 koszaliński
 kościański
 kościerski
 kozienicki
 krakowski
Kraków
 krapkowicki
 krasnostawski
 kraśnicki
Krosno
 krośnieński
 krośnieński
 krotoszyński
 kutnowski
 kwidzyński
 legionowski
Legnica
 legnicki
 leski
 leszczyński
Leszno
 leżajski
 lęborski
 lidzbarski
 limanowski
 lipnowski
 lipski
 lubaczowski
 lubański
 lubartowski
 lubelski
 lubiński
Lublin
 lubliniecki
 lwówecki
 łańcucki
 łaski
 łęczycki
 łęczyński
 łobeski
Łomża
 łomżyński
 łosicki
 łowicki
 łódzki wschodni
Łódź
 łukowski
 makowski
 malborski
 miechowski
 mielecki
 międzychodzki
 międzyrzecki
 mikołowski
 milicki
 miński
 mławski
 mogileński
 moniecki
 mrągowski
Mysłowice
 myszkowski
 myślenicki
 myśliborski
 nakielski
 namysłowski
 nidzicki
 niżański
 nowodworski
 nowodworski
 nowomiejski
 nowosądecki
 nowosolski
 nowotarski
 nowotomyski
Nowy Sącz
 nyski
 obornicki
 olecki
 oleski
 oleśnicki
 olkuski
Olsztyn
 olsztyński
 oławski
 opatowski
 opoczyński
Opole
 opolski
 opolski
 ostrołęcki
Ostrołęka
 ostrowiecki
 ostrowski
 ostrowski
 ostródzki
 ostrzeszowski
 oświęcimski
 otwocki
 pabianicki
 pajęczański
 parczewski
 piaseczyński
Piekary Śląskie
 pilski
 pińczowski
 piotrkowski
Piotrków Trybunalski
 piski
 pleszewski
Płock
 płocki
 płoński
 poddębicki
 policki
 polkowicki
Poznań
 poznański
 proszowicki
 prudnicki
 pruszkowski
 przasnyski
 przemyski
Przemyśl
 przeworski
 przysuski
 pszczyński
 pucki
 puławski
 pułtuski
 pyrzycki
 raciborski
Radom
 radomski
 radomszczański
 radziejowski
 radzyński
 rawicki
 rawski
 ropczycko-sędziszowski
Ruda Śląska
 rybnicki
Rybnik
 rycki
 rypiński
 rzeszowski
Rzeszów
 sandomierski
 sanocki
 sejneński
 sępoleński
Siedlce
 siedlecki
Siemianowice Śląskie
 siemiatycki
 sieradzki
 sierpecki
 skarżyski
Skierniewice
 skierniewicki
 sławieński
 słubicki
 słupecki
Słupsk
 słupski
 sochaczewski
 sokołowski
 sokólski
Sopot
Sosnowiec
 stalowowolski
 starachowicki
 stargardzki
 starogardzki
 staszowski
 strzelecki
 strzelecko-drezdenecki
 strzeliński
 strzyżowski
 sulęciński
 suski
 suwalski
Suwałki
 szamotulski
Szczecin
 szczecinecki
 szczycieński
 sztumski
 szydłowiecki
 średzki
 średzki
 śremski
 świdnicki
 świdnicki
 świdwiński
 świebodziński
 świecki
Świętochłowice
Świnoujście
Tarnobrzeg
 tarnobrzeski
 tarnogórski
 tarnowski
Tarnów
 tatrzański
 tczewski
 tomaszowski
 tomaszowski
Toruń
 toruński
 trzebnicki
 tucholski
 turecki
Tychy
 wadowicki
Wałbrzych
 wałbrzyski
 wałecki
Warszawa
 warszawski zachodni
 wąbrzeski
 wągrowiecki
 wejherowski
 węgorzewski
 węgrowski
 wielicki
 wieluński
 wieruszowski
Włocławek
 włocławski
 włodawski
 włoszczowski
 wodzisławski
 wolsztyński
 wołomiński
 wołowski
Wrocław
 wrocławski
 wrzesiński
 wschowski
 wysokomazowiecki
 wyszkowski
Zabrze
 zambrowski
 zamojski
Zamość
 zawierciański
 ząbkowicki
 zduńskowolski
 zgierski
 zgorzelecki
Zielona Góra
 zielonogórski
 złotoryjski
 złotowski
 zwoleński
 żagański
 żarski
 żniński
Żory
 żuromiński
 żyrardowski
 żywiecki"""

ADMINISTRATIVE_UNIT_CHOICES_PL = ((slugify(unit.strip()), unit.strip()) for unit in units_raw.split("\n"))

NATIONALITIES_CHOICES = (
    ('', _('Select...')),
    ('Polish', _('Polish')),
    ('Afghan', _('Afghan')), ('Albanian', _('Albanian')), ('Algerian', _('Algerian')), ('American', _('American')),
    ('Argentinean', _('Argentinean')),
    ('Armenian', _('Armenian')), ('Australian', _('Australian')), ('Austrian', _('Austrian')),
    ('Azerbaijani', _('Azerbaijani')),
    ('Belarusian', _('Belarusian')),
    ('Belgian', _('Belgian')),
    ('Bolivian', _('Bolivian')),
    ('Bosnian', _('Bosnian')), ('Brazilian', _('Brazilian')), ('British', _('British')),
    ('Bulgarian', _('Bulgarian')),
    ('Cambodian', _('Cambodian')), ('Cameroonian', _('Cameroonian')), ('Canadian', _('Canadian')),
    ('Chilean', _('Chilean')),
    ('Chinese', _('Chinese')),
    ('Colombian', _('Colombian')),

    ('Croatian', _('Croatian')), ('Cuban', _('Cuban')), ('Cypriot', _('Cypriot')), ('Czech', _('Czech')),
    ('Danish', _('Danish')),
    ('Dominican', _('Dominican')), ('Dutch', _('Dutch')), ('Ecuadorean', _('Ecuadorean')),
    ('Egyptian', _('Egyptian')),
    ('Estonian', _('Estonian')),
    ('Filipino', _('Filipino')), ('Finnish', _('Finnish')), ('French', _('French')), ('Gabonese', _('Gabonese')),
    ('Georgian', _('Georgian')), ('German', _('German')),
    ('Greek', _('Greek')),
    ('Haitian', _('Haitian')),
    ('Hungarian', _('Hungarian')),

    ('Indian', _('Indian')), ('Indonesian', _('Indonesian')), ('Iranian', _('Iranian')), ('Iraqi', _('Iraqi')),
    ('Irish', _('Irish')),
    ('Israeli', _('Israeli')), ('Italian', _('Italian')), ('Jamaican', _('Jamaican')),
    ('Japanese', _('Japanese')), ('Jordanian', _('Jordanian')), ('Kazakhstani', _('Kazakhstani')),
    ('Kenyan', _('Kenyan')),
    ('Kuwaiti', _('Kuwaiti')),
    ('Laotian', _('Laotian')),
    ('Latvian', _('Latvian')), ('Lebanese', _('Lebanese')), ('Liberian', _('Liberian')), ('Libyan', _('Libyan')),
    ('Lithuanian', _('Lithuanian')), ('Luxembourger', _('Luxembourger')),
    ('Macedonian', _('Macedonian')), ('Malagasy', _('Malagasy')), ('Malawian', _('Malawian')),
    ('Malaysian', _('Malaysian')),
    ('Maltese', _('Maltese')),
    ('Mauritanian', _('Mauritanian')), ('Mauritian', _('Mauritian')), ('Mexican', _('Mexican')),

    ('Moldovan', _('Moldovan')), ('Mongolian', _('Mongolian')), ('Moroccan', _('Moroccan')),
    ('Nepalese', _('Nepalese')), ('Netherlander', _('Netherlander')),
    ('New Zealander', _('New Zealander')),
    ('Nigerian', _('Nigerian')),
    ('Nigerien', _('Nigerien')),
    ('North Korean', _('North Korean')), ('Norwegian', _('Norwegian')),

    ('Pakistani', _('Pakistani')), ('Panamanian', _('Panamanian')),
    ('Peruvian', _('Peruvian')),
    ('Portuguese', _('Portuguese')), ('Qatari', _('Qatari')), ('Romanian', _('Romanian')),
    ('Russian', _('Russian')), ('Rwandan', _('Rwandan')),
    ('Salvadoran', _('Salvadoran')),
    ('Samoan', _('Samoan')),
    ('Saudi', _('Saudi')),
    ('Scottish', _('Scottish')), ('Senegalese', _('Senegalese')), ('Serbian', _('Serbian')),

    ('Singaporean', _('Singaporean')), ('Slovakian', _('Slovakian')),
    ('Slovenian', _('Slovenian')), ('Somali', _('Somali')),
    ('South African', _('South African')), ('South Korean', _('South Korean')), ('Spanish', _('Spanish')),
    ('Sudanese', _('Sudanese')),
    ('Swedish', _('Swedish')), ('Swiss', _('Swiss')), ('Syrian', _('Syrian')), ('Taiwanese', _('Taiwanese')),
    ('Tajik', _('Tajik')),
    ('Tanzanian', _('Tanzanian')), ('Thai', _('Thai')), ('Tunisian', _('Tunisian')),
    ('Turkish', _('Turkish')),
    ('Ugandan', _('Ugandan')), ('Ukrainian', _('Ukrainian')),
    ('Uruguayan', _('Uruguayan')),
    ('Uzbekistani', _('Uzbekistani')), ('Venezuelan', _('Venezuelan')), ('Vietnamese', _('Vietnamese')),
    ('Welsh', _('Welsh')),
    ('Yemenite', _('Yemenite'))
)
