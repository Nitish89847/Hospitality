"use client";

import { useEffect, useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useRouter, useParams } from "next/navigation";
import { getPlans, enrollInPlan } from "@/lib/api";

type Plan = {
  id: number;
  name: string;
  insurer_name: string;
  scheme_type: string;
  sum_insured: string;
  room_eligibility: {
    category: string;
    cap_per_day: number;
    icu_covered: boolean;
    icu_cap_per_day: number;
  };
  covered_procedures: string[];
  exclusions: string[];
  co_pay_percent: string;
};

export default function PlansForInsurerPage() {
  const router = useRouter();
  const params = useParams();
  const insurerId = Number(params.insurerId);

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

  const { data: plans, isLoading, error } = useQuery({
    queryKey: ["plans", insurerId, auth.token],
    queryFn: () => getPlans(insurerId, auth.token!),
    enabled: !!auth.token,
  });

  const enrollMutation = useMutation({
    mutationFn: (planId: number) => enrollInPlan(planId, auth.token!),
    onSuccess: () => {
      router.push("/dashboard");
    },
  });

  if (!auth.checked || !auth.token) {
    return null;
  }

  if (isLoading) return <main className="p-8 text-center">Loading plans...</main>;
  if (error) return <main className="p-8 text-center text-red-600">Failed to load plans.</main>;
  if (!plans || plans.length === 0)
    return <main className="p-8 text-center text-gray-700">No plans available for this insurer.</main>;

  return (
    <main className="max-w-3xl mx-auto p-6">
      <button
        onClick={() => router.push("/plans")}
        className="text-sm text-blue-600 hover:underline mb-4"
      >
        ← Back to insurers
      </button>

      <h1 className="text-2xl font-bold mb-6 text-gray-900">
        {plans[0].insurer_name} — Available Plans
      </h1>

      <div className="space-y-5">
        {plans.map((plan: Plan) => (
          <div key={plan.id} className="bg-white shadow rounded-lg p-6 border">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h2 className="text-lg font-semibold text-gray-900">{plan.name}</h2>
                <p className="text-sm text-gray-500">{plan.scheme_type}</p>
              </div>
              <span className="text-lg font-bold text-gray-900">
                ₹{Number(plan.sum_insured).toLocaleString("en-IN")}
              </span>
            </div>

            <dl className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm text-gray-700 mb-4">
              <dt className="font-medium">Room eligibility</dt>
              <dd className="capitalize">
                {plan.room_eligibility.category.replace("_", " ")} (₹{plan.room_eligibility.cap_per_day}/day)
              </dd>

              <dt className="font-medium">ICU</dt>
              <dd>
                {plan.room_eligibility.icu_covered
                  ? `Covered up to ₹${plan.room_eligibility.icu_cap_per_day}/day`
                  : "Not covered"}
              </dd>

              <dt className="font-medium">Co-pay</dt>
              <dd>{plan.co_pay_percent}%</dd>

              <dt className="font-medium">Covered procedures</dt>
              <dd>{plan.covered_procedures.length > 0 ? plan.covered_procedures.join(", ") : "—"}</dd>

              <dt className="font-medium">Exclusions</dt>
              <dd>{plan.exclusions.length > 0 ? plan.exclusions.join(", ") : "—"}</dd>
            </dl>

            <button
              onClick={() => enrollMutation.mutate(plan.id)}
              disabled={enrollMutation.isPending}
              className="w-full bg-blue-600 text-white rounded py-2 font-medium hover:bg-blue-700 disabled:opacity-50"
            >
              {enrollMutation.isPending ? "Enrolling..." : "Enroll in this Plan"}
            </button>
          </div>
        ))}
      </div>
    </main>
  );
}