from setuptools import setup, find_packages

setup(
    name='Opening Deviation',  # Replace with your own project name
    version='0.1.0',  # The initial project version
    author='Aaron Demby Jones',  # Replace with your name
    author_email='aaron.demby.jones@gmail.com',  # Replace with your email
    description='Find when you first left your chess opening preparation.',  # Provide a short description
    long_description=open('README.md').read(),  # This will read the contents of your README.md file
    long_description_content_type='text/markdown',  # This is the content type of the long description
    url='http://github.com/aadjones/opening-deviation',  
    packages=find_packages(),  # This will automatically find your packages to include
    install_requires=[
        'streamlit>=1.31.1',
        'chess==1.10.0',
        'requests>=2.31.0', 
    ],
    classifiers=[
        # Choose your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.7',  
    # You can include package data like this:
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },
    # If you want to include data files outside of your packages, you can do so like this:
    data_files=[('my_data', ['data/data_file'])],  # Optional
    # If you want to create scripts that are installed to the PATH, you can do so like this:
    entry_points={  # Optional
        'console_scripts': [
            'my-command=my_package.module:function',
        ],
    },
)

