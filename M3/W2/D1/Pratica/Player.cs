using UnityEngine;

public class Player : MonoBehaviour
{
    [SerializeField] private float speed = 5f;
    [SerializeField] private float jumpForce = 7f;

    private Rigidbody rb;
    private float inputX;
    private float inputY;
    private bool isJumping = false;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    private void Update()
    {
        // Prendere gli input SEMPRE in Update
        inputX = Input.GetAxisRaw("Vertical");
        inputY = Input.GetAxisRaw("Horizontal");

        if (Input.GetButtonDown("Jump") && !isJumping)
        {
            isJumping = true;
        }
    }

    private void FixedUpdate()
    {
        // Movimento orizzontale (X)
        rb.velocity = new Vector3(inputX * speed, rb.velocity.y, 0f);
        
        // Movimento verticale (Y)
        rb.velocity = new Vector3(rb.velocity.x, rb.velocity.y, inputY * speed);

        // Salto
        if (isJumping)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
            isJumping = false;
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        // Se tocchi il terreno o piattaforma, puoi saltare di nuovo
        if (collision.gameObject.CompareTag("Ground"))
        {
            isJumping = false;
        }
    }
}

