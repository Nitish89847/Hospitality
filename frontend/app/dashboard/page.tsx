"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { authenticatedFetch } from "@/lib/api";

type RoomType = {
  id: number;
  category: string;
  indicative_cost_per_day: string;
  covered: boolean;
  reason: string;
  estimated_out_of_pocket_per_day: number;
};

type Hospital = {
  id: number;
  name: string;
  city: string;
  ownership_type: string;
  room_types: RoomType[];
};

type Policy = {
  id: number;
  insurer: string;
  scheme_type: string;
  sum_insured: string;
  room_eligibility: {
    category: string;
    cap_per_day: number;
    icu_covered: boolean;
    icu_cap_per_day: number;
  };
  co_pay_percent: string;
};

const formatCategory = (value: string) =>
  value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());

const formatCurrency = (value: string | number) =>
  `₹${Number(value).toLocaleString("en-IN")}`;

export default function DashboardPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("access_token");
    setToken(stored);
    setMounted(true);
    if (!stored) {
      router.push("/login");
    }
  }, [router]);

  const {
    data: policies,
    isLoading: policiesLoading,
    error: policiesError,
    refetch: refetchPolicies,
  } = useQuery<Policy[]>({
    queryKey: ["policies", token],
    queryFn: () => authenticatedFetch("/api/insurance/policies/", token!),
    enabled: !!token,
  });

  const activePolicy = policies?.[0];

  const {
    data: hospitals,
    isLoading: hospitalsLoading,
    error: hospitalsError,
    refetch: refetchHospitals,
  } = useQuery<Hospital[]>({
    queryKey: ["hospitalMatches", activePolicy?.id],
    queryFn: () =>
      authenticatedFetch(
        `/api/hospitals/match/?policy_id=${activePolicy!.id}`,
        token!
      ),
    enabled: !!activePolicy,
  });

  if (!mounted || (mounted && !token)) {
    return (
      <main className="p-8 text-center text-gray-500">
        {mounted ? "Redirecting to login…" : "Loading…"}
      </main>
    );
  }

  if (policiesLoading) {
    return (
      <main className="p-8 text-center text-gray-500">
        Loading your coverage details…
      </main>
    );
  }

  if (policiesError) {
    return (
      <main className="p-8 text-center">
        <p className="text-red-600 mb-4">Failed to load your policy.</p>
        <button
          onClick={() => refetchPolicies()}
          className="px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700"
        >
          Retry
        </button>
      </main>
    );
  }

  if (!activePolicy) {
    return (
      <main className="p-8 text-center text-gray-500">
        No policy found for this account.
      </main>
    );
  }

  return (
    <main className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Your Coverage Dashboard</h1>

      <section className="bg-white shadow rounded-lg p-5 mb-8 border">
        <h2 className="text-lg font-semibold mb-3">Policy Summary</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-2 gap-x-6 text-sm">
          <p><span className="font-medium">Insurer:</span> {activePolicy.insurer}</p>
          <p><span className="font-medium">Scheme:</span> {activePolicy.scheme_type}</p>
          <p><span className="font-medium">Sum Insured:</span> {formatCurrency(activePolicy.sum_insured)}</p>
          <p>
            <span className="font-medium">Room Eligibility:</span>{" "}
            {formatCategory(activePolicy.room_eligibility.category)} (cap{" "}
            {formatCurrency(activePolicy.room_eligibility.cap_per_day)}/day)
          </p>
          <p>
            <span className="font-medium">ICU:</span>{" "}
            {activePolicy.room_eligibility.icu_covered
              ? `Covered up to ${formatCurrency(activePolicy.room_eligibility.icu_cap_per_day)}/day`
              : "Not covered"}
          </p>
          <p><span className="font-medium">Co-pay:</span> {activePolicy.co_pay_percent}%</p>
        </div>
      </section>

      <h2 className="text-lg font-semibold mb-4">Matched Hospitals</h2>

      {hospitalsLoading && (
        <p className="text-gray-500">Finding matching hospitals…</p>
      )}

      {hospitalsError && (
        <div className="text-center py-6">
          <p className="text-red-600 mb-4">Failed to load matched hospitals.</p>
          <button
            onClick={() => refetchHospitals()}
            className="px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      )}

      {hospitals && hospitals.length === 0 && (
        <p className="text-gray-500">
          No hospitals currently match this policy.
        </p>
      )}

      {hospitals && hospitals.length > 0 && (
        <div className="space-y-6">
          {hospitals.map((hospital) => (
            <div key={hospital.id} className="bg-white shadow rounded-lg p-5 border">
              <h3 className="text-xl font-semibold">{hospital.name}</h3>
              <p className="text-sm text-gray-500 mb-4">
                {hospital.city} · {hospital.ownership_type}
              </p>

              <div className="overflow-x-auto">
                <table className="w-full text-sm min-w-[480px]">
                  <thead>
                    <tr className="text-left border-b">
                      <th className="pb-2">Room</th>
                      <th className="pb-2">Cost/day</th>
                      <th className="pb-2">Covered</th>
                      <th className="pb-2">Your out-of-pocket/day</th>
                      <th className="pb-2">Reason</th>
                    </tr>
                  </thead>
                  <tbody>
                    {hospital.room_types.map((room) => (
                      <tr key={room.id} className="border-b last:border-0 align-top">
                        <td className="py-2 whitespace-nowrap">{formatCategory(room.category)}</td>
                        <td className="py-2 whitespace-nowrap">{formatCurrency(room.indicative_cost_per_day)}</td>
                        <td className="py-2 whitespace-nowrap">
                          <span className={room.covered ? "text-green-600" : "text-red-600"}>
                            {room.covered ? "Covered" : "Not covered"}
                          </span>
                        </td>
                        <td className="py-2 whitespace-nowrap">
                          {formatCurrency(room.estimated_out_of_pocket_per_day)}
                        </td>
                        <td className="py-2 text-gray-500">{room.reason}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}