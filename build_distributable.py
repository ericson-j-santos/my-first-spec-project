"""
build_distributable.py
======================
Execute NESTE PC para gerar o script distribuivel.

Uso:
    python build_distributable.py               # empacota o diretorio atual
    python build_distributable.py ./outra-pasta # empacota outra pasta
    python build_distributable.py . -o meu_dist.py --zip meu_projeto.zip

O arquivo de saida (padrao: distribuir.py) pode ser enviado para qualquer
PC com Python 3.6+ e, ao ser executado la, gera o ZIP do projeto.
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

# Pastas e extensoes ignoradas ao varrer o projeto
IGNORE_DIRS = {
    ".git", ".svn", ".hg",
    ".venv", "venv", "env", ".env",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "node_modules", ".next", "dist", "build",
    ".idea", ".vscode", ".vs",
}
IGNORE_EXTS = {".pyc", ".pyo", ".pyd", ".egg-info"}


# ---------------------------------------------------------------------------
# Coleta de arquivos
# ---------------------------------------------------------------------------

def collect_files(root: Path, output_script: str) -> dict[str, str]:
    """Retorna {caminho_relativo: conteudo_base64} para todos os arquivos validos."""
    result = {}
    skipped = []
    output_name = Path(output_script).name  # nao incluir o proprio distribuidor

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        # Ignora pastas proibidas em qualquer nivel da arvore
        if any(part in IGNORE_DIRS for part in path.parts):
            skipped.append(str(path))
            continue

        # Ignora extensoes proibidas
        if path.suffix.lower() in IGNORE_EXTS:
            skipped.append(str(path))
            continue

        # Ignora o proprio script gerado (evita recursao)
        if path.name == output_name or path.name == Path(__file__).name:
            continue

        rel = path.relative_to(root).as_posix()

        try:
            data = path.read_bytes()
            result[rel] = base64.b64encode(data).decode("ascii")
        except (PermissionError, OSError) as exc:
            print(f"  [AVISO] Nao foi possivel ler '{rel}': {exc}", file=sys.stderr)

    if skipped:
        print(f"  Ignorados: {len(skipped)} item(s) (git, venv, cache, etc.)")

    return result


# ---------------------------------------------------------------------------
# Geracao do script distribuivel
# ---------------------------------------------------------------------------

TEMPLATE = '''\
#!/usr/bin/env python3
"""
{script_name}
{separator}
Script auto-contido gerado por build_distributable.py.
Execute em qualquer PC com Python 3.6+ para criar o ZIP do projeto.

Uso:
    python {script_name}                 # cria {zip_name} no diretorio atual
    python {script_name} -o outro_nome.zip
"""

import argparse
import base64
import json
import sys
import zipfile
from pathlib import Path

ZIP_DEFAULT = "{zip_name}"
FILE_COUNT  = {file_count}

# Dados dos arquivos (base64-encoded JSON)
_DATA = {data_repr}


def _decode_files() -> dict:
    return json.loads(_DATA)


def create_zip(dest: Path) -> None:
    files = _decode_files()
    print(f"Criando {{dest.name}} com {{FILE_COUNT}} arquivo(s)...")
    print()

    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel_path, b64 in files.items():
            data = base64.b64decode(b64)
            zf.writestr(rel_path, data)
            print(f"  [+] {{rel_path}}")

    size_kb = dest.stat().st_size / 1024
    print()
    print(f"ZIP criado   : {{dest.resolve()}}")
    print(f"Tamanho      : {{size_kb:.1f}} KB")
    print(f"Arquivos     : {{FILE_COUNT}}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera o ZIP do projeto.")
    parser.add_argument("-o", "--output", default=ZIP_DEFAULT,
                        help=f"Nome do ZIP de saida (padrao: {{ZIP_DEFAULT}})")
    args = parser.parse_args()

    dest = Path(args.output)
    if dest.exists():
        resp = input(f"Arquivo '{{dest}}' ja existe. Sobrescrever? (s/N): ").strip().lower()
        if resp != "s":
            print("Cancelado.")
            sys.exit(0)

    create_zip(dest)


if __name__ == "__main__":
    main()
'''


def generate_distributor(
    files: dict[str, str],
    output_script: str = "distribuir.py",
    zip_name: str = "projeto.zip",
) -> None:
    script_name = Path(output_script).name
    data_repr = repr(json.dumps(files, ensure_ascii=True))

    content = TEMPLATE.format(
        script_name=script_name,
        separator="=" * len(script_name),
        zip_name=zip_name,
        file_count=len(files),
        data_repr=data_repr,
    )

    Path(output_script).write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera um script Python auto-contido que recria o ZIP do projeto."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=".",
        help="Pasta raiz do projeto a empacotar (padrao: diretorio atual)",
    )
    parser.add_argument(
        "-o", "--output",
        default="distribuir.py",
        help="Nome do script distribuivel a gerar (padrao: distribuir.py)",
    )
    parser.add_argument(
        "--zip",
        default="projeto.zip",
        help="Nome do ZIP que sera criado ao executar o distribuivel (padrao: projeto.zip)",
    )
    args = parser.parse_args()

    root = Path(args.source).resolve()
    if not root.is_dir():
        print(f"ERRO: '{args.source}' nao e um diretorio valido.", file=sys.stderr)
        sys.exit(1)

    print(f"Coletando arquivos de: {root}")
    files = collect_files(root, args.output)

    if not files:
        print("Nenhum arquivo encontrado. Verifique o caminho informado.")
        sys.exit(1)

    print(f"  Arquivos coletados: {len(files)}")
    print()

    print(f"Gerando script distribuivel: {args.output}")
    generate_distributor(files, args.output, args.zip)

    size_kb = Path(args.output).stat().st_size / 1024
    print(f"  Tamanho do script : {size_kb:.1f} KB")
    print()
    print("Pronto!")
    print(f"  Envie '{args.output}' para o outro PC e execute:")
    print(f"      python {args.output}")
    print(f"  O arquivo '{args.zip}' sera criado la.")


if __name__ == "__main__":
    main()
