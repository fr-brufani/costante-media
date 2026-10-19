# costante-media

Le immagini e i video **approvati e pronti da pubblicare** dei clienti di costante., messi online perché Metricool li possa prendere da un link pubblico.

Il lavoro vero (copy, sorgenti, versioni scartate) resta nel progetto privato dell'agenzia. Qui finisce solo ciò che sta per uscire sui social, quindi niente di riservato: niente bozze, niente materiale grezzo, niente dati dei clienti.

## Struttura

Stessa struttura del progetto dell'agenzia, così da un file si risale subito al lavoro:

```
clienti/<cliente>/<servizio>/<AAAA-MM-GG>_<lavoro>/
    slide_01.png
    slide_02.png
    ...
```

Esempio: `clienti/costante/post/2026-11-02_chi-siamo/slide_01.png`

Il link pubblico di un file è:

```
https://raw.githubusercontent.com/fr-brufani/costante-media/main/clienti/<cliente>/<servizio>/<lavoro>/<file>
```

## Come si carica

Dal progetto dell'agenzia:

```sh
python3 ~/Desktop/costante-media/strumenti/carica.py "<cartella del lavoro sotto clienti/>"
```

Copia le slide di `carosello/` (o i file di `out/` per i video), fa commit e push, controlla che ogni link risponda e stampa l'elenco dei link da passare a Metricool.

## Regole

- Si carica solo ciò che è approvato e sta per essere programmato.
- Un file caricato non si sovrascrive mai: se il post cambia, si ricarica con un nome di lavoro nuovo, perché un post già programmato potrebbe puntare al vecchio link.
