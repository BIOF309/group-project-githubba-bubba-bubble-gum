import pypandoc
import doctest

def write_file(filename: str, contents: str) -> None:
    with open(filename, 'w') as f:
        f.write(contents)

def make_slides(path: str = 'FInal_Project.md', framework: str = 'slidy') -> str:
    if type(framework) is str:
        if framework in 'slidy':
            return pypandoc.convert_file('FInal_Project.md', to=framework, extra_args=['-s'])


if __name__ == '__main__':
    doctest.testmod(verbose=True)
    write_file('slides.html', make_slides('FInal_Project.md', framework='slidy'))
