using UnityEngine;

public class LifeController : MonoBehaviour
{
    // La vita del giocatore
    public int health = 10;

    // riferimento oggetto da distruggere
    private GameObject oggettoDaDistruggere;


    void Start()
    {
        // assegna il gameObject
        oggettoDaDistruggere = this.gameObject;
    }

    public void TakeDamage(int damage)
    {
        
        // tolgo la vita 
        health -= damage;

        // stampa della vita
        Debug.Log("Vita attuale del giocatore: " + health);

        // se la vita è <= 0... allora ciaone
        if (health <= 0)
        {
            Debug.Log("Il giocatore è stato sconfitto");

            // qui distruggo proprio l'oggetto
            Destroy(oggettoDaDistruggere);
        }
    }

    public void TakeHeal(int amount)
    {
        // curo il giocatore un po'... ma senza esagerare
        health += amount;

        // stampo così vedo se funziona
        Debug.Log("Vita attuale del giocatore: " + health);
    }
}