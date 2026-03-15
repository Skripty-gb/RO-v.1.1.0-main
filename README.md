# RO-Sharp 🇷🇴

**RO-Sharp** este un limbaj de programare simplu, scris in limba romana. Fisierele au extensia `.rop` si sunt interpretate in Python.

```rop
// Primul tau program in RO-Sharp
scrie "Salut, lume!"

seteaza x la 10
daca x > 5 atunci
    scrie "x este mare!"
stop
```

---

## Sintaxa

### Output & Variabile
```rop
scrie "Hello, World!"
seteaza x la 42
scrie "Valoarea este: " + x
intreaba nume cu "Cum te cheama?"
```

### Operatii Matematice
```rop
seteaza y la x * 2 + 5
seteaza p la x ** 2
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

### Bucle
```rop
pentru i de la 1 la 10
    scrie i
stop

cat timp x < 100 executa
    seteaza x la x * 2
stop
```

### Functii
```rop
functie salut(nume)
    scrie "Salut, " + nume
stop

salut("Ion")
```

### Liste
```rop
lista fructe = []
adauga "mar" la lista fructe
adauga "para" la lista fructe
pentru f in fructe
    scrie f
stop
```

### Fisiere
```rop
scrie_fisier "date.txt" cu "continut"
citeste_fisier "date.txt"
seteaza ex la exista_fisier("date.txt")
```

### GUI (Tkinter)
```rop
fereastra "Aplicatia mea" latime 400 inaltime 300
titlu_mare "Bun venit!"
eticheta "Scrie numele tau:"
input_text nume
buton "Trimite"
porniste
```

### Gestionare Erori
```rop
incearca
    seteaza n la transforma_nr("abc")
daca_eroare
    scrie "Eroare: " + _eroare
stop
```

---

## Extensie VS Code

Extensia adauga syntax highlighting si rulare directa pentru fisierele `.rop`.

**Instalare:**
```bash
unzip ro-sharp-vscode.zip
cp -r ro-sharp-vscode ~/.vscode/extensions/ro-sharp
```

Dupa repornirea VS Code, apasa **F5** pe orice fisier `.rop` pentru a-l rula.

> Vezi [INSTRUCTIUNI.md](INSTRUCTIUNI.md) pentru mai multe detalii.

---

## Versiune

**v2.0.0** — Vezi [DOCS.md](DOCS.md) pentru documentatie completa.

---

*Facut cu ❤️ de [Skripty-gb](https://github.com/Skripty-gb)*
