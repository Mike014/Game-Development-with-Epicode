using UnityEditor.AssetImporters;
using UnityEngine;

public class MoveSquare : MonoBehaviour
{
    [SerializeField] private float speed = 5f;
    [SerializeField] private float maxDistance = 5f;
    private Rigidbody2D rb;
    private Vector2 input;
    private Vector3 startPosition;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        // Quando parte il gioco, salvo la posizione originale
        startPosition = transform.position;
    }

    void Update()
    {
        // Leggo l'input WASD (Horizontal = A/D, Vertical = W/S)
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");

        input = new Vector2(h, v);
    }

    void FixedUpdate()
    {
        // Movimento fisico
        rb.velocity = input * speed;

        // Distanza dallo start 
        float distance = Vector3.Distance(transform.position, startPosition);
        
        if (distance > maxDistance)
        {
            // Riporto il quadrato alla posizione iniziale
            rb.position = startPosition;
            rb.velocity = Vector2.zero; // per sicurezza blocco il movimento
        }
    }
}


// Update() → leggiamo input (meglio leggere qui)
// FixedUpdate() → applichiamo la fisica (velocity)
// Usa velocity in modo da avere movimento corretto su X e Y
// Nessun deltaTime → velocity è già "al secondo"

