using UnityEngine;

public class CoinsHandler : MonoBehaviour
{
    // qui tengo i coins...
    public int coins = 0;

    public void AggiungiCoin(int quantoAggiungo)
    {
        coins += quantoAggiungo;
        Debug.Log("Coins attuali: " + coins);
    }
}

