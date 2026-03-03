# Command Pattern — Schema di Riferimento

## Definizione
> Un comando è una chiamata a metodo trasformata in oggetto.  
> Disaccoppia **chi ordina** da **chi esegue**.

---

## Struttura

```
IMyCommand (interface)
├── Execute()
└── Undo()
        │
        ├── JumpCommand : IMyCommand
        ├── FireCommand : IMyCommand
        └── DoNothingCommand : IMyCommand  ← Null Object Pattern

InputHandler : MonoBehaviour
├── _buttonX, _buttonY          ← binding tasti → comandi
├── _history : Stack<IMyCommand> ← storia per Undo
├── HandleInput() → IMyCommand  ← restituisce, non esegue
└── Update()                    ← esegue + salva in history
```

---

## Codice Minimo

```csharp
// 1. Interfaccia
public interface IMyCommand {
    void Execute();
    void Undo();
}

// 2. Comando concreto
public class JumpCommand : IMyCommand {
    public void Execute() => Debug.Log("Salta!");
    public void Undo()    => Debug.Log("Annulla salto");
}

// 3. Null Object (nessun crash se tasto non assegnato)
public class DoNothingCommand : IMyCommand {
    public void Execute() { }
    public void Undo()    { }
}

// 4. Handler
public class InputHandler : MonoBehaviour {
    private IMyCommand _buttonX;
    private Stack<IMyCommand> _history = new Stack<IMyCommand>();

    private void Start()  => _buttonX = new JumpCommand();

    private void Update() {
        IMyCommand cmd = HandleInput();
        if (cmd != null) { cmd.Execute(); _history.Push(cmd); }

        if (Input.GetKeyDown(KeyCode.Z) && _history.Count > 0)
            _history.Pop().Undo();
    }

    private IMyCommand HandleInput() {
        if (Input.GetKeyDown(KeyCode.X)) return _buttonX;
        return null;
    }
}
```

---

## Quando Usarlo

| Hai bisogno di...             | Usa Command Pattern |
|-------------------------------|---------------------|
| Input remappabile a runtime   | ✅                  |
| Undo / Redo                   | ✅                  |
| Replay di azioni              | ✅                  |
| AI che usa stessi comandi del player | ✅           |
| Input semplice e fisso        | ❌ sovraingegnerizzato |

---

## Varianti

### Con GameActor (comandi riusabili su qualsiasi oggetto)
```csharp
public interface IMyCommand {
    void Execute(GameActor actor);
    void Undo(GameActor actor);
}
// Stessa JumpCommand può far saltare player, nemico, NPC
```

### Senza GameActor (comandi autonomi)
```csharp
public interface IMyCommand {
    void Execute();
    void Undo();
}
// Il comando sa già su chi agisce (utile per comandi one-shot)
```

---

## Stack vs List per la History

```csharp
Stack<IMyCommand> _history  // LIFO — semanticamente corretto per Undo
                            // Pop() = "dammi l'ultimo comando"

List<IMyCommand> _history   // generico, richiede gestione manuale dell'indice
```

---

## Pattern Correlati

| Pattern | Relazione |
|---------|-----------|
| **Null Object** | `DoNothingCommand` elimina i null check |
| **State** | Cambia quali comandi sono attivi per stato |
| **Observer** | I comandi possono notificare eventi dopo Execute() |
| **Flyweight** | Comandi stateless condivisi (es. JumpCommand singleton) |
