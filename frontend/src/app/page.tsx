import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-8">
          Welcome to The Farmer Market
        </h1>
        <p className="text-xl text-white mb-8">
          Connecting Ethiopian farmers, buyers, and government for a modern marketplace.
        </p>
        <div className="space-x-4">
          <Link
            href="/login"
            className="bg-white text-green-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition duration-300"
          >
            Login
          </Link>
          <Link
            href="/products"
            className="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 transition duration-300"
          >
            Browse Products
          </Link>
        </div>
      </div>
    </div>
  );
}
