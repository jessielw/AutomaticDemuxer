from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

long_desc = "A package that utilizes ffmpeg to automatically demux tracks into single file formats. " \
            "See https://github.com/jlw4049/AutomaticDemuxer for more information"

setup(
    name='AutomaticDemuxer',
    version='1.33',
    description='Automatically Demux tracks from media-files',
    long_description=long_desc,
    url='https://github.com/jlw4049/AutomaticDemuxer',
    author='Jessie Wilson',
    author_email='jessielw4049@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='AutomaticDemuxer',
    packages=find_packages(),
    install_requires=['pymediainfo']
)
