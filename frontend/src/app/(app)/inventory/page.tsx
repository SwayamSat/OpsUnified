"use client"
import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Plus, Minus, AlertTriangle } from 'lucide-react';

interface InventoryItem {
    id: number;
    name: string;
    quantity: number;
    low_stock_threshold: number;
}

export default function InventoryPage() {
    const [items, setItems] = useState<InventoryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [newItemName, setNewItemName] = useState("");
    const [newItemQty, setNewItemQty] = useState(0);
    const [newItemThreshold, setNewItemThreshold] = useState(5);
    const [showAddForm, setShowAddForm] = useState(false);

    useEffect(() => {
        fetchInventory();
    }, []);

    const fetchInventory = async () => {
        try {
            const res = await api.get('/workspaces/inventory');
            setItems(res.data);
        } catch (error) {
            console.error("Failed to fetch inventory", error);
        } finally {
            setLoading(false);
        }
    };

    const handleAddItem = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/workspaces/inventory', {
                name: newItemName,
                quantity: newItemQty,
                low_stock_threshold: newItemThreshold
            });
            setNewItemName("");
            setNewItemQty(0);
            setShowAddForm(false);
            fetchInventory();
        } catch (error) {
            console.error("Failed to add item", error);
        }
    };

    const handleUpdateQuantity = async (id: number, currentQty: number, change: number) => {
        try {
            // We can use PUT /inventory/{id} or POST /usage
            // For decrement, usage is better. For increment, PUT?
            // Or just use PUT for everything here for simplicity if allowed.
            // Backend has PUT /inventory/{item_id}.
            // We need to find the item to get other fields? Or just update all?
            // Let's find item in state.
            const item = items.find(i => i.id === id);
            if (!item) return;

            const newQty = item.quantity + change;
            if (newQty < 0) return;

            if (change < 0) {
                // Use usage endpoint for decrement to log it?
                // But validation logic might be strict.
                // Let's use PUT to be safe and simple for "Adjustment".
                await api.put(`/workspaces/inventory/${id}`, {
                    name: item.name,
                    quantity: newQty,
                    low_stock_threshold: item.low_stock_threshold
                });
            } else {
                await api.put(`/workspaces/inventory/${id}`, {
                    name: item.name,
                    quantity: newQty,
                    low_stock_threshold: item.low_stock_threshold
                });
            }
            fetchInventory();
        } catch (error) {
            console.error("Failed to update quantity", error);
        }
    };

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-900">Inventory</h1>
                <button
                    onClick={() => setShowAddForm(!showAddForm)}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                    {showAddForm ? 'Cancel' : 'Add Item'}
                </button>
            </div>

            {showAddForm && (
                <div className="bg-white p-6 rounded-lg shadow mb-6 border border-gray-200">
                    <h2 className="text-lg font-semibold mb-4">Add New Item</h2>
                    <form onSubmit={handleAddItem} className="flex gap-4 items-end">
                        <div className="flex-1">
                            <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                            <input
                                type="text"
                                value={newItemName}
                                onChange={(e) => setNewItemName(e.target.value)}
                                className="w-full border border-gray-300 rounded px-3 py-2"
                                required
                            />
                        </div>
                        <div className="w-32">
                            <label className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                            <input
                                type="number"
                                value={newItemQty}
                                onChange={(e) => setNewItemQty(parseInt(e.target.value))}
                                className="w-full border border-gray-300 rounded px-3 py-2"
                                required
                            />
                        </div>
                        <div className="w-32">
                            <label className="block text-sm font-medium text-gray-700 mb-1">Low Threshold</label>
                            <input
                                type="number"
                                value={newItemThreshold}
                                onChange={(e) => setNewItemThreshold(parseInt(e.target.value))}
                                className="w-full border border-gray-300 rounded px-3 py-2"
                                required
                            />
                        </div>
                        <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                            Save
                        </button>
                    </form>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {items.map((item) => (
                    <div key={item.id} className="bg-white rounded-lg shadow p-6 border border-gray-200 relative">
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <h3 className="text-lg font-bold text-gray-900">{item.name}</h3>
                                <p className="text-sm text-gray-500">Threshold: {item.low_stock_threshold}</p>
                            </div>
                            {item.quantity <= item.low_stock_threshold && (
                                <AlertTriangle className="text-red-500" size={24} />
                            )}
                        </div>

                        <div className="flex items-center justify-between mt-4">
                            <span className={`text-3xl font-bold ${item.quantity <= item.low_stock_threshold ? 'text-red-600' : 'text-gray-900'}`}>
                                {item.quantity}
                            </span>
                            <div className="flex items-center gap-2">
                                <button
                                    onClick={() => handleUpdateQuantity(item.id, item.quantity, -1)}
                                    className="p-2 rounded-full hover:bg-gray-100 text-gray-600"
                                >
                                    <Minus size={20} />
                                </button>
                                <button
                                    onClick={() => handleUpdateQuantity(item.id, item.quantity, 1)}
                                    className="p-2 rounded-full hover:bg-gray-100 text-gray-600"
                                >
                                    <Plus size={20} />
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {!loading && items.length === 0 && (
                <div className="text-center py-12 text-gray-500">No inventory items found. Add one above.</div>
            )}
        </div>
    );
}
