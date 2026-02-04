import React from 'react';
import { motion } from 'framer-motion';

const LoadingSpinner = () => {
    return (
        <div className="flex flex-col items-center justify-center p-8 space-y-4">
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full"
            />
            <p className="text-slate-500 font-medium">Analyzing ingredients...</p>
        </div>
    );
};

export default LoadingSpinner;
