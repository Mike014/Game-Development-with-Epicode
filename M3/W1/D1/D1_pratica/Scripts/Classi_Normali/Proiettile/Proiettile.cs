using UnityEngine;

// Classe Base
public class Proiettile
{
    public float Velocità;
    public float Gittata;

    public Proiettile(float velocità, float gittata)
    {
        this.Velocità = velocità;
        this.Gittata = gittata;
    }
    
    // Funzione che verrà ereditata e sovrascritta nelle sottoclassi
    public virtual void Lancia()
    {

    }
}