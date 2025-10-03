# Tris al Contrario — Flip + Passa-Punto (2 giocatori umani)
# Regole chiave:
# - Ogni giocatore alterna il simbolo tra X e O a ogni propria mossa (Flip-per-Giocatore).
# - Se completi un tris nel tuo turno, il punto va all'AVVERSARIO (Passa-Punto).
# - Si gioca a round; perde chi raggiunge per primo 3 punti.

def stampa_griglia(g):
    def cell(i):
        return g[i] if g[i] != " " else str(i+1)
    print(f"\n {cell(0)} | {cell(1)} | {cell(2)}")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)}")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)}\n")

LINEE = [(0,1,2),(3,4,5),(6,7,8),
         (0,3,6),(1,4,7),(2,5,8),
         (0,4,8),(2,4,6)]

def tris_fatto(g, sym):
    i = 0
    while i < len(LINEE):
        a,b,c = LINEE[i]
        if g[a] == sym and g[b] == sym and g[c] == sym:
            return True
        i += 1
    return False

def round_tris_al_contrario(starter):
    # starter: "A" oppure "B"
    griglia = [" "] * 9
    giocatore = starter
    # Il simbolo "iniziale" per round: starter usa X, l'altro usa O
    prossimo_simbolo = {"A": "X" if starter == "A" else "O",
                        "B": "O" if starter == "A" else "X"}

    mosse_fatte = 0
    vincitore_passa_punto = None  # "A" o "B" che riceverà il punto (l'avversario di chi chiude)

    while True:
        stampa_griglia(griglia)
        sym = prossimo_simbolo[giocatore]

        # input posizione
        scelta_valida = False
        while not scelta_valida:
            try:
                s = input(f"Giocatore {giocatore} (simbolo {sym}) - scegli una casella [1-9]: ").strip()
                pos = int(s) - 1
                if 0 <= pos <= 8 and griglia[pos] == " ":
                    scelta_valida = True
                else:
                    print("Mossa non valida. Riprova.")
            except:
                print("Inserisci un numero da 1 a 9.")

        # piazza
        griglia[pos] = sym
        mosse_fatte += 1

        # check tris (se fai tris, punto all'AVVERSARIO)
        if tris_fatto(griglia, sym):
            avversario = "A" if giocatore == "B" else "B"
            vincitore_passa_punto = avversario
            stampa_griglia(griglia)
            print(f"Tris completato da {giocatore} con '{sym}' → Punto PASSATO a {avversario}!")
            break

        # pareggio (board piena)
        if mosse_fatte == 9:
            stampa_griglia(griglia)
            print("Nessun tris: round patta (0 punti).")
            break

        # flip simbolo per il prossimo turno di QUEL giocatore
        prossimo_simbolo[giocatore] = "O" if sym == "X" else "X"

        # passa turno
        giocatore = "A" if giocatore == "B" else "B"

    # ritorna chi ha ricevuto il punto (None se patta)
    return vincitore_passa_punto

def partita(max_punti=3):
    punteggio = {"A": 0, "B": 0}
    starter = "A"  # alterna lo starter a ogni round per equità

    while True:
        print(f"\n=== Nuovo round (Starter: {starter}) | Punti: A={punteggio['A']}  B={punteggio['B']} ===")
        assegnato = round_tris_al_contrario(starter)
        if assegnato is not None:
            punteggio[assegnato] += 1
            print(f"Punto assegnato a {assegnato}. Punteggio: A={punteggio['A']}  B={punteggio['B']}")

        # check fine partita (perde chi arriva a max_punti)
        if punteggio["A"] >= max_punti:
            print("\nFine partita: A ha raggiunto il limite. Vince B.")
            break
        if punteggio["B"] >= max_punti:
            print("\nFine partita: B ha raggiunto il limite. Vince A.")
            break

        # alterna starter e chiedi se continuare
        starter = "A" if starter == "B" else "B"
        cont = input("Continuare? [Invio=si / n=no] ").strip().lower()
        if cont == "n":
            print("Partita terminata.")
            break

if __name__ == "__main__":
    partita(max_punti=3)