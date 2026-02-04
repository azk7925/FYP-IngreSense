import React from 'react';
import { motion } from 'framer-motion';
import { Info, Check, AlertCircle, HelpCircle } from 'lucide-react';

const StatusBadge = ({ status }) => {
    let color = 'bg-slate-100 text-slate-600';
    let icon = HelpCircle;

    if (status.toLowerCase().includes('safe')) {
        color = 'bg-emerald-100 text-emerald-700';
        icon = Check;
    } else if (status.toLowerCase().includes('not') || status.toLowerCase().includes('allergen')) {
        color = 'bg-red-100 text-red-700';
        icon = AlertCircle;
    } else if (status.toLowerCase().includes('unknown')) {
        color = 'bg-slate-100 text-slate-600';
    }

    const Icon = icon;

    return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}>
            <Icon className="w-3 h-3" />
            {status}
        </span>
    );
};

const ExplanationSection = ({ explanations }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="glass-card p-6"
        >
            <div className="flex items-center gap-2 mb-6">
                <Info className="w-5 h-5 text-blue-600" />
                <h2 className="text-xl font-semibold text-slate-800">Detailed Analysis</h2>
            </div>

            <div className="overflow-hidden rounded-xl border border-slate-100">
                <table className="min-w-full divide-y divide-slate-100">
                    <thead className="bg-slate-50/50">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Ingredient</th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Reasoning</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white/50 divide-y divide-slate-100">
                        {explanations.map((item, idx) => (
                            <tr key={idx} className="hover:bg-blue-50/30 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900 capitalize">
                                    {item.name}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    <StatusBadge status={item.status} />
                                </td>
                                <td className="px-6 py-4 text-sm text-slate-600">
                                    {item.details}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </motion.div>
    );
};

export default ExplanationSection;
