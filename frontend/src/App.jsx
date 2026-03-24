import React, { useState } from 'react';
import axios from 'axios';
import InputSection from './components/InputSection';
import ResultsSection from './components/ResultsSection';
import ExplanationSection from './components/ExplanationSection';
import XAISection from './components/XAISection';
import LoadingSpinner from './components/LoadingSpinner';
import { Microscope, Info, Sparkles } from 'lucide-react';

function App() {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [modelStatus, setModelStatus] = useState(null);
  const [logoError, setLogoError] = useState(false);

  const [xaiData, setXaiData] = useState(null);
  const [isExplaining, setIsExplaining] = useState(false);

  const handleAnalyze = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    setError(null);
    setData(null);
    setXaiData(null); // Reset XAI on new prediction

    try {
      const response = await axios.post('http://127.0.0.1:8000/classify', {
        ingredients: input
      });
      setData(response.data);
      setModelStatus(response.data.model_status);
      console.log(`[Analysis] Source: ${response.data.model_status}`);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze ingredients. Please check if the backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDetailedAnalysis = async () => {
    if (!input.trim()) return;

    setIsExplaining(true);
    setError(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/explain', {
        ingredients: input
      });
      setXaiData(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch detailed analysis. Please check the backend.");
    } finally {
      setIsExplaining(false);
    }
  };

  const handleClear = () => {
    setInput('');
    setData(null);
    setXaiData(null);
    setError(null);
  };

  return (
    <div className="min-h-screen gradient-bg pb-20">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            {!logoError ? (
              <img
                src="/logo.png"
                alt="IngreSense Logo"
                className="h-14 w-auto"
                onError={() => setLogoError(true)}
              />
            ) : (
              <>
                <div className="bg-blue-600 p-2 rounded-lg">
                  <Microscope className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-slate-900 tracking-tight">IngreSense</h1>
                  <p className="text-xs text-slate-500 font-medium tracking-wide">COSMETIC COMPANION</p>
                </div>
              </>
            )}
          </div>
          {modelStatus && (
            <span className={`text-xs px-2 py-1 rounded-md border ${modelStatus === 'Active' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-amber-50 text-amber-700 border-amber-200'}`}>
              Model: {modelStatus}
            </span>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
        {/* Intro */}
        <div className="text-center max-w-2xl mx-auto mb-10">
          <h2 className="text-3xl font-bold text-slate-900 mb-3">Understand What's Inside</h2>
          <p className="text-slate-600 text-lg">
            Enter your cosmetic ingredient list below to instantly analyze for Halal, Vegan, Allergen, and Eco-friendly status.
          </p>
        </div>

        {/* Input */}
        <InputSection
          input={input}
          setInput={setInput}
          onAnalyze={handleAnalyze}
          onClear={handleClear}
          isLoading={isLoading}
        />

        {/* Loading */}
        {isLoading && <LoadingSpinner />}

        {/* Error */}
        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-xl border border-red-200 flex items-center gap-2">
            <Info className="w-5 h-5" />
            {error}
          </div>
        )}

        {/* Results */}
        {data && (
          <div className="space-y-8">
            <ResultsSection results={data.results} />
            {/* <ExplanationSection explanations={data.explanations} /> */}

            {/* Detailed Analysis Button */}
            {!xaiData && (
              <div className="flex justify-center mt-6 ">
                <button
                  onClick={handleDetailedAnalysis}
                  disabled={isExplaining}
                  className="flex items-center gap-2 px-6 py-3 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-xl font-bold transition-all border border-indigo-200 shadow-sm disabled:opacity-50"
                >
                  {isExplaining ? (
                    <>
                      <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
                      Analyzing deeply...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      Get Detailed Analysis
                    </>
                  )}
                </button>
              </div>
            )}

            {/* XAI Section */}
            {xaiData && <XAISection data={xaiData} />}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
