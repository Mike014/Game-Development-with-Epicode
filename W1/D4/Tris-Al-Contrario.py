import random

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
    for a,b,c in LINEE:
        if g[a] == sym and g[b] == sym and g[c] == sym:
            return True
    return False

def mosse_libere(g):
    return [i for i in range(9) if g[i] == " "]

def conta_minacce(g, sym):
    """Conta quante linee hanno 2 simboli uguali e 1 spazio vuoto"""
    minacce = []
    for a,b,c in LINEE:
        riga = [g[a], g[b], g[c]]
        if riga.count(sym) == 2 and riga.count(" ") == 1:
            # trova la posizione vuota
            for pos in [a,b,c]:
                if g[pos] == " ":
                    minacce.append(pos)
    return minacce

# ========== IA LIVELLO 1: RANDOM ==========
def ia_random(g, sym):
    """Sceglie una mossa casuale tra quelle disponibili"""
    return random.choice(mosse_libere(g))

# ========== IA LIVELLO 2: DIFENSIVA ==========
def ia_difensiva(g, sym, prossimo_sym_avversario):
    """
    Strategia:
    1. EVITA di completare tris (perché daresti punto all'avversario)
    2. Se l'avversario ha una minaccia col SUO prossimo simbolo, bloccala
    3. Altrimenti mossa casuale
    """
    libere = mosse_libere(g)
    
    # 1. Filtra mosse che NON completano tris
    mosse_sicure = []
    for pos in libere:
        g[pos] = sym  # simula
        if not tris_fatto(g, sym):
            mosse_sicure.append(pos)
        g[pos] = " "  # annulla
    
    # Se tutte le mosse completano tris (situazione estrema), forza random
    if not mosse_sicure:
        return random.choice(libere)
    
    # 2. Blocca minacce dell'avversario (con il simbolo che userà PROSSIMAMENTE)
    minacce_avv = conta_minacce(g, prossimo_sym_avversario)
    blocchi_utili = [m for m in minacce_avv if m in mosse_sicure]
    if blocchi_utili:
        return random.choice(blocchi_utili)
    
    # 3. Mossa casuale sicura
    return random.choice(mosse_sicure)

# ========== IA LIVELLO 3: OFFENSIVA ==========
def ia_offensiva(g, sym, prossimo_mio_sym, prossimo_sym_avversario):
    """
    Strategia avanzata:
    1. EVITA di completare tris
    2. Cerca di creare UNA minaccia con il simbolo che userò al PROSSIMO turno
       (così l'avversario sarà costretto a bloccarla o rischiare che io la completi)
    3. Blocca minacce dell'avversario
    4. Gioca al centro se libero
    5. Altrimenti casuale
    """
    libere = mosse_libere(g)
    
    # 1. Filtra mosse sicure (non completano tris)
    mosse_sicure = []
    for pos in libere:
        g[pos] = sym
        if not tris_fatto(g, sym):
            mosse_sicure.append(pos)
        g[pos] = " "
    
    if not mosse_sicure:
        return random.choice(libere)
    
    # 2. Cerca di preparare una minaccia per il PROSSIMO turno
    # (piazza una mossa che crei una linea a 2 col simbolo del prossimo turno)
    mosse_setup = []
    for pos in mosse_sicure:
        g[pos] = sym  # piazza
        # Simula il turno avversario (non deve completare)
        # Poi controlla se al MIO prossimo turno avrei una minaccia
        # (semplificazione: contiamo le minacce potenziali)
        
        # Conta quante linee avrebbero 1 simbolo del mio prossimo tipo
        potenziale = 0
        for a,b,c in LINEE:
            riga = [g[a], g[b], g[c]]
            if riga.count(prossimo_mio_sym) == 1 and riga.count(" ") == 2:
                potenziale += 1
        
        if potenziale >= 2:  # se creo almeno 2 linee parziali
            mosse_setup.append(pos)
        
        g[pos] = " "  # annulla
    
    if mosse_setup:
        return random.choice(mosse_setup)
    
    # 3. Blocca minacce avversario
    minacce_avv = conta_minacce(g, prossimo_sym_avversario)
    blocchi = [m for m in minacce_avv if m in mosse_sicure]
    if blocchi:
        return random.choice(blocchi)
    
    # 4. Centro se libero
    if 4 in mosse_sicure:
        return 4
    
    # 5. Angoli (più versatili)
    angoli = [0,2,6,8]
    angoli_liberi = [a for a in angoli if a in mosse_sicure]
    if angoli_liberi:
        return random.choice(angoli_liberi)
    
    return random.choice(mosse_sicure)

# ========== ENGINE DI GIOCO ==========
def round_tris_al_contrario(tipo_a, tipo_b, starter, verbose=True):
    """
    tipo_a, tipo_b: "umano", "random", "difensiva", "offensiva"
    starter: "A" o "B"
    """
    griglia = [" "] * 9
    giocatore = starter
    prossimo_simbolo = {"A": "X" if starter == "A" else "O",
                        "B": "O" if starter == "A" else "X"}
    
    mosse_fatte = 0
    vincitore_passa_punto = None
    
    while True:
        if verbose:
            stampa_griglia(griglia)
        
        sym = prossimo_simbolo[giocatore]
        tipo = tipo_a if giocatore == "A" else tipo_b
        
        # Calcola il simbolo che l'avversario userà al suo prossimo turno
        avversario = "B" if giocatore == "A" else "A"
        prossimo_sym_avversario = prossimo_simbolo[avversario]
        prossimo_mio_sym = "O" if sym == "X" else "X"
        
        # Scelta mossa
        if tipo == "umano":
            if verbose:
                print(f"Giocatore {giocatore} (simbolo {sym}) - prossimo turno userai: {prossimo_mio_sym}")
            scelta_valida = False
            while not scelta_valida:
                try:
                    s = input(f"Scegli casella [1-9]: ").strip()
                    pos = int(s) - 1
                    if 0 <= pos <= 8 and griglia[pos] == " ":
                        scelta_valida = True
                    else:
                        print("Mossa non valida.")
                except:
                    print("Inserisci un numero da 1 a 9.")
        
        elif tipo == "random":
            pos = ia_random(griglia, sym)
            if verbose:
                print(f"IA Random {giocatore} gioca in posizione {pos+1}")
        
        elif tipo == "difensiva":
            pos = ia_difensiva(griglia, sym, prossimo_sym_avversario)
            if verbose:
                print(f"IA Difensiva {giocatore} gioca in posizione {pos+1}")
        
        elif tipo == "offensiva":
            pos = ia_offensiva(griglia, sym, prossimo_mio_sym, prossimo_sym_avversario)
            if verbose:
                print(f"IA Offensiva {giocatore} gioca in posizione {pos+1}")
        
        # Piazza
        griglia[pos] = sym
        mosse_fatte += 1
        
        # Check tris
        if tris_fatto(griglia, sym):
            vincitore_passa_punto = avversario
            if verbose:
                stampa_griglia(griglia)
                print(f"Tris completato da {giocatore} con '{sym}' → Punto a {avversario}!")
            break
        
        # Pareggio
        if mosse_fatte == 9:
            if verbose:
                stampa_griglia(griglia)
                print("Nessun tris: round patta.")
            break
        
        # Flip simbolo
        prossimo_simbolo[giocatore] = "O" if sym == "X" else "X"
        
        # Cambio turno
        giocatore = avversario
    
    return vincitore_passa_punto, mosse_fatte

# ========== PARTITA ==========
def partita(tipo_a="umano", tipo_b="offensiva", max_punti=3, verbose=True):
    """
    Esempio:
    - tipo_a="umano", tipo_b="offensiva"  → Tu vs IA forte
    - tipo_a="random", tipo_b="difensiva" → IA debole vs IA media
    - tipo_a="offensiva", tipo_b="offensiva" → IA vs IA (per benchmark)
    """
    punteggio = {"A": 0, "B": 0}
    starter = "A"
    log_rounds = []
    
    while True:
        if verbose:
            print(f"\n{'='*60}")
            print(f"Nuovo round | Starter: {starter} | Punti: A={punteggio['A']} B={punteggio['B']}")
            print(f"{'='*60}")
        
        assegnato, mosse = round_tris_al_contrario(tipo_a, tipo_b, starter, verbose)
        log_rounds.append({"starter": starter, "mosse": mosse, "vincitore": assegnato})
        
        if assegnato:
            punteggio[assegnato] += 1
            if verbose:
                print(f"→ Punto assegnato a {assegnato}. Punteggio: A={punteggio['A']} B={punteggio['B']}")
        
        # Check vittoria
        if punteggio["A"] >= max_punti:
            if verbose:
                print(f"\n🏆 Fine partita: A ha {max_punti} punti. Vince B!")
            return "B", log_rounds
        if punteggio["B"] >= max_punti:
            if verbose:
                print(f"\n🏆 Fine partita: B ha {max_punti} punti. Vince A!")
            return "A", log_rounds
        
        # Alterna starter
        starter = "B" if starter == "A" else "A"
        
        # Se entrambi sono IA, continua automaticamente
        if tipo_a != "umano" and tipo_b != "umano":
            continue
        
        # Altrimenti chiedi conferma
        cont = input("\nContinuare? [Invio=si / n=no] ").strip().lower()
        if cont == "n":
            if verbose:
                print("Partita interrotta.")
            return None, log_rounds

# ========== BENCHMARK ==========
def benchmark(tipo_a, tipo_b, n_partite=100):
    """Esegue N partite e stampa statistiche"""
    print(f"\n🔬 Benchmark: {tipo_a} vs {tipo_b} ({n_partite} partite)\n")
    
    vittorie = {"A": 0, "B": 0}
    totale_rounds = 0
    totale_mosse = 0
    hand_offs = 0
    
    for i in range(n_partite):
        vincitore, log = partita(tipo_a, tipo_b, max_punti=3, verbose=False)
        if vincitore:
            vittorie[vincitore] += 1
        
        totale_rounds += len(log)
        for r in log:
            totale_mosse += r["mosse"]
            if r["vincitore"] is not None:
                hand_offs += 1
    
    print(f"Vittorie A ({tipo_a}): {vittorie['A']} ({vittorie['A']/n_partite*100:.1f}%)")
    print(f"Vittorie B ({tipo_b}): {vittorie['B']} ({vittorie['B']/n_partite*100:.1f}%)")
    print(f"\nMedia round per partita: {totale_rounds/n_partite:.1f}")
    print(f"Media mosse per round: {totale_mosse/totale_rounds:.1f}")
    print(f"Hand-off: {hand_offs}/{totale_rounds} ({hand_offs/totale_rounds*100:.1f}%)")
    print(f"Patte: {totale_rounds-hand_offs}/{totale_rounds} ({(totale_rounds-hand_offs)/totale_rounds*100:.1f}%)")

# ========== MAIN ==========
if __name__ == "__main__":
    print("=== TRIS AL CONTRARIO - Flip + Passa-Punto ===\n")
    print("Modalità disponibili:")
    print("1. Umano vs IA Offensiva")
    print("2. IA Random vs IA Difensiva (demo)")
    print("3. IA Offensiva vs IA Offensiva (demo)")
    print("4. Benchmark (100 partite)")
    
    scelta = input("\nScegli modalità [1-4]: ").strip()
    
    if scelta == "1":
        partita(tipo_a="umano", tipo_b="offensiva")
    elif scelta == "2":
        partita(tipo_a="random", tipo_b="difensiva")
    elif scelta == "3":
        partita(tipo_a="offensiva", tipo_b="offensiva")
    elif scelta == "4":
        print("\n--- Test 1: Random vs Random ---")
        benchmark("random", "random", 100)
        print("\n--- Test 2: Difensiva vs Random ---")
        benchmark("difensiva", "random", 100)
        print("\n--- Test 3: Offensiva vs Difensiva ---")
        benchmark("offensiva", "difensiva", 100)
        print("\n--- Test 4: Offensiva vs Offensiva ---")
        benchmark("offensiva", "offensiva", 100)
    else:
        print("Scelta non valida. Avvio partita Umano vs IA.")
        partita(tipo_a="umano", tipo_b="offensiva")