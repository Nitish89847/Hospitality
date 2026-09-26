"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
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

export default function DashboardPage() {
  const [policy, setPolicy] = useState<Policy | null>(null);
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = sessionStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }

    async function loadData() {
      try {
        const policies: Policy[] = await authenticatedFetch("/api/insurance/policies/", token!);
        if (policies.length === 0) {
          setError("No policy found for this account.");
          setLoading(false);
          return;
        }
        const activePolicy = policies[0];
        setPolicy(activePolicy);

        const matches: Hospital[] = await authenticatedFetch(
          `/api/hospitals/match/?policy_id=${activePolicy.id}`,
          token!
        );
        setHospitals(matches);
      } catch (err) {
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [router]);

  if (loading) return <main className="p-8 text-center">Loading...</main>;
  if (error) return <main className="p-8 text-center text-red-600">{error}</main>;

  return (
    <main className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Your Coverage Dashboard</h1>

      {policy && (
        <section className="bg-white shadow rounded-lg p-5 mb-8 border">
          <h2 className="text-lg font-semibold mb-2">Policy Summary</h2>
          <p><span className="font-medium">Insurer:</span> {policy.insurer}</p>
          <p><span className="font-medium">Scheme:</span> {policy.scheme_type}</p>
          <p><span className="font-medium">Sum Insured:</span> ₹{policy.sum_insured}</p>
          <p><span className="font-medium">Room Eligibility:</span> {policy.room_eligibility.category} (cap ₹{policy.room_eligibility.cap_per_day}/day)</p>
          <p><span className="font-medium">ICU:</span> {policy.room_eligibility.icu_covered ? `Covered up to ₹${policy.room_eligibility.icu_cap_per_day}/day` : "Not covered"}</p>
          <p><span className="font-medium">Co-pay:</span> {policy.co_pay_percent}%</p>
        </section>
      )}

      <h2 className="text-lg font-semibold mb-4">Matched Hospitals</h2>
      <div className="space-y-6">
        {hospitals.map((hospital) => (
          <div key={hospital.id} className="bg-white shadow rounded-lg p-5 border">
            <h3 className="text-xl font-semibold">{hospital.name}</h3>
            <p className="text-sm text-gray-500 mb-4">{hospital.city} · {hospital.ownership_type}</p>

            <table className="w-full text-sm">
              <thead>
                <tr className="text-left border-b">
                  <th className="pb-2">Room</th>
                  <th className="pb-2">Cost/day</th>
                  <th className="pb-2">Covered</th>
                  <th className="pb-2">Your out-of-pocket/day</th>
                </tr>
              </thead>
              <tbody>
                {hospital.room_types.map((room) => (
                  <tr key={room.id} className="border-b last:border-0">
                    <td className="py-2 capitalize">{room.category.replace("_", " ")}</td>
                    <td className="py-2">₹{room.indicative_cost_per_day}</td>
                    <td className="py-2">
                      <span className={room.covered ? "text-green-600" : "text-red-600"}>
                        {room.covered ? "Covered" : "Not covered"}
                      </span>
                    </td>
                    <td className="py-2">₹{room.estimated_out_of_pocket_per_day}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </main>
  );
}