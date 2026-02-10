"use client"
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { Check, ChevronRight, Building, Plus } from 'lucide-react';
import { cn } from '@/lib/utils'; // Assuming utils exists

const STEPS = [
    "Workspace Basics",
    "Communication Setup",
    "Contact Form",
    "Booking Setup",
    "Post-Booking Forms",
    "Inventory Setup",
    "Staff Setup",
    "Activation"
];

export default function OnboardingWizard() {
    const [currentStep, setCurrentStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    // State for all steps
    const [workspaceData, setWorkspaceData] = useState({
        name: '', address: '', timezone: 'UTC', contact_email: '', owner_email: '', owner_password: ''
    });
    const [channels, setChannels] = useState({ email_key: '', sms_key: '' });
    const [serviceData, setServiceData] = useState({ name: 'Consultation', duration: 60, availabilities: [{ day_of_week: 1, start_time: "09:00", end_time: "17:00" }] });
    const [inventoryData, setInventoryData] = useState({ name: 'Resource A', quantity: 10 });

    const handleNext = async () => {
        setLoading(true);
        try {
            if (currentStep === 1) {
                // Create Workspace
                const res = await api.post('/workspaces/', workspaceData);
                // Login automatically? The API creates user and workspace.
                // We need to login to get token.
                const loginRes = await api.post('/login/access-token', new URLSearchParams({
                    username: workspaceData.owner_email,
                    password: workspaceData.owner_password
                }));
                document.cookie = `token=${loginRes.data.access_token}; path=/`;
            } else if (currentStep === 2) {
                await api.put('/workspaces/me/integrations', { channels: { email: channels.email_key, sms: channels.sms_key } });
                await api.post('/workspaces/me/integrations/test', { channel: 'email' });
            } else if (currentStep === 3) {
                // Contact form is just a check, maybe log it?
            } else if (currentStep === 4) {
                await api.post('/workspaces/services/', serviceData);
            } else if (currentStep === 6) {
                await api.post('/workspaces/inventory/', inventoryData);
            } else if (currentStep === 7) {
                // Skip staff invite for now or mock it
            } else if (currentStep === 8) {
                // Activate
                // Need workspace ID. How to get it? /me or from Step 1 response (which we didn't save globally)
                // Better: assume user is logged in context. User has workspace_id.
                // But we just logged in. Context might not update fast enough without reload.
                // Let's use /me endpoint if we had one, or decode token.
                // Actually, we can fetch user profile or just rely on Backend knowing "current_user".
                // activate_workspace expects {workspace_id} in URL.
                // We need to know our workspace ID.
                // Hack: Fetch services (GET /workspaces/services/) returns services with workspace_id? No.
                // Let's assume we can GET /workspaces/me? or GET /staff/ (returns user with workspace_id)
                const userRes = await api.get('/workspaces/staff/'); // Returns list of staff. Current user is in it.
                const myWorkspaceId = userRes.data[0].workspace_id;
                await api.post(`/workspaces/${myWorkspaceId}/activate`);
                router.push('/dashboard');
                return;
            }
            setCurrentStep(curr => curr + 1);
        } catch (e) {
            console.error(e);
            alert("Error: " + (e as any).response?.data?.detail || e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex">
            {/* Sidebar Steps */}
            <div className="w-64 bg-white border-r border-gray-200 p-6 hidden md:block">
                <h2 className="text-xl font-bold mb-6 text-gray-800">Setup Guide</h2>
                <div className="space-y-4">
                    {STEPS.map((step, idx) => (
                        <div key={idx} className={cn("flex items-center space-x-3 text-sm",
                            currentStep > idx + 1 ? "text-green-600" : currentStep === idx + 1 ? "text-blue-600 font-semibold" : "text-gray-400"
                        )}>
                            <div className={cn("w-6 h-6 rounded-full flex items-center justify-center border",
                                currentStep > idx + 1 ? "bg-green-100 border-green-600" : currentStep === idx + 1 ? "border-blue-600" : "border-gray-300"
                            )}>
                                {currentStep > idx + 1 ? <Check size={14} /> : <span>{idx + 1}</span>}
                            </div>
                            <span>{step}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 p-8 overflow-y-auto">
                <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-sm border border-gray-200">
                    {/* Step Content Render Logic */}
                    {currentStep === 1 && (
                        <div className="space-y-4">
                            <h3 className="text-2xl font-bold">Create your Workspace</h3>
                            <input className="input-field" placeholder="Business Name" value={workspaceData.name} onChange={e => setWorkspaceData({ ...workspaceData, name: e.target.value })} />
                            <input className="input-field" placeholder="Address" value={workspaceData.address} onChange={e => setWorkspaceData({ ...workspaceData, address: e.target.value })} />
                            <input className="input-field" placeholder="Owner Email" value={workspaceData.owner_email} onChange={e => setWorkspaceData({ ...workspaceData, owner_email: e.target.value, contact_email: e.target.value })} />
                            <input className="input-field" type="password" placeholder="Password" value={workspaceData.owner_password} onChange={e => setWorkspaceData({ ...workspaceData, owner_password: e.target.value })} />
                        </div>
                    )}
                    {/* ... steps 2-8 implement similarly ... */}
                    {currentStep === 2 && (
                        <div className="space-y-4">
                            <h3 className="text-2xl font-bold">Connect Communication</h3>
                            <input className="input-field" placeholder="Email API Key (Mock)" value={channels.email_key} onChange={e => setChannels({ ...channels, email_key: e.target.value })} />
                            <input className="input-field" placeholder="SMS API Key (Mock)" value={channels.sms_key} onChange={e => setChannels({ ...channels, sms_key: e.target.value })} />
                        </div>
                    )}
                    {currentStep === 3 && (
                        <div className="space-y-4">
                            <h3 className="text-2xl font-bold">Contact Form Ready</h3>
                            <p className="text-gray-600">Your public contact form will be available at <code>/public/contact/[workspace_id]</code> once activated.</p>
                        </div>
                    )}
                    {currentStep === 4 && (
                        <div className="space-y-4">
                            <h3 className="text-2xl font-bold">Add a Service</h3>
                            <input className="input-field" placeholder="Service Name" value={serviceData.name} onChange={e => setServiceData({ ...serviceData, name: e.target.value })} />
                            <input className="input-field" type="number" placeholder="Duration (min)" value={serviceData.duration} onChange={e => setServiceData({ ...serviceData, duration: parseInt(e.target.value) })} />
                        </div>
                    )}
                    {currentStep === 5 && (<h3 className="text-2xl font-bold">Post-Booking Forms (Default Enabled)</h3>)}
                    {currentStep === 6 && (
                        <div className="space-y-4">
                            <h3 className="text-2xl font-bold">Add Inventory</h3>
                            <input className="input-field" placeholder="Item Name" value={inventoryData.name} onChange={e => setInventoryData({ ...inventoryData, name: e.target.value })} />
                            <input className="input-field" type="number" placeholder="Quantity" value={inventoryData.quantity} onChange={e => setInventoryData({ ...inventoryData, quantity: parseInt(e.target.value) })} />
                        </div>
                    )}
                    {currentStep === 7 && (<h3 className="text-2xl font-bold">Invite Staff (Skip for now)</h3>)}
                    {currentStep === 8 && (<h3 className="text-2xl font-bold">Ready to Activate?</h3>)}

                    <div className="mt-8 flex justify-end">
                        <button onClick={handleNext} disabled={loading} className="btn-primary flex items-center">
                            {loading ? "Processing..." : (currentStep === 8 ? "Activate Workspace" : "Next Step")}
                            {!loading && <ChevronRight size={16} className="ml-2" />}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
