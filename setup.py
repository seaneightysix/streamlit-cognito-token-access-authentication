from setuptools import setup

setup(
    name='streamlit-cognito-authentication',
    version='1.1.1',    
    description="This is a library to authenticate users of a streamlit application that is embedded in a host application using AWS Cognito's access token.  A example use case would be an Angular application that has a streamlit app in an iframe. A user would first login to the host angular app and receive an access token.\
    The user would then use this access token to sign in to the embedded streamlit app.",
    url='https://github.com/seaneightysix/streamlit-cognito-authentication',
    author='Sean Tasaki',
    author_email='sean.tasaki@gmail.com',
    license='BSD 2-clause',
    python_requires=">=3.9",
    packages=['streamlit_cognito_authentication'],
    keywords=['cognito', 'streamlit', 'access token', 'userinfo', 'login', 'authentication'],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        "python-jose[cryptography]",
        "streamlit>=1.10.0"
    ]
)