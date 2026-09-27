"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter();

  function handleLogout() {
    sessionStorage.removeItem("access_token");
    sessionStorage.removeItem("refresh_token");
    router.push("/login");
  }

  return (
    <nav className="bg-white border-b shadow-sm">
      <div className="max-w-4xl mx-auto px-6 py-3 flex justify-between items-center">
        <Link href="/dashboard" className="font-bold text-gray-900">
          Hospitality
        </Link>
        <div className="flex gap-6 items-center">
          <Link href="/dashboard" className="text-sm text-gray-700 hover:text-blue-600">
            Dashboard
          </Link>
          <Link href="/journey" className="text-sm text-gray-700 hover:text-blue-600">
            Journey
          </Link>
          <button
            onClick={handleLogout}
            className="text-sm text-red-600 hover:underline"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}