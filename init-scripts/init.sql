CREATE DATABASE app_akustyka;

\c app_akustyka;

CREATE SEQUENCE public.materials_pkey_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;



create table materials(
	pkey serial,
	"type" varchar(100) not null,
	name varchar(100) not null,
	"_120"  decimal(22,2) not null,
	"_250"  decimal(22,2) not null,
	"_500"  decimal(22,2) not null,
	"_1000" decimal(22,2) not null,
	"_2000" decimal(22,2) not null,
	"_4000" decimal(22,2) not null
);



create table norms(
	pkey serial,
	name varchar(255) not null,
	absorption_multiplayer decimal(22,2) not null
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) UNIQUE,
    password VARCHAR(150),
    first_name VARCHAR(150)
);



CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    data VARCHAR(10000),
    date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id INTEGER REFERENCES users(id)
);


insert into norms values
(default,'Biura wielkoprzestrzenne, pomieszczenia biurowe typu "open space", sale operacyjne banków i urzędów, biura obsługi klienta oraz inne pomieszczenia o podobnym przeznaczeniu',1.1);

insert into norms values
(default,'Centra obsługi telefonicznej',1.3);

insert into norms values
(default,'Szatnie w szkołach i przedszkołach, w których ubrania zamknięte są w szafkach z pełnymi drzwiami',0.6);

insert into norms values
(default,'Pracownie do zajęć technicznych i warsztaty szkolne',0.6);

insert into norms values
(default,'Sale chorych na oddziałach intensywnej opieki medycznej',0.8);

insert into norms values
(default,'Poczekalnie i punkty przyjęć w szpitalach i przychodniach lekarskich',0.8);

insert into norms values
(default,'Korytarze w przedszkolach, szkołach podstawowych, gimnazjach i szkołach ponadgimnazjalnych',1.0);

insert into norms values
(default,'Korytarze w hotelach, szpitalach i przychodniach lekarskich',0.6);

insert into norms values
(default,'Klatki schodowe w przedszkolach, szkołach, obiektach służby zdrowia i administracji publicznej',0.4);

insert into norms values
(default,'Kuchnie i pomieszczenia zaplecza gastronomicznego (z wyjatkiem magazynów)',0.4);


Insert into materials values (default,'Ściany','Fasada aluminiowa słupowo-ryglowa',0.15,0.05,0.03,0.03,0.02,0.02);
Insert into materials values (default,'Ściany','Beton niemalowany (surowy)',0.01,0.01,0.02,0.02,0.02,0.04);
Insert into materials values (default,'Ściany','Beton szorstki ',0.02,0.03,0.03,0.03,0.04,0.07);
Insert into materials values (default,'Ściany','Beton zatarty na gładko',0.01,0.01,0.02,0.02,0.02,0.05);
Insert into materials values (default,'Ściany','Beton, gładki lub malowany',0.01,0.01,0.02,0.02,0.02,0.02);
Insert into materials values (default,'Ściany','Beton, szorstkie wykończenie',0.02,0.03,0.03,0.03,0.04,0.07);
Insert into materials values (default,'Ściany','Bloczki - 115mm malowane',0.1,0.08,0.05,0.03,0.04,0.07);
Insert into materials values (default,'Ściany','Bloczki - 115mm porowate',0.13,0.1,0.07,0.08,0.14,0.2);
Insert into materials values (default,'Ściany','Bloczki malowane',0.02,0.03,0.03,0.03,0.04,0.07);
Insert into materials values (default,'Ściany','Bloczki porowate',0.05,0.05,0.05,0.08,0.14,0.2);
Insert into materials values (default,'Ściany','Boazeria drewniana z desek o grubości od 16 mm do 22 mm z pustką 50 mm wypełnioną wełną mineralną',0.25,0.15,0.1,0.09,0.08,0.07);
Insert into materials values (default,'Ściany','Cegła ceramiczna licowa porowata',0.15,0.13,0.15,0.15,0.13,0.14);
Insert into materials values (default,'Ściany','Cegła nieotynkowana',0.02,0.02,0.03,0.04,0.05,0.07);
Insert into materials values (default,'Ściany','Cegła nieotynkowana z głębokimi fugami (10 mm)',0.08,0.09,0.12,0.16,0.22,0.24);
Insert into materials values (default,'Ściany','Deski sosnowe na murze',0.1,0.11,0.1,0.08,0.08,0.11);
Insert into materials values (default,'Ściany','Deskowanie z otwartymi szczelinami, pustka 50 mm',0.24,0.8,0.35,0.18,0.1,0.1);
Insert into materials values (default,'Ściany','Drewniane płyty akustyczne z włókniną akustyczną, pustka 50 mm',0.7,0.59,0.71,0.67,0.66,0.63);
Insert into materials values (default,'Ściany','Drewniane płyty akustyczne ze specjalnym tynkiem, pustka 50 mm',0.25,0.54,0.64,0.63,0.72,0.68);
Insert into materials values (default,'Ściany','Drewno politurowane',0.05,0.04,0.03,0.03,0.04,0.04);
Insert into materials values (default,'Sufit','Beton niemalowany',0.01,0.01,0.02,0.02,0.02,0.02);
Insert into materials values (default,'Sufit','Miękkie włókna 20mm na twardym podłożu',0.05,0.2,0.6,0.8,0.67,0.53);
Insert into materials values (default,'Sufit','Płyta na 200mm pustki powietrznej',0.45,0.65,0.7,0.55,0.95,0.95);
Insert into materials values (default,'Sufit','Płyta (Ecophon) na 200mm pustki powietrznej',0.5,0.85,0.9,0.85,0.95,0.85);
Insert into materials values (default,'Sufit','Płyta (Ecophon) 200mm pustki powietrznej',0.5,0.85,0.95,0.85,1,1);
Insert into materials values (default,'Sufit','Płyta (Ecophon)',0.4,0.95,1,0.95,0.95,1);
Insert into materials values (default,'Sufit','Płyta na 200mm pustki powietrznej',0.55,0.75,0.95,0.85,1,1);
Insert into materials values (default,'Sufit','Płyta na 200mm pustki powietrznej',0.4,0.85,1,0.95,0.8,0.7);
Insert into materials values (default,'Sufit','Płyta na 200mm pustki powietrznej',0.4,0.7,0.7,0.65,0.9,1);
Insert into materials values (default,'Sufit','Płyty gipsowo-kartonowe na 200mm przestrzeni powietrznej',0.55,0.7,0.75,0.65,0.04,0.04);
Insert into materials values (default,'Sufit','Płyty gipsowo-kartonowe na legarach',0.2,0.15,0.1,0.05,0.6,0.55);
Insert into materials values (default,'Sufit','Płyty z wełny drzewnej 50mm na 50mm pustce',0.15,0.45,0.75,0.6,0.6,0.55);
Insert into materials values (default,'Sufit','Płyty z wełny drzewnej 50mm na twardym podłożu',0.1,0.2,0.45,0.8,0.8,0.75);
Insert into materials values (default,'Sufit','Stal',0.02,0.03,0.03,0.02,0.1,0.05);
Insert into materials values (default,'Sufit','Strop drewniany gładki bez rys',0.28,0.1,0.07,0.06,0.05,0.06);
Insert into materials values (default,'Sufit','Strop z siatką Rabitza',0.25,0.2,0.1,0.05,0.7,0.75);
Insert into materials values (default,'Sufit','Tynk akustyczny 9-12mm na płycie gipsowo-kartonowej',0.25,0.25,0.35,0.5,0.02,0.03);
Insert into materials values (default,'Sufit','Tynk akustyczny 9-12mm na twardym podłożu',0.05,0.15,0.3,0.5,0.7,0.75);
Insert into materials values (default,'Sufit','Tynk na listwach',0.2,0.15,0.1,0.05,0.5,0.35);
Insert into materials values (default,'Sufit','Tynk na twardym podłożu',0.03,0.03,0.02,0.02,0.04,0.04);
Insert into materials values (default,'Inne','Alpha ClassFrames',0.2,0.6,1,1,1,1);
Insert into materials values (default,'Inne','Axam Acoustic 1.44m2 ',0.27,0.47,0.76,1.17,1.32,1.29);
Insert into materials values (default,'Inne','Axam Acoustic 2.16m2',0.41,0.71,1.14,1.75,1.98,1.94);
Insert into materials values (default,'Inne','Axam Acoustic 2.88m2',0.55,0.95,1.51,2.33,2.63,2.58);
Insert into materials values (default,'Inne','Axam Acoustic 3.24m2',0.61,1.07,1.7,2.63,2.96,2.9);
Insert into materials values (default,'Inne','Axam  Acoustic 3.60m2',0.68,1.19,1.89,2.92,3.29,3.23);
Insert into materials values (default,'Inne','Axam Acoustic 4.32m2',0.82,1.42,2.27,3.5,3.95,3.87);
Insert into materials values (default,'Inne','Axam Acoustic 5.40m2',1.02,1.78,2.84,4.38,4.94,4.84);
Insert into materials values (default,'Inne','Axam Acoustic 5.76m2',1.09,1.9,3.03,4.67,5.27,5.16);
Insert into materials values (default,'Inne','Axam Acoustic 7.20m2',1.36,2.37,3.79,5.84,6.59,6.45);
Insert into materials values (default,'Inne','Axam Acoustic 9.00m2',1.7,2.97,4.73,7.3,8.23,8.07);
Insert into materials values (default,'Inne','Axam Acoustic 2.54m2',0.48,0.84,1.34,2.06,2.32,2.28);
Insert into materials values (default,'Inne','Axam Plain 4.52m2',0.85,1.49,2.38,3.67,4.13,4.05);
Insert into materials values (default,'Inne','Axam Plain 3.62m2',0.68,1.19,1.9,2.94,3.31,3.24);
Insert into materials values (default,'Inne','Axam Plain 4.70m2',0.89,1.55,2.47,3.81,4.3,4.21);
Insert into materials values (default,'Inne','Axam Plain 5.07m2',0.96,1.67,2.67,4.11,4.64,4.54);
Insert into materials values (default,'Inne','Axam Plain 6.50m2',1.23,2.14,3.42,5.27,5.95,5.83);
Insert into materials values (default,'Inne','Axam Plain Acoustic 8.30m2',1.57,2.74,4.37,6.73,7.59,7.44);
Insert into materials values (default,'Inne','Axam Acoustic 1.44m2',0.25,0.29,0.37,0.43,0.57,0.74);
Insert into materials values (default,'Inne','Axam Plain 2.16m2',0.38,0.44,0.56,0.65,0.86,1.12);
Insert into materials values (default,'Inne','Okno, pełnej wysokości z podwójną ramą',0.15,0.05,0.03,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Drzwi drewniane pełne',0.15,0.1,0.08,0.08,0.05,0.05);
Insert into materials values (default,'Inne','Drzwi drewniane puste',0.3,0.25,0.15,0.1,0.1,0.07);
Insert into materials values (default,'Inne','Drzwi drewniane, masywne Tab. B.1.',0.14,0.1,0.08,0.08,0.08,0.08);
Insert into materials values (default,'Inne','Pustka powietrzna',0.25,0.3,0.4,0.45,0.5,0.5);
Insert into materials values (default,'Inne','Pustka powietrzna dla innej otwartej przestrzenie - estymacja',0.4,0.4,0.6,0.7,0.8,0.8);
Insert into materials values (default,'Inne','Pustka powietrzna, scena z dekoracją',0.4,0.4,0.6,0.7,0.8,0.8);
Insert into materials values (default,'Inne','Szyba podwójna 2 ÷ 3 mm z pustką powietrzną ≥ 30 mm',0.15,0.05,0.03,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Szyba podwójna 2 ÷ 3 mm z pustką powietrzną 10 mm',0.1,0.07,0.05,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Szyba podwójna z izolacją akustyczną',0.15,0.05,0.03,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Szyba podwójna z izolacją cieplną',0.1,0.07,0.05,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Szyba pojedyncza 3 mm',0.08,0.04,0.03,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Szklana fasada z izolacją termiczną',0.15,0.05,0.03,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Drzwi drewniane, masywne',0.14,0.1,0.08,0.08,0.08,0.08);
Insert into materials values (default,'Inne','Szyba podwójna 2+3mm z pustką 10 mm',0.1,0.07,0.05,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Drzwi malowane olejno',0.08,0.14,0.12,0.15,0.19,0.17);
Insert into materials values (default,'Inne','Dzrwi malowane olejno ',0.08,0.14,0.12,0.15,0.19,0.17);
Insert into materials values (default,'Inne','Drzwi malowane olejowo',0.08,0.14,0.12,0.15,0.19,0.17);
Insert into materials values (default,'Inne','Drzwi malowane olejno',0.08,0.14,0.12,0.15,0.19,0.17);
Insert into materials values (default,'Inne','PCV (dwuszybowe)',0.1,0.07,0.05,0.03,0.02,0.02);
Insert into materials values (default,'Inne','Meble w zabudowie kuchennej i przedsionku',0,0,0,0,0,0);
Insert into materials values (default,'Inne','Krzesła w rzędach w odstepach od 0,9 do 1,2 m, bez ludzi (drewno, tw, sztuczne)',0.06,0.08,0.1,0.12,0.14,0.16);
Insert into materials values (default,'Inne','Krzesła drewniane z siedzącą osobą',0.72,0.88,0.95,0.98,0.99,1);
Insert into materials values (default,'Inne','Krzesła puste',0.1,0.12,0.12,0.3,0.25,0.14);
Insert into materials values (default,'Inne','Ludzie na krzesłach materiałowych',0,0,0.42,0.47,0,0);
Insert into materials values (default,'Inne','Płyty gipsowe perforowane',0.65,0.6,0.65,0.71,0.75,0.7);
Insert into materials values (default,'Inne','osoba siedząca na miękkim krześle',0.16,0.35,0.42,0.47,0.52,0.53);
Insert into materials values (default,'Inne','Fotele teatralne częściowo wyścielane puste',0.56,0.64,0.7,0.72,0.68,0.62);
Insert into materials values (default,'Inne','Krzesło miękkie',0.1,0.12,0.12,0.3,0.25,0.14);
Insert into materials values (default,'Inne','Osoba siedząca na miękkim krześle',0.16,0.35,0.42,0.47,0.52,0.53);
Insert into materials values (default,'Inne','Krzesła z widownią',0.68,0.75,0.79,0.83,0.87,0.87);
Insert into materials values (default,'Inne','Publiczność na krzesłach v.1',0.76,0.83,0.88,0.91,0.91,0.89);
Insert into materials values (default,'Inne','Publiczność na widowni (osoba)',0.15,0.25,0.4,0.5,0.6,0.6);
Insert into materials values (default,'Inne','Krzesło twarde',0.02,0.03,0.03,0.04,0.04,0.04);
Insert into materials values (default,'Inne','Krzesło miękkie',0.1,0.12,0.12,0.3,0.25,0.14);
Insert into materials values (default,'Inne','Meble drewniane: stoły, krzesła, regał, szafki, biurko',0.35,0.4,0.45,0.45,0.6,0.6);
Insert into materials values (default,'Inne','Fotel bujany',0.04,0.04,0.07,0.06,0.06,0.07);
Insert into materials values (default,'Podłogi','Lite drewno na twardym podłożu',0.02,0.04,0.05,0.06,0.06,0.05);
Insert into materials values (default,'Podłogi','Chropowata posadzka kamienna, piaskowiec',0.02,0.02,0.03,0.04,0.05,0.05);
Insert into materials values (default,'Podłogi','Deski na legarach',0.15,0.11,0.1,0.07,0.06,0.07);
Insert into materials values (default,'Podłogi','Drewno lub płyta wiórowa grubości 19mm na legarach lub listwach',0.15,0.11,0.1,0.07,0.06,0.05);
Insert into materials values (default,'Podłogi','Dywan długowłosy na betonie',0.09,0.08,0.21,0.26,0.27,0.37);
Insert into materials values (default,'Podłogi','Dywan na piance poliuretanowej',0.3,0.35,0.35,0.65,0.62,0.75);
Insert into materials values (default,'Podłogi','Dywan tłoczony, 5mm na miękkim podłożu',0.11,0.09,0.06,0.15,0.3,0.4);
Insert into materials values (default,'Podłogi','Dywan tłoczony, 5mm na twardym podłożu',0.01,0.02,0.05,0.15,0.3,0.4);
Insert into materials values (default,'Podłogi','Dywan wyplatany, 6mm na miękkim podłożu',0.13,0.16,0.26,0.31,0.33,0.44);
Insert into materials values (default,'Podłogi','Dywan wyplatany, 6mm na miękkim podłożu z izolacją',0.18,0.17,0.31,0.6,0.75,0.8);
Insert into materials values (default,'Podłogi','Dywan wyplatany, 6mm na twardym podłożu',0.03,0.09,0.25,0.31,0.33,0.44);
Insert into materials values (default,'Podłogi','Dywan wyplatany, 6mm na twardym podłożu z izolacją',0.08,0.1,0.3,0.6,0.75,0.8);
Insert into materials values (default,'Podłogi','Dywan z nylonu, 2mm na miękkim podłożu',0.11,0.09,0.04,0.05,0.08,0.1);
Insert into materials values (default,'Podłogi','Dywan z nylonu, 2mm na twardym podłożu',0.01,0.02,0.03,0.05,0.08,0.1);
Insert into materials values (default,'Podłogi','Dywan z przędzy włosowej',0.07,0.11,0.19,0.3,0.39,0.41);
Insert into materials values (default,'Podłogi','Gładka posadzka kamienna, płytki ceramiczne',0.01,0.01,0.02,0.02,0.03,0.03);
Insert into materials values (default,'Podłogi','Guma na miękkim podłożu',0.12,0.1,0.05,0.04,0.02,0.02);
Insert into materials values (default,'Podłogi','Guma na twardym podłożu',0.02,0.03,0.04,0.04,0.02,0.02);
Insert into materials values (default,'Podłogi','Lawa bazaltowa o grubości płyt 20 mm',0.06,0.13,0.17,0.2,0.22,0.24);
Insert into materials values (default,'Podłogi','Linoleum',0.02,0.03,0.03,0.04,0.06,0.05);
Insert into materials values (default,'Inne','Chór (<= 0,5 m² / osoba)',0.15,0.25,0.4,0.5,0.6,0.6);
Insert into materials values (default,'Inne','Dziecko w przedszkolu (2 m² / osoba)',0.03,0.14,0.17,0.2,0.3,0.23);
Insert into materials values (default,'Inne','Krzesła drewniane teatralne całkowicie zapełnione',0.5,0.3,0.4,0.76,0.8,0.76);
Insert into materials values (default,'Inne','Krzesła drewniane teatralne puste',0.03,0.04,0.05,0.07,0.08,0.08);
Insert into materials values (default,'Inne','Krzesła drewniane teatralne w 2/3 zajete',0.34,0.21,0.28,0.53,0.56,0.53);
Insert into materials values (default,'Inne','Krzesła w rzędach w odstępach od 0,9 m do 1,2 m (drewno, tworzywo sztuczne)',0.06,0.08,0.1,0.12,0.14,0.16);
Insert into materials values (default,'Inne','Krzesła z fabryczną tapicerką, puste',0.49,0.66,0.8,0.88,0.82,0.7);
Insert into materials values (default,'Inne','Krzesła z fabryczną tapicerką, zapełnione',0.6,0.74,0.88,0.96,0.93,0.85);
Insert into materials values (default,'Inne','Ławki drewniane całkowicie zapełnione',0.5,0.56,0.66,0.76,0.8,0.76);
Insert into materials values (default,'Inne','Ławki drewniane, proste',0.1,0.09,0.08,0.08,0.08,0.08);
Insert into materials values (default,'Inne','Ławki drewniane, w 2/3 zajęte',0.37,0.4,0.47,0.53,0.56,0.53);
Insert into materials values (default,'Inne','Ławki z wyścielanymi siedzeniami i oparciami całkowicie zapełnione',0.5,0.64,0.76,0.86,0.86,0.76);
Insert into materials values (default,'Inne','Ławki z wyścielanymi siedzeniami i oparciami puste',0.32,0.4,0.42,0.44,0.43,0.48);
Insert into materials values (default,'Inne','Ławki z wyścielanymi siedzeniami i oparciami w 2/3 zajęte',0.44,0.56,0.65,0.72,0.72,0.67);
Insert into materials values (default,'Inne','Łóżka szpitalne, składane ',0.6,0.7,0.8,0.9,1,1);
Insert into materials values (default,'Inne','Meble biurowe',0.25,0.15,0.07,0.05,0.05,0.05);
Insert into materials values (default,'Inne','Meble biurowe + osoby siedząca (6 m² / osoba)',0.37,0.33,0.42,0.61,0.73,0.79);
Insert into materials values (default,'Inne','Muzyk z instrumentem (1,1 m² / osoba)',0.16,0.42,0.87,1.07,1.04,0.94);
Insert into materials values (default,'Inne','Muzyk z instrumentem (2,3 m² / osoba)',0.03,0.13,0.43,0.7,0.86,0.99);
Insert into materials values (default,'Inne','Osoba dorosła',0.25,0.35,0.42,0.46,0.5,0.5);

