from setuptools import setup

setup(
    name='streamlit-cognito-authentication',
    version='0.1.3',    
    description='Streamlit authentication using Cognito with 2 endpoint options: Token and UserInfo',
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