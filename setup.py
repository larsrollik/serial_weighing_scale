from os import path

from setuptools import find_packages
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

with open(path.join(this_directory, "LICENSE")) as f:
    license_text = f.read()


setup(
    name="serial_weighing_scale",
    version="1.0.1",
    description="serial_weighing_scale",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=find_packages(),
    url="https://github.com/larsrollik/SerialWeighingScale",
    author="Lars B. Rollik",
    author_email="L.B.Rollik@protonmail.com",
    license=license_text,
    install_requires=[
        "pyserial",
    ],
    extras_require={
        "dev": [
            "black",
            "pytest-cov",
            "pytest",
            "gitpython",
            "coverage>=5.0.3",
            "bump2version",
            "pre-commit",
            "flake8",
        ],
    },
    zip_safe=False,
    include_package_data=True,
    # entry_points={
    #     "console_scripts": [
    #         "console_script_name = module.path.to.function:function_name",
    #     ],
    # },
)
