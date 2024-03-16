#!/bin/env python3

from pathlib import Path
import urllib.request
import subprocess
import tempfile
import tarfile
import shutil


font_size = '8.8pt'
font = 'Inter'


def md_to_typ(
    source_dir: Path,
    target_dir: Path,
):
    additional_text = f'''\
#set text(
    font: "{font}",
    size: {font_size},
)
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
        while r'https:\/\/' in output:
            output = output.replace(
                r'https:\/\/',
                'https://',
            )
        with target_file.open(
            'w',
            encoding='utf-8',
        ) as file:
            file.write(additional_text + '\n' + output)


def typ_to_pdf(
    typst_path: Path,
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
            [typst_path, 'compile', source_file, target_file, f'--font-path={fonts_dir}'],
            check=True,
        )


def download_typst(
    data_dir: Path,
) -> Path:
    data_dir.mkdir(
        exist_ok=True,
        parents=True,
    )
    typst_exec_dst = data_dir / 'typst'
    if typst_exec_dst.exists():
        return typst_exec_dst
    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir_path = Path(tmp_dir_str)
        typst_archive_file = tmp_dir_path / 'typst.tar.xz'
        typst_unpacked_dir = tmp_dir_path / 'typst_dir'
        download(
            url = 'https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz',
            file_path = typst_archive_file,
        )
        with tarfile.open(
            name=typst_archive_file,
            mode='r:xz',
        ) as file:
            file.extractall(path=typst_unpacked_dir)
        typst_exec_src = typst_unpacked_dir / 'typst-x86_64-unknown-linux-musl' / 'typst'
        assert typst_exec_src.exists()
        shutil.copyfile(
            src=typst_exec_src,
            dst=typst_exec_dst,
        )
    typst_exec_dst.chmod(0o755)
    return typst_exec_dst


def download(
    url: str,
    file_path: Path,
):
    response = urllib.request.urlopen(url)
    total_size = int(
        response.headers.get('content-length', 0)
    )
    block_size = 1024 * 8
    count = 0
    with file_path.open('wb') as file:
        while True:
            chunk = response.read(block_size)
            if not chunk:
                break
            file.write(chunk)
            count += 1
            done = count * block_size
            percent_done = done * 100 // total_size
            print(
                f'\rdownloading typst: {percent_done}%',
                flush=True,
                end = '',
            )
    print()


def main(
    repo_path: Path | None = None,
):
    if not repo_path:
        repo_path = Path(__file__).parent.resolve()
    md_dir: Path = repo_path / 'md'
    typ_dir: Path = repo_path / 'typ'
    pdf_dir: Path = repo_path / 'pdf'
    fonts_dir: Path = repo_path / 'fonts'
    data_dir: Path = repo_path / 'converter_data'
    is_typst = shutil.which('typst')
    if is_typst:
        typst_path: Path = Path(is_typst)
    else:
        typst_path: Path = download_typst(
            data_dir=data_dir,
        )
    md_to_typ(
        source_dir=md_dir,
        target_dir=typ_dir,
    )
    typ_to_pdf(
        typst_path=typst_path,
        source_dir=typ_dir,
        target_dir=pdf_dir,
        fonts_dir=fonts_dir,
    )
    

if __name__ == '__main__':
    main()

