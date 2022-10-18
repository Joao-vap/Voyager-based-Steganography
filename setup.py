from setuptools import setup

if __name__ == "__main__":
    setup(
        name='VBS - Voyager Based Steganography',
        version='0.0.1',
        install_requires=[
            'numpy',
            'pydub',
            'matplotlib',
            'cv2',
            'importlib-metadata; python_version == "3.8"',
        ],
    )