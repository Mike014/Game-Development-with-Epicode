using UnityEngine;

public class Warrior : Character
{
    private const int DannoSpada = 10;

    public Warrior(string nome, int vita) : base(nome, vita)
    {
        // ---
    }

    public override void Attack(Character target)
    {
        int vitaPrima = target.Vita;

        Debug.Log($"{Nome} colpisce {target.Nome} con la spada! " +
                  $"Danno: {DannoSpada}. Vita target prima: {vitaPrima}");

        target.TakeDamage(DannoSpada);

        int vitaDopo = target.Vita;

        Debug.Log($"[RISULTATO] {target.Nome} ora ha {vitaDopo} punti vita.");
    }
}