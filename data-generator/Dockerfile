FROM python:3.9-slim

# Configure o docker file para rodar instalar as dependências e rodar o script em python

RUN mkdir /usr/src/data-generator/

COPY ./ /usr/src/data-generator/

WORKDIR /usr/src/data-generator/

RUN pip install -r requirements.txt

CMD ["python", "generate_data.py"]
