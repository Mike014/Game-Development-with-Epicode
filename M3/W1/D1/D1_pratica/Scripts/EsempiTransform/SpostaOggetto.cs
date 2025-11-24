using UnityEngine;

public class MuoviOggetto : MonoBehaviour
{
    void Update()
    {
        // Se premo la barra spaziatrice
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // Prendo la posizione attuale
            Vector3 nuovaPosizione = transform.position;

            // Modifica la posizione (mi muovo di 1 sull'asse X)
            nuovaPosizione.x += 1;

            // Applica la nuova posizion al Transform
            transform.position = nuovaPosizione;

            Debug.Log("Oggetto Spostato!");
        }
    }
}

