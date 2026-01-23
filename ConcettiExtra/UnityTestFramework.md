### 1. Le Fondamenta: Assembly Definitions (.asmdef)

Questo è il sistema con cui organizzi "fisicamente" il tuo codice per renderlo modulare.

* **Il Problema:** Di base, Unity compila *tutto* il codice in un unico blocco. Se modifichi una riga, ricompila tutto (lento) e il codice di test è mischiato a quello di gioco (sporco).
* **La Soluzione:** Usare i file `.asmdef` per dividere il codice in "moduli" separati (Assembly).
* **Vantaggi:**
* **Velocità:** Modificando un modulo (es. i Test), Unity ricompila solo quello, non tutto il gioco.
* **Dipendenze:** Definisci chi vede chi. I Test vedono il Gioco, ma il Gioco non vede i Test.
* **Build Pulita:** Puoi escludere il codice di test dalla versione finale del gioco (Build) facilmente.

### 2. Lo Strumento: Unity Test Framework (UTF)

È il pacchetto integrato (basato sulla libreria *NUnit*) per scrivere ed eseguire test automatizzati.

#### A. Le Tipologie di Test

Il framework distingue nettamente due ambienti:

| Caratteristica | **Edit Mode Tests** | **Play Mode Tests** |
| --- | --- | --- |
| **Dove gira** | Nell'Editor di Unity (senza premere Play). | Nella scena di gioco (come se premessi Play). |
| **Velocità** | Molto veloce. | Più lento (simula il tempo reale). |
| **Cosa testare** | Logica pura (es. calcolo danni), Algoritmi, Tool dell'Editor. | Fisica, Movimento, Coroutines, Spawn di oggetti. |
| **Configurazione** | L'assembly deve avere `IncludePlatforms: Editor`. | L'assembly deve referenziare gli script di gioco. |

#### B. Il Flusso di Lavoro (Workflow)

Per impostare un ambiente di test corretto, devi seguire questi step:

1. **Installazione:** Assicurarsi che il pacchetto *Test Framework* sia installato dal Package Manager.
2. **Creazione Assembly:**
* Creare una cartella `Tests`.
* Usare il **Test Runner** per generare automaticamente la cartella e il file `.asmdef` corretto.
* **Importante:** Nel `.asmdef` dei Test, devi aggiungere un riferimento (Reference) all'Assembly dei tuoi script di gioco, altrimenti i test non "vedranno" le tue classi.

3. **Scrittura ed Esecuzione:**
* Creare lo script di test (C#).
* Aprire il **Test Runner Window** per vedere l'albero dei test.
* Eseguire (`Run All` o `Run Selected`).

#### C. Dettagli Tecnici Importanti

* **Attributi:** Si usa `[Test]` (standard NUnit) per test immediati e `[UnityTest]` per test che richiedono coroutines (es. "aspetta 1 secondo e controlla se il nemico è morto").
* **Piattaforme:** Puoi lanciare i *Play Mode Tests* anche su un dispositivo reale (es. Android/iOS) usando "Run all in player".
* **Build:** È buona pratica disabilitare i test runner nelle impostazioni di progetto prima di fare la build finale per evitare errori o file inutili.

---

