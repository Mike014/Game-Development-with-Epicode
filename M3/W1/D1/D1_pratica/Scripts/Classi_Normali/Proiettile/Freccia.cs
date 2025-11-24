using UnityEngine;

public class Freccia : Proiettile
{
    public int NumeroFrecceSimultanee;

    // In questo modo stiamo ereditando il costruttore della classe Proiettile con base()
    public Freccia(float velocità, float gittata, int numeroFrecce)
        : base(velocità, gittata)
    {
        NumeroFrecceSimultanee = numeroFrecce;
    }
    
    
    // Funzione ereditata dalla superclasse e sovrascritta con override
    public override void Lancia()
    {
        Debug.Log($"[FRECCIA] Scoccate {NumeroFrecceSimultanee} frecce simultanee " +
                  $"a velocità {Velocità} e gittata {Gittata}.");

        Debug.Log($"[INFO] Il proiettile Freccia è stato lanciato a velocità {Velocità}.");
    }
}
