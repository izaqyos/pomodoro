from setuptools import setup, find_packages

setup(
    name="pomodoro",
    version="0.1.0",
    packages=find_packages(include=["src", "src.*"]),
    install_requires=[
        "streamlit>=1.30.0",
        "plyer>=2.1.0",
        "plotly>=5.18.0",
    ],
)
