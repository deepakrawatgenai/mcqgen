from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Deepak Rawat',
    author_email='deepakrawat12@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","datetime"],
    packages=find_packages()
)