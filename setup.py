# Standard
import pathlib
import platform
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

class InstallTesserocr(install):
  def run(self):
    print("Choosing tesserocr version depending on platform...")
    install.run(self)
    
    # If Platform is window, exchange tesserocr with pre compiled wheel from
    # https://github.com/simonflueckiger/tesserocr-windows_build/releases
    TESSEROCR = { "pypi package": "tesserocr",
                  "prebuild wheel for win32" : (
                                "https://github.com/simonflueckiger/tesserocr-windows_build/releases/download/"
                                "tesserocr-v2.4.0-tesseract-4.0.0/tesserocr-2.4.0-cp37-cp37m-win32.whl"
                            ),
                  "prebuild wheel for win64": (
                                "https://github.com/simonflueckiger/tesserocr-windows_build/releases/download/"
                                "tesserocr-v2.4.0-tesseract-4.0.0/tesserocr-2.4.0-cp37-cp37m-win_amd64.whl"
                            )
                }
    tess_version = "pypi package"
    if platform.system().lower() == "windows":
        if platform.machine().endswith("64"):
            tess_version = "prebuild wheel for win64"
        if platform.machine().endswith("86"):
            tess_version = "prebuild wheel for win32"
    print(f"Installing tesserocr from {tess_version}: {TESSEROCR[tess_version]}...")  
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', TESSEROCR[tess_version], "--trusted-host", "github-production-release-asset-2e65be.s3.amazonaws.com"])
    print("Done.")
    
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="normcap",
    version="0.0.9",
    description="Intelligent screencapture tool to capture information instead of images.",
    keywords="screenshot ocr capture",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dynobo/normcap",
    author="dynobo",
    author_email="dynobo@mailbox.org",
    license="GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Utilities",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=False,
    python_requires=">=3.7.0",
    install_requires=["mss", "Pillow", "pyperclip", "python-Levenshtein"],
    entry_points={"console_scripts": ["normcap=normcap.normcap:main",]},
    cmdclass={'install': InstallTesserocr}
)
