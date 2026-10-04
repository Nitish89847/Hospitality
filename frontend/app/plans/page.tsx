"use client";

import { useEffect,useState } from "react";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { getInsurers } from "@/lib/api";

type Insurer = { id: number; name: string; insurer_type: string };

export default function InsurersPage() {
  const router = useRouter();
  const [auth, setAuth] = useState<{ token: string | null; checked: boolean }>({
    token: null,
    checked: false,
  });

  useEffect(() => {
    const stored = sessionStorage.getItem("access_token");
    setAuth({ token: stored, checked: true });
    if (!stored) {
      router.push("/login");
    }
  }, [router]);

  const { data: insurers, isLoading, error } = useQuery({
    queryKey: ["insurers", auth.token],
    queryFn: () => getInsurers(auth.token!),
    enabled: !!auth.token,
  });

  if (!auth.checked || !auth.token) {
    return null;
  }

  if (isLoading) return <main className="p-8 text-center">Loading insurers...</main>;
  if (error) return <main className="p-8 text-center text-red-600">Failed to load insurers.</main>;

  return (
    <main className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-gray-900">Choose Your Insurer</h1>

      <div className="grid gap-4">
        {insurers?.map((insurer: Insurer) => (
          <button
            key={insurer.id}
            onClick={() => router.push(`/plans/${insurer.id}`)}
            className="bg-white border rounded-lg p-5 text-left shadow-sm hover:shadow-md hover:border-blue-500 transition"
          >
            <h2 className="text-lg font-semibold text-gray-900">{insurer.name}</h2>
            <p className="text-sm text-gray-500 capitalize">{insurer.insurer_type} insurer</p>
          </button>
        ))}
      </div>
    </main>
  );
}