# md to pdf convert


## run on github actions

1. fork repo
2. go to https://github.com/YOUR_USERNAME/md_pdf_convert/settings/actions -> workflow permissions -> click read and write permissions -> save
3. put your .md files in md dir
4. commit and push changes
5. .pdf and .typ files will appear on releases page

## run on local machine

1. clone repo:
```shell
git clone https://github.com/gmankab/md_pdf_convert
```
2. put your .md files in md dir
3. [install distrobox](https://github.com/89luca89/distrobox#installation)
4. create arch distrobox:
```shell
distrobox create -i docker.io/archlinux:latest -n arch
```
5. install dependencies:
```shell
distrobox enter arch -- sudo pacman -Syu --noconfirm pandoc typst
```
6. run converter:
```shell
distrobox enter arch -- python convert.py
```

## faq

#### q: how to run on windows?

a: use wsl or use [github actions](#run-on-github-actions)

#### q: how to chane font and font size?

a: see line 11 in convert.py

