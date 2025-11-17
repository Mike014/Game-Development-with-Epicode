using System;
using UnityEngine;

public class Archer : Character
{
    private const int DannoFreccia = 7;
    private const int NumeroFrecce = 2;

    public Archer(string nome, int vita) : base(nome, vita)
    {
    }

    public override void Attack(Character target)
    {
        Debug.Log($"{Nome} attacca {target.Nome} scagliando {NumeroFrecce} frecce!");

        for (int i = 1; i <= NumeroFrecce; i++)
        {
            int vitaPrima = target.Vita;

            // Debug.Log aggiuntivo: numero freccia + danno
            Debug.Log($"Freccia n°{i} lanciata da {Nome}. " +
                      $"Danno: {DannoFreccia}. Vita target prima: {vitaPrima}");

            target.TakeDamage(DannoFreccia);

            int vitaDopo = target.Vita;
            Debug.Log($"[RISULTATO FRECCIA {i}] {target.Nome} ora ha {vitaDopo} punti vita.");
        }
    }
}