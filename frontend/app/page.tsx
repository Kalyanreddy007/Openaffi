'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to login or dashboard based on auth state
    router.push('/auth/login');
  }, [router]);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold">OpenAffi</h1>
        <p className="text-muted-foreground mt-2">Loading...</p>
      </div>
    </main>
  );
}
