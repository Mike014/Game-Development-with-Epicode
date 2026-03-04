# UnityEngine.Debug — Tutti i Metodi Spiegati

---

## LOGGING BASE

### `Debug.Log`
```csharp
Debug.Log("Messaggio");
Debug.Log("Messaggio", this); // context = evidenzia l'oggetto in Hierarchy
```
Stampa un messaggio informativo nella Console. L'icona è bianca/grigia. Il secondo parametro `context` è prezioso: cliccando il messaggio in Console, Unity seleziona automaticamente l'oggetto nella Hierarchy.

---

### `Debug.LogWarning`
```csharp
Debug.LogWarning("Attenzione: valore fuori range");
```
Stampa con icona gialla. Non blocca l'esecuzione — segnala una situazione anomala ma non fatale. Usalo quando qualcosa funziona ma in modo inatteso.

---

### `Debug.LogError`
```csharp
Debug.LogError("Componente mancante!");
```
Stampa con icona rossa. Se in Console hai attivo **Error Pause**, il Play Mode si mette in pausa automaticamente. Usalo per condizioni che non dovrebbero mai verificarsi.

---

### `Debug.LogException`
```csharp
try { /* codice pericoloso */ }
catch (Exception e)
{
    Debug.LogException(e, this);
}
```
Stampa un'eccezione C# nella Console con stack trace completo. Diverso da `LogError` perché accetta un oggetto `Exception` tipizzato, non una stringa.

---

## LOGGING CON FORMATO

### `Debug.LogFormat`
```csharp
Debug.LogFormat("Pos: {0}, Rot: {1}", transform.position, transform.rotation);
```
Equivalente a `string.Format` + `Debug.Log`. Più efficiente della concatenazione con `+` perché la stringa viene costruita solo se il logging è attivo. Preferibile in Update() se il log è condizionale.

---

### `Debug.LogWarningFormat` / `Debug.LogErrorFormat`
```csharp
Debug.LogWarningFormat("HP: {0} sotto soglia minima {1}", currentHp, minHp);
Debug.LogErrorFormat("GameObject {0} non trovato nella scena", targetName);
```
Stessa logica di `LogFormat` ma con icona gialla o rossa rispettivamente.

---

## ASSERZIONI

### `Debug.Assert`
```csharp
Debug.Assert(speed > 0, "La velocità non può essere negativa");
Debug.Assert(_controller != null, "CharacterController mancante", this);
```
Verifica una condizione. Se è `false`, stampa un messaggio di errore con `LogType.Assert`. **Cruciale:** le Assert vengono **strippate automaticamente** nelle build release — zero overhead in produzione. Usale liberamente per validare precondizioni.

---

### `Debug.AssertFormat`
```csharp
Debug.AssertFormat(_audioSource != null, "AudioSource mancante su {0}", gameObject.name);
```
Come `Assert` ma con stringa formattata. Stesso comportamento — rimossa nelle build release.

---

## VISUALIZZAZIONE NELLA SCENE VIEW

### `Debug.DrawLine`
```csharp
// Disegna una linea da A a B, visibile nella Scene view
Debug.DrawLine(transform.position, target.position, Color.red);

// Con durata — rimane visibile per 2 secondi anche se non è in Update
Debug.DrawLine(transform.position, target.position, Color.red, 2f);

// depthTest = false → visibile anche attraverso la geometria
Debug.DrawLine(transform.position, target.position, Color.red, 0f, false);
```
Disegna una linea tra due punti nel mondo 3D, visibile **solo nella Scene view** (non nel Game view). Utilissimo per visualizzare distanze, connessioni tra oggetti, range.

---

### `Debug.DrawRay`
```csharp
// Disegna un raggio da un punto in una direzione
Debug.DrawRay(transform.position, transform.forward * 10f, Color.green);

// Caso d'uso classico: visualizzare un raycast prima di lanciarlo
Debug.DrawRay(transform.position, Vector3.down * 1.5f, Color.yellow);
if (Physics.Raycast(transform.position, Vector3.down, 1.5f))
    Debug.Log("A terra");
```
Simile a `DrawLine` ma il secondo parametro è una **direzione + lunghezza** (Vector3), non un punto di arrivo. Fondamentale per debuggare raycast, AI sight lines, range audio spaziale.

---

## CONTROLLO DEL PLAY MODE

### `Debug.Break`
```csharp
if (health <= 0)
{
    Debug.LogError("Player morto — pausa per ispezione");
    Debug.Break(); // Mette in pausa il Play Mode al frame corrente
}
```
Pausa l'editor **alla fine del frame corrente**, non istantaneamente. Permette di ispezionare lo stato esatto degli oggetti nel momento critico. Equivalente a mettere un breakpoint visivo senza IDE.

---

### `Debug.ClearDeveloperConsole`
```csharp
Debug.ClearDeveloperConsole();
```
Svuota la Console programmaticamente. Utile in tool editor custom o quando vuoi isolare i log di una fase specifica.

---

## PROPRIETÀ STATICHE

### `Debug.isDebugBuild`
```csharp
if (Debug.isDebugBuild)
    Debug.Log("Solo in Development Build");
```
`true` se la build è una **Development Build**. Usalo per attivare sistemi di debug solo in fase di sviluppo senza toccare il codice di produzione.

---

### `Debug.unityLogger`
```csharp
// Disabilitare tutti i log in una volta
Debug.unityLogger.logEnabled = false;

// Filtrare per tipo
Debug.unityLogger.filterLogType = LogType.Error; // Solo errori
```
Accesso diretto al logger interno di Unity. Puoi disabilitarlo globalmente, filtrare per tipo, o sostituirlo con un `ILogHandler` custom — utile per redirectare i log su file o sistemi di telemetria.

---

### `Debug.developerConsoleEnabled` / `developerConsoleVisible`
```csharp
Debug.developerConsoleEnabled = true;  // Abilita la console in-game
Debug.developerConsoleVisible = true;  // La rende visibile
```
Controlla la console in-game nelle build, non quella dell'editor. Raramente usata direttamente.

---

## Quale usi di più in produzione?

In ordine di utilità pratica:
`Assert` > `DrawRay/DrawLine` > `Log/LogWarning/LogError` > `Break` > `unityLogger`
