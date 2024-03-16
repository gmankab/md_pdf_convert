#!/bin/env python3

from pathlib import Path
import subprocess


repo_path = Path(__file__).parent.resolve()
md_path = repo_path / 'md'
typ_path = repo_path / 'typ'
pdf_path = repo_path / 'pdf'


def convert(
    source_dir: Path,
    target_dir: Path,
    args: list[str] = [],
):
    target_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    source_file: Path = Path()
    for source_file in source_dir.iterdir():
        target_file = target_dir / f'{source_file.stem}.{target_dir.name}'
        print(
            f'converting {source_file} to {target_file}'
        )
        subprocess.run(
            ['pandoc', source_file, '-o', target_file] + args,
            check=True,
        )


def main():
    convert(
        source_dir=md_path,
        target_dir=typ_path,
    )
    convert(
        source_dir=typ_path,
        target_dir=pdf_path,
        args=['--pdf-engine=xelatex', '-V', 'mainfont="OpenSans"']
    )
    

main()

