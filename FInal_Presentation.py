import pypandoc, doctest

def write_file(filename: str, contents: str) -> None:
    with open(filename, 'w') as f:
        f.write(contents)


slides = pypandoc.convert_file('Final_Project.md', to = 'dzslides', extra_args=['-s'])

write_file('Final_Project.html', slides)
