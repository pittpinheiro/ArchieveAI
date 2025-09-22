'use client';

import { useState } from 'react';

// Define the type for a book result
type Book = {
  titulo: string;
  autor: string;
  genero: string;
  ano: number;
};

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch results.');
      }

      const data = await response.json();
      setResults(data.results);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred.');
      }
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: 'auto' }}>
      <h1>ArchiveAI</h1>
      <p>Busca de livros via linguagem natural.</p>

      <form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ex: livros de fantasia de J.R.R. Tolkien"
          style={{ width: '100%', padding: '0.5rem', marginBottom: '0.5rem' }}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'pesquisando...' : 'pesquisa'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {results.length > 0 && (
        <div>
          <h2>Results</h2>
          <ul>
            {results.map((book: Book, index) => (
              <li key={index} style={{ borderBottom: '1px solid #ccc', padding: '0.5rem 0' }}>
                <h3>{book.titulo}</h3>
                <p>Author: {book.autor}</p>
                <p>Genre: {book.genero} | Year: {book.ano}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}