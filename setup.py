import setuptools

with open('README.md') as file:
    read_me_descriotion = file.read()

setuptools.setup(
    name="qiwiBillPaymentsAPI",
    version="0.1",
    author="LucifierArchangel",
    author_email="lucifier.archangel@gmail.com",
    description="Qiwi Bill Payments API",
    long_description=read_me_descriotion,
    long_description_content_type="text/markdown",
    url="https://github.com/LucifierArchangel/QiwiBillPaymentsAPI",
    packages=['QiwiBillPaymentsAPI'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.4'
)