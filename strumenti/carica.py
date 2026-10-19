#!/usr/bin/env python3
"""Carica su costante-media le slide (o i video) di un lavoro e stampa i link pubblici per Metricool.

Uso:
  carica.py <cartella-lavoro>     # es. ".../clienti/costante/post/2026-11-02_chi-siamo"

La cartella deve stare sotto clienti/<cliente>/<servizio>/<lavoro>/ del progetto dell'agenzia.
Prende carosello/slide_*.png; se non ci sono, i file di out/. Stampa i link in JSON su stdout.
"""
import filecmp, glob, json, os, shutil, subprocess, sys, time, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://raw.githubusercontent.com/fr-brufani/costante-media/main"
FORMATI = (".png", ".jpg", ".jpeg", ".mp4", ".mov")


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True, text=True).stdout


def percorso_relativo(cartella):
    parti = os.path.abspath(cartella).rstrip("/").split(os.sep)
    if "clienti" not in parti:
        sys.exit("La cartella deve stare sotto clienti/<cliente>/<servizio>/<lavoro>/")
    i = len(parti) - 1 - parti[::-1].index("clienti")
    resto = parti[i:]
    if len(resto) != 4:
        sys.exit(f"Mi aspetto clienti/<cliente>/<servizio>/<lavoro>, trovato: {'/'.join(resto)}")
    return "/".join(resto)


def file_del_lavoro(cartella):
    slide = sorted(glob.glob(os.path.join(cartella, "carosello", "slide_*.png")))
    if slide:
        return slide
    return sorted(p for p in glob.glob(os.path.join(cartella, "out", "*")) if p.lower().endswith(FORMATI))


def risponde(url):
    try:
        return urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=20).status == 200
    except Exception:
        return False


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit(__doc__)
    cartella = sys.argv[1]
    rel = percorso_relativo(cartella)
    sorgenti = file_del_lavoro(cartella)
    if not sorgenti:
        sys.exit(f"Niente da caricare in {cartella} (né carosello/slide_*.png né out/)")

    git("pull", "-q", "--rebase", "origin", "main")
    dest = os.path.join(REPO, rel)
    os.makedirs(dest, exist_ok=True)
    for p in sorgenti:
        d = os.path.join(dest, os.path.basename(p))
        if os.path.exists(d) and not filecmp.cmp(p, d, shallow=False):
            sys.exit(f"{rel}/{os.path.basename(p)} esiste già ed è diverso: un file caricato non si sovrascrive. "
                     "Ricarica il post con un nome di lavoro nuovo.")
        shutil.copy2(p, d)

    git("add", rel)
    if git("status", "--porcelain", rel).strip():
        git("commit", "-q", "-m", f"{rel}: {len(sorgenti)} file da pubblicare")
        git("push", "-q", "origin", "main")

    urls = [f"{BASE_URL}/{rel}/{os.path.basename(p)}" for p in sorgenti]
    mancanti = urls
    for _ in range(12):  # raw.githubusercontent può metterci qualche secondo
        mancanti = [u for u in mancanti if not risponde(u)]
        if not mancanti:
            break
        time.sleep(5)
    if mancanti:
        sys.exit("Questi link non rispondono ancora:\n" + "\n".join(mancanti))
    print(json.dumps(urls, indent=2))


if __name__ == "__main__":
    main()
