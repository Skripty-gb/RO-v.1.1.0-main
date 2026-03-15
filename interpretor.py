#!/usr/bin/env python3

import sys
import os
import shutil
import re
import random
from datetime import date, datetime

VERSIUNE = "2.0.0"
AUTOR = "Skripty-gb"
DESCRIERE = "RO-Sharp - Un limbaj de programare in limba romana"
ROP_FOLDER = os.path.join(os.path.expanduser("~"), ".ROSharp")


class ReturnException(Exception):
    def __init__(self, valoare=None):
        self.valoare = valoare

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

variabile = {}
functii = {}

def eval_expresie_matematica(expresie):
    def inlocuieste_var(match):
        var = match.group(0)
        if var in variabile:
            return str(variabile[var])
        return var
    expresie_eval = re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*', inlocuieste_var, expresie)
    try:
        rezultat = eval(expresie_eval, {"__builtins__": {}}, {})
        return rezultat
    except:
        return None

def eval_conditie(cond):
    cond = cond.strip()
    # Operatori logici: si, sau
    if " sau " in cond:
        parti = cond.split(" sau ", 1)
        return eval_conditie(parti[0]) or eval_conditie(parti[1])
    if " si " in cond:
        parti = cond.split(" si ", 1)
        return eval_conditie(parti[0]) and eval_conditie(parti[1])
    if cond.startswith("nu "):
        return not eval_conditie(cond[3:])
    # Conditie simpla
    parti = cond.split()
    if len(parti) == 3:
        stanga, operator, dreapta = parti
        stanga_val = variabile.get(stanga, stanga)
        dreapta_val = variabile.get(dreapta, dreapta)
        # Incearca comparatie numerica
        try:
            stanga_val = float(stanga_val)
            dreapta_val = float(dreapta_val)
        except:
            # Comparatie string
            return {
                "==": str(stanga_val) == str(dreapta_val),
                "!=": str(stanga_val) != str(dreapta_val),
            }.get(operator, False)
        return {
            ">": stanga_val > dreapta_val,
            "<": stanga_val < dreapta_val,
            "==": stanga_val == dreapta_val,
            "!=": stanga_val != dreapta_val,
            ">=": stanga_val >= dreapta_val,
            "<=": stanga_val <= dreapta_val
        }.get(operator, False)
    # Valoare singura (da/nu sau variabila)
    if len(parti) == 1:
        val = variabile.get(parti[0], parti[0])
        return val not in ["nu", "fals", "0", "", False, 0, None]
    return False


# ============ TKINTER GUI ============
_tk_root = None
_tk_frame = None
_tk_entries = {}

def gui_fereastra(linie):
    global _tk_root, _tk_frame
    try:
        import tkinter as tk
    except ImportError:
        print("EROARE: tkinter nu este disponibil! Instaleaza Python complet.")
        return
    try:
        titlu_match = re.search(r'"([^"]+)"', linie)
        latime_match = re.search(r'latime (\d+)', linie)
        inaltime_match = re.search(r'inaltime (\d+)', linie)
        titlu = titlu_match.group(1) if titlu_match else "RO-Sharp"
        latime = int(latime_match.group(1)) if latime_match else 400
        inaltime = int(inaltime_match.group(1)) if inaltime_match else 300
        _tk_root = tk.Tk()
        _tk_root.title(titlu)
        _tk_root.geometry(f"{latime}x{inaltime}")
        _tk_root.resizable(False, False)
        _tk_frame = tk.Frame(_tk_root, padx=15, pady=15)
        _tk_frame.pack(fill="both", expand=True)
    except Exception as e:
        print(f"EROARE: Nu pot deschide fereastra: {e}")

def gui_eticheta(text):
    import tkinter as tk
    val = text.strip('"')
    # Inlocuieste variabile
    for k, v in variabile.items():
        val = val.replace(k, str(v))
    lbl = tk.Label(_tk_frame, text=val, font=("Arial", 12))
    lbl.pack(pady=4, anchor="w")

def gui_buton(text):
    import tkinter as tk
    val = text.strip('"')
    def on_click():
        if val in functii:
            executa_functie(val, [])
        else:
            print(f"Buton apasat: {val}")
    btn = tk.Button(_tk_frame, text=val, command=on_click,
                    font=("Arial", 11), bg="#002B7F", fg="white",
                    activebackground="#CE1126", activeforeground="white",
                    relief="flat", padx=10, pady=5)
    btn.pack(pady=4, fill="x")

def gui_input_text(nume_var):
    import tkinter as tk
    row = tk.Frame(_tk_frame)
    row.pack(fill="x", pady=4)
    tk.Label(row, text=nume_var + ":", font=("Arial", 11)).pack(side="left", padx=(0,8))
    entry = tk.Entry(row, font=("Arial", 11), relief="solid", bd=1)
    entry.pack(side="left", fill="x", expand=True)
    def salveaza(*a):
        variabile[nume_var] = entry.get()
    entry.bind("<KeyRelease>", salveaza)
    _tk_entries[nume_var] = entry


def gui_titlu_mare(text):
    try:
        import tkinter as tk
        val = text.strip('"')
        for k, v in variabile.items():
            val = val.replace(k, str(v))
        lbl = tk.Label(_tk_frame, text=val, font=("Arial", 20, "bold"))
        lbl.pack(pady=8, anchor="w")
    except Exception as e:
        print(f"EROARE titlu_mare: {e}")

def gui_culoare_fundal(culoare):
    try:
        culoare = culoare.strip('"')
        if _tk_root:
            _tk_root.configure(bg=culoare)
        if _tk_frame:
            _tk_frame.configure(bg=culoare)
    except Exception as e:
        print(f"EROARE culoare_fundal: {e}")

def gui_imagine(cale):
    try:
        import tkinter as tk
        from PIL import Image, ImageTk
        cale = cale.strip('"')
        img = Image.open(cale)
        img = img.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(_tk_frame, image=photo)
        lbl.image = photo
        lbl.pack(pady=8)
    except ImportError:
        try:
            import tkinter as tk
            photo = tk.PhotoImage(file=cale.strip('"'))
            lbl = tk.Label(_tk_frame, image=photo)
            lbl.image = photo
            lbl.pack(pady=8)
        except Exception as e:
            print(f"EROARE imagine: {e}")
    except Exception as e:
        print(f"EROARE imagine: {e}")

def gui_mesaj(text):
    try:
        import tkinter.messagebox as mb
        val = text.strip('"')
        for k, v in variabile.items():
            val = val.replace(k, str(v))
        mb.showinfo("RO-Sharp", val)
    except Exception as e:
        print(f"EROARE mesaj: {e}")

def gui_porneste():
    if _tk_root:
        _tk_root.mainloop()

def interpreteaza(linie):
    # Ignora comentarii
    if linie.startswith("//"):
        return
    if linie.startswith("scrie lista "):
        lista_var = linie[12:].strip()
        if lista_var in variabile and isinstance(variabile[lista_var], list):
            print("[" + ", ".join(str(v) for v in variabile[lista_var]) + "]")
    elif linie.startswith("scrie "):
        expresie = linie[6:].strip()
        parti = re.split(r'\+(?=(?:[^"]*"[^"]*")*[^"]*$)', expresie)
        rezultat = ""
        for p in parti:
            p = p.strip()
            if p.startswith('"') and p.endswith('"'):
                rezultat += p[1:-1]
            elif p in variabile:
                rezultat += str(variabile[p])
            else:
                val = eval_expresie_matematica(p)
                if val is not None:
                    rezultat += str(val)
                else:
                    rezultat += p
        print(rezultat)
    elif linie.startswith("seteaza "):
        parti = linie.split(" la ")
        if len(parti) == 2:
            nume = parti[0].replace("seteaza", "").strip()
            valoare = parti[1].strip()
            if valoare.startswith('"') and valoare.endswith('"'):
                variabile[nume] = valoare[1:-1]
            elif valoare.isdigit():
                variabile[nume] = int(valoare)
            elif valoare in variabile:
                variabile[nume] = variabile[valoare]
            elif valoare.startswith("transforma_nr(") and valoare.endswith(")"):
                arg = valoare[14:-1].strip()
                val = str(variabile.get(arg, arg)).strip('"')
                try:
                    variabile[nume] = int(val)
                except:
                    try:
                        variabile[nume] = float(val)
                    except:
                        raise ValueError(f"Nu pot converti '{val}' la numar")
            elif valoare.startswith("transforma_text(") and valoare.endswith(")"):
                arg = valoare[16:-1].strip()
                val = variabile.get(arg, arg)
                variabile[nume] = str(val)
            else:
                if valoare.startswith("lungime(") and valoare.endswith(")"):
                    arg = valoare[8:-1].strip()
                    arg_val = variabile.get(arg, arg)
                    variabile[nume] = len(arg_val) if isinstance(arg_val, list) else len(str(arg_val).strip('"'))
                elif valoare.startswith("random(") and valoare.endswith(")"):
                    args = valoare[7:-1].split(",")
                    min_v = int(variabile.get(args[0].strip(), args[0].strip()))
                    max_v = int(variabile.get(args[1].strip(), args[1].strip()))
                    variabile[nume] = random.randint(min_v, max_v)
                elif valoare == "data_azi()":
                    variabile[nume] = str(date.today())
                elif valoare == "ora_acum()":
                    variabile[nume] = datetime.now().strftime("%H:%M:%S")
                elif valoare.startswith("majuscule(") and valoare.endswith(")"):
                    arg = valoare[10:-1].strip()
                    variabile[nume] = str(variabile.get(arg, arg)).upper()
                elif valoare.startswith("minuscule(") and valoare.endswith(")"):
                    arg = valoare[10:-1].strip()
                    variabile[nume] = str(variabile.get(arg, arg)).lower()
                elif valoare.startswith("taie(") and valoare.endswith(")"):
                    args = valoare[5:-1].split(",")
                    src = str(variabile.get(args[0].strip(), args[0].strip().strip('"')))
                    start = int(variabile.get(args[1].strip(), args[1].strip()))
                    end = int(variabile.get(args[2].strip(), args[2].strip())) if len(args) > 2 else len(src)
                    variabile[nume] = src[start:end]
                elif valoare.startswith("contine(") and valoare.endswith(")"):
                    args = valoare[8:-1].split(",", 1)
                    lista_obj = variabile.get(args[0].strip(), [])
                    search = args[1].strip().strip('"') if len(args) > 1 else ""
                    variabile[nume] = "da" if search in [str(x) for x in lista_obj] else "nu"
                elif "[" in valoare and valoare.endswith("]"):
                    lista_var = valoare[:valoare.index("[")]
                    idx_str = valoare[valoare.index("[")+1:-1].strip()
                    idx = int(variabile.get(idx_str, idx_str))
                    if lista_var in variabile and isinstance(variabile[lista_var], list):
                        variabile[nume] = variabile[lista_var][idx]
                elif "(" in valoare and valoare.endswith(")"):
                    nume_f = valoare.split("(", 1)[0].strip()
                    args_str = valoare.split("(", 1)[1][:-1]
                    args_f = [a.strip() for a in args_str.split(",") if a.strip()]
                    if nume_f in functii:
                        rez = executa_functie(nume_f, args_f)
                        if rez is not None:
                            variabile[nume] = rez
                    else:
                        rezultat_mat = eval_expresie_matematica(valoare)
                        if rezultat_mat is not None:
                            variabile[nume] = rezultat_mat
                else:
                    rezultat_mat = eval_expresie_matematica(valoare)
                    if rezultat_mat is not None:
                        variabile[nume] = rezultat_mat
    elif linie.startswith("## linie"):
        print("-" * 40)
    elif linie.startswith("intreaba "):
        parti = linie.replace("intreaba", "").strip().split(" cu ")
        if len(parti) == 2:
            nume_var = parti[0].strip()
            mesaj = parti[1].strip().strip('"')
            variabile[nume_var] = input(mesaj + " ")
    elif linie.strip() == "opreste_bucla":
        raise BreakException()
    elif linie.strip() == "continua":
        raise ContinueException()

    # ============ LUNGIME ============
    elif linie.startswith("seteaza ") and "lungime(" in linie:
        parti = linie.split(" la ", 1)
        if len(parti) == 2:
            nume = parti[0].replace("seteaza", "").strip()
            val_str = parti[1].strip()
            if val_str.startswith("lungime(") and val_str.endswith(")"):
                arg = val_str[8:-1].strip()
                arg_val = variabile.get(arg, arg)
                if isinstance(arg_val, list):
                    variabile[nume] = len(arg_val)
                else:
                    variabile[nume] = len(str(arg_val).strip('"'))

    # ============ ACCES LISTA[i] ============
    elif linie.startswith("seteaza ") and "[" in linie and "]" in linie and " la " in linie:
        parti = linie.split(" la ", 1)
        nume = parti[0].replace("seteaza", "").strip()
        val_str = parti[1].strip()
        if "[" in val_str and val_str.endswith("]"):
            lista_var = val_str[:val_str.index("[")]
            idx_str = val_str[val_str.index("[")+1:-1].strip()
            idx = int(variabile.get(idx_str, idx_str))
            if lista_var in variabile and isinstance(variabile[lista_var], list):
                variabile[nume] = variabile[lista_var][idx]

    # ============ SETEAZA lista[i] la valoare ============
    elif linie.startswith("seteaza ") and "[" in linie and "]" in linie and " la " in linie and linie.index("[") < linie.index(" la "):
        m = re.match(r'seteaza (\w+)\[(.+?)\] la (.+)', linie)
        if m:
            lista_var = m.group(1).strip()
            idx_str = m.group(2).strip()
            val_str = m.group(3).strip()
            idx = int(variabile.get(idx_str, idx_str))
            if val_str.startswith('"') and val_str.endswith('"'):
                val = val_str[1:-1]
            else:
                val = variabile.get(val_str, eval_expresie_matematica(val_str) or val_str)
            if lista_var in variabile and isinstance(variabile[lista_var], list):
                variabile[lista_var][idx] = val

    # ============ PENTRU element IN lista ============
    # handled in interpreteaza_bloc

    # ============ CONTINE ============
    elif linie.startswith("seteaza ") and "contine(" in linie:
        parti = linie.split(" la ", 1)
        if len(parti) == 2:
            nume = parti[0].replace("seteaza", "").strip()
            val_str = parti[1].strip()
            if val_str.startswith("contine(") and val_str.endswith(")"):
                args = val_str[8:-1].split(",", 1)
                lista_var = args[0].strip()
                search_val = args[1].strip().strip('"') if len(args) > 1 else ""
                lista_obj = variabile.get(lista_var, [])
                variabile[nume] = "da" if search_val in [str(x) for x in lista_obj] else "nu"

    # ============ RANDOM ============
    elif linie.startswith("seteaza ") and "random(" in linie:
        parti = linie.split(" la ", 1)
        if len(parti) == 2:
            nume = parti[0].replace("seteaza", "").strip()
            val_str = parti[1].strip()
            if val_str.startswith("random(") and val_str.endswith(")"):
                args = val_str[7:-1].split(",")
                min_v = int(variabile.get(args[0].strip(), args[0].strip()))
                max_v = int(variabile.get(args[1].strip(), args[1].strip()))
                variabile[nume] = random.randint(min_v, max_v)

    # ============ DATA / ORA ============
    elif linie.startswith("seteaza ") and "data_azi()" in linie:
        parti = linie.split(" la ", 1)
        nume = parti[0].replace("seteaza", "").strip()
        variabile[nume] = str(date.today())
    elif linie.startswith("seteaza ") and "ora_acum()" in linie:
        parti = linie.split(" la ", 1)
        nume = parti[0].replace("seteaza", "").strip()
        variabile[nume] = datetime.now().strftime("%H:%M:%S")

    # ============ STRING OPS ============
    elif linie.startswith("seteaza ") and "majuscule(" in linie:
        parti = linie.split(" la ", 1)
        if len(parti) == 2:
            nume = parti[0].replace("seteaza", "").strip()
            arg = parti[1].strip()[10:-1].strip()
            variabile[nume] = str(variabile.get(arg, arg)).upper()
    elif linie.startswith("seteaza ") and "minuscule(" in linie:
        parti = linie.split(" la ", 1)
        if len(parti) == 2:
            nume = parti[0].replace("seteaza", "").strip()
            arg = parti[1].strip()[10:-1].strip()
            variabile[nume] = str(variabile.get(arg, arg)).lower()
    elif linie.startswith("seteaza ") and "taie(" in linie:
        parti = linie.split(" la ", 1)
        if len(parti) == 2:
            nume = parti[0].replace("seteaza", "").strip()
            val_str = parti[1].strip()
            if val_str.startswith("taie(") and val_str.endswith(")"):
                args = val_str[5:-1].split(",")
                src = str(variabile.get(args[0].strip(), args[0].strip().strip('"')))
                start = int(variabile.get(args[1].strip(), args[1].strip()))
                end = int(variabile.get(args[2].strip(), args[2].strip())) if len(args) > 2 else len(src)
                variabile[nume] = src[start:end]

    # ============ INCLUDE ============
    elif linie.startswith("include "):
        cale = linie[8:].strip().strip('"')
        try:
            with open(cale, 'r', encoding='utf-8') as f:
                linii_inc = f.readlines()
            interpreteaza_bloc(linii_inc, 0)
        except Exception as e:
            print(f"EROARE include: {e}")

    # ============ INCEARCA / DACA_EROARE ============
    # handled in interpreteaza_bloc

    elif linie.startswith("citeste_fisier "):
        cale = linie[15:].strip().strip('"')
        try:
            with open(cale, 'r', encoding='utf-8') as f:
                variabile["_fisier"] = f.read()
            scrie_val = variabile["_fisier"]
            print(scrie_val)
        except Exception as e:
            print(f"EROARE citire fisier: {e}")
    elif linie.startswith("citeste_fisier ") and " in " in linie:
        parti = linie[15:].split(" in ")
        cale = parti[0].strip().strip('"')
        var = parti[1].strip()
        try:
            with open(cale, 'r', encoding='utf-8') as f:
                variabile[var] = f.read()
        except Exception as e:
            print(f"EROARE citire fisier: {e}")
    elif linie.startswith("scrie_fisier ") and " cu " in linie:
        parti = linie[13:].split(" cu ", 1)
        cale = parti[0].strip().strip('"')
        continut_var = parti[1].strip()
        if continut_var.startswith('"') and continut_var.endswith('"'):
            continut = continut_var[1:-1]
        else:
            continut = str(variabile.get(continut_var, continut_var))
        try:
            with open(cale, 'w', encoding='utf-8') as f:
                f.write(continut)
            print(f"Fisier '{cale}' salvat!")
        except Exception as e:
            print(f"EROARE scriere fisier: {e}")
    elif linie.startswith("seteaza ") and " la lista[" in linie:
        # seteaza x la lista[0]
        parti = linie.split(" la lista[", 1)
        nume = parti[0].replace("seteaza", "").strip()
        rest = parti[1]
        lista_nume, idx_str = rest.split("]", 1)[0].rsplit(",", 1) if "," in rest.split("]")[0] else (rest.split("]")[0], rest.split("]")[0])
        # simpler: seteaza x la lista[varname, index]
        inner = rest.split("]")[0]
        if "," in inner:
            lista_var, idx = inner.split(",", 1)
            lista_var = lista_var.strip()
            idx = int(str(variabile.get(idx.strip(), idx.strip())))
            if lista_var in variabile and isinstance(variabile[lista_var], list):
                variabile[nume] = variabile[lista_var][idx]
    elif linie.startswith("adauga ") and " la lista " in linie:
        # adauga valoare la lista numeLista
        parti = linie[7:].split(" la lista ", 1)
        val_str = parti[0].strip()
        lista_var = parti[1].strip()
        if val_str.startswith('"') and val_str.endswith('"'):
            val = val_str[1:-1]
        else:
            val = variabile.get(val_str, val_str)
        if lista_var not in variabile or not isinstance(variabile[lista_var], list):
            variabile[lista_var] = []
        variabile[lista_var].append(val)
    elif linie.startswith("lista ") and " = []" in linie:
        # lista numeLista = []
        lista_var = linie[6:].split("=")[0].strip()
        variabile[lista_var] = []

    elif linie.startswith("returneaza "):
        expr = linie[10:].strip()
        if expr.startswith('"') and expr.endswith('"'):
            raise ReturnException(expr[1:-1])
        elif expr in variabile:
            raise ReturnException(variabile[expr])
        else:
            val = eval_expresie_matematica(expr)
            raise ReturnException(val if val is not None else expr)
    elif linie.strip() == "returneaza":
        raise ReturnException(None)
    elif linie.startswith("fereastra "):
        gui_fereastra(linie)
    elif linie.startswith("eticheta "):
        gui_eticheta(linie[9:].strip())
    elif linie.startswith("buton "):
        gui_buton(linie[6:].strip())
    elif linie.startswith("input_text "):
        gui_input_text(linie[11:].strip())
    elif linie.startswith("titlu_mare "):
        gui_titlu_mare(linie[11:].strip())
    elif linie.startswith("culoare_fundal "):
        gui_culoare_fundal(linie[15:].strip())
    elif linie.startswith("imagine "):
        gui_imagine(linie[8:].strip())
    elif linie.startswith("mesaj(") and linie.endswith(")"):
        gui_mesaj(linie[6:-1].strip())
    elif linie.strip() == "porneste":
        gui_porneste()
    elif "(" in linie and linie.endswith(")"):
        nume, args_str = linie.split("(", 1)
        nume = nume.strip()
        args = [a.strip() for a in args_str[:-1].split(",")]
        executa_functie(nume, args)

def extrage_bloc_stop(linii, start_index):
    bloc = []
    i = start_index
    adancime = 0
    while i < len(linii):
        linie = linii[i].strip()
        if (linie.startswith("daca ") and " atunci" in linie) or \
           (linie.startswith("cat timp ") and linie.endswith(" executa")) or \
           (linie.startswith("pentru ") and " de la " in linie and " la " in linie) or \
           linie.startswith("functie "):
            adancime += 1
        elif linie == "stop":
            if adancime == 0:
                return bloc, i
            adancime -= 1
        bloc.append(linie)
        i += 1
    return bloc, i

def interpreteaza_bloc(linii, start_index):
    i = start_index
    while i < len(linii):
        linie = linii[i].strip()
        if linie == "stop":
            return i
        elif linie.startswith("//"):
            pass
        elif linie.startswith("functie "):
            i = defineste_functie(linii, i)
        elif linie.startswith("daca ") and " atunci" in linie:
            i = interpreteaza_conditional(linii, i)
        elif linie.startswith("cat timp ") and linie.endswith(" executa"):
            i = interpreteaza_cat_timp(linii, i)
        elif linie.startswith("pentru ") and " de la " in linie and " la " in linie:
            i = interpreteaza_pentru(linii, i)
        elif linie.startswith("pentru ") and " in " in linie:
            i = interpreteaza_pentru_in(linii, i)
        elif linie.startswith("incearca"):
            i = interpreteaza_incearca(linii, i)
        else:
            try:
                interpreteaza(linie)
            except (ReturnException, BreakException, ContinueException):
                raise
        i += 1
    return i


def interpreteaza_pentru_in(linii, index):
    """pentru element in lista"""
    linie = linii[index].strip()
    parti = linie.replace("pentru ", "").split(" in ", 1)
    var = parti[0].strip()
    lista_var = parti[1].strip()
    lista_obj = variabile.get(lista_var, [])
    if not isinstance(lista_obj, list):
        lista_obj = list(str(lista_obj))
    bloc, end_index = extrage_bloc_stop(linii, index + 1)
    for val in lista_obj:
        variabile[var] = val
        try:
            interpreteaza_bloc(bloc, 0)
        except BreakException:
            break
        except ContinueException:
            continue
        except ReturnException:
            raise
    return end_index

def interpreteaza_incearca(linii, index):
    """incearca ... daca_eroare ... stop"""
    bloc_incearca = []
    bloc_eroare = []
    i = index + 1
    in_eroare = False
    adancime = 0
    while i < len(linii):
        linie = linii[i].strip()
        if linie == "incearca":
            adancime += 1
        elif linie == "daca_eroare" and adancime == 0:
            in_eroare = True
        elif linie == "stop" and adancime == 0:
            break
        elif linie == "stop":
            adancime -= 1
        if not in_eroare:
            bloc_incearca.append(linie)
        else:
            if linie != "daca_eroare":
                bloc_eroare.append(linie)
        i += 1
    try:
        interpreteaza_bloc(bloc_incearca, 0)
    except Exception as e:
        variabile["_eroare"] = str(e)
        if bloc_eroare:
            interpreteaza_bloc(bloc_eroare, 0)
    return i

def interpreteaza_cat_timp(linii, index):
    linie = linii[index].strip()
    conditie = linie.replace("cat timp", "").replace("executa", "").strip()
    bloc, end_index = extrage_bloc_stop(linii, index + 1)
    limita = 0
    while eval_conditie(conditie):
        try:
            interpreteaza_bloc(bloc, 0)
        except BreakException:
            break
        except ContinueException:
            pass
        except ReturnException:
            raise
        limita += 1
        if limita > 10000:
            print("EROARE: Bucla infinita detectata (>10000 iteratii)")
            break
    return end_index

def interpreteaza_pentru(linii, index):
    linie = linii[index].strip()
    try:
        rest = linie.replace("pentru ", "")
        var, rest2 = rest.split(" de la ")
        var = var.strip()
        start_str, end_str = rest2.split(" la ")
        start_val = int(variabile.get(start_str.strip(), start_str.strip()))
        end_val = int(variabile.get(end_str.strip(), end_str.strip()))
    except:
        return index
    bloc, end_index = extrage_bloc_stop(linii, index + 1)
    for val in range(start_val, end_val + 1):
        variabile[var] = val
        try:
            interpreteaza_bloc(bloc, 0)
        except BreakException:
            break
        except ContinueException:
            continue
        except ReturnException:
            raise
    return end_index

def defineste_functie(linii, index):
    linie = linii[index].strip()
    linie = linie.replace("functie", "").strip()
    nume = linie.split("(")[0].strip()
    parametri = linie.split("(")[1].split(")")[0].split(",")
    parametri = [p.strip() for p in parametri if p.strip()]
    corp = []
    i = index + 1
    adancime = 0
    while i < len(linii):
        linie_corp = linii[i].strip()
        # Blocuri care deschid un nivel nou
        if (linie_corp.startswith("daca ") and " atunci" in linie_corp) or            (linie_corp.startswith("cat timp ") and linie_corp.endswith(" executa")) or            (linie_corp.startswith("pentru ") and (" de la " in linie_corp or " in " in linie_corp)) or            linie_corp.startswith("incearca") or            linie_corp.startswith("functie "):
            adancime += 1
        elif linie_corp == "stop":
            if adancime == 0:
                break
            adancime -= 1
        corp.append(linie_corp)
        i += 1
    functii[nume] = (parametri, corp)
    return i

def executa_functie(nume, args):
    global variabile
    if nume not in functii:
        return
    parametri, corp = functii[nume]
    args = [a for a in args if a.strip()]
    if len(parametri) != len(args):
        return
    local_vars = {}
    for i in range(len(parametri)):
        arg = args[i]
        if arg.startswith('"') and arg.endswith('"'):
            valoare = arg[1:-1]
        elif arg in variabile:
            valoare = variabile[arg]
        else:
            valoare = arg
        local_vars[parametri[i]] = valoare
    variabile_backup = variabile.copy()
    variabile.update(local_vars)
    rezultat_return = None
    try:
        interpreteaza_bloc(corp, 0)
    except ReturnException as r:
        rezultat_return = r.valoare
    variabile = variabile_backup
    return rezultat_return

def extrage_bloc_conditional(linii, start_index):
    """Extrage un bloc dintr-un conditional (daca/altfeldaca/altfel),
    tinand cont de blocuri imbricate. Se opreste la altfel/altfeldaca/stop de la nivelul curent."""
    bloc = []
    i = start_index
    adancime = 0
    while i < len(linii):
        linie = linii[i].strip()
        if (linie.startswith("daca ") and " atunci" in linie) or \
           (linie.startswith("cat timp ") and linie.endswith(" executa")) or \
           (linie.startswith("pentru ") and " de la " in linie and " la " in linie) or \
           linie.startswith("functie "):
            adancime += 1
        elif adancime == 0 and (linie == "stop" or linie == "altfel" or linie.startswith("altfeldaca ")):
            return bloc, i
        elif linie == "stop":
            adancime -= 1
        bloc.append(linie)
        i += 1
    return bloc, i

def interpreteaza_conditional(linii, index):
    conditii = []
    i = index
    while i < len(linii):
        linie = linii[i].strip()
        if linie.startswith("daca ") and " atunci" in linie:
            tip = "daca"
            conditie = linie.replace("daca", "").replace("atunci", "").strip()
        elif linie.startswith("altfeldaca ") and " atunci" in linie:
            tip = "altfeldaca"
            conditie = linie.replace("altfeldaca", "").replace("atunci", "").strip()
        elif linie == "altfel":
            tip = "altfel"
            conditie = None
        elif linie == "stop":
            break
        else:
            i += 1
            continue
        bloc, i = extrage_bloc_conditional(linii, i + 1)
        conditii.append((tip, conditie, bloc))
    executat = False
    for tip, conditie, bloc in conditii:
        if tip in ["daca", "altfeldaca"] and eval_conditie(conditie) and not executat:
            try:
                interpreteaza_bloc(bloc, 0)
            except (ReturnException, BreakException, ContinueException):
                raise
            executat = True
        elif tip == "altfel" and not executat:
            try:
                interpreteaza_bloc(bloc, 0)
            except (ReturnException, BreakException, ContinueException):
                raise
            break
    return i

def interpreteaza_fisier(cale_fisier):
    if not os.path.isfile(cale_fisier):
        print(f"EROARE: Fisierul '{cale_fisier}' nu exista!")
        return
    with open(cale_fisier, 'r', encoding='utf-8') as f:
        linii = f.readlines()
    interpreteaza_bloc(linii, 0)

def cmd_ver():
    print(f"RO-Sharp v{VERSIUNE}")

def cmd_help():
    print(f"""
RO-Sharp v{VERSIUNE} - Ajutor

  Utilizare:
    rop <fisier.rop>        Executa un program RO-Sharp
    rop --ver               Afiseaza versiunea
    rop --help              Afiseaza acest mesaj
    rop --about             Informatii despre RO-Sharp
    rop --new <fisier.rop>  Creeaza un fisier .rop nou cu exemplu
    rop --delete-rop        Dezinstaleaza RO-Sharp complet

  Comenzi disponibile in limbaj:
    scrie "text"                Afiseaza text
    seteaza x la 10             Seteaza o variabila
    seteaza x la y + 5          Operatii matematice (+, -, *, /, **)
    intreaba x cu "text"        Citeste input de la utilizator
    daca x > 5 atunci           Conditie (if)
    altfeldaca x == 5 atunci    Conditie alternativa (else if)
    altfel                      Altfel (else)
    cat timp x < 10 executa     Bucla while
    pentru i de la 1 la 10      Bucla for
    functie nume(param)         Defineste o functie
    stop                        Incheie un bloc
    // comentariu               Linie de comentariu
    ## linie                    Afiseaza separator

  Exemple:
    rop program.rop
    rop --new proiect.rop
""")

def cmd_about():
    print(f"""
  {DESCRIERE}
  Versiune : {VERSIUNE}
  Autor    : {AUTOR}
  Limbaj   : Python
  Extensie : .rop

  RO-Sharp este un limbaj de programare interpretat,
  conceput pentru a putea scrie cod in limba romana.
  Sursa: https://github.com/Skripty-gb/RO-Sharp
""")

def cmd_new(nume_fisier):
    if not nume_fisier.endswith(".rop"):
        nume_fisier += ".rop"
    if os.path.exists(nume_fisier):
        print(f"EROARE: Fisierul '{nume_fisier}' exista deja!")
        return
    continut = f'// Fisier: {nume_fisier}\n// Creat cu RO-Sharp v{VERSIUNE}\n\nscrie "Salut, lume!"\n'
    with open(nume_fisier, 'w', encoding='utf-8') as f:
        f.write(continut)
    print(f"Fisier '{nume_fisier}' creat cu succes!")

def cmd_delete_rop():
    print("Esti sigur ca vrei sa dezinstalezi RO-Sharp? (da/nu)")
    raspuns = input("> ").strip().lower()
    if raspuns != "da":
        print("Dezinstalare anulata.")
        return
    print("Dezinstalare in curs...")
    # Sterge folderul principal
    if os.path.exists(ROP_FOLDER):
        shutil.rmtree(ROP_FOLDER)
        print(f"Folder '{ROP_FOLDER}' sters.")
    else:
        print("Folderul de instalare nu a fost gasit.")
    # Mesaj pentru curatare manuala registry pe Windows
    if sys.platform == "win32":
        print("""
  Pentru a finaliza dezinstalarea pe Windows:
  1. Deschide Command Prompt ca Administrator si ruleaza:
       reg delete \"HKCU\\Software\\Classes\\.rop\" /f
       reg delete \"HKCU\\Software\\Classes\\ROSharp.File\" /f
  2. Sau ruleaza fisierul uninstall-windows.bat daca il ai.
        """)
    print("RO-Sharp a fost dezinstalat. La revedere!")

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        print(f"RO-Sharp v{VERSIUNE} - Utilizare: rop <fisier.rop> | rop --help")
    elif args[0] == "--ver":
        cmd_ver()
    elif args[0] == "--help":
        cmd_help()
    elif args[0] == "--about":
        cmd_about()
    elif args[0] == "--new":
        if len(args) < 2:
            print("Utilizare: rop --new <nume_fisier.rop>")
        else:
            cmd_new(args[1])
    elif args[0] == "--delete-rop":
        cmd_delete_rop()
    elif args[0].startswith("--"):
        print(f"Comanda necunoscuta: '{args[0]}'. Scrie 'rop --help' pentru ajutor.")
    else:
        interpreteaza_fisier(args[0])
