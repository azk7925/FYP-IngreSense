import React, { useState } from 'react';
import { Sparkles, CheckCircle2, XCircle, AlertTriangle, ShieldCheck, Leaf, HeartPulse, Activity } from 'lucide-react';

const categoryIcons = {
  'Halal': ShieldCheck,
  'Vegan': Leaf,
  'Allergen-Safe': HeartPulse,
  'Eco-Friendly': Activity,
};

const XAISection = ({ data }) => {
  const [activeTab, setActiveTab] = useState('contributors');

  if (!data) return null;

  return (
    <div className="bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-indigo-100 mb-8 mt-8 overflow-hidden relative">
      <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
        <Sparkles className="w-48 h-48 text-indigo-600" />
      </div>

      <div className="relative z-10">
        <div className="flex items-center gap-3 mb-6">
          <div className="bg-indigo-100 p-2.5 rounded-xl">
            <Sparkles className="w-6 h-6 text-indigo-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-900">INGRESENSE Deep Analysis</h2>
            {/* <p className="text-sm text-slate-500 font-medium">Model Confidence: <span className="text-indigo-600 capitalize">{data.confidence_level}</span></p> */}
          </div>
        </div>

        {/* Custom Tabs */}
        <div className="flex space-x-2 mb-6 bg-slate-50 p-1.5 rounded-xl">
          <button
            onClick={() => setActiveTab('contributors')}
            className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-200 ${activeTab === 'contributors'
              ? 'bg-white text-indigo-700 shadow-sm border border-indigo-100'
              : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'
              }`}
          >
            Top Contributors
          </button>
          <button
            onClick={() => setActiveTab('evidence')}
            className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-200 ${activeTab === 'evidence'
              ? 'bg-white text-indigo-700 shadow-sm border border-indigo-100'
              : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'
              }`}
          >
            Knowledge Graph Evidence
          </button>
        </div>

        <div className="min-h-[300px]">
          {activeTab === 'contributors' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(data.top_contributors).map(([category, items]) => {
                const Icon = categoryIcons[category] || Activity;
                return (
                  <div key={category} className="bg-slate-50 rounded-2xl p-5 border border-slate-100">
                    <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-200">
                      <Icon className="w-5 h-5 text-indigo-500" />
                      <h3 className="font-bold text-slate-800">{category}</h3>
                    </div>
                    {items.length > 0 ? (
                      <div className="space-y-3">
                        {items.map((item, idx) => (
                          <div key={idx} className="flex items-center justify-between text-sm">
                            <span className="text-slate-700 capitalize break-all mr-2">{item.ingredient}</span>
                            <div className="flex items-center gap-1.5 min-w-fit">
                              {item.impact === 'positive' && <CheckCircle2 className="w-4 h-4 text-emerald-500" />}
                              {item.impact === 'negative' && <XCircle className="w-4 h-4 text-rose-500" />}
                              {item.impact === 'neutral' && <AlertTriangle className="w-4 h-4 text-amber-500" />}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-slate-500 italic">No significant contributors found.</p>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {activeTab === 'evidence' && (
            <div className="space-y-6">
              <div className="overflow-hidden rounded-xl border border-slate-200">
                <table className="min-w-full divide-y divide-slate-200">
                  <thead className="bg-slate-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Name</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Source</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Reasoning</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-slate-100">
                    {data.kg_evidence.map((ev, idx) => {
                      // Determine status based on scores from python response
                      let statusText = "Safe";
                      let statusColor = "bg-emerald-100 text-emerald-700";
                      let StatusIcon = CheckCircle2;

                      const s = ev.scores;
                      if (s.halal < 0.5 || s.vegan < 0.5 || s.allergen > 0.5) {
                        const issues = [];
                        if (s.halal < 0.5) issues.push("Not Halal");
                        if (s.vegan < 0.5) issues.push("Not Vegan");
                        if (s.allergen > 0.5) issues.push("Allergen");
                        statusText = issues.join(", ");
                        statusColor = "bg-rose-100 text-rose-700";
                        StatusIcon = AlertTriangle;
                      }

                      return (
                        <tr key={idx} className="hover:bg-slate-50 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900 capitalize">
                            {ev.ingredient}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm">
                            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${statusColor}`}>
                              <StatusIcon className="w-3.5 h-3.5" />
                              {statusText}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600 capitalize">
                            {ev.source}
                          </td>
                          <td className="px-6 py-4 text-sm text-slate-600 leading-relaxed max-w-md">
                            {ev.reasoning}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {data.ambiguous_ingredients?.length > 0 && (
                <div className="bg-amber-50 rounded-xl p-5 border border-amber-200">
                  <div className="flex items-center gap-3 mb-3 pb-3 border-b border-amber-200/50">
                    <AlertTriangle className="w-5 h-5 text-amber-600" />
                    <h4 className="font-bold text-amber-800">Unknown or Ambiguous Ingredients</h4>
                  </div>
                  <div className="overflow-hidden rounded-lg border border-amber-200/50">
                    <table className="min-w-full divide-y divide-amber-200/50 bg-white">
                      <thead className="bg-amber-50/50">
                        <tr>
                          <th scope="col" className="px-4 py-2.5 text-left text-xs font-semibold text-amber-800 uppercase tracking-wider">Name</th>
                          {/* <th scope="col" className="px-4 py-2.5 text-left text-xs font-semibold text-amber-800 uppercase tracking-wider">Status</th> */}
                          <th scope="col" className="px-4 py-2.5 text-left text-xs font-semibold text-amber-800 uppercase tracking-wider">Reason</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-amber-100">
                        {data.ambiguous_ingredients.map((amb, idx) => (
                          <tr key={idx} className="hover:bg-amber-50/30">
                            <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-slate-900 capitalize">{amb.ingredient}</td>
                            {/* <td className="px-4 py-3 whitespace-nowrap text-sm">
                                 <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
                                    Unknown
                                 </span>
                              </td> */}
                            <td className="px-4 py-3 text-sm text-amber-700">{amb.reason}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default XAISection;
