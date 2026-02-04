In Unity, una **Layer Mask** è essenzialmente un filtro. Immaginala come un paio di occhiali selettivi che permettono a una luce, a una telecamera o a un raggio (Raycast) di "vedere" solo determinati oggetti nel mondo di gioco, ignorando completamente gli altri.

Tecnicamente, una Layer Mask è un intero a 32 bit, dove ogni singolo bit rappresenta uno dei 32 layer disponibili in Unity.

---

## 1. Come funziona: Il Bitmasking

In Unity, ogni oggetto appartiene a un **Layer** (es. Layer 0: Default, Layer 8: Player, Layer 9: Enemy). Per gestire questi layer in modo efficiente, Unity usa la logica binaria.

* Ogni bit dell'intero rappresenta un layer.
* Se il bit è `1`, il layer è "attivo" o selezionato.
* Se il bit è `0`, il layer è ignorato.

### Analogia: L'interruttore della luce

Pensa a una stanza con 32 lampadine diverse. Una Layer Mask è un pannello con 32 interruttori. Se vuoi che il tuo Raycast colpisca solo i nemici, "accendi" solo l'interruttore corrispondente al layer dei nemici. Anche se il raggio attraversa un muro (Layer "Wall"), se l'interruttore del muro è spento nella tua maschera, il raggio passerà attraverso come se il muro fosse invisibile.

---

## 2. Applicazioni comuni in Unity

### A. Raycasting (Il caso più frequente)

Quando lanci un raggio, spesso non vuoi che colpisca tutto. Se il Player spara, il raggio non deve colpire il Player stesso, ma solo i nemici o l'ambiente.

```csharp
// Definizione tramite inspector (best practice per manutenibilità)
public LayerMask enemyLayer; 

void Update() {
    if (Physics.Raycast(transform.position, transform.forward, out RaycastHit hit, 10f, enemyLayer)) {
        // Colpirà SOLO gli oggetti nel layer specificato
        Debug.Log("Ho colpito un nemico!");
    }
}

```

### B. Camera Culling Mask

Ogni telecamera ha una proprietà **Culling Mask**. Questa decide quali oggetti renderizzare.

* **Esempio:** Puoi avere una telecamera che renderizza tutto tranne l'interfaccia utente (UI), e una seconda telecamera "Overlay" che renderizza solo la UI.

### C. Luci e Collisioni

Le luci possono illuminare solo certi layer, e la **Collision Matrix** (nelle impostazioni del Physics Engine) definisce quali layer possono scontrarsi fisicamente tra loro.

---

## 3. Best Practices e Performance

1. **Usa l'Inspector:** Non scrivere i numeri dei layer direttamente nel codice (es. `layer 8`). Usa `public LayerMask myMask;`. Questo ti permette di selezionare i layer tramite un comodo menu a tendina nell'Editor di Unity, rendendo il codice **manutenibile** e meno propenso a errori.
2. **Performance:** Operare con le Layer Mask è estremamente veloce perché si basa su operazioni bit a bit (Bitwise operations), che la CPU esegue quasi istantaneamente. È molto più performante che controllare il tag di ogni oggetto colpito (`if (hit.collider.tag == "Enemy")`).

---

### Esercizio di ragionamento

Immagina di voler creare un sistema in cui il giocatore può vedere oggetti segreti (Layer "Hidden") solo quando indossa degli occhiali speciali.

1. **Cosa succederebbe se** invece di usare le Layer Mask usassi `gameObject.SetActive(true/false)` su tutti gli oggetti segreti ogni volta che metti gli occhiali? Quali sarebbero i problemi di performance in una scena con 1000 oggetti?
2. **Come pensi che questo si applichi al tuo progetto?** Hai una situazione in cui un raggio o una telecamera devono ignorare certi oggetti?

**Vuoi che approfondisca questo argomento?**
C'è qualche aspetto specifico su cui vuoi maggiori dettagli? Potremmo esplorare:

* **Operazioni Bitwise:** Come manipolare le maschere via codice (operatori `<<`, `|`, `~`).
* **Collision Matrix:** Come ottimizzare la fisica del gioco usando i layer.
* **Camera Stack:** Gestire più telecamere con Culling Mask diverse per effetti avanzati.

---

In Unity, sebbene i nomi siano simili, **Layer Mask** e **Sorting Layer** servono a scopi completamente diversi: uno riguarda la **logica/fisica**, l'altro la **visualizzazione 2D**.

Ecco la differenza fondamentale:

### 1. Layer (e Layer Mask)

* **Scopo:** Logica e interazione.
* **Cosa controllano:** Chi collide con chi, cosa vede una telecamera e cosa colpisce un Raycast.
* **Utilizzo:** Si usano principalmente per la fisica 3D/2D e per ottimizzare il rendering (Culling Mask). 
Il Culling Mask in Unity è una funzionalità della Camera che permette di scegliere selettivamente quali Layer (livelli) di oggetti renderizzare, attivando o disattivando la visualizzazione via bitmask.
* **Esempio:** "Il proiettile deve ignorare il giocatore (Layer: Player) ma colpire il nemico (Layer: Enemy)".

### 2. Sorting Layer

* **Scopo:** Ordine di visualizzazione (Rendering).
* **Cosa controllano:** L'ordine con cui gli oggetti vengono disegnati sullo schermo, ovvero chi appare "sopra" e chi "sotto".
* **Utilizzo:** Sono essenziali nel **2D** (Sprite, UI). Non influenzano le collisioni o i Raycast.
* **Esempio:** "Voglio che l'albero (Sorting Layer: Background) sia sempre disegnato dietro al personaggio (Sorting Layer: Foreground)", anche se hanno la stessa coordinata Z.

---

### Analogie a confronto

* **Layer Mask:** È come decidere quali persone possono parlare tra loro in una stanza. È una questione di **interazione**.
* **Sorting Layer:** È come decidere l'ordine dei fogli di carta in una pila. È una questione di **visibilità**.

---

### Analisi tecnica e Best Practices

1. **Indipendenza:** Un oggetto può appartenere al Layer "Player" (per la fisica) e contemporaneamente essere nel Sorting Layer "Heroes" (per il rendering). Sono due sistemi paralleli.
2. **Performance:** Usare i Sorting Layer correttamente evita il "Z-fighting" (sfarfallio tra sprite alla stessa profondità) senza dover spostare gli oggetti avanti e indietro sull'asse Z, il che è più pulito per il workflow 2D.
3. **Sorting Order:** All'interno dello stesso Sorting Layer, puoi usare il valore "Order in Layer" (un numero intero) per un controllo ancora più granulare (es. Order 1 è sopra Order 0).

---

