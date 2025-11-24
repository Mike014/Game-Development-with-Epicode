using UnityEngine;

public class Character
{
    public string Nome { get; private set; }
    public int Vita { get; private set; }

    public Character(string nome, int vita)
    {
        this.Nome = nome;
        this.Vita = vita;
    }

    public virtual void Attack(Character target)
    {
        Debug.Log($"{Nome} attacca {target.Nome} infliggendo 1 danno (attacco base).");
        target.TakeDamage(1);
    }

    public virtual void TakeDamage(int damage)
    {
        int vitaPrima = Vita;
        Vita -= damage;
        if (Vita < 0) Vita = 0;

        Debug.Log(
            $"{Nome} subisce {damage} danni. Vita prima: {vitaPrima}, vita dopo: {Vita}"
        );
    }


















}