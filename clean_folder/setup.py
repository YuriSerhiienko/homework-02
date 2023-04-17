from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='0.1.1',
    url="https://github.com/YuriSerhiienko/homework-02.git",
    author="Yurii Serhiienko",
    author_email="yurasergienko97@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["clean-folder = clean_folder.clean:run"]
    }

)
