import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speaker-switch",
    version="0.0.1",
    author="alumae",
    author_email="author@example.com",
    description="Online (streaming) speaker change detection model implemented in Pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TzurV/online_speaker_change_detector.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "online_scd"},
    packages=setuptools.find_packages(where="online_scd"),
    python_requires=">=3.8",
)
