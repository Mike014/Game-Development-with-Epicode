using UnityEngine;

public class Heal : MonoBehaviour
{
    // amount della cura... lo cambio da Inspector
    public int healAmount = 1;

    private void OnTriggerEnter2D(Collider2D other)
    {
        // anche qui prendo LifeController dal player
        LifeController vita = other.GetComponent<LifeController>();

        if (vita != null)
        {
            vita.TakeHeal(healAmount);

            // una volta curato, sparisco
            Destroy(this.gameObject);
        }
    }
}
