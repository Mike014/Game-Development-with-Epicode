using UnityEngine;

public class Mage : Character
{
    private const int DannoMagia = 12;
    public Mage(string nome, int vita) : base(nome, vita)
    {
    }

    public override void Attack(Character target)
    {
        int vitaPrima = target.Vita;

        Debug.Log($"{Nome} lancia una magia contro {target.Nome}! " +
                  $"Danno: {DannoMagia}. Vita target prima: {vitaPrima}");

        target.TakeDamage(DannoMagia);

        int vitaDopo = target.Vita;

        Debug.Log($"[RISULTATO] {target.Nome} ora ha {vitaDopo} punti vita.");
    }
}