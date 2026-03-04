# Eventi, Delegate e Callback in Unity / C#

---

## Cos'è un Callback

Un **callback** è una funzione passata come argomento a un'altra funzione, da eseguire in un momento futuro.

```
"Fai questa cosa, e quando hai finito chiama questa funzione."
```

In C#, i delegate sono il meccanismo con cui si implementano i callback.

---

## Le 4 modalità a confronto

### 1. `delegate` + `event` — controllo massimo

```csharp
public delegate void JumpingEvent();       // definisce la firma
public event JumpingEvent OnPlayerJump;    // crea l'evento

OnPlayerJump?.Invoke();                    // spara l'evento
```

- ✅ Firma esplicita e leggibile
- ✅ `event` protegge l'invocazione (solo la classe owner può spararlo)
- ❌ Verboso — richiede la dichiarazione del delegate

---

### 2. `Action` / `Func` — delegate predefiniti di System

```csharp
public event Action OnPlayerJump;                 // void, 0 parametri
public event Action<int, string> OnPlayerHit;     // void, con parametri
public event Func<bool> OnCheckGrounded;          // ritorna bool
```

- ✅ Più conciso — niente dichiarazione manuale del delegate
- ✅ `Action` è esattamente un `delegate void` già scritto da Microsoft
- ❌ Firma meno descrittiva rispetto a un delegate nominato

---

### 3. `UnityEvent` — sistema di Unity

```csharp
using UnityEngine.Events;

public UnityEvent OnPlayerJump;           // configurabile da Inspector
public UnityEvent<int> OnPlayerHit;       // con parametro
```

- ✅ Visibile e configurabile nell'Inspector senza codice
- ✅ Ottimo per UI, designer-friendly
- ❌ Più lento a runtime rispetto ai delegate C#

---

### 4. `UnityAction` — wrapper Unity su Action

```csharp
using UnityEngine.Events;

public event UnityAction OnPlayerJump;
```

- Usato internamente da `UnityEvent`
- Raramente necessario direttamente nel codice

---

## Confronto rapido

| Tipo              | Controllo   | Concisione | Inspector | Performance |
|-------------------|-------------|------------|-----------|-------------|
| `delegate+event`  | ✅ massimo  | ❌ verboso | ❌        | ✅          |
| `Action`          | ✅          | ✅         | ❌        | ✅          |
| `UnityEvent`      | ⚠️ medio   | ✅         | ✅        | ⚠️ lento   |
| `UnityAction`     | ✅          | ✅         | ❌        | ✅          |

---

## Pattern base — implementazione completa

### PlayerBehaviour — dichiara e spara

```csharp
using UnityEngine;

public class PlayerBehaviour : MonoBehaviour
{
    // Firma del callback: void, nessun parametro
    public delegate void JumpingEvent();
    public event JumpingEvent OnPlayerJump;

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Backspace))
        {
            OnPlayerJump?.Invoke();         // ?. = nessun crash se 0 subscriber
            Debug.Log("Evento sparato");
        }
    }
}
```

---

### SingletonGameBehaviour — ascolta l'evento

```csharp
using UnityEngine;

public class SingletonGameBehaviour : Singleton<SingletonGameBehaviour>
{
    private PlayerBehaviour _player;

    // Start garantisce che tutti gli Awake siano già eseguiti
    private void Start()
    {
        _player = FindAnyObjectByType<PlayerBehaviour>();

        if (_player == null)
        {
            Debug.LogWarning("PlayerBehaviour non trovato!");
            return;
        }

        _player.OnPlayerJump += HandleJump;     // iscrizione
        Debug.Log("Iscritto all'evento");
    }

    private void OnDisable()
    {
        if (_player == null) return;

        _player.OnPlayerJump -= HandleJump;     // pulizia
        Debug.Log("Disiscritto dall'evento");
    }

    // Callback: firma deve corrispondere al delegate
    private void HandleJump()
    {
        Debug.Log("Il player ha saltato.");
    }
}
```

---

### Singleton base

```csharp
using UnityEngine;

public class Singleton<T> : MonoBehaviour where T : Component
{
    public static T Instance { get; private set; }

    public virtual void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
        }
        else
        {
            Instance = this as T;
            DontDestroyOnLoad(gameObject);
        }
    }
}
```

---

## Flusso di esecuzione

```
[PlayerBehaviour]  dichiara delegate + event
        ↓
[SingletonGameBehaviour]  si iscrive con +=  (in Start)
        ↓
[PlayerBehaviour]  chiama Invoke()  →  tutti i subscriber ricevono
        ↓
[SingletonGameBehaviour]  HandleJump() esegue
        ↓
[OnDisable]  pulizia con -=
```

---

## Regole da ricordare

- **`?. Invoke()`** — sempre, per evitare crash con 0 subscriber
- **Iscriviti in `Start`**, non in `OnEnable`, quando dipendi da altri componenti
- **Pulisci sempre in `OnDisable`** — le subscription non rimosse consumano risorse e causano errori dopo la distruzione dell'oggetto
- **`event`** impedisce a classi esterne di invocare l'evento direttamente — solo `+=` e `-=` sono permessi dall'esterno
