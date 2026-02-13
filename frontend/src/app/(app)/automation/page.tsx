"use client"
import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Plus, Trash, Zap } from 'lucide-react';

interface AutomationRule {
    id: number;
    name: string;
    form_template_id: number;
    action_type: string;
    action_config: any;
    is_active: number;
}

interface FormTemplate {
    id: number;
    name: string;
}

export default function AutomationPage() {
    const [rules, setRules] = useState<AutomationRule[]>([]);
    const [templates, setTemplates] = useState<FormTemplate[]>([]);
    const [loading, setLoading] = useState(true);
    const [showAddForm, setShowAddForm] = useState(false);

    // New Rule State
    const [newName, setNewName] = useState("");
    const [selectedTemplate, setSelectedTemplate] = useState<number>(0);
    const [actionType, setActionType] = useState("send_email");
    const [recipient, setRecipient] = useState("contact"); // 'contact' or specific email

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [rulesRes, formsRes] = await Promise.all([
                api.get('/workspaces/automation'),
                api.get('/workspaces/forms')
            ]);
            setRules(rulesRes.data);
            setTemplates(formsRes.data);
            if (formsRes.data.length > 0) {
                setSelectedTemplate(formsRes.data[0].id);
            }
        } catch (error) {
            console.error("Failed to fetch automation data", error);
        } finally {
            setLoading(false);
        }
    };

    const handleAddRule = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/workspaces/automation', {
                name: newName,
                form_template_id: selectedTemplate,
                action_type: actionType,
                action_config: { recipient: recipient },
                is_active: 1
            });
            setNewName("");
            setShowAddForm(false);
            fetchData();
        } catch (error) {
            console.error("Failed to add rule", error);
        }
    };

    const handleDeleteRule = async (id: number) => {
        try {
            await api.delete(`/workspaces/automation/${id}`);
            fetchData();
        } catch (error) {
            console.error("Failed to delete rule", error);
        }
    };

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-900">Automation Rules</h1>
                <button
                    onClick={() => setShowAddForm(!showAddForm)}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                    {showAddForm ? 'Cancel' : 'Create Rule'}
                </button>
            </div>

            {showAddForm && (
                <div className="bg-white p-6 rounded-lg shadow mb-6 border border-gray-200">
                    <h2 className="text-lg font-semibold mb-4">New Automation Rule</h2>
                    <form onSubmit={handleAddRule} className="space-y-4 max-w-lg">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Rule Name</label>
                            <input
                                type="text"
                                value={newName}
                                onChange={(e) => setNewName(e.target.value)}
                                className="w-full border border-gray-300 rounded px-3 py-2"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">When Form Submitted:</label>
                            <select
                                value={selectedTemplate}
                                onChange={(e) => setSelectedTemplate(parseInt(e.target.value))}
                                className="w-full border border-gray-300 rounded px-3 py-2"
                            >
                                {templates.map(t => (
                                    <option key={t.id} value={t.id}>{t.name}</option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Action:</label>
                            <select
                                value={actionType}
                                onChange={(e) => setActionType(e.target.value)}
                                className="w-full border border-gray-300 rounded px-3 py-2"
                            >
                                <option value="send_email">Send Email</option>
                                <option value="send_sms">Send SMS</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Recipient:</label>
                            <select
                                value={recipient}
                                onChange={(e) => setRecipient(e.target.value)}
                                className="w-full border border-gray-300 rounded px-3 py-2"
                            >
                                <option value="contact">The Contact (Submitter)</option>
                                <option value="staff@example.com">Staff (staff@example.com)</option>
                            </select>
                        </div>
                        <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                            Save Rule
                        </button>
                    </form>
                </div>
            )}

            <div className="space-y-4">
                {rules.map((rule) => {
                    const templateName = templates.find(t => t.id === rule.form_template_id)?.name || "Unknown Form";
                    return (
                        <div key={rule.id} className="bg-white rounded-lg shadow p-6 border border-gray-200 flex justify-between items-center">
                            <div className="flex items-start gap-4">
                                <div className="p-3 bg-blue-100 text-blue-600 rounded-full">
                                    <Zap size={24} />
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold text-gray-900">{rule.name}</h3>
                                    <p className="text-sm text-gray-600">
                                        When <strong>{templateName}</strong> is submitted,
                                        <strong> {rule.action_type.replace('_', ' ')}</strong> to
                                        <strong> {rule.action_config?.recipient}</strong>.
                                    </p>
                                </div>
                            </div>
                            <button
                                onClick={() => handleDeleteRule(rule.id)}
                                className="text-red-500 hover:text-red-700 p-2"
                            >
                                <Trash size={20} />
                            </button>
                        </div>
                    );
                })}

                {!loading && rules.length === 0 && (
                    <div className="text-center py-12 text-gray-500">No automation rules configured.</div>
                )}
            </div>
        </div>
    );
}
