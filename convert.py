#!/bin/env python3

from pathlib import Path
import subprocess
import shutil


def md_to_typ(
    source_dir: Path,
    target_dir: Path,
):
    additional_text = '''\
#set text(font: "Inter")
#show link: set text(blue)
'''
    if target_dir.exists():
        shutil.rmtree(
            path=target_dir,
        )
    target_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    source_file: Path = Path()
    for source_file in source_dir.iterdir():
        target_file = target_dir / f'{source_file.stem}.typ'
        print(
            f'converting {source_file} to {target_file}'
        )
        result = subprocess.run(
            ['pandoc', source_file, '--to=typst', '--output=/dev/stdout', '--wrap=none'],
            capture_output=True,
            check=True,
            text=True,
        )
        output = result.stdout
        with target_file.open('w', encoding = 'utf-8') as file:
            file.write(additional_text + '\n' + output)


def typ_to_pdf(
    source_dir: Path,
    target_dir: Path,
    fonts_dir: Path,
):
    if target_dir.exists():
        shutil.rmtree(
            path=target_dir,
        )
    target_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    source_file: Path = Path()
    for source_file in source_dir.iterdir():
        target_file = target_dir / f'{source_file.stem}.pdf'
        print(
            f'converting {source_file} to {target_file}'
        )
        subprocess.run(
            ['typst', 'compile', source_file, target_file, f'--font-path={fonts_dir}'],
            check=True,
        )


def main(
    repo_path: Path | None = None,
):
    if not repo_path:
        repo_path = Path(__file__).parent.resolve()
    md_path = repo_path / 'md'
    typ_path = repo_path / 'typ'
    pdf_path = repo_path / 'pdf'
    fonts_dir = repo_path / 'fonts'
    md_to_typ(
        source_dir=md_path,
        target_dir=typ_path,
    )
    typ_to_pdf(
        source_dir=typ_path,
        target_dir=pdf_path,
        fonts_dir=fonts_dir,
    )
    

if __name__ == '__main__':
    main()

