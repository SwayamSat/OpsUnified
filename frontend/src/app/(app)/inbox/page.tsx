"use client"
import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Search, Send, Phone, Mail } from 'lucide-react';
import { cn } from '@/lib/utils'; // Ensure utils exists

export default function InboxPage() {
    const [conversations, setConversations] = useState([]);
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const [messages, setMessages] = useState([]);
    const [reply, setReply] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchConversations();
    }, []);

    useEffect(() => {
        if (selectedId) fetchMessages(selectedId);
    }, [selectedId]);

    const fetchConversations = async () => {
        try {
            const res = await api.get('/workspaces/conversations');
            setConversations(res.data);
            if (res.data.length > 0 && !selectedId) setSelectedId(res.data[0].id);
        } catch (e) { console.error(e); } finally { setLoading(false); }
    };

    const fetchMessages = async (id: number) => {
        try {
            const res = await api.get(`/workspaces/conversations/${id}/messages`);
            setMessages(res.data);
        } catch (e) { console.error(e); }
    };

    const handleReply = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!reply.trim() || !selectedId) return;

        try {
            const res = await api.post(`/workspaces/conversations/${selectedId}/messages`, {
                content: reply,
                type: 'email' // Default or derive from last message
            });
            setMessages([...messages, res.data] as any);
            setReply('');
        } catch (e) {
            console.error(e);
            alert("Failed to send reply");
        }
    };

    return (
        <div className="flex h-[calc(100vh-64px)] overflow-hidden bg-white border-t border-gray-200">
            {/* Conversation List */}
            <div className="w-1/3 border-r border-gray-200 flex flex-col">
                <div className="p-4 border-b border-gray-200">
                    <div className="relative">
                        <Search className="absolute left-3 top-3 text-gray-400" size={18} />
                        <input className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none" placeholder="Search..." />
                    </div>
                </div>
                <div className="flex-1 overflow-y-auto">
                    {conversations.map((conv: any) => (
                        <div
                            key={conv.id}
                            onClick={() => setSelectedId(conv.id)}
                            className={cn(
                                "p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors",
                                selectedId === conv.id ? "bg-blue-50 border-l-4 border-l-blue-500" : ""
                            )}
                        >
                            <div className="flex justify-between mb-1">
                                <h4 className="font-semibold text-gray-800">Contact #{conv.contact_id}</h4>
                                <span className="text-xs text-gray-500">{new Date(conv.last_message_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                            </div>
                            <p className="text-sm text-gray-500 truncate">
                                {conv.status === 'paused' && <span className="text-orange-500 mr-2">[Paused]</span>}
                                Click to view messages...
                            </p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 flex flex-col bg-gray-50">
                {selectedId ? (
                    <>
                        <div className="p-4 border-b border-gray-200 bg-white shadow-sm flex justify-between items-center">
                            <div>
                                <h3 className="font-bold text-lg">Conversation #{selectedId}</h3>
                                <p className="text-xs text-green-600 flex items-center">
                                    <span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                                    Active Integration
                                </p>
                            </div>
                        </div>

                        <div className="flex-1 overflow-y-auto p-6 space-y-4">
                            {messages.map((msg: any) => (
                                <div key={msg.id} className={cn("flex", msg.direction === 'outbound' ? "justify-end" : "justify-start")}>
                                    <div className={cn(
                                        "max-w-md p-4 rounded-xl shadow-sm text-sm",
                                        msg.direction === 'outbound'
                                            ? "bg-blue-600 text-white rounded-br-none"
                                            : "bg-white text-gray-800 border border-gray-200 rounded-bl-none"
                                    )}>
                                        <p>{msg.content}</p>
                                        <div className={cn("text-xs mt-2 opacity-70", msg.direction === 'outbound' ? "text-blue-100" : "text-gray-400")}>
                                            {msg.type === 'sms' ? <Phone size={12} className="inline mr-1" /> : <Mail size={12} className="inline mr-1" />}
                                            {new Date(msg.timestamp).toLocaleTimeString()}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="p-4 bg-white border-t border-gray-200">
                            <form onSubmit={handleReply} className="flex gap-2">
                                <input
                                    value={reply}
                                    onChange={(e) => setReply(e.target.value)}
                                    className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    placeholder="Type your reply to pause automation..."
                                />
                                <button type="submit" className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition-colors">
                                    <Send size={20} />
                                </button>
                            </form>
                        </div>
                    </>
                ) : (
                    <div className="flex-1 flex items-center justify-center text-gray-400">
                        Select a conversation to start
                    </div>
                )}
            </div>
        </div>
    );
}
