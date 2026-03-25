import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, AlertTriangle, Leaf, Heart } from 'lucide-react';

const ResultCard = ({ label, probability, isPresent, icon: Icon, color, xaiReasoning }) => {
    return (
        <div className={`relative overflow-hidden rounded-xl p-5 border ${isPresent ? 'bg-white border-slate-200 shadow-md' : 'bg-slate-50 border-slate-100 opacity-60'}`}>
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">{label}</p>
                    <h3 className={`text-2xl font-bold mt-1 ${isPresent ? color : 'text-red-600'}`}>
                        {isPresent ? 'Yes' : 'No'}
                    </h3>
                </div>
                <div className={`p-2 rounded-lg ${isPresent ? 'bg-slate-100' : 'bg-slate-100'}`}>
                    <Icon className={`w-6 h-6 ${isPresent ? color : 'text-slate-400'}`} />
                </div>
            </div>

            {xaiReasoning && (
                <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="mt-4 pt-4 border-t border-slate-100"
                >
                    {isPresent && <p className="text-sm text-slate-600 leading-relaxed">
                        {xaiReasoning}
                    </p>}
                </motion.div>
            )}

            {/* <div className="mt-4">
                <div className="flex justify-between text-xs mb-1 text-slate-500">
                    <span>Confidence</span>
                    <span>{(probability * 100).toFixed(1)}%</span>
                </div>
                <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${probability * 100}%` }}
                        transition={{ duration: 1, ease: "easeOut" }}
                        className={`h-full rounded-full ${isPresent ? color.replace('text-', 'bg-') : 'bg-slate-300'}`}
                    />
                </div>
            </div> */}
        </div>
    );
};

const ResultsSection = ({ results, xaiData }) => {
    // Map backend labels to UI config
    // Backend: Halal, Vegan, Contains Allergens, Eco-Friendly
    const getIcon = (label) => {
        if (label.includes('Halal')) return CheckCircle;
        if (label.includes('Vegan')) return Heart;
        if (label.includes('Allergen')) return CheckCircle;
        if (label.includes('Eco')) return Leaf;
        return CheckCircle;
    };

    const getColor = (label, isPresent) => {
        if (!isPresent) return 'text-slate-500'; // Neutral if not present
        if (label === 'Contains Allergens') return 'text-red-500';
        if (label === 'Allergen-Safe' || label.includes('Eco')) return 'text-emerald-500';
        return 'text-blue-600';
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 gap-4"
        >
            {results.map((res, idx) => {
                let xaiKey = res.label;
                if (res.label === 'Contains Allergens') xaiKey = 'Allergen-Safe';

                const reasoning = xaiData?.predictions?.[xaiKey]?.xai_reasoning;

                return (
                    <ResultCard
                        key={idx}
                        label={res.label}
                        probability={res.probability}
                        isPresent={res.is_present}
                        icon={getIcon(res.label)}
                        color={getColor(res.label, res.is_present)}
                        xaiReasoning={reasoning}
                    />
                )
            })}
        </motion.div>
    );
};

export default ResultsSection;
