using UnityEngine;

public class BattleTest : MonoBehaviour
{
    void Start()
    {
        Warrior warrior = new Warrior("Conan", 100);
        Mage mage = new Mage("Merlin", 80);
        Archer archer = new Archer("Legolas", 70);

        warrior.Attack(mage);
        mage.Attack(warrior);
        archer.Attack(warrior);
    }
}