using System.Collections.Generic;
using UnityEngine;

public class RPGManager : MonoBehaviour
{
    private List<Character> characters = new List<Character>();

    void Start()
    {
        characters.Add(new Warrior("Conan", 100));
        characters.Add(new Mage("Merlin", 80));
        characters.Add(new Archer("Legolas", 70));

        foreach (Character c in characters)
        {
            Debug.Log($"[PRIMA] {c.Nome} ha {c.Vita} punti vita prima dell’azione.");

            c.Attack(c);

            int randomDamage = Random.Range(1, 21);  

            Debug.Log($"[DANNO RANDOM] {c.Nome} riceve un danno casuale di {randomDamage}.");

            c.TakeDamage(randomDamage);

            Debug.Log($"[DOPO] {c.Nome} ora ha {c.Vita} punti vita.");
            Debug.Log("------------------------------------------------------");
        }
    }
}

