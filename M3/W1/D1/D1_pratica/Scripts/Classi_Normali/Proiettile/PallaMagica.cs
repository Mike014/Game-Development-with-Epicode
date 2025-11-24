using UnityEngine;

public class PallaMagica : Proiettile
{
    public int MaxRimbalzi;

    public PallaMagica(float velocità, float gittata, int maxRimbalzi)
        : base(velocità, gittata)
    {
        MaxRimbalzi = maxRimbalzi;
    }

    public override void Lancia()
    {
        int rimbalzi = Random.Range(0, MaxRimbalzi + 1);

        Debug.Log($"[PALLA MAGICA] La palla ha rimbalzato {rimbalzi} volte, " +
                  $"a velocità {Velocità}, raggiungendo altezza (gittata) {Gittata}.");

        Debug.Log($"[INFO] Il proiettile PallaMagica è stato lanciato a velocità {Velocità}.");
    }
}
