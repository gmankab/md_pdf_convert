# md to pdf convert

run on local machine

1. put your .md files in md dir
2. install distrobox
```shell
distrobox create -i docker.io/ubuntu:latest -n ubuntu
curl -L github.com/jgm/pandoc/releases/download/3.1.12.2/pandoc-3.1.12.2-1-amd64.deb -o /tmp/pandoc.deb
distrobox enter ubuntu -- sudo apt install texlive-latex-recommended texlive-fonts-recommended texlive-xetex fonts-open-sans /tmp/pandoc.deb
distrobox enter ubuntu -- python3 convert.py
```

run on github actions

1. clone repo
2. put your .md files in md dir
3. commit and push changes
4. .pdf and .typ files will appear on releases page

