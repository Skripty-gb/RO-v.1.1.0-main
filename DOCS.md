# Documentatie RO-Sharp

**Bun venit in documentatia oficiala a limbajului RO-Sharp!**

---

## Cuprins

1. [Sintaxa Limbajului](#sintaxa-limbajului)
2. [Functii Built-in](#functii-built-in)
3. [GUI Tkinter](#gui-tkinter)
4. [Exemple](#exemple)


## Sintaxa Limbajului

### Comentarii
```rop
// Acesta este un comentariu
scrie "Salut!"
```

### Output
```rop
scrie "Salut, lume!"
scrie x
scrie "Valoarea: " + x
```

### Variabile
```rop
seteaza x la 10
seteaza nume la "Ion"
seteaza y la x + 5
```

### Matematica

| Operator | Descriere |
|---|---|
| `+` | Adunare |
| `-` | Scadere |
| `*` | Inmultire |
| `/` | Impartire |
| `**` | Putere |

### Input
```rop
intreaba nume cu "Cum te cheama?"
scrie "Salut, " + nume
```

### Conditii
```rop
daca x > 10 atunci
    scrie "mare"
altfeldaca x == 10 atunci
    scrie "exact 10"
altfel
    scrie "mic"
stop
```

Operatori de comparatie: `>` `<` `==` `!=` `>=` `<=`

Operatori logici: `si`, `sau`, `nu`

```rop
daca x > 5 si x < 20 atunci
    scrie "intre 5 si 20"
stop
```

### Bucle

#### Bucla For
```rop
pentru i de la 1 la 10
    scrie i
stop
```

#### Bucla For-In
```rop
pentru element in lista
    scrie element
stop
```

#### Bucla While
```rop
cat timp x < 10 executa
    seteaza x la x + 1
stop
```

#### Oprire si Continuare
```rop
opreste_bucla   // iese din bucla (break)
continua        // sare la urmatoarea iteratie (continue)
```

### Functii
```rop
functie salut(nume)
    scrie "Salut, " + nume
stop

salut("Ion")

// Cu valoare returnata
functie aduna(a, b)
    returneaza a + b
stop

seteaza total la aduna(5, 3)
```

### Liste
```rop
lista fructe = []
adauga "mar" la lista fructe
adauga "para" la lista fructe
scrie lista fructe
seteaza primul la fructe[0]
seteaza n la lungime(fructe)
seteaza gasit la contine(fructe, "mar")
seteaza _ la sterge(fructe, 0)
```

### Fisiere
```rop
scrie_fisier "date.txt" cu "continut"
citeste_fisier "date.txt"
seteaza ex la exista_fisier("date.txt")
sterge_fisier "date.txt"
redenumeste_fisier "vechi.txt" in "nou.txt"
```

### Sistem
```rop
seteaza out la ruleaza("echo salut")
scrie out
ruleaza "clear"
```

### Gestionare Erori
```rop
incearca
    seteaza n la transforma_nr("abc")
daca_eroare
    scrie "Eroare: " + _eroare
stop
```

### Include
```rop
include "alt_fisier.rop"
```

---

## Functii Built-in

### Conversii
| Functie | Descriere |
|---|---|
| `transforma_nr(x)` | Converteste string la numar |
| `transforma_text(x)` | Converteste numar la string |
| `tip(x)` | Returneaza tipul: `"numar"`, `"text"`, `"lista"` |

### String
| Functie | Descriere |
|---|---|
| `lungime(x)` | Lungimea stringului sau listei |
| `majuscule(x)` | Transforma in majuscule |
| `minuscule(x)` | Transforma in minuscule |
| `taie(x, start, end)` | Extrage o portiune din string |
| `inlocuieste(x, vechi, nou)` | Inlocuieste text |
| `imparte(x, separator)` | Imparte string in lista |

### Matematica si Date
| Functie | Descriere |
|---|---|
| `random(min, max)` | Numar intreg aleator |
| `data_azi()` | Data curenta |
| `ora_acum()` | Ora curenta |

---

## GUI Tkinter

### Comenzi

| Comanda | Descriere |
|---|---|
| `fereastra "titlu" latime W inaltime H` | Creeaza fereastra |
| `eticheta "text"` | Adauga text |
| `titlu_mare "text"` | Titlu bold mare |
| `buton "text"` | Adauga buton |
| `input_text variabila` | Camp de text |
| `culoare_fundal "#hex"` | Culoarea fondului |
| `imagine "fisier.png"` | Afiseaza imagine |
| `mesaj("text")` | Popup de mesaj |
| `separator_gui` | Linie orizontala |
| `progres variabila max 100` | Bara de progres |
| `checkbox variabila "text"` | Bifa on/off |
| `lista_dropdown var optiuni "A","B","C"` | Dropdown |
| `porneste` | Deschide fereastra |

### Exemplu
```rop
fereastra "Aplicatia mea" latime 400 inaltime 300
culoare_fundal "#1a1a2e"
titlu_mare "Bun venit!"
eticheta "Scrie numele tau:"
input_text nume
checkbox sunet "Activeaza sunet"
lista_dropdown culoare optiuni "Rosu","Verde","Albastru"
buton "Trimite"
porneste
```

---

## Exemple

### Factorial
```rop
functie factorial(n)
    daca n <= 1 atunci
        returneaza 1
    stop
    returneaza n * factorial(n - 1)
stop

seteaza f la factorial(5)
scrie "5! = " + f
```

### Suma 1 la 100
```rop
seteaza suma la 0
pentru i de la 1 la 100
    seteaza suma la suma + i
stop
scrie "Suma = " + suma
```

### Joc ghiceste numarul
```rop
seteaza secret la random(1, 100)
seteaza incercari la 0

cat timp incercari < 10 executa
    seteaza incercari la incercari + 1
    intreaba ghici cu "Ghiceste:"
    seteaza nr la transforma_nr(ghici)
    daca nr == secret atunci
        scrie "Ai ghicit in " + incercari + " incercari!"
        opreste_bucla
    altfeldaca nr < secret atunci
        scrie "Prea mic!"
    altfel
        scrie "Prea mare!"
    stop
stop
```

---

*RO-Sharp v2.0.0 — https://github.com/Skripty-gb/RO-Sharp*
