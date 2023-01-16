# app/Dockerfile

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install -i https://test.pypi.org/simple/ streamlit-cognito-authentication
EXPOSE 8501
COPY . /app
ENTRYPOINT [ "streamlit", "run" ]
CMD ["app.py"]