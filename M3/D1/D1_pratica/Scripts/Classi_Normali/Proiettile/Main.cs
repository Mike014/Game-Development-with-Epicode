// contiene collezioni generiche, cioè strutture dati che puoi usare per memorizzare insiemi di oggetti in modo tipizzato, sicuro e performante.
using System.Collections.Generic;
using UnityEngine;

public class GestoreProiettili : MonoBehaviour
{
    private List<Proiettile> listaProiettili = new List<Proiettile>();

    void Start()
    {
        Freccia f1 = new Freccia(20f, 50f, 3);
        PallaMagica p1 = new PallaMagica(10f, 30f, 5);

        listaProiettili.Add(f1);
        listaProiettili.Add(p1);

        foreach (var proiettile in listaProiettili)
        {
            proiettile.Lancia();
        }
    }
}