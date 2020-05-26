from setuptools import setup

with open('README.md', 'r') as f:
    README = f.read()

setup(name="multireq",
      version="0.0.8",
      author="rafet",
      license="MIT",
      description="Package for sending multi requests with different proxies.",
      url="https://github.com/rafet/multi-requester",
      packages=[str('multireq')],
      long_description=README,
      long_description_content_type="text/markdown",
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Operating System :: OS Independent",
      ],
      include_package_data=True,
      install_requires=["requests"])
