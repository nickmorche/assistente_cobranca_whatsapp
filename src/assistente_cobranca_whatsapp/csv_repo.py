import csv
from pathlib import Path

CSV_PATH = Path("contatos.csv")


def carregar_contatos() -> list[dict]:
    contatos = []

    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contatos.append({
                "nome": row["nome_completo"].strip(),
                "telefone": row["telefone"].strip(),
                "pagou": row["pagou"].lower() == "true",
            })

    return contatos


def salvar_contatos(contatos: list[dict]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["nome_completo", "telefone", "pagou"]
        )
        writer.writeheader()

        for c in contatos:
            writer.writerow({
                "nome_completo": c["nome"],
                "telefone": c["telefone"],
                "pagou": str(c["pagou"]).lower(),
            })