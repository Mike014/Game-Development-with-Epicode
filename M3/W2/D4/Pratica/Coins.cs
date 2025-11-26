using UnityEngine;

public class Coin : MonoBehaviour
{
    // di solito è 1... ma la lascio modificabile, non si sa mai
    public int valoreCoin = 1;

    private void OnTriggerEnter2D(Collider2D other)
    {
        // provo a prendere il gestore coins dal player
        CoinsHandler handler = other.GetComponent<CoinsHandler>();

        if (handler != null)
        {
            // aggiungo la coin... easy
            handler.AggiungiCoin(valoreCoin);

            // distruggo questo oggetto, così sparisce dalla scena
            Destroy(this.gameObject);
        }
    }
}
