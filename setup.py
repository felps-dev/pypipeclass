import setuptools
import pathlib

REPO = pathlib.Path(__file__).parent

README = (REPO / "README.md").read_text()

setuptools.setup(
    name='pypipeclass',
    version='0.1',
    author='Felipe Correa',
    author_email='eu@felps.dev',
    description='An async multiprocessing Python class with easy communication using pipes',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/felps-dev/pypipeclass',
    project_urls={
        "Bug Tracker": "https://github.com/felps-dev/pypipeclass/issues"
    },
    license='MIT',
    packages=['pypipeclass'],
)
