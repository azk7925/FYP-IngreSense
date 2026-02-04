import React from 'react';
import { Search, X, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

const InputSection = ({ input, setInput, onAnalyze, onClear, isLoading }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-6"
        >
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-slate-800 flex items-center gap-2">
                    <Search className="w-5 h-5 text-blue-600" />
                    Input Ingredients
                </h2>
                {input && (
                    <button
                        onClick={onClear}
                        className="text-sm text-slate-500 hover:text-red-500 flex items-center gap-1 transition-colors"
                    >
                        <X className="w-4 h-4" /> Clear
                    </button>
                )}
            </div>

            <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Paste (Ctrl+V) your cosmetic ingredient list here... (e.g. Water, Glycerin, Niacinamide...)"
                className="w-full h-40 p-4 rounded-xl border border-slate-200 bg-white/50 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none transition-all placeholder:text-slate-400 text-slate-700 font-mono text-sm shadow-inner"
            />

            <div className="mt-4 flex justify-end">
                <button
                    onClick={onAnalyze}
                    disabled={!input.trim() || isLoading}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white px-6 py-2.5 rounded-lg font-medium shadow-lg shadow-blue-200 transition-all flex items-center gap-2 active:scale-95"
                >
                    <Sparkles className="w-4 h-4" />
                    Analyze Ingredients
                </button>
            </div>
        </motion.div>
    );
};

export default InputSection;
