# SC2005 study guide

Open **study guide.pdf** to read the guide. The LaTeX project has three parts:

- **study guide.tex** contains the chapters, ELI5 explanations, Theory and More theory pages, two worked examples per chapter, and practice solutions.
- **mermaid/** contains the editable Mermaid sources.
- **mermaid/rendered/** contains the vector PDF figures that LaTeX includes.

Keep the folder structure when moving the project. Compile from this directory with:

```sh
tectonic "study guide.tex"
```

Alternatively, run `xelatex "study guide.tex"` twice to refresh the topic map and links. The included figure PDFs let you build with an installed TeX distribution without running Mermaid first. After editing a Mermaid source, export it to PDF at the matching path under `mermaid/rendered/` and recompile the guide.

Gantt sources encode elapsed time as seconds after midnight on 1 January 1970. The date is a rendering anchor. Use the numerical intervals in each worked example for the exercise's time units.
