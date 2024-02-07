---
author: Piotr Żuchowski
links-as-notes: true
geometry: "top=2.5cm,bottom=2.5cm,inner=3cm,outer=2cm, headheight=1.25cm, footskip=1.25cm"
pappersize: a4
fontsize: 12pt
documentclass: article
classoption:
    - twoside
linestretch: 1.2
lang: pl
---


# Wstęp

\newpage

# Cel i zakres pracy

\newpage

# Przegląd literatury i analiza rozwiązań

Rozdział ten stanowi techniczne wprowadzenie do zagadnienia, oparte na analizie literatury i istniejących rozwiązań inżynierskich.
Analiza literatury i istniejących rozwiązań stanowi istotny etap procesu projektowego, umożliwiający lepsze zrozumienie kontekstu danego problemu oraz identyfikację potencjalnych obszarów doskonalenia. Rozdział skupia się na przeglądzie literatury związanej z tematyką pracy inżynierskiej oraz analizie istniejących rozwiązań, mającej na celu dostarczenie solidnej podstawy teoretycznej i technologicznej dla dalszych etapów badawczych.
W tym rozdziale zostaną dogłębnie poruszone teoretyczne kwestie związane z tematem pracy.

## Strumienie danych

Strumieniem danych nazywamy uporządkowany zestaw danych, gdzie każda wartość jest przypisana do określonego momentu czasowego.

Strumień składa się z punktów danych, najczęściej zbieranych w regularnych odstępach czasowych, co pozwala na dokładniejszą analizę zmian w czasie.
W ramach szeregów czasowych można identyfikować różne wzorce, trendy, sezonowe wahania oraz nieregularne zdarzenia.

W pracy A.Arsau, S.Babu, J.Widom[@python-docs] strumien danych jest nazywany nieograniczonym zbiorem elementów krotek należących do schematu strumienia i stempli czasowych tych elementów.

\begin{equation}
S = (s,t)
\end{equation}

Z tego wynika, że charakterystyczną naturalną cechą strumieni jest szeregowość. Wartości nie są jedynym przedmiotem analizy, ale głównie ich kolejność i kontekst który zarysowują w czasie.

Szeregi czasowe są używane do monitorowania i prognozowania zmian, co pozwala wspierać procesy decyzyjne w każdej dziedzinie biznesu.
Mogą obejmować dane z różnych dziedzin, takich jak gospodarka, nauki przyrodnicze, zdrowie, finanse czy technologia.

## Wykrywanie wyjątków w strumieniach danych

Procesy gromadzenia danych, mimo postępu technologicznego, zawsze niosą ze sobą pewne ryzyko i nie są idealne. Istnieje wiele czynników, zarówno technicznych, jak i ludzkich, które mogą wprowadzić błędy do zebranych danych.
Może on wynikać z wadliwego sprzętu pomiarowego, błędu ludzkiego lub przypadkowego zbiegu okoliczności. Dane przesyłane do analizy mogą zawierać szum, błędy pomiarowe, wartości niemożliwe lub w skrajnych przypadkach nie mieć wartości.

Proces czyszczenia danych stał się integralnym i fundamentalnym krokiem w procesie analizy danych, w szczególności w dzisiejszych czasach kiedy ilość przesyłanych danych z roku na rok jest coraz większa.

![Ilość danych stworzonych / pobranych / skopiowanych w latach 2010 - 2021 z prognozami do roku 2024 [@datavolume]](./img/data-volume.png)

Dzięki czyszczeniu analiza staję się dokładniejsza a modele lepiej spełniają swoją role w prognozowaniu kolejnych wartości. Podstawowym krokiem czyszczenia danych jest wykrywanie i usuwanie wyjątków z serii danych.

Wyjątkiem
: nazywamy obserwację, której wartość znacząco różni się od innych wartości w losowej próbie z populacji. Określenie "znacząco różni" nie jest precyzyjnym określeniem. Kontekst każdej analizy jest wyjątkowy. W rozumieniu tej definicji, każda analiza ma za zadanie zdefiniować czym i jaka będzie znacząca różnica.

## Efekt Maskowania

Efekt maskowania *(ang. masking effect)* jest obecnym problemem w wykrywaniu wyjątków, wpływa on negatywnie na dokonywane analizy. Dlatego metoda wykrywania wyjątków powinna być odporna na działanie efektu i wykryć zamaskowaną anomalię.

Maskowaniem
: wyjątku nazywamy zjawisko nie wykrycia wyjątku, z powodu wpływu większej anomalii na statystykę testową, która determinuję wyjątek.

Efekt maskowania może wystąpić w sytuacji, gdy analiza, z góry narzuca wykrycie i usunięcie ustalonej liczby wyjątków. Maskowanie wystąpi w przypadku nieoszacowania liczby wyjątków. Ciekawym przypadkiem jest sytuacja odwrotna, gdy założenie liczby wyjątków przeszacowuję faktyczną liczbę
wyjątków. Dochodzi do przeciwnego efektu zwanego **swamping**, kiedy element bliskiego skupiska zostaje rozpoznany jako wyjątek

![Efekt Maskowania: Wyjątek $x2$ jest bardziej odstający, $x2$ może zamaskować wykrycie wyjątku $x1$](./img/masking.svg){width=70%}

## Algorytm Chen-Liu
Praca Chung Chen i Lon-Mu Liu *"Joint Estimation of Model Parameters and Outlier Effects in Time Series"* dokumentuję algorytm analizy strumienia danych.
Podstawowym celem badań było przedstawienia procedury wykrywania wyjątków, która uwzględnia możliwość istnienia fałszywych i zamaskowanych wyjątków. Dodatkowo była w stanie obliczyć wpływ wyjątków na model, oraz oszacować nowe parametry modelu.

Dzięki precyzyjnemu zdefiniowaniu czterech różnych typów wyjątków, które pojawiały się w poprzednich badaniach, staje się możliwe pełniejsze zrozumienie ich wpływu na dane badawcze. Określenie obliczonego wpływu staje się kluczową podstawą do przeprowadzenia korekty parametrów modelu oraz umożliwia dalszą analizę.

Poniższy przykład bazuję na modelu ARIMA postaci:

\begin{equation}
Y_t = \frac{\theta(B)}{\alpha(B)\phi(B)}
\end{equation}

Procedura "Chen-Liu" przedstawia szereg czasowy w następujący sposób:
\begin{equation}
Y_t^* = Y_t + \omega \xi (B) I_t(t_1)
\end{equation}

Gdzie:

- Funkcja $I_t$ przyjmuję wartość 1 kiedy występuję wyjątek w każdym innym wypadku jest równa 0.
- $\omega$ jest początkową wartością odchylenia
- $\xi (B)$ określa jak będzie kształtował się wpływ wyjątku w czasie.


Algorytm przyjmuję rozróżnia następujące wyjątki na następujące typy:

- *Additive Outlier* (AO): Efekt charakteryzuję się pojedynczą, nagłą anomalią.

\begin{equation}
AO: \xi (B) = 1
\end{equation}

- *Level Shift* (LS): Trwały, ciągła zmiana wartości.

\begin{equation}
LS: \xi (B) = \frac{1}{1 - B}
\end{equation}

- *Temporary change* (TC): Efekt słabnie w czasie. Dodatkowym parametrem jest $\delta$ która określa krzywiznę.

\begin{equation}
TC: \xi (B) = \frac{1}{1 - \delta B} \quad \quad \quad 0 < \delta < 1
\end{equation}


- *Innovational Outlier* (IO): Krzywa w czasie jest odzwierciedleniem modelu. W przypadku modelu ARMA wygląda następująco:

\begin{equation}
IO: \xi (B) = \frac{\theta(B)}{\alpha(B) \phi(B) }
\end{equation}

W późniejszych pracach i implantacjach [@alsdkf] można napotkać na 5 typ wyjątków $SLS$. Ma za zadanie lepiej odwzorcowywać sezonowość szeregu czasowego niż typ IO, który nie musi dziedziczyć cech sezonowości z przyjętego modelu.

\begin{equation}
SLS: \xi (B) = 1/S \quad \quad \quad S = 1 + B + ... + B^{s-1}
\end{equation}

![Porównanie efektów różnych wyjątków a) AO, b) LS, c) TC, d) IO ARIMA(0,1,1)(0,1,1)](./img/effects.svg){width=95%}


Algorytm postępowania jest iteracyjny i jest podzielony na 3 oddzielne etapy. Przedstawione poniżej kroki algorytmu są uproszczone. Dokładny opis procedury można znaleźć w oryginalnej pracy[@dupa]:

#. Obejmuję wykrycie potencjalnych wyjątków. W tym celu dokonuję się dopasowania przyjętego modelu do serii danych i obliczenia odchyleń dla każdego punktu.
W następnym kroku, dla każdego punktu i szukanego typu obliczane są statystyki $\tau$ i $\omega$. Jeśli statystyka $| \tau |$ w czasie $t$ jest większa niż przyjęta wartość krytyczna $C$ oznacza, że w tym punkcie wystąpił wyjątek.
Jeżeli 2 lub więcej typów przekroczyła wartość krytyczną wybierany jest typ z największym współczynnikiem $\tau$.
Następuję obliczenie efektów wykrytych wyjątków i usunięcie z serii danych. Poprawiona seria danych zostaję ponownie analizowana zgodnie z poprzednimi krokami, dopóki w iteracji nie zostanie wykryty żaden wyjątek, lub zostanie przekroczona ustalona liczba iteracji.

#. W tym etapie zostaję sprawdzony wpływ potencjalnych wyjątków. Do tego celu zostaje użyty model regresji obliczyć wielkość wyjątku $\hat{\omega}$.
Obliczana jest ponownie $\tau_j$ korzystając ze wzoru: $\hat{\tau}_j = \hat{\omega}_j / std(\omega)$. Jeśli statystyka jest niższa niż wartość krytyczna $C$ wyjątek jest usuwany z listy potencjalnych. Pętla zostaję przerwana w przypadku braku wykrycia błędu lub przekroczenia liczby iteracji.
Następuję kolejne dopasowanie modelu skorygowanej serii.

#. Ostatnim etapem jest powtórzenie pierwszej i drugiej fazy algorymu wykorzystując nowe parametry modelu: W pierwszej fazie nie koryguję parametrów. W drugiej fazie $\hat{\omega}$ jest końcową wartością.

## Wykrywanie wyjątków w systemach informatycznych

Algorytm "Chen-Liu" nie jest jedynym algorytmem wykrywania wyjątków. Na przestrzeni lat postało wiele metod stworzonych w tym celu.
Przykładami takich algorytmów są:

- Isolation Forest
: Jedna z najnowszych metod wykrywania wyjątków. Metoda polega na wykorzystaniu drzew binarnych do losowego podziału serii danych. Implementacja jest dostępna w wielu językach programoawnia tj Python, R i dostępna dla platformy Apache Spark. [@iforest]

- Auto enkodery
: Grupa algorytmów oparta na sztucznej inteligencji. Główna idea stojąca za autoenkoderami polega na nauczeniu się skompresowanego przedstawienia lub kodowania danych wejściowych. Anomalie są wykrywane poprzez pomiar błędu rekonstrukcji między wejściem a odtworzonym wyjściem.

Istnieje dużo dziedzin gdzie wykrywanie wyjątków znalazło zastosowanie. Algorytmy są stosowanie w cyberbezpieczeństwie jako systemy **IDS** *(Intrusion Detection System)*. Takie systemy mogą bazować na sztucznej inteligencji lub działać na zasadzie data-miningu.

![Przykładem systemu IDS jest Surikata](https://3.bp.blogspot.com/-mYFCDwWougw/U_B7IjW9w5I/AAAAAAAAAgs/5Wfa2OBU4hM/s1600/Custom1.PNG)

Dzięki algorytmom, możliwe jest wykrywanie oszustw bankowych. Przykładem takich aplikacji jest "SEON".

Wykrywanie wyjątków znalazło zastosowanie w systemach IOT, zarządzaniu infrastrukturą IT jak i mikro serwisów. Algorytmy stają się pomocne przy wykrywaniu usterek sprzętu. Wczesne wykrycie problemów z wydajnością systemów zwiększa jakość, efektywność i stabilność samego systemu jak i biznesu.

Przykładem oprogramowania służącej do monitorowania zasobów aplikacji / klastra jest Grafana, która daję możliwość podglądu na żywo statystyk CPU, pamięci, transferu internetowego. Grafana udostępnia płatnym użytkownikom wykrywanie wyjątków w wybranych strumieniach i zintegrowanie z systemem powiadomień.[@grafana-docs]

![Konfiguracja detekcji wyjątków w programie grafana](./img/grafana)

Istnieją rozwiązania w postaci bibliotek. Sektorem, w którym wykrywanie wyjątków jest szeroko stosowane są media społecznościowe. Firmy takie jak Meta *(dawniej Facebook)* czy X *(dawniej Twitter)* udostępniają kod swoich bibliotek przeznaczone do analizy danych i  wykrywania wyjątków [@twitter-docs] [@prophet-docs].

Popularnymi bibliotekami w języku python są scikit-learn i TODS. Zaletą bezpośredniego użycia metody jest elastyczność rozwiązania, jednak wymagają pracy specjalistów w dziedzinie analizy danych [@scikit-learn] [@Lai_Zha_Wang_Xu_Zhao_Kumar_Chen_Zumkhawaka_Wan_Martinez_Hu_2021].


## Podsumowanie

Analiza strumieni danych jest popularnym i prężnie rozwijanym tematem w obecnej stanie technologi informatycznych. Niewątpliwie algorytmy bazujące na sztucznej inteligencji otwierają kolejne kierunki rozwoju. Z tego powodu istnieje ryzyko wyparcia metod tradycyjnych na rzecz technologi uczenia
maszynowego.
Jednakże, przedstawiona metoda "Chen-Liu" wyróżnia się swoimi właściwościami, a wyniki w postaci klasyfikacji wykrywanych wyjątków, mogą wzbogacić analizę danych.

Język Python jest jednym z najpopularniejszych języków w dziedzinie analizie danych, dlatego implementacja zaprojektowana dla tego języka, może być
najbardziej dostrzeżona i jednocześnie najprzydatniejsza dla społeczności.


\newpage

# Metodologia i implementacja projektu

Ten rozdziej opisuję szczegóły implementowanego rozwiązania. Zostaną poruszone dogłębnie aspekty techniczne i wykorzystanej technologii. Zostanie też przedstawiony proces implementacji jak i etap wdrożenia aplikacji.

## Wymagania

Wymagania odnośnie aplikacji możemy podzielić na funkcjonalne i niefunkcjonalne:

Funkcjonalne:

- Algorytm musi przedstawiać wynik analizy w formie listy wykrytych wyjątków i statystyk modelu.
- Użytkownik może przetestować zbiór danych.
- Rozwiązanie udostępnia możliwość przesłania serii danych do analizy w postaci pliku csv.
- Użytkownik może prosić o wygenerowanie danego typu efektu.
- Serwis daję możliwość połączenia efektów w jedno rozwiązanie.

Niefunkcjonalne:

- Wyjątki muszą być kategoryzowane.
- serwis być odporna na znaczny ruch.
- serwis przedstawia swój stan zdrowia.
- serwis loguję kolejne kroki postępowania wg przyjętego formatu.
- aplikacja musi być bezstanowa aby była lepiej skalowalna.


## Wybór technologii

Główną technologią użytą do implementacji algorytmu jak i usługi jest język Python. Python jest doskonałym narzędziem do szybkiego tworzenia aplikacji. Dodatkowo Python jest popularnym językiem w społeczności analityków danych.

Biblioteki wykorzystane w implementacji modułu algorytmu to:

- Numpy
: popularna i ceniona biblioteka przeznaczona do obliczeń na macierzach. Głównym typem wykorzystywanym do obliczeń jest ``Ndarray``. Numpy daję możliwości zaawansowanych operacji na macierzach, stosowanie filtrów i przekształceń.
Plusem biblioteki jest implementacja krytycznych funkcji i struktur w języku C. W ten sposób biblioteka łączy ze sobą efektywny kod i udostępnia proste struktury Python'a. [@numpy-docs]

- Pandas
: Biblioteka, która udostępnia struktury danych i narzędzia do sprawnego manipulowania danymi numerycznymi i tabelarycznymi. Pandas jest. Pandas jest szczególnie przydatny do analizy danych, przetwarzania danych i pracy z danymi czasowymi. Pandas oferuje wiele funkcji umożliwiających łatwe wczytywanie danych z różnych źródeł (takich jak pliki CSV, Excel, bazy danych), manipulowanie nimi, grupowanie, filtrowanie, agregację, a także operacje na czasie. [@pandas-docs]

- Statsmodels
: Biblioteka, zaprojektowana do statystycznego modelowania danych. Jest używana głównie do analizy danych, testowania hipotez, tworzenia modeli regresji i wielu innych zastosowań w dziedzinie statystyki i ekonometrii. StatsModels dostarcza narzędzi do estymacji modeli statystycznych, testowania hipotez, prowadzenia analizy czasowej i wielu innych operacji statystycznych. [@statsmodels-docs]

Biblioteki i technologie użyte do tworzenia serwisu:

- FastAPI, Pydantic i Uvicorn
: Biblioteka programistyczna, która umożliwia szybkie tworzenie aplikacji internetowych zgodnych z protokołem RESTful. Jest oparta na standardzie Python oraz bazuje na bibliotekach standardowych. FastAPI jest znane ze swojej wysokiej wydajności, automatycznego generowania dokumentacji API i łatwości użycia. FastAPI wykorzystuję bibliotekę Pydantic do tworzenia klas DTO (Data Tranfer Objects), serializacji danych i na ich podstawie tworzenia dokumentacji interfejsu REST. Biblioteka Uvicorn jest asynchronicznym serwerem http.

- Konteneryzacja Docker
: Docker jako technologia wirtualizacji na poziomie jądra systemu operacyjnego jest idealnym rozwiązaniem. Konteneryzacja zapewnia stałe środowisko uruchomieniowe aplikacji. Dzięki zastosowaniu technologi produkt zyskuję na jakości poprzez standaryzację, elastyczność dla największych chmur obliczeniowych. Aplikacja staję łatwo skalowalna i zarządzanie instancjami jest łatwiejsze. Poza izolacją aplikacji budowanie obrazów Docker otwiera możliwości lepszej pracy nad projektem i wprowadzania technik DevOps tj. CI/CD pipelines.

- Chmura Google Cloud (GCP)
: Chmura obliczeniowa Google jest jedną z największych dostawców usług chmurowych na świecie. Usługi chmury pozwalają na szybkie i automatyzowane wdrażanie aplikacji lub konfiguracji infrastruktury. Chmura jest prężnie rozwijaną technologią, ponieważ z perspektywy biznesu chmura jest szansą na
zaoszczędzenie kosztów związanych z utrzymaniem własnej infrastruktury i specjalistów związanych nimi związanymi. Koszty stają się bardziej przewidywalne dzięki cennikom i kalkulatorom. Google dzięki SLA (https://cloud.google.com/run/sla) gwarntuję dostępność usług na poziomie 99.5% w skali miesiąca. Jeżeli usługa nie osiągnie wzorowej dostępności poprzez (np. zbyt duży "Error Rate" nie związany z wdrożoną aplikacją), Google zwraca koszt według cennika.

![Udziały na rynku usług chmurowych](https://cdn.statcdn.com/Infographic/images/normal/18819.jpeg)

## Zastosowane narzędzia

- Git & Github
: System zarządzania kodem. Użycie systemu wersjonowania jest kluczowy w perspektywie dalszej rozwoju projektu jak i ułatwia dokumentację projektu. Zewnętrzne repozytorium Github pozwala na przechowywanie projektu pozawala na udostępnianie projektu społeczności i możliwej kontrybucji.

- Terraform
: Narzędzie służące do automatyzacji infrastruktury chmurowej. Projekt Open Source stworzony przez Hashicorp, który pozwala na zastosowanie technik IaC i otwiera możliwości automatyzacji poprzez techniki Devops.

- Narzędzia jakości kodu
: Niewątpliwie narzędzia formatowania poprawiają jakość oprogramowania poprzez wymuszenie przyjętych standardów. Formater kodu python "Blue" udostępnia narzędzie CLI dzięki czemu proces formatowanie można łatwo zintegrować z edytorem kodu. Warto aby edytor tekstu wspierał funkcje LSP (Language Server Protocol) lub dodawał funkcję wspomagające prace przy kodzie tj. podświetlanie błędów składni przed uruchomieniem kodu, wyświetlanie dokumentacji funkcji, przewidywał użytych i zwracanych typów.

## Implementacja algorytmu

Implementacja algorytmu znajduję się w oddzielnym module 'algorithm'. Moduł ma za zadanie zwrócenie analizy zgodnie z metodą opisaną przez poprzednim rozdziale.

Biblioteka stara się być możliwie minimalistyczna. Dla zapewnienia możliwie najlepszej wydajności implementacja unika tworzenia nowych klas i abstrakcji nad użytymi bibliotekami, które mogłyby potencjalnie spowolnić wykonywanie obliczeń.

Jednym z problem stojącym przed implementacją 1 fazy algorytmu, jest dokonanie transformacji przyjętego modelu do postaci:

\begin{equation}
\pi(B) = \xi(B) = 1 - \pi_1B - \pi_2B^2...
\end{equation}

Tym zadaniem ma się zająć funkcja `arma2ma`, która przyjmuje parametry AR i MA dla modelu ARIMA oraz oczekiwany stopień wielomianu $\pi$.

```python
def arma2ma(ar, ma, lag_max):
    ar = ar.tolist() if isinstance(ar, np.ndarray) else ar
    ma = ma.tolist() if isinstance(ma, np.ndarray) else ma

    if not isinstance(ar, list):
        ar = [ar]
    if not isinstance(ma, list):
        ma = [ma]

    if len(ar) == 0:
        ar = [1]
    if len(ma) == 0:
        ma = [1]

    p = len(ar)
    q = len(ma)
    m = int(lag_max)

    logging.debug(f'ar: {ar}')
    logging.debug(f'ma: {ma}')
    if m <= 0:
        raise ValueError('Invalid value of lag_max')

    psi = np.zeros(m)
    for i in range(m):
        tmp = ma[i] if i < q else 0.0
        for j in range(min(i + 1, p)):
            tmp += ar[j] * (psi[i - j - 1] if i - j - 1 >= 0 else 1.0)
        psi[i] = tmp

    return psi
```

Funkcja przed wykonaniem poprawnych obliczeń musi sprawdzić czy podane argumenty są postaci listy. Jeżeli wykryte obiekty typu `numpy.Ndarray` są konwertowane do list. Zauważyć można logowanie parametrów AM i MA.

Logowanie odbywa się poprzez zmienna `logging`, która jest konfigurowana w module `logger.py`

```python
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='[%(asctime)s] %(levelname)s %(funcName)s:\n %(message)s',  # Define the log message format
    datefmt='%Y-%m-%d %H:%M:%S',  # Define the date-time format
)
```

Konfiguracja w tym formacie pozwala na czytelne sprawdzenie działania aplikacji. Aplikacja jest zaprojektowana do działania w chmurze obliczeniowej. Z związku z tym logi nie są zapisywane do zewnętrznego pliku, tylko przesyłane do strumieni `stdout` i w przypadku błędów `stderr`. Dzięki temu
podejściu rozwiązanie jest bardziej otwarte na integracje z narzędziami przeznaczonymi do analizy i agregacji logów.
Przykładem może być platforma Kubernetes(k8s), czy Grafana Loki które domyślnie pobiera logi ze strumieni kontenerów, aby później móc procesować i wyświetlić wyniki analiz.

Najważniejszym etapem jest obliczenie współczynników $\hat{\omega}$ i $\hat{\tau}$ dla każdego punku i typu w zbiorze danych. Równania współczynników są różne dla każdego typu. W tym miejscu dokonano optymalizacji kodu poprzez zbiorowe obliczenia współczynników wykorzystując bibliotekę numpy.

Wyniki obliczeń są zapisywane do postaci obiektów Dataframe, które dalej będą prezekazywane.

## Moduł REST

Moduł interfejsu REST pozawala na zdalnie testowanie zbiorów danych i sprawdzanie wyników analizy.

Interfejs zapewnia metody GET dla sprawdzenia generowania effektów.

Najważniejszy enpoint jest związany z przesyłaniem pliku do analizy. Przesyłanie pliku jest osiągnięte poprzez rozszerzenie biblioteki FastAPI `UploadFile`. W dalszych etapach funkcji następuję walidacja pliku. Funkcja obsługuję pliki csv istara się odczytać wybraną serię.
Endpoint udostępnia możliwość zaznaczenia, że pierwsza linia zawiera tytuły i pozwala na wybranie kolumny z danymi

```python
@app.post('/analyze/')
async def analyze_file(
    file: UploadFile,
    cval: float = 2,
    have_header: bool = False,
    col: int = 0,
) -> AnalyzeResult:
```

Zwrot analizy jest podany w postaci klasy `AnalizeResult`. Biblioteka Pydantic jest szczególnie przydatna w tym wypadku.
Poprzez stworzenie klas pochodnych  klasy `BaseModel` Konstruktory i podstawowe metody dostępu są automatycznie zaimplementowane.

Biblioteka FastAPI potrafi integrować się z przekazaną klasą i stworzyć odpowiedni endpoint, który można można sprawdzić poprzez endpoint `/docs`. Dodatkowym plusem jest fakt automatycznej aktualizacji manifestu openAPI który jest oficialną dokumentacją interfejsu.

```python
class Entry(BaseModel):
    index: float
    origin: float
    effect: float
    result: float
    AO: float | None
    IO: float | None
    TC: float | None
    LS: float | None

class AnalyzeResult(BaseModel):
    id: UUID
    time: datetime
    data: list[Entry]
    raport: Raport
```

![Swagger jako forma interaktywnej dokumentacji](./img/Swagger.png)

## Docker

Jak wcześniej zostało wspomniane konteneryzacja aplikacji jest ważnym aspektem w dalszego wdrażania i utrzymania aplikacji w spójności.

```dockerfile
FROM python:3.11.6-alpine
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
COPY . /code
EXPOSE 80
CMD ["uvicorn", "code.app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

Warto zwrócić uwagę na rozdzielenie pliku requirements.txt od pozostałego kodu aplikacji. W takim ustawieniu warstw podczas budowania możliwe jest zaoszczędzenie czasu poprzez wykorzystanie mechanizmu cachowania warstw.
Plik `requirements.txt` jest plikiem zawierającym wszystkie wymagane zależności dla aplikacji. Generowany jest poprzez komendę `pip freeze`.

Jeżeli jednak zmiany w aplikacji nie dotyczą zewnętrznych bibliotek mechanizm wypychania obrazów i budowania wykorzysta z pamięci cache z poprzednich akcji.


Wykorzystanie polecenia `EXPOSE 80` nie wpływa na budowany obraz aplikacji. Jest jedynie dobrą praktyką która dokumentuję porty na których aplikacja nasłuchuję.

Dodatkiem pomocnym podczas aktywnej pracy developerskiej jest plik compose.yaml, który automatycznie potrafi aktualizować edytowany serwis oraz odtworzyć lokalną infrastrukturę. W przypadku projektów python wymagane jest tylko montowanie odpowiednich wolumenów z plikami projektu.

Aby zbudować aplikację, należy wykonać komendę.

```bash
docker build . --tag chenliu
```

Oczywiście nazwa może się różnić. Uruchomienie aplikacji jest wykonywane poprzez komendę, jednocześnie wiążąc porty 8080 Hosta z portem 80 kontenera.

```bash
docker run -p 8080:80 chenliu
```

## Chmura obliczeniowa

W powyższy sposób aplikacja jest przygotowana do łatwego wdrożenia. Chmura obliczeniowa, umożliwa łatwe wdrożenie aplikacji i archiwizowanie zmian obrazów.

Projekt wykorzystuję usługi Google Cloud (GCP), lecz sposób wdrożenia jest podobny dla każdych popularnych dostawców usług chmurowych.

Pierwszym etapem jest stworzenie repozytorium dla stworzonych obrazów. Google cloud udostępnia usługę "Artifact Registry" gdzie stworzone jest standardowe repozytorium dla obrazów docker - `pzuchowski`.

Po utworzeniu rejestru możliwe jest wypychanie dowolnych obrazów aplikacji poprzez `docker push`

![Ręczne tworzenie repozytorium docker](./img/gcp-pzuchowski.png)

Uruchamianie instancji obrazu odbywa się poprzez usługę "Cloud Run". Cloud Run pozwala na uruchomienie instancji prywatnego repozytorium i wstępną konfigurację usługi.

Zaletą tego rozwiązanie jest odciążeniem dewelopera od zadań związanych z zarządzaniem aplikacją i ręcznym tworzeniem Load Balancerów dla aplikacji.

![Panel tworzenia usługi google Cloud Run](./img/gcp-cloud-run.png)


![GCP - Informacje z adresem URL usługi ](./img/gcp-app.png)

Usługa Cloud Run pozwala też na przeglądanie statystyk aplikacji i tworzenie alertów w przypadku naruszenia ustalonych reguł oraz przeglądania logów.

## Infrastruktura jako Kod

Rozwiązanie przedstawione powyżej spełnia swoje zadanie. Aplikacja została sukcesywnie wdrożona na gdzie możemy otrzymywać raporty z logów oraz alerty w razie niepowodzeń.

W dłuższej perspektywie i dalszych pracach nad projektami zaczyją pojawiać się problemy z automatyzacją czy dokuemntacją infrastruktury aplikacji.

Dlatego warto we czesnych etapach projektu zapisać utrwalić infrastrukturę w postaci kodu.
Przy użyciu narzędzia Terraform możliwe jest utrwalenie infrastruktury i bezpieczne przechowywanie w repozytorium Git.

Wdrożenie aplikacji z pomocą narzędzia Terraform wymaga pobrania klucza dostępu roli użytkownika i zintegrowanie z konfiguracją.

Wdrożenie definicja wdrożenia instancji składa się z definicji `google_cloud_run_v2_service` gdzie są zdefiniowane porty kontenera, lokalizację usługi czy ustawienia load balacingu.

Aby udostępnić instancję jako publiczne API wymagana jest konfiguracja IAM poprzez odpowiedni definicje `google_iam_policy` i połączenie w `google_cloud_run_v2_service_iam_policy`
\newpage

# Opis przeprowadzonych testów

W rozdziale dotyczącym testowania implementacji algorytmu skupia się na kluczowym aspekcie procesu tworzenia oprogramowania – zapewnieniu jakości poprzez systematyczne testowanie.
Testowanie implementacji algorytmu jest niezwykle istotne dla zapewnienia poprawnego działania systemu oraz oczekiwanych wyników.
Rozdział przedstawia szczegółowy plan testów, obejmujący cele, strategie, środowisko testowe oraz rodzaje testów, mając na celu zaprezentowanie kompleksowego podejścia do sprawdzania funkcjonalności algorytmu.

Poprzez analizę wyników testów oraz ocenę ich efektywności, będziemy starali się przedstawić wnioski i zidentyfikowali ewentualnych problemów w implementacji.


## Lokalne testy aplikacji

## Testy obciążeniowe wdrożenia

\newpage

# Bibliografia
