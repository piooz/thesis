# Cel i zakres pracy
Celem pracy dyplomowej jest stworzenie implementacji algorytmu wykrywania wyjątków i poprawy dopasowania modelu.
Dodatkowym zadaniem poza zaimplementowaniem algorytmu jest stworzenie publicznej usługi internetowej która umożliwi analizę przesłanych danych. Usługa internetowa pozwoli na stworzenie abstrakcji nad zaimplementowanym algorytmem, dzięki czemu projekt może zostać zintegrowany z dowolną aplikacją lub innym serwisem
obsługujący zwykłą komunikację http. 

Implementacja zarówno biblioteki algorytmu jak i serwisu ma zostać wykonana technologi Python. 

Implementacja algorytmu powinna być wydajna lub porównywalna z innymi podobnymi algorytmami. Ponieważ algorytm zaproponowany przez Chen i Liu rozwiązuję problemy z detekcją wyjątków, określeniem typu wyjątku, sprawdzeniem wpływu na model szeregu czasowego i ostateczna poprawa modelu dopuszczalne
jest aby czas obliczeń był dłuższy on innych.

Usługa internetowa musi być dostępna nieprzerwanie, dlatego celem niefunkcjonalnym jest stworzenie usługi wykorzystując usługi chmurowe. Wdrożenie w chmurze będzie wiązało dodatkowymi przygotowaniami aplikacji. Dzięki cze
