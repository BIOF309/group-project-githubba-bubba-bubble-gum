import pypandoc, doctest

def write_file(filename: str, contents: str) -> None:
    with open(filename, 'w') as f:
        f.write(contents)


slides = pypandoc.convert_file('Final_Project.md', to = 'slidy', extra_args=['-s'])
#slides = pypandoc.convert_file('Final_Project.md', to='revealjs', extra_args=['-s', '-V', 'revealjs-url=http://lab.hakim.se/reveal-js', '-V', 'theme=sky'])

write_file('Final_Project.html', slides)


