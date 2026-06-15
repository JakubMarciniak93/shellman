🌲 **dir_tree – Wyświetlanie struktury katalogów**

Rysuje strukturę folderów w formacie podobnym do `tree`.

#### Opcje
| opcja        | opis |
|--------------|------|
| `--files`    | pokaż także pliki |
| `--depth N`  | maksymalna głębokość zaglądania |
| `--output`   | zapisz wynik do pliku |
| `--hidden`   | uwzględnij ukryte pliki i foldery |
| `--ascii`    | użyj znaków ASCII zamiast linii Unicode |

#### Przykłady
shellman dir_tree .
shellman dir_tree . --files --depth 2# 🌲 dir_tree – Wyświetlanie struktury katalogów

Komenda `dir_tree` wyświetla strukturę katalogów w czytelnym formacie drzewa.

Może pokazywać same foldery albo foldery razem z plikami, ograniczać głębokość skanowania, wykluczać wybrane wzorce, uwzględniać ukryte elementy, używać znaków ASCII oraz zapisywać wynik do pliku tekstowego.

---

## 🔧 Opcje

| Opcja                             | Opis                                                                               |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| `--files`, `-f`                   | Pokazuje także pliki, nie tylko foldery                                            |
| `--depth N`, `-d N`               | Ogranicza głębokość skanowania, gdzie `0` oznacza tylko katalog główny             |
| `--output FILE`, `-o FILE`        | Zapisuje wynik do pliku tekstowego                                                 |
| `--hidden`, `-hd`                 | Uwzględnia ukryte pliki i foldery                                                  |
| `--exclude PATTERN`, `-x PATTERN` | Wyklucza pliki lub foldery pasujące do wzorca, np. `__pycache__`, `*.pyc`, `*.log` |
| `--ascii`, `-a`                   | Używa znaków ASCII zamiast linii Unicode                                           |
| `--lang-help pl/eng`              | Wyświetla rozszerzoną pomoc językową                                               |

---

## 📦 Przykłady

Pokaż tylko katalogi:
shellman dir_tree .

Pokaż katalogi i pliki:
shellman dir_tree . --files

Pokaż pliki i ogranicz głębokość do 2 poziomów:
shellman dir_tree . --files --depth 2

Użyj znaków ASCII:
shellman dir_tree . --files --ascii

Wyklucz cache i pliki logów:
shellman dir_tree . --files --exclude __pycache__ --exclude "*.log"

Zapisz wynik do pliku:
shellman dir_tree . --files --output struktura.txt

Wyświetl pomoc po angielsku:
shellman dir_tree --lang-help eng

shellman dir_tree . --output struktura.txt
