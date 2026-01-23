# Unity MonoBehaviour Lifecycle Methods — Guida Completa

## Indice
1. [Filosofia Fondamentale](#filosofia-fondamentale)
2. [Fasi del Ciclo di Vita](#fasi-del-ciclo-di-vita)
3. [Metodi per Fase](#metodi-per-fase)
4. [Quando Usare Cosa](#quando-usare-cosa)
5. [Diagramma Temporale](#diagramma-temporale)
6. [Esempi Pratici per Pong](#esempi-pratici-per-pong)

---

## Filosofia Fondamentale

Unity esegue il codice in **ordine specifico e prevedibile**. Ogni metodo ha un momento esatto in cui viene chiamato.

**Principio cardine:** Se metti il codice nel metodo sbagliato, otterrai comportamenti impredetti, race condition, o oggetti non inizializzati.

Per questo importa **dove** metti il codice, non solo **che cosa** metti.

---

## Fasi del Ciclo di Vita

Un MonoBehaviour passa attraverso queste fasi:

```
1. INSTANZIAZIONE        → Awake()
2. ABILITAZIONE          → OnEnable()
3. PRIMA ESECUZIONE      → Start()
4. LOOP DI GIOCO         → Update() → FixedUpdate() → LateUpdate() (ripetuto ogni frame)
5. DISABILITAZIONE       → OnDisable()
6. DISTRUZIONE           → OnDestroy()
```

---

## Metodi per Fase

### **FASE 1: INSTANZIAZIONE**

#### `Awake()`
```csharp
void Awake()
{
    // Eseguito SUBITO dopo che l'oggetto è creato
    // PRIMA di qualsiasi Start()
    // Chiamato anche se lo script è disabilitato
}
```

**Quando viene chiamato:**
- Immediatamente dopo `Instantiate()` o quando Unity carica la scena
- PRIMA di `OnEnable()` e `Start()`
- ANCHE se il GameObject o lo script è disabilitato

**Cosa farne:**
- Cache di riferimenti a componenti dello stesso oggetto
- Inizializzazione di variabili interne semplici
- Configurazione di default che non dipendono da altri oggetti

**Esempio - Pong:**
```csharp
public class PaddleController : MonoBehaviour
{
    private Rigidbody2D rb;
    private AudioSource audioSource;
    
    void Awake()
    {
        // Cache i componenti una sola volta
        rb = GetComponent<Rigidbody2D>();
        audioSource = GetComponent<AudioSource>();
        
        // Non dipende da niente, posso inizializzare
        maxSpeed = 10f;
    }
}
```

**Perché qui e non in Start()?**
- `Awake()` è garantito di avvenire prima di qualsiasi `Start()`
- Se la Paddle deve riferirsi alla Ball, e la Ball si inizializza in Start(), Awake() assicura che la Paddle è pronta prima che la Ball cerchi di interagire con essa

---

### **FASE 2: ABILITAZIONE**

#### `OnEnable()`
```csharp
void OnEnable()
{
    // Eseguito ogni volta che il componente/GameObject viene ABILITATO
    // Dopo Awake(), ma potrebbe essere chiamato più volte
}
```

**Quando viene chiamato:**
- Dopo `Awake()` la prima volta che lo script viene caricato
- Ogni volta che fai `gameObject.SetActive(true)` o `this.enabled = true`
- **Multiple volte durante il ciclo di vita**

**Cosa farne:**
- Sottoscrivere eventi (event listener)
- Riattivare comportamenti che erano stati disattivati
- Setup che deve ripetersi se l'oggetto viene riabilitato

**Esempio - Pong con Wwise:**
```csharp
public class GameManager : MonoBehaviour
{
    public UnityEvent<int> onScoreChanged;
    private AudioSource uiAudioSource;
    
    void OnEnable()
    {
        // Sottoscrivi l'evento di score
        onScoreChanged.AddListener(OnScoreChanged);
        
        // Riattiva l'audio UI
        uiAudioSource.enabled = true;
    }
    
    void OnScoreChanged(int newScore)
    {
        uiAudioSource.Play(); // Riproduci suono di score
    }
}
```

**Perché separate OnEnable() e Start()?**
- `Start()` viene chiamato UNA SOLA VOLTA
- `OnEnable()` viene chiamato OGNI VOLTA che l'oggetto si riattiva
- Se disattivi e riattivi il GameObject, OnEnable() si riesegue ma Start() NO

---

### **FASE 3: PRIMA ESECUZIONE**

#### `Start()`
```csharp
void Start()
{
    // Eseguito al primo frame in cui lo script è ABILITATO
    // Dopo Awake() e OnEnable()
    // Garantito di essere chiamato UNA SOLA VOLTA
}
```

**Quando viene chiamato:**
- Primo frame in cui il MonoBehaviour è abilitato
- DOPO `Awake()` e `OnEnable()`
- UNA SOLA VOLTA durante il ciclo di vita (a meno che il GameObject non venga distrutto e ricreato)

**Cosa farne:**
- Inizializzazioni che dipendono da altri oggetti nella scena
- Setup che riferisce oggetti trovati con `GameObject.Find()` o tramite Inspector
- Logica iniziale che assume altri GameObject siano già stati inizializzati

**Esempio - Pong:**
```csharp
public class BallController : MonoBehaviour
{
    private PaddleController playerPaddle;
    private PaddleController aiPaddle;
    private GameManager gameManager;
    
    void Start()
    {
        // Cerca gli altri oggetti della scena
        // Questi devono ESISTERE già
        playerPaddle = GameObject.Find("PlayerPaddle").GetComponent<PaddleController>();
        aiPaddle = GameObject.Find("AIPaddle").GetComponent<PaddleController>();
        gameManager = GameObject.Find("GameManager").GetComponent<GameManager>();
        
        // Ora posso lanciare la palla verso il giocatore
        LaunchBall();
    }
}
```

**Perché non in Awake()?**
- Se metti `GameObject.Find()` in Awake(), rischi che l'oggetto cercato non sia ancora stato inizializzato
- Start() è dopo tutti gli Awake(), quindi è sicuro

---

### **FASE 4: LOOP DI GIOCO (ripetuto ogni frame)**

#### `FixedUpdate()`
```csharp
void FixedUpdate()
{
    // Eseguito a intervalli FISSI di tempo
    // Time.fixedDeltaTime ≈ 0.02 secondi (50 volte al secondo di default)
}
```

**Quando viene chiamato:**
- A intervalli fissi definiti da `Time.fixedDeltaTime` (Settings > Time > Fixed Timestep)
- PRIMA di `Update()` nello stesso frame
- Numero di volte per frame può variare (0, 1, 2+) in base al frame rate

**Cosa farne:**
- **TUTTE le modifiche di Rigidbody/fisica**
- Applicazione di forze, velocità, impulsi
- Qualsiasi cosa che deve essere deterministico e prevedibile fisicamente

**Esempio - Pong:**
```csharp
public class PaddleController : MonoBehaviour
{
    private Rigidbody2D rb;
    private float moveInput;
    public float speed = 5f;
    
    void Update()
    {
        // Leggi l'input in Update() — è basato su frame
        moveInput = Input.GetAxis("Vertical");
    }
    
    void FixedUpdate()
    {
        // APPLICA il movimento in FixedUpdate() — è basato su fisica
        Vector2 newVelocity = new Vector2(0, moveInput * speed);
        rb.velocity = newVelocity;
        
        // Perché qui e non in Update()?
        // Perché il Rigidbody viene aggiornato dal motore di fisica
        // che usa FixedUpdate per calcoli coerenti
    }
}
```

**Perché qui per la fisica?**
- Il motore di fisica di Unity è deterministico e usa passo fisso
- Se modifichi Rigidbody in Update(), a frame rate bassi rischi comportamenti incoerenti
- FixedUpdate() sincronizza il tuo codice con il motore di fisica

---

#### `Update()`
```csharp
void Update()
{
    // Eseguito una volta per frame
    // Frame rate varia (60 FPS = 16.67ms, 30 FPS = 33.33ms)
    // Usa Time.deltaTime per normalizzare il tempo
}
```

**Quando viene chiamato:**
- Una volta per frame, dopo `FixedUpdate()`
- Frame rate dipende dalla performance (varia!)

**Cosa farne:**
- Input da tastiera/mouse/joystick
- Logica di gioco frame-based (animazioni, controlli, camerata)
- Qualsiasi cosa non legata a fisica

**Esempio - Pong:**
```csharp
public class PaddleController : MonoBehaviour
{
    void Update()
    {
        // Leggi input
        float moveInput = Input.GetAxis("Vertical");
        
        // Applica logica basata su frame rate variabile
        // transform.Translate() automaticamente usa Time.deltaTime
        transform.Translate(Vector3.up * moveInput * 5f * Time.deltaTime);
    }
}
```

**Nota importante:**
- Sempre moltiplica per `Time.deltaTime` se dipendi dal tempo
- Senza Time.deltaTime, a 60 FPS il movimento sarà il doppio che a 30 FPS

---

#### `LateUpdate()`
```csharp
void LateUpdate()
{
    // Eseguito DOPO tutti gli Update() dello stesso frame
    // Perfetto per operazioni che devono avvenire "dopo"
}
```

**Quando viene chiamato:**
- Dopo TUTTI gli `Update()` di tutti i GameObject dello stesso frame
- Utile quando l'ordine importa

**Cosa farne:**
- Camera follow (assicura che il giocatore si è mosso prima di seguire)
- Pulizia finale del frame
- Operazioni che dipendono dalla posizione finale degli oggetti

**Esempio - Pong:**
```csharp
public class CameraFollow : MonoBehaviour
{
    private Transform ballTransform;
    public Vector3 offset = new Vector3(0, 0, -10);
    
    void LateUpdate()
    {
        // Dopo che la palla si è mossa in Update()
        // Ora posso seguirla senza lag
        transform.position = ballTransform.position + offset;
    }
}
```

**Perché non in Update()?**
- Se metti camera follow in Update(), c'è una piccola desincronizzazione: la palla si muove in Update(), la camera la segue... ma ci vorrà un frame prima che la camera sia veramente sincronizzata
- LateUpdate() assicura che tutto è stato già mosso, poi aggiorno la camera

---

### **FASE 5: DISABILITAZIONE**

#### `OnDisable()`
```csharp
void OnDisable()
{
    // Eseguito quando il componente/GameObject viene DISABILITATO
    // Opposto di OnEnable()
}
```

**Quando viene chiamato:**
- Quando fai `gameObject.SetActive(false)` o `this.enabled = false`
- Quando l'oggetto viene distrutto
- Quando la scena viene scaricata

**Cosa farne:**
- Desottoscrivere eventi (rimuovere listener)
- Liberare risorse temporanee
- Salvare dati prima che l'oggetto scompaia

**Esempio - Pong:**
```csharp
public class GameManager : MonoBehaviour
{
    public UnityEvent<int> onScoreChanged;
    
    void OnEnable()
    {
        onScoreChanged.AddListener(OnScoreChanged);
    }
    
    void OnDisable()
    {
        // IMPORTANTE: rimuovi il listener per evitare memory leak
        onScoreChanged.RemoveListener(OnScoreChanged);
    }
}
```

**Perché è importante?**
- Se non desottoscrivi, l'evento mantiene un riferimento al GameObject anche dopo che è stato distrutto
- Questo causa memory leak

---

### **FASE 6: DISTRUZIONE**

#### `OnDestroy()`
```csharp
void OnDestroy()
{
    // Eseguito quando l'oggetto viene definitivamente DISTRUTTO
    // Ultimo metodo del ciclo di vita
}
```

**Quando viene chiamato:**
- Quando chiami `Destroy(gameObject)`
- Quando la scena viene scaricata
- Quando l'applicazione chiude

**Cosa farne:**
- Pulizia finale di risorse
- Salvataggio di dati persistenti
- Desottoscrizioni finali (backup di OnDisable)

**Esempio:**
```csharp
public class AudioManager : MonoBehaviour
{
    void OnDestroy()
    {
        // Salva le impostazioni audio prima che l'oggetto muoia
        PlayerPrefs.SetFloat("MasterVolume", masterVolume);
        PlayerPrefs.Save();
    }
}
```

---

## Collisioni e Trigger

### **Collisioni Fisiche (3D)**

Quando due Rigidbody con Collider (non-trigger) collidono:

```csharp
void OnCollisionEnter(Collision collision)
{
    // Momento esatto del contatto
    // Chiamato una sola volta quando inizia la collisione
}

void OnCollisionStay(Collision collision)
{
    // Ogni frame mentre rimangono in contatto
    // Utile per "pressione" continua
}

void OnCollisionExit(Collision collision)
{
    // Quando si separano
}
```

### **Collisioni Fisiche (2D)**

Quando due Rigidbody2D con Collider2D (non-trigger) collidono:

```csharp
void OnCollisionEnter2D(Collision2D collision)
{
    // Per giochi 2D
    Debug.Log("Colpito: " + collision.gameObject.name);
    audioSource.PlayOneShot(collisionSound);
}
```

### **Trigger (3D e 2D)**

Quando un Collider con `Is Trigger = true` è toccato:

```csharp
// 3D
void OnTriggerEnter(Collider other)
{
    // Qualcosa è entrato nel trigger
}

// 2D
void OnTriggerEnter2D(Collider2D other)
{
    // 2D version
}
```

**Differenza:**
- **Collider normale** = collisione fisica (rimbalzi, spinte)
- **Trigger** = solo rilevamento (niente fisica)

**Esempio - Pong 2D:**
```csharp
public class BallController : MonoBehaviour
{
    private AudioSource ballAudio;
    
    void OnCollisionEnter2D(Collision2D collision)
    {
        // Palla ha colpito la racchetta
        if (collision.gameObject.CompareTag("Paddle"))
        {
            // Riproduci suono di impatto
            ballAudio.PlayOneShot(paddleHitSound);
            
            // Applica rimbalzo
            Vector2 bounceDirection = GetBounceDirection(collision);
            GetComponent<Rigidbody2D>().velocity = bounceDirection * ballSpeed;
        }
    }
}
```

---

## Diagramma Temporale

```
CICLO COMPLETO DI UN GAMEOBJECT:

[CREAZIONE GAMEOBJECT]
        ↓
    Awake()  ← Cache componenti, init base
        ↓
    OnEnable()  ← Sottoscrivi eventi
        ↓
    Start()  ← Init che dipende da altri oggetti
        ↓
   ┌──────────────────── LOOP DI GIOCO ──────────────────┐
   │                                                       │
   │  FixedUpdate()  ← Fisica (Rigidbody)                 │
   │       ↓                                               │
   │  Update()  ← Input, logica frame-based               │
   │       ↓                                               │
   │  [Rendering/Collisioni/Trigger rilevati]            │
   │       ↓                                               │
   │  LateUpdate()  ← Camera follow, pulizia             │
   │       ↓                                               │
   │  [Fine frame, continua al prossimo frame]           │
   │       ↓                                               │
   │  (ritorna a FixedUpdate)                            │
   │                                                       │
   └───────────────────────────────────────────────────────┘
        ↓
    OnDisable()  ← Desottoscrivi eventi
        ↓
    OnDestroy()  ← Pulizia finale
        ↓
   [OGGETTO DISTRUTTO]
```

---

## Quando Usare Cosa — Tabella Rapida

| Operazione | Metodo | Perché |
|-----------|--------|-------|
| Cache componenti | `Awake()` | Prima di qualsiasi altro codice |
| Sottoscrivi eventi | `OnEnable()` | Ripetuto se riabilitato |
| Cerca oggetti nella scena | `Start()` | Dopo tutti gli Awake() |
| Modifica Rigidbody | `FixedUpdate()` | Sincronizzato con motore di fisica |
| Leggi input | `Update()` | Basato su frame variabile |
| Aggiorna camera | `LateUpdate()` | Dopo che tutto è mosso |
| Rileva collisioni | `OnCollisionEnter2D()` | Callback fisico automatico |
| Desottoscrivi eventi | `OnDisable()` | Prima di distruggere |
| Salva dati | `OnDestroy()` | Ultimo momento utile |

---

## Esempi Pratici per Pong

### **Sistema Completo: BallController**

```csharp
public class BallController : MonoBehaviour
{
    private Rigidbody2D rb;
    private AudioSource audioSource;
    private GameManager gameManager;
    
    public float initialSpeed = 5f;
    private float currentSpeed;
    
    // ============= FASE INIZIALIZZAZIONE =============
    
    void Awake()
    {
        // Cache componenti locali SUBITO
        rb = GetComponent<Rigidbody2D>();
        audioSource = GetComponent<AudioSource>();
    }
    
    void OnEnable()
    {
        // Se la palla viene riabilitata (es. reset), ascolta gli eventi
        gameManager.onGameReset.AddListener(ResetBallPosition);
    }
    
    void Start()
    {
        // Cerca il GameManager DOPO che tutto è stato inizializzato
        gameManager = GameObject.Find("GameManager").GetComponent<GameManager>();
        
        // Inizializza velocità
        currentSpeed = initialSpeed;
        
        // Lancia la palla
        LaunchBall();
    }
    
    // ============= LOOP DI GIOCO =============
    
    void FixedUpdate()
    {
        // Applica accelerazione graduale (fisica pura)
        currentSpeed += 0.01f;
        currentSpeed = Mathf.Clamp(currentSpeed, initialSpeed, 15f);
        
        // Mantieni direzione, aumenta velocità
        Vector2 direction = rb.velocity.normalized;
        rb.velocity = direction * currentSpeed;
    }
    
    void Update()
    {
        // Logica di gioco basata su frame
        // (non c'è molto qui per Pong, ma potrebbe servire per effetti)
    }
    
    void LateUpdate()
    {
        // Niente per la palla, ma potrebbe servire per sincronizzare audio
    }
    
    // ============= COLLISIONI =============
    
    void OnCollisionEnter2D(Collision2D collision)
    {
        // Palla ha colpito qualcosa (racchetta, muro, ecc)
        
        if (collision.gameObject.CompareTag("Paddle"))
        {
            // Rimbalzo sulla racchetta
            Vector2 hitPoint = collision.GetContact(0).point;
            HandlePaddleHit(collision.gameObject, hitPoint);
            
            // Riproduci suono UX
            audioSource.PlayOneShot(paddleHitClip);
        }
        else if (collision.gameObject.CompareTag("Wall"))
        {
            // Rimbalzo sul muro
            audioSource.PlayOneShot(wallHitClip);
        }
    }
    
    void OnTriggerEnter2D(Collider2D other)
    {
        // Se la palla esce dal campo (trigger zone)
        if (other.CompareTag("GoalZone"))
        {
            HandleGoalScored(other.gameObject);
        }
    }
    
    // ============= DISABILITAZIONE =============
    
    void OnDisable()
    {
        // Desottoscrivi eventi per evitare memory leak
        gameManager.onGameReset.RemoveListener(ResetBallPosition);
    }
    
    void OnDestroy()
    {
        // Se la palla viene distrutta, salva statistiche
        // (per un gioco vero)
    }
    
    // ============= METODI HELPER =============
    
    private void LaunchBall()
    {
        Vector2 randomDirection = Random.insideUnitCircle.normalized;
        rb.velocity = randomDirection * currentSpeed;
    }
    
    private void HandlePaddleHit(GameObject paddle, Vector2 hitPoint)
    {
        // Logica di rimbalzo intelligente
        Vector2 newDirection = Vector2.Reflect(rb.velocity.normalized, paddle.transform.up);
        rb.velocity = newDirection * currentSpeed;
    }
    
    private void HandleGoalScored(GameObject goalZone)
    {
        // Notifica al GameManager che è stato segnato
        gameManager.OnGoalScored();
        
        // Reset palla
        ResetBallPosition();
    }
    
    private void ResetBallPosition()
    {
        transform.position = Vector3.zero;
        currentSpeed = initialSpeed;
        LaunchBall();
    }
}
```

### **Sistema Completo: PaddleController**

```csharp
public class PaddleController : MonoBehaviour
{
    private Rigidbody2D rb;
    private AudioSource audioSource;
    
    public float maxSpeed = 8f;
    public bool isPlayerControlled = true;
    
    private float moveInput;
    
    void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        audioSource = GetComponent<AudioSource>();
    }
    
    void Start()
    {
        // Inizializzazione specifica se necessaria
    }
    
    void Update()
    {
        if (isPlayerControlled)
        {
            // Leggi input da tastiera
            moveInput = Input.GetAxis("Vertical");
        }
        // Se controllata da IA, moveInput viene settato altrove
    }
    
    void FixedUpdate()
    {
        // Applica velocità basata su input
        // IMPORTANTE: FixedUpdate per Rigidbody
        rb.velocity = new Vector2(0, moveInput * maxSpeed);
        
        // Clamp della posizione per rimanere nel campo
        ClampPosition();
    }
    
    void OnCollisionEnter2D(Collision2D collision)
    {
        // Racchetta ha colpito qualcosa
        if (collision.gameObject.CompareTag("Ball"))
        {
            // Feedback audio
            audioSource.PlayOneShot(hitSound);
        }
    }
    
    private void ClampPosition()
    {
        Vector3 pos = transform.position;
        pos.y = Mathf.Clamp(pos.y, -4.5f, 4.5f);
        transform.position = pos;
    }
}
```

### **Sistema Completo: GameManager**

```csharp
public class GameManager : MonoBehaviour
{
    // Events
    public UnityEvent onGameReset;
    public UnityEvent<int> onScoreChanged;
    
    private int playerScore = 0;
    private int aiScore = 0;
    private AudioSource uiAudioSource;
    
    void Awake()
    {
        // Singleton pattern — un solo GameManager
        if (FindObjectsOfType<GameManager>().Length > 1)
        {
            Destroy(gameObject);
        }
    }
    
    void OnEnable()
    {
        // Ascolta eventi di gioco
        // (potrebbero essere sottoscritti qui)
    }
    
    void Start()
    {
        uiAudioSource = GetComponent<AudioSource>();
        Debug.Log("Game started!");
    }
    
    void Update()
    {
        // Logica di turno (pause, reset, ecc)
        if (Input.GetKeyDown(KeyCode.R))
        {
            ResetGame();
        }
    }
    
    void OnDisable()
    {
        // Desottoscrivi se necessario
    }
    
    public void OnGoalScored()
    {
        // Callback dalla BallController
        playerScore++;
        onScoreChanged.Invoke(playerScore);
        
        // Riproduci suono di goal
        uiAudioSource.PlayOneShot(goalSound);
        
        // Reset palla tramite evento
        onGameReset.Invoke();
    }
    
    private void ResetGame()
    {
        playerScore = 0;
        aiScore = 0;
        onGameReset.Invoke();
        uiAudioSource.PlayOneShot(resetSound);
    }
}
```

---

## Checklist Finale: Come Strutturare il Tuo Pong

```csharp
// ✓ BallController
void Awake() { rb = GetComponent<Rigidbody2D>(); audioSource = GetComponent<AudioSource>(); }
void Start() { gameManager = FindObjectOfType<GameManager>(); LaunchBall(); }
void FixedUpdate() { /* Modifica velocità */ }
void OnCollisionEnter2D() { /* Audio + rimbalzo */ }

// ✓ PaddleController
void Awake() { rb = GetComponent<Rigidbody2D>(); }
void Update() { moveInput = Input.GetAxis("Vertical"); }
void FixedUpdate() { rb.velocity = new Vector2(0, moveInput * speed); }

// ✓ GameManager
void Awake() { /* Singleton setup */ }
void Start() { /* Inizializza UI */ }
void Update() { /* Input comandi globali */ }
```

---

## Riassunto Rapido

| Fase | Metodo | Quando | Usa Per |
|-----|--------|--------|---------|
| Init | Awake() | Istante della creazione | Cache componenti |
| Init | OnEnable() | Ogni abilitazione | Sottoscrizioni eventi |
| Init | Start() | Primo frame | Logica dipendente da altri obj |
| Loop | FixedUpdate() | Passo fisso | Rigidbody, forze |
| Loop | Update() | Ogni frame | Input, logica |
| Loop | LateUpdate() | Dopo Update() | Camera, pulizia |
| Collisioni | OnCollisionEnter2D() | Impatto | Effetti, rimbalzi |
| Cleanup | OnDisable() | Disattivazione | Desottoscrizioni |
| Cleanup | OnDestroy() | Distruzione | Salvataggio finale |

---

## Note Importanti

1. **Non getComponent() in Update()** — è costoso, cache in Awake()
2. **Sempre Time.deltaTime** — se usi tempo, moltiplicalo per Time.deltaTime
3. **FixedUpdate per fisica** — Rigidbody SEMPRE in FixedUpdate()
4. **Desottoscrivi gli eventi** — OnDisable() deve rimuovere i listener di OnEnable()
5. **Update() per input** — Leggi tastiera/mouse in Update(), non FixedUpdate()

