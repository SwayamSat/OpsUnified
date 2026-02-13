"use client"
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Inbox, Users, Settings, LogOut, Package, Zap } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { cn } from '@/lib/utils'; // Make sure utils exists

const NAV_ITEMS = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Inbox', href: '/inbox', icon: Inbox },
    { name: 'Leads', href: '/leads', icon: Users },
    { name: 'Inventory', href: '/inventory', icon: Package },
    { name: 'Automation', href: '/automation', icon: Zap },
    // { name: 'Staff', href: '/staff', icon: Users }, // We didn't plan a staff page but good to have link
    // { name: 'Settings', href: '/settings', icon: Settings },
];

export default function Sidebar() {
    const pathname = usePathname();
    const { logout } = useAuth();

    return (
        <div className="w-64 bg-gray-900 text-gray-300 flex flex-col h-screen border-r border-gray-800">
            <div className="p-6">
                <h1 className="text-2xl font-bold text-white tracking-tight">CareOps</h1>
            </div>

            <nav className="flex-1 px-4 space-y-2">
                {NAV_ITEMS.map((item) => {
                    const Icon = item.icon;
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors",
                                isActive ? "bg-blue-600 text-white" : "hover:bg-gray-800 hover:text-white"
                            )}
                        >
                            <Icon size={20} />
                            <span className="font-medium">{item.name}</span>
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-gray-800">
                <button
                    onClick={logout}
                    className="flex items-center space-x-3 px-4 py-3 w-full text-left hover:bg-red-500/10 hover:text-red-400 rounded-lg transition-colors"
                >
                    <LogOut size={20} />
                    <span className="font-medium">Sign Out</span>
                </button>
            </div>
        </div>
    );
}
