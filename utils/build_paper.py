import argparse
import json
import re
import subprocess
from pathlib import Path


def _slugify(title: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return slug


def _run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a manuscript PDF from paper.json.")
    parser.add_argument(
        "--paper",
        default="manuscript/paper.json",
        help="Path to paper.json (default: manuscript/paper.json)",
    )
    parser.add_argument(
        "--skip-bibtex",
        action="store_true",
        help="Skip running bibtex",
    )
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.is_file():
        raise FileNotFoundError(f"Missing paper config: {paper_path}")

    paper = json.loads(paper_path.read_text(encoding="utf-8"))
    title = paper.get("title", "").strip()
    slug = paper.get("slug", "").strip()
    main_tex = paper.get("main_tex", "manuscript/tex/main.tex")
    build_dir = paper.get("build_dir", "manuscript/build")

    if not slug:
        if not title:
            raise ValueError("paper.json must include either 'slug' or 'title'")
        slug = _slugify(title)

    main_tex_path = Path(main_tex)
    if not main_tex_path.is_file():
        raise FileNotFoundError(f"Missing main.tex: {main_tex_path}")

    build_dir_path = Path(build_dir)
    build_dir_path.mkdir(parents=True, exist_ok=True)

    pdflatex = "pdflatex"
    jobname_arg = f"-jobname={slug}"
    output_arg = f"-output-directory={build_dir_path.as_posix()}"

    _run([pdflatex, jobname_arg, output_arg, main_tex_path.as_posix()])

    if not args.skip_bibtex:
        _run(["bibtex", slug], cwd=build_dir_path.as_posix())

    _run([pdflatex, jobname_arg, output_arg, main_tex_path.as_posix()])
    _run([pdflatex, jobname_arg, output_arg, main_tex_path.as_posix()])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
