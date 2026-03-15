#!/bin/bash

DEST="$HOME/.ROSharp"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing RO-Sharp..."

if [ ! -f "$SCRIPT_DIR/interpretor.py" ]; then
    echo "EROARE: Nu gasesc interpretor.py langa acest script!"
    echo "Asigura-te ca install-linux-mac.sh si interpretor.py sunt in acelasi folder."
    exit 1
fi

# Creaza folderul daca nu exista
mkdir -p "$DEST"

# Copiaza interpretorul
cp "$SCRIPT_DIR/interpretor.py" "$DEST/interpretor.py"
echo "Interpretor copiat cu succes!"

# Copiaza iconita daca exista (pentru Linux cu suport .desktop)
if [ -f "$SCRIPT_DIR/ro-sharp.ico" ]; then
    cp "$SCRIPT_DIR/ro-sharp.ico" "$DEST/ro-sharp.ico"
    echo "Iconita copiata!"
fi

# Adauga aliasul in shellul potrivit
add_alias() {
    local RC_FILE="$1"
    if [ -f "$RC_FILE" ]; then
        if grep -q "alias rop=" "$RC_FILE"; then
            echo "Aliasul 'rop' exista deja in $RC_FILE."
        else
            echo "alias rop='python3 $DEST/interpretor.py'" >> "$RC_FILE"
            echo "Alias 'rop' adaugat in $RC_FILE."
        fi
    fi
}

add_alias "$HOME/.bashrc"
add_alias "$HOME/.zshrc"
add_alias "$HOME/.bash_profile"

echo ""
echo "===================================="
echo " Instalare completa!"
echo " Ruleaza: source ~/.bashrc"
echo " (sau redeschide terminalul)"
echo " apoi: rop fisier.rop"
echo "===================================="
