# Programowanie dla analityki danych
**Przemysław Oneksiak s34225,  Krzysztof Piórkowski s34226**

Projekt ma na celu analizę rynku wtórnego konsol do gier, w szczególności predykcji ich ceny. Dane zebrane na cele projektu
pochodziły z ogłoszeń wystawionych na stronie:  
https://www.ebay.com/

Ogłoszenia pochodziły z okresu od września do grudnia zeszłego roku (2024). Pobrane dane zawierały informacje takie jak:
Tytył ogłoszenia, cena przedmiotu, data sprzedaży, model produktu, nazwa producenta, nazwa oraz oceny sprzedawcy itp. Dane
zostały pobrane z wykorzystaniem biblioteki scrapy. Pobranych zostało blisko 200 000 produktów z 
wcześniej wspomnianego okresu. Nieprzetworzony plik znajduje się w lokalizacji **\notebooks\raw**.  

Dane zostały poddane przetworzeniu, transformacji oraz kodowaniu zmiennych. Trzy wersje przetworzenego pliku znajdują się
w lokalizacji **\notebooks\cleaned**. Jeden z nich jest używany do wykresów (_full_cleaned.csv), jeden został przygotowany przy
pomocy transformacji danych kategorycznych na numeryczne przy użyciu biblioteki **category_encoders** (_encoded.csv). Ostatni zawiera 
wyselekcjonowane atrybuty (_dropped.csv). 

Na ich podstawie zbudowane zostały trzy modele regresyjne, służące do przewidywania wyników zmiennej ceny:   
1. Model regresji liniowej: **\notebooks\models\LinearRegression.ipynb** - z wykorzystaniem bibliotek statsmodels oraz sklearn
2. Drzewo decyzyjne regrysjne: **\notebooks\models\DecisionTree.ipynb** - z wykorzysaniem biblioteki sklearn
3. Model Ensemble: **\notebooks\models\EnsembleModel.ipynb** - z wykorzysaniem biblioteki sklearn oraz klasy VotingRegressor

Wszystkie modele zostały trenowane zarówno na zbiorze z usuniętymi kolumnami (_dropped.csv), jak i na tym z 
kolumnami zakodowanymi (_encoded.csv).

Szczegółowa wizualizacja danych, zarówno po czyszczeniu jak i już po modelowaniu, zawarta została w pliku 
**\notebooks\data_visualization.ipynb**. Wykresy generowane z biblioteki **plotly** zostały umieszczoene w katalogu
**\notebooks\graphs**, z uwagi na brak możliwości ich podglądu przez githuba - niemniej wszystko znadjuje się również w 
głównym notebooku do wizualizacji **\notebooks\data_visualization.ipynb**.


Dane Techniczne:  
W celu poprania zależnych paczek uruchomić komendę: **pip install -r requirements.txt**  
W celu pobrania danych ze strony ebay: **scrapy crawl eBaySpider -o output_ebayspidercat_2.csv** bądź uruchomić kod znajdujący się bezpośrednio w pliku **\services\eBaySpiderCat.py**