using UnityEngine;

public abstract class ProiettileAbstract
{
    public float Velocita;

    public ProiettileAbstract(float velocità)
    {
        Velocita = velocità;
    }

    public abstract void Lancia();
}

// Una classe astratta in C# è un 
// concetto fondamentale della programmazione orientata agli oggetti e serve a definire un modello, 
// una struttura, un comportamento comune, senza permettere di creare direttamente un’istanza di quella classe.
// Una classe astratta:
// - non può essere istanziata
// - definisce un comportamento comune
// - contiene metodi astratti che le sottoclassi devono implementare
// - evita duplicazioni
// - rappresenta concetti generici (non concreti)