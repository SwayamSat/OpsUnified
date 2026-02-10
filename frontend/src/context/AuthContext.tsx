"use client"
import React, { createContext, useContext, useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

interface User {
    id: number;
    email: string;
    role: string;
    workspace_id: number;
}

interface AuthContextType {
    user: User | null;
    login: (token: string) => void;
    logout: () => void;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType>({
    user: null,
    login: () => { },
    logout: () => { },
    loading: true,
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const token = Cookies.get('token');
        if (token) {
            // Validate and decode
            // For now, just assume we can fetch user profile or decode token
            // We'll trust the presence of token but fetches will fail if invalid
            // Ideally we call /me endpoint. We don't have one? 
            // We have /workspaces/staff? No that lists staff.
            // Let's decode token for now if we had jwt-decode, or just set simple user state
            // Let's add a /me endpoint to Auth router later? 
            // For hackathon, just trusting token existence + redirect if 401
            setLoading(false);
        } else {
            setLoading(false);
        }
    }, []);

    const login = (token: string) => {
        Cookies.set('token', token, { expires: 1 });
        router.push('/dashboard');
        // Retrieve user info...
    };

    const logout = () => {
        Cookies.remove('token');
        setUser(null);
        router.push('/login');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
