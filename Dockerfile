# Use a imagem oficial do Node.js como base. Use uma versão LTS.
FROM node:20-alpine

# Defina o diretório de trabalho no contêiner.
WORKDIR /app

# Copie os arquivos de dependência do projeto.
# Use este passo para aproveitar o cache do Docker.
COPY package*.json ./

# Copie a pasta do Prisma e seu schema.
# Isso garante que o schema esteja disponível para o comando `prisma generate`.
COPY prisma ./prisma/

# Instale as dependências do projeto.
RUN npm install

# Gere o cliente Prisma para que a aplicação possa se conectar ao banco de dados.
RUN npx prisma generate

# Copie o restante dos arquivos do projeto.
COPY . .

# Exponha a porta na qual a aplicação Next.js vai rodar.
EXPOSE 3000

# Compile a aplicação para produção.
RUN npm run build

# O comando para iniciar a aplicação quando o contêiner for iniciado.
CMD ["npm", "run", "start"]