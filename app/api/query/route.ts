// app/api/query/route.ts
import { NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// URL do seu serviço SQL Chat rodando localmente.
// Isso mudará para a URL de produção quando você implantar.
const SQLCHAT_API_URL = 'http://localhost:5000/api/generate';

export async function POST(request: Request) {
  try {
    const { query } = await request.json();

    if (!query) {
      return NextResponse.json({ error: 'A pergunta é obrigatória.' }, { status: 400 });
    }
    
    // Faça a chamada para a API do SQL Chat
    const sqlChatResponse = await fetch(SQLCHAT_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, schemas: [{ name: 'books', columns: [/* ... */] }] }),
    });

    const { sql } = await sqlChatResponse.json();

    // Execute a query SQL gerada no banco de dados
    const results = await prisma.$queryRawUnsafe(sql);

    return NextResponse.json({ results });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Erro interno do servidor.' }, { status: 500 });
  }
}