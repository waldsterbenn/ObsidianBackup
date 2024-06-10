from setuptools import setup, find_packages

setup(
    name="ObsidianBackup",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'plyer'
    ],
    entry_points={
        'console_scripts': [
            # We'll need to adjust the main script for this
            'obsidian_backup=main:main_function',
        ],
    }
)
