---
author: Piotr Żuchowski
links-as-notes: true
header-includes: |
    \usepackage{setspace}
    \usepackage{fancyhdr}
    \usepackage{titlesec}
    \usepackage{enumitem}
    \usepackage{hyperref}
    \usepackage[polish]{babel}
    \usepackage{pdfpages}
    \usepackage{graphicx}
    \usepackage{float}
    \usepackage[normalem]{ulem}
    \usepackage[nottoc]{tocbibind}

    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage{helvet}
    \renewcommand{\familydefault}{\sfdefault}
    \usepackage{amsmath}
    \usepackage{chngcntr}
    \counterwithin{figure}{section}
    \usepackage{amsmath}
    \usepackage{tocloft}
    \usepackage{nomencl}
    \makenomenclature
    \newcommand{\listequationsname}{Spis równań}
    \newlistof{myequations}{equ}{\listequationsname}
    \newcommand{\myequations}[1]{%
        \addcontentsline{equ}{myequations}{\protect\numberline{\theequation}#1}\par
    }

    \usepackage{caption}
    \captionsetup[figure]{name=Rys.}


    \usepackage{listings}
    \lstset{
        language=Python, % Wybierz język programowania
        basicstyle=\ttfamily, % Styl podstawowy
        numbers=left, % Numery linii po lewej stronie
        numberstyle=\tiny\color{gray}, % Styl numerów linii
        frame=single, % Rama wokół kodu
        breaklines=true, % Automatyczne łamanie linii
        captionpos=b, % Pozycja podpisu
        showstringspaces=false, % Nie pokazuj spacji w napisach
    }


    \usepackage{lmodern}
    \renewcommand*\familydefault{\sfdefault}

    \pagestyle{fancy}
    \fancyhead{}
    \fancyhead[LO,RE]{}
    \fancyfoot{}
    \fancyfoot[LE,RO]{\thepage}
    \fancyfoot[LO,RE]{}
    \renewcommand{\headrulewidth}{0pt}

    \setlength{\parindent}{0.5cm}
    \setlist[itemize]{label=•,itemsep=0pt}

    \titleformat{\section}{\normalfont\fontsize{16}{18}\bfseries}{\thesection}{1em}{}
    \titleformat{\subsection}{\normalfont\fontsize{14}{16}\bfseries}{\thesubsection}{1em}{}
    \titleformat{\subsubsection}{\normalfont\fontsize{13}{15}\bfseries}{\thesubsubsection}{1em}{}

    \newcommand{\MMp}[1]{\marginpar{\textcolor{blue}{\textbf{MM}: \footnotesize #1}}}
    \newcommand{\MM}[1]{\textcolor{blue}{\textbf{MM}: #1}}
---


# Sekcja

## podsekcja

Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis.

wiecej w pracy chen,[@chen1993joint]

wiecej w pracy chen,[@box1975intervention]

wiecej w pracy chen,[@chomatek2017multiobjective]

wiecej w pracy chen,[@docker-docs]

wiecej w pracy chen,[@python-docs]

wiecej w pracy chen,[@numpy-docs]

wiecej w pracy chen,[@pandas-docs]

wiecej w pracy chen,[@statsmodels-docs]

wiecej w pracy chen,[@grafana-docs]

wiecej w pracy chen,[@thakkar2016survey]

wiecej w pracy chen,[@akouemo2016probabilistic]

wiecej w pracy chen,[@chandola2008comparative]

wiecej w pracy chen,[@talk]

ksiażka [@kaiser1999seasonal]

Duraj [@duraj2021outlier]

Duraj [@wykrywanie-wyjatkow]

```bash
echo "slieal" | base64

```

```{.python caption="Python Code" label=lst:example}
print("Hello, World!")
````


# Bibliografia
