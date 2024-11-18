# Usa uma imagem oficial do Node.js como base
FROM node:16

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo package.json e package-lock.json para o diretório de trabalho
COPY package*.json ./

# Instala as dependências da aplicação
RUN npm install

# Copia todos os arquivos do projeto para o contêiner
COPY . .

# Compila a aplicação React para produção
RUN npm run build

# Expõe a porta que o React usará
EXPOSE 3000

# Define o comando para iniciar a aplicação
CMD ["npx", "serve", "-s", "build"]
