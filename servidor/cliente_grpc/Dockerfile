# Usa uma imagem base oficial
FROM python:3.12-slim

# Instala build-essential (compilador c++)
RUN apt-get update && apt-get install -y build-essential

# Define diretório de trabalho
WORKDIR /app

# Copia os ficheiros para dentro do container
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto da aplicação
COPY . .

# Expõe a porta do gRPC
EXPOSE 50051

# Comando para iniciar o servidor
CMD ["python", "grpc_server.py"]
