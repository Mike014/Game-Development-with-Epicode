# Glossario — Matematica per Unity
*Bounding Box, Vettori, Piani*

---

## Spazio e Coordinate

### Sistema di Coordinate Cartesiane 3D
Tre assi perpendicolari (X, Y, Z) che descrivono posizioni nello spazio. In Unity: X = destra, Y = su, Z = avanti. L'origine è il punto `(0,0,0)`.
```csharp
Vector3 position = new Vector3(x, y, z);
```

### Sistema Left-Handed (Mano Sinistra)
Convenzione di Unity per l'orientamento degli assi. L'asse Z positivo punta "dentro" lo schermo. Influisce sul risultato del Cross Product: V1 × V2 segue la regola della mano sinistra.

### Origine
Il punto `(0,0,0)` nello spazio 3D. Ogni posizione è tecnicamente un vettore che "spinge" dall'origine fino al punto stesso (Position Vector).
```csharp
Vector3 origin = Vector3.zero;
```

---

## Bounding Volumes

### Bounding Box (AABB)
*Axis-Aligned Bounding Box.* Scatola invisibile allineata agli assi del mondo che racchiude un oggetto complesso. Usata per semplificare i calcoli di collisione.
**Trade-off:** guadagni velocità (performance), perdi precisione (falsi positivi).
```csharp
Bounds box = GetComponent<Renderer>().bounds;
```

### Min / Max (Bounding Box)
I due punti che definiscono una AABB. `Min` = angolo in basso-sinistra-dietro. `Max` = angolo in alto-destra-avanti. Da questi si derivano centro e dimensioni.
```csharp
Vector3 center = 0.5f * (MinPos + MaxPos);
Vector3 size   = MaxPos - MinPos;
```

### Void Space
Lo spazio vuoto all'interno di una Bounding Box non occupato dalla mesh reale. Causa **falsi positivi** nelle collisioni. Soluzione: Compound Colliders.

### Compound Colliders
Tecnica che usa più collider piccoli al posto di uno grande, per adattarsi alla forma irregolare dell'oggetto. Bilancia precisione e performance.

### Bounding Sphere
Volume di collisione sferico definito da un centro e un raggio. Ideale per oggetti rotondi. Test di collisione: distanza tra centri ≤ somma dei raggi.
```csharp
bool hit = (centerA - centerB).sqrMagnitude <= (rA + rB) * (rA + rB);
```

### Gerarchia di Sfere (BVH)
Struttura ad albero di Bounding Volumes.
- **Broad Phase:** sfera grande per test rapido iniziale.
- **Narrow Phase:** sfere piccole interne per precisione.

Ottimizza evitando test inutili su oggetti distanti.

---

## Intervalli e Intersezioni

### Intervallo (Min-Max Range)
Regione definita da un valore minimo e uno massimo lungo un singolo asse. Mattone base delle Bounding Box: una AABB è la combinazione di 3 intervalli (uno per asse X, Y, Z).
```csharp
float min = Mathf.Min(a, b);
float max = Mathf.Max(a, b);
```

### Regola d'Oro dell'Intersezione (AABB)
Due Bounding Box collidono **se e solo se** gli intervalli si sovrappongono su tutti e tre gli assi contemporaneamente.
```csharp
bool hit =
    (a.min.x <= b.max.x && a.max.x >= b.min.x) &&
    (a.min.y <= b.max.y && a.max.y >= b.min.y) &&
    (a.min.z <= b.max.z && a.max.z >= b.min.z);
```

### Volume di Intersezione (Overlap)
La regione comune a due Bounding Box che si intersecano. Si calcola prendendo il **massimo dei minimi** (pavimento più alto) e il **minimo dei massimi** (soffitto più basso).
```csharp
Vector3 overlapMin = Vector3.Max(a.Min, b.Min);
Vector3 overlapMax = Vector3.Min(a.Max, b.Max);
```

---

## Vettori

### Vettore
Entità matematica definita da magnitudine (lunghezza) e direzione. Non è legato a una posizione fissa. In Unity, `Vector3` rappresenta sia posizioni che direzioni, velocità e forze.
```csharp
Vector3 v = new Vector3(x, y, z);
```

### Vettore Unitario (Unit Vector)
Vettore con magnitudine esattamente uguale a 1. Rappresenta una **direzione pura**, senza influenza sulla velocità. Ottenuto con `.normalized`.
```csharp
Vector3 dir = myVector.normalized; // |dir| == 1
```

### Normalizzazione
Operazione che riduce la magnitudine di un vettore a 1 mantenendo la direzione invariata. Formula: `V_norm = V / |V|`. Essenziale per separare direzione da velocità.
```csharp
Vector3 normalized = direction / direction.magnitude;
```

### Magnitudine (`.magnitude`)
Lunghezza di un vettore. Calcolata con il Teorema di Pitagora: `√(x²+y²+z²)`. Operazione **costosa** per la CPU (contiene una radice quadrata). Preferire `.sqrMagnitude` per confronti.
```csharp
float len = myVector.magnitude;
```

### sqrMagnitude
Quadrato della lunghezza del vettore: `x²+y²+z²`. Più efficiente di `.magnitude` perché evita la radice quadrata. Da usare per confronti di distanza.
```csharp
// Ottimizzato — nessuna radice quadrata
if (v.sqrMagnitude <= radius * radius) { ... }
```

### Sottrazione Vettoriale (B - A)
Calcola il vettore che punta da A verso B. Operazione fondamentale per targeting e calcolo della distanza. Componente per componente: `(Bx-Ax, By-Ay, Bz-Az)`.
```csharp
Vector3 direction = target.position - transform.position;
float   distance  = direction.magnitude;
```

### Scaling Vettoriale
Moltiplicazione di un vettore per uno scalare (`float`). Modifica la magnitudine senza cambiare la direzione. Scalare negativo: inverte la direzione.
```csharp
Vector3 velocity = direction.normalized * speed;
```

---

## Prodotti Vettoriali

### Prodotto Scalare (Dot Product)
Operazione tra due vettori che restituisce un **numero** (scalare).
Formula: `A·B = AxBx + AyBy + AzBz = |A||B|cos(θ)`
Con vettori normalizzati il risultato è direttamente il coseno dell'angolo.

| Risultato | Significato |
|-----------|-------------|
| `> 0` | stesso verso generale (θ < 90°) |
| `= 0` | perpendicolari (θ = 90°) |
| `< 0` | verso opposto (θ > 90°) |

```csharp
float dot = Vector3.Dot(A, B);
```

### Proiezione Vettoriale
"L'ombra" di un vettore su un altro. Indica quanto `V1` si estende lungo la direzione di `V2`. Usata ad esempio per sapere la posizione di un oggetto lungo un percorso.
```csharp
float projection = Vector3.Dot(V1, V2.normalized);
```

### Prodotto Vettoriale (Cross Product)
Operazione tra due vettori che restituisce un **terzo vettore** perpendicolare a entrambi. Anti-commutativo: `A×B = -(B×A)`. La magnitudine equivale all'area del parallelogramma formato dai due vettori.
```csharp
Vector3 normal = Vector3.Cross(A, B);
```

### Normale di una Superficie
Vettore perpendicolare a una faccia 3D. Calcolato con il Cross Product di due vettori giacenti sul piano. Indica "dove guarda" la superficie. Fondamentale per illuminazione, riflessioni e Ray Casting.
```csharp
Vector3 normal = Vector3.Cross(edge1, edge2).normalized;
```

---

## Distanze e Collisioni Sferiche

### Distanza (Pitagora 3D)
Distanza tra due punti P1 e P2: `√(Δx² + Δy² + Δz²)`. In Unity si ottiene dalla magnitudine del vettore differenza. L'ordine di sottrazione non conta (i valori vengono elevati al quadrato).
```csharp
float dist = (P2 - P1).magnitude;
// oppure:
float dist = Vector3.Distance(P1, P2);
```

### Test Inside-Outside (Sfera)
Un punto è dentro una sfera se la sua distanza dal centro è ≤ al raggio. Ottimizzabile con `sqrMagnitude` per evitare la radice quadrata.
```csharp
bool inside = (point - center).sqrMagnitude <= radius * radius;
```

### Collisione Sfera-Sfera
Due sfere collidono quando la distanza tra i loro centri è ≤ alla somma dei loro raggi.
```csharp
float sumR = rA + rB;
bool  hit  = (centerA - centerB).sqrMagnitude <= sumR * sumR;
```

---

## Piani

### Piano (Equazione Vettoriale)
Superficie 2D infinita nello spazio 3D. Definita da `n · p = D`, dove `n` è la normale normalizzata e `D` è la distanza minima dall'origine. Tutti i punti del piano condividono la stessa proiezione `D`.
```csharp
float D = Vector3.Dot(normal, pointOnPlane);
```

### Ray Casting (Linea-Piano)
Tecnica per trovare dove un raggio interseca un piano. Il denominatore è il Dot Product tra la direzione del raggio e la normale del piano. Se `= 0`, il raggio è parallelo al piano (nessuna intersezione).
```csharp
float denom = Vector3.Dot(rayDir, planeNormal);
if (Mathf.Abs(denom) > 1e-6f)
{
    // calcola il punto di intersezione
}
```

### Riflessione Speculare
Formula per far rimbalzare un vettore su una superficie: `V_riflesso = V_in - 2*(V_in · n)*n`. Usata per fisica dei proiettili, ottica e shader. `n` deve essere normalizzato.
```csharp
Vector3 reflected = Vector3.Reflect(incoming, normal);
// manuale:
// v - 2 * Vector3.Dot(v, n) * n
```

### Axis Frame (Sistema di Assi Locali)
Triade di vettori perpendicolari tra loro (Destra, Su, Avanti) che definisce un sistema di coordinate locale. Si costruisce con il Cross Product doppio partendo da 3 punti. Usato per telecamere, oggetti inclinati, animazioni.
```csharp
Vector3 forward = (P2 - P1).normalized;
Vector3 right   = Vector3.Cross(forward, Vector3.up).normalized;
Vector3 up      = Vector3.Cross(right, forward);
```

---

## Ottimizzazioni e Best Practices

### Broad Phase / Narrow Phase
Pattern di ottimizzazione per la collision detection.
- **Broad Phase:** test rapido e approssimativo (es. sfera grande).
- **Narrow Phase:** test preciso solo se la Broad Phase è positiva.

Riduce drasticamente i calcoli inutili su oggetti distanti.

### Swap (Prevenzione Errore Min > Max)
Garantisce che `IntervalMin` sia sempre ≤ `IntervalMax`. Previene comportamenti indefiniti nelle Bounding Box.
```csharp
if (min > max) { float t = min; min = max; max = t; }
// oppure con clamp:
max = Mathf.Max(max, min);
```

### Center Offset (Pivot Correction)
I modelli 3D hanno spesso il pivot a terra (`y = 0`). Per centrare la Bounding Box sul volume reale si aggiunge un offset: `CentroReale = transform.position + CenterOffset`.
```csharp
Vector3 boxCenter = transform.position + centerOffset;
```

### Debug.DrawLine / DrawRay
Disegna linee visibili solo nella Scene View durante il Play Mode. Utile per visualizzare vettori, raggi e collider custom. Nessun impatto sulla build finale.
```csharp
Debug.DrawLine(start, end, Color.red);
Debug.DrawRay(origin, direction, Color.green);
```

---

*32 termini · 8 sezioni · E-C-H-O SYSTEMS*
