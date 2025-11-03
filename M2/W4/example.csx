// 2) Eseguire “al volo” senza progetto (script .csx)

// Perfetto per snippet/esperimenti.

// Installa lo strumento:

// Bash: dotnet tool install -g dotnet-script


// Assicurati che ~/.dotnet/tools sia nel PATH (su Git Bash aggiungi al tuo .bashrc):

// Bash: export PATH="$PATH:$HOME/.dotnet/tools"


// Crea ed esegui uno script:

// printf 'Console.WriteLine("Ciao!");' > hello.csx
// Bash: dotnet script hello.csx

using System;

//Funzioni

void IncrementaByValue(int n)
{
    n++;
}

void IncrementaByRef(ref int n)
{
    n++;
}
