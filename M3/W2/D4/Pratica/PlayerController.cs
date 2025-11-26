using UnityEngine;

public class PlayerController : MonoBehaviour
{
    // Velocità del player
    public float velocitaMovimento = 5f;

    // riferimento rigidBody
    private Rigidbody2D mioRb; 

    void Start()
    {
        // prendo rigidbody
        mioRb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        // Movimento del player
        float movimentoX = Input.GetAxisRaw("Horizontal");
        float movimentoY = Input.GetAxisRaw("Vertical");

        // vettore che poi passa al rigidbody
        Vector2 direzioneDaSeguire = new Vector2(movimentoX, movimentoY).normalized;

        // applico la velocità al rigidbody 
        mioRb.velocity = direzioneDaSeguire * velocitaMovimento;
    }
}