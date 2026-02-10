"use client"
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuth } from '@/context/AuthContext'; // We need to actually export/import this correctly

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isOwner, setIsOwner] = useState(true); // Toggle for signup vs login?
    // Actually requirements say "Step 1: Workspace Creation" is the first step.
    // Maybe "Login" is for existing users. "Get Started" for new.
    // But "No customer login". Internal login only.
    // Let's implement Login. Workspace creation is a separate flow (Onboarding).

    const router = useRouter();
    const [error, setError] = useState('');

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const res = await api.post('/login/access-token', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            // Store token (logic in AuthContext ideally, or here manually for now)
            document.cookie = `token=${res.data.access_token}; path=/`;
            router.push('/dashboard');
        } catch (err) {
            setError('Invalid credentials');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-900 to-black text-white">
            <div className="bg-white/10 backdrop-blur-lg border border-white/20 p-8 rounded-2xl shadow-xl w-full max-w-md">
                <h1 className="text-3xl font-bold mb-6 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                    CareOps
                </h1>
                <h2 className="text-xl font-semibold mb-6 text-center text-gray-200">
                    Internal Access
                </h2>

                {error && <div className="bg-red-500/20 text-red-200 p-3 rounded mb-4 text-sm">{error}</div>}

                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full bg-black/30 border border-gray-600 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                            placeholder="name@company.com"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full bg-black/30 border border-gray-600 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-3 rounded-lg transition-all transform hover:scale-[1.02]"
                    >
                        Sign In
                    </button>
                </form>

                <div className="mt-6 text-center text-sm text-gray-400">
                    <p>Don't have a workspace?</p>
                    <button
                        onClick={() => router.push('/onboarding')}
                        className="text-blue-400 hover:text-blue-300 font-medium ml-1"
                    >
                        Create New Workspace
                    </button>
                </div>
            </div>
        </div>
    );
}
