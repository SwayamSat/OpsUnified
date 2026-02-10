"use client"
import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Calendar, Clock, MapPin } from 'lucide-react';

export default function PublicBookingPage({ params }: { params: { workspaceId: string } }) {
    const [services, setServices] = useState([]);
    const [selectedService, setSelectedService] = useState<any>(null);
    const [contactId, setContactId] = useState(''); // Simulated: in real flow might come from URL param or previous step
    const [selectedTime, setSelectedTime] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);

    // Fetch services for workspace
    useEffect(() => {
        // We need a public endpoint for services? 
        // Currently `services.py` requires auth.
        // I should probably add a public endpoint or just make the existing one permissive?
        // Detailed constraints: "All public interactions via links/forms/messages only".
        // Let's assume we need a public/services endpoint or similar.
        // For hackathon speed, let's just add a public fetch to `public.py` or use the authenticated one (which will fail).
        // I need to add `GET /public/workspaces/{id}/services` to `public.py`.
        // I will do that in the backend next.
    }, []);

    const handleBook = async () => {
        if (!selectedService || !selectedTime || !contactId) return;
        setLoading(true);
        try {
            await api.post(`/public/workspaces/${params.workspaceId}/bookings`, {
                service_id: selectedService.id,
                contact_id: parseInt(contactId), // This assumes user knows their ID - in real app, flow is Contact Form -> returns ID -> Redirect to Book? 
                // "Flow A: Contact -> Book ... Booking link shared"
                // Maybe the booking link includes ?contact_id=123
                start_time: selectedTime
            });
            setSubmitted(true);
        } catch (e) {
            alert("Booking failed. Ensure Contact ID is valid.");
        } finally {
            setLoading(false);
        }
    };

    if (submitted) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <div className="text-center p-8 bg-white rounded-xl shadow-lg">
                    <h2 className="text-2xl font-bold text-green-600 mb-2">Booking Confirmed!</h2>
                    <p className="text-gray-600">Check your email/SMS for details.</p>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-2xl mx-auto">
                <h1 className="text-3xl font-bold text-center mb-8">Book a Service</h1>

                {/* Mock Contact ID Input for Demo */}
                <div className="bg-yellow-50 p-4 rounded-lg mb-6 border border-yellow-200 text-sm">
                    <p><strong>Demo Mode:</strong> Please enter your Contact ID (received after submitting contact form).</p>
                    <input
                        type="number"
                        placeholder="Contact ID"
                        value={contactId}
                        onChange={e => setContactId(e.target.value)}
                        className="mt-2 p-2 border rounded"
                    />
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    {/* Service Selection Mock */}
                    <div className="p-6 border-b border-gray-100">
                        <h3 className="font-semibold text-lg mb-4">Select Service</h3>
                        <div className="space-y-3">
                            {/* Hardcoded mock for now if fetch not ready, or will implement fetch */}
                            <div
                                onClick={() => setSelectedService({ id: 1, name: 'Consultation', duration: 60 })}
                                className={`p-4 border rounded-lg cursor-pointer flex justify-between items-center ${selectedService?.id === 1 ? 'border-blue-500 bg-blue-50' : 'hover:bg-gray-50'}`}
                            >
                                <div className="flex items-center">
                                    <div className="bg-blue-100 p-2 rounded text-blue-600 mr-3">
                                        <Clock size={20} />
                                    </div>
                                    <div>
                                        <p className="font-medium">Consultation</p>
                                        <p className="text-sm text-gray-500">60 mins • Online</p>
                                    </div>
                                </div>
                                <div className="text-blue-600 font-medium">$0</div>
                            </div>
                        </div>
                    </div>

                    {/* Time Selection Mock */}
                    {selectedService && (
                        <div className="p-6">
                            <h3 className="font-semibold text-lg mb-4">Select Time</h3>
                            <input
                                type="datetime-local"
                                className="w-full p-3 border rounded-lg"
                                onChange={(e) => setSelectedTime(e.target.value)}
                            />
                        </div>
                    )}

                    <div className="p-6 bg-gray-50 flex justify-end">
                        <button
                            onClick={handleBook}
                            disabled={!selectedService || !selectedTime || !contactId || loading}
                            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50"
                        >
                            {loading ? "Confirming..." : "Confirm Booking"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
