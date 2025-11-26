using UnityEngine;

public class Bomb : MonoBehaviour
{
    // quanto danno fa... modificabile a piacere
    public int damage = 1;

    private void OnTriggerEnter2D(Collider2D other)
    {
        // prendo il LifeController del player... sperando che esista
        LifeController vita = other.GetComponent<LifeController>();

        if (vita != null)
        {
            // ok, gli faccio del male...
            vita.TakeDamage(damage);

            // e poi sparisco
            Destroy(this.gameObject);
        }
    }
}
