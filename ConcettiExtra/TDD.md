Il **TDD**, ovvero **Test-Driven Development** (Sviluppo Guidato dai Test), è una metodologia di programmazione in cui il processo di sviluppo viene letteralmente "guidato" dai test.

Invece di scrivere il codice e poi testarlo per vedere se funziona (approccio tradizionale), con il TDD **scrivi il test prima ancora di scrivere il codice della funzionalità.**

### Il Ciclo "Red-Green-Refactor"

Il TDD si basa su un ciclo ripetitivo molto veloce, spesso paragonato a un mantra:

1. 🔴 **RED (Fallimento):** Scrivi un test per una piccola funzionalità che vuoi implementare. Esegui il test: deve fallire (perché non hai ancora scritto il codice).
2. 🟢 **GREEN (Successo):** Scrivi la quantità **minima** di codice necessaria per far passare il test. Non deve essere perfetto, deve solo funzionare.
3. 🔵 **REFACTOR (Ottimizzazione):** Ora che il test è "verde", pulisci il codice, migliora l'architettura e rimuovi le duplicazioni, avendo la certezza che il test ti avviserà se rompi qualcosa.

> [!TIP]
> **L'analogia della serratura:**
> Immagina di voler costruire una serratura. Invece di fabbricare prima la serratura e poi sperare che una chiave funzioni, il TDD ti dice: **"Prendi prima la chiave (il test) e poi modella la serratura finché la chiave non gira perfettamente."**


### Perché è così potente in Unity?

Spesso in Unity si tende a scrivere codice "spaghetti" dentro l'Unity `Update`, rendendo tutto difficile da testare. Il TDD ti obbliga a:

* **Pensare prima di scrivere:** Devi sapere esattamente cosa deve fare una funzione prima di toccare i tasti.
* **Disaccoppiare il codice:** Se una funzione è troppo legata a Unity (es. usa `Input` o `Physics` direttamente), sarà quasi impossibile scrivere un test semplice. Il TDD ti spinge a separare la logica pura dalle dipendenze del motore.

---

