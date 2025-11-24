using UnityEngine;

public class MovimentoDeltaTime : MonoBehaviour
{
    [SerializeField] private float speed = 5f;

    void Update()
    {
        // 1) Leggo l'input (A/D o frecce sinistra/destra)
        float inputX = Input.GetAxis("Horizontal");   // -1 .. 1
        float inputZ = Input.GetAxis("Vertical");     // -1 .. 1

        // 2) Costruisco il vettore direzione sul piano XZ
        Vector3 direction = new Vector3(inputX, 0f, inputZ);

        // 3) Normalizzo per evitare che in diagonale sia più veloce
        if (direction.sqrMagnitude > 0f)
        {
            direction = direction.normalized;
        }

        // 4) Calcolo lo spostamento: velocità * tempo
        Vector3 movement = direction * speed * Time.deltaTime;

        // 5) Applico lo spostamento alla posizione
        transform.position = transform.position + movement;
    }
}
