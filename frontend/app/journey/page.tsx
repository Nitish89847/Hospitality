"use client";

import { useEffect, useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { getJourneys, advanceJourneyStage } from "@/lib/api";

const STAGES = ["admission", "investigation", "procedure", "recovery", "discharge"];

export default function JourneyPage() {
  const router = useRouter();
  const queryClient = useQueryClient();

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


  const { data: journeys, isLoading, error } = useQuery({
    queryKey: ["journeys", auth.token],
    queryFn: () => getJourneys(auth.token!),
    enabled: !!auth.token,
  });

  const activeJourney = journeys?.[0];

  const advanceMutation = useMutation({
    mutationFn: () => advanceJourneyStage(activeJourney.id, auth.token!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["journeys"] });
    },
  });

  if (!auth.checked || !auth.token) {
    return null;
  }

  if (isLoading) return <main className="p-8 text-center">Loading journey...</main>;
  if (error) return <main className="p-8 text-center text-red-600">Failed to load journey.</main>;
  if (!activeJourney) return <main className="p-8 text-center text-gray-700">No active journey found.</main>;

  const currentIndex = STAGES.indexOf(activeJourney.current_stage);
  const isFinalStage = currentIndex === STAGES.length - 1;

  return (
    <main className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-gray-900">Care Journey</h1>

      <div className="bg-white shadow rounded-lg p-6 border mb-6">
        <div className="flex justify-between mb-2">
          {STAGES.map((stage, i) => (
            <div key={stage} className="flex-1 text-center">
              <div
                className={`mx-auto w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold
                  ${i <= currentIndex ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-500"}`}
              >
                {i + 1}
              </div>
              <p className={`text-xs mt-1 capitalize ${i <= currentIndex ? "text-gray-900 font-medium" : "text-gray-400"}`}>
                {stage}
              </p>
            </div>
          ))}
        </div>

        <div className="flex mt-2">
          {STAGES.slice(0, -1).map((_, i) => (
            <div
              key={i}
              className={`flex-1 h-1 ${i < currentIndex ? "bg-blue-600" : "bg-gray-200"}`}
            />
          ))}
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-5 border mb-6">
        <h2 className="text-lg font-semibold mb-3 text-gray-900">Stage History</h2>
        {activeJourney.stage_history.length === 0 ? (
          <p className="text-gray-500 text-sm">No stage transitions yet.</p>
        ) : (
          <ul className="space-y-2">
            {activeJourney.stage_history.map((log: any, i: number) => (
              <li key={i} className="text-sm text-gray-700">
                <span className="font-medium capitalize">{log.stage}</span> —{" "}
                {new Date(log.timestamp).toLocaleString()}
              </li>
            ))}
          </ul>
        )}
      </div>

      <button
        onClick={() => advanceMutation.mutate()}
        disabled={isFinalStage || advanceMutation.isPending}
        className="w-full bg-blue-600 text-white rounded py-2 font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {isFinalStage
          ? "Journey Complete"
          : advanceMutation.isPending
          ? "Advancing..."
          : "Advance to Next Stage"}
      </button>
    </main>
  );
}