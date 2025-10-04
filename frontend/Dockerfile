# Next.js用 Node.js イメージ
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .

# ビルド
RUN npm run build

# 本番サーバー起動
EXPOSE 3000
CMD ["npm", "start"]
