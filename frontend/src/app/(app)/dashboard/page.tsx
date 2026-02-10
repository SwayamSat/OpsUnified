"use client"
import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Users, Calendar, MessageSquare, FileText, AlertTriangle } from 'lucide-react';

export default function DashboardPage() {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await api.get('/workspaces/dashboard/stats');
                setStats(res.data);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        fetchStats();
    }, []);

    if (loading) return <div className="p-8">Loading stats...</div>;

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-8 text-gray-800">Operational Overview</h1>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <StatCard title="Total Bookings" value={stats?.metrics?.bookings || 0} icon={Calendar} color="bg-blue-500" />
                <StatCard title="Active Leads" value={stats?.metrics?.contacts || 0} icon={Users} color="bg-green-500" />
                <StatCard title="Conversations" value={stats?.metrics?.active_conversations || 0} icon={MessageSquare} color="bg-purple-500" />
                <StatCard title="Pending Forms" value={stats?.metrics?.pending_forms || 0} icon={FileText} color="bg-orange-500" />
            </div>

            {/* Alerts Section */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-bold mb-4 flex items-center">
                    <AlertTriangle className="mr-2 text-red-500" size={20} />
                    System Alerts
                </h2>
                {stats?.alerts?.length === 0 ? (
                    <p className="text-gray-500">No active alerts. System running smoothly.</p>
                ) : (
                    <div className="space-y-3">
                        {stats?.alerts?.map((alert: any) => (
                            <div key={alert.id} className="flex items-start p-4 bg-red-50 rounded-lg border border-red-100">
                                <div className="flex-1">
                                    <h4 className="font-semibold text-red-800 capitalize">{alert.type.replace('_', ' ')}</h4>
                                    <p className="text-sm text-red-600 mt-1">{alert.message}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

function StatCard({ title, value, icon: Icon, color }: any) {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex items-center space-x-4">
            <div className={`p-3 rounded-lg ${color} text-white`}>
                <Icon size={24} />
            </div>
            <div>
                <p className="text-sm font-medium text-gray-500">{title}</p>
                <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
            </div>
        </div>
    )
}
