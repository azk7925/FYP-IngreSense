import React, { useState } from 'react';
import { Sparkles, CheckCircle2, XCircle, AlertTriangle, ShieldCheck, Leaf, HeartPulse, Activity, CloudCog } from 'lucide-react';

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
            onClick={() => setActiveTab('all_contributors')}
            className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-200 ${activeTab === 'all_contributors'
              ? 'bg-white text-indigo-700 shadow-sm border border-indigo-100'
              : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'
              }`}
          >
            All Factors
          </button>
          <button
            onClick={() => setActiveTab('evidence')}
            className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-200 ${activeTab === 'evidence'
              ? 'bg-white text-indigo-700 shadow-sm border border-indigo-100'
              : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'
              }`}
          >
            Explanation Section
          </button>
        </div>

        <div className="min-h-[300px]">
          {activeTab === 'contributors' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(data.all_contributors).map(([category, factors]) => {
                const Icon = categoryIcons[category] || Activity;
                // For Top Contributors, just show up to 5 supporting factors
                const topSupporting = factors.supporting.slice(0, 5);

                return (
                  <div key={category} className="bg-slate-50 rounded-2xl p-5 border border-slate-100">
                    <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-200">
                      <Icon className="w-5 h-5 text-indigo-500" />
                      <h3 className="font-bold text-slate-800">{category}</h3>
                    </div>
                    {topSupporting.length > 0 ? (
                      <div className="space-y-3">
                        {topSupporting.map((item, idx) => (
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
                      <p className="text-sm text-slate-500 italic">No primary contributors found.</p>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {activeTab === 'all_contributors' && (
            <div className="space-y-6">
              {Object.entries(data.all_contributors).map(([category, factors]) => {
                const Icon = categoryIcons[category] || Activity;

                return (
                  <div key={`all-${category}`} className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                    <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
                      <div className="bg-indigo-50 p-2 rounded-lg">
                        <Icon className="w-6 h-6 text-indigo-600" />
                      </div>
                      <h3 className="text-xl font-bold text-slate-800">{category} Factors</h3>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Supporting Factors */}
                      <div className="bg-emerald-50/50 rounded-xl p-4 border border-emerald-100">
                        <div className="flex items-center gap-2 mb-3 text-emerald-700 font-semibold">
                          <CheckCircle2 className="w-5 h-5" />
                          <h4>Supporting {category} Status</h4>
                        </div>
                        {factors.supporting.length > 0 ? (
                          <ul className="space-y-2">
                            {factors.supporting.map((item, idx) => (
                              <li key={idx} className="flex items-center justify-between text-sm bg-white p-2 rounded-lg border border-emerald-50">
                                <span className="capitalize text-slate-700">{item.ingredient}</span>
                                {/* <span className="bg-emerald-100 text-emerald-700 font-medium px-2 py-0.5 rounded-md text-xs border border-emerald-200">
                                  +{Math.round((item.score) * 100)}% Match
                                </span> */}
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <p className="text-sm text-emerald-600/70 italic p-2">None found</p>
                        )}
                      </div>

                      {/* Preventing Factors */}
                      <div className="bg-rose-50/50 rounded-xl p-4 border border-rose-100">
                        <div className="flex items-center gap-2 mb-3 text-rose-700 font-semibold">
                          <XCircle className="w-5 h-5" />
                          <h4>Preventing {category} Status</h4>
                        </div>
                        {factors.preventing.length > 0 ? (
                          <ul className="space-y-2">
                            {factors.preventing.map((item, idx) => (
                              <li key={idx} className="flex items-center justify-between text-sm bg-white p-2 rounded-lg border border-rose-50">
                                <span className="capitalize text-slate-700">{item.ingredient}</span>
                                {/* <span className="bg-rose-100 text-rose-700 font-medium px-2 py-0.5 rounded-md text-xs border border-rose-200">
                                  -{Math.round((item.score) * 100)}% Match
                                </span> */}
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <p className="text-sm text-rose-600/70 italic p-2">None found</p>
                        )}
                      </div>
                    </div>
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
                    {data.ingredient_reasoning && Object.entries(data.ingredient_reasoning).map(([ingredient, labels], idx) => {
                      let statusText = "Safe";
                      let statusColor = "bg-emerald-100 text-emerald-700";
                      let StatusIcon = CheckCircle2;

                      const issues = [];
                      if (labels['Halal']?.impact_raw?.includes('negatively') || labels['Halal']?.impact === 'preventing') issues.push("Not Halal");
                      if (labels['Vegan']?.impact_raw?.includes('negatively') || labels['Vegan']?.impact === 'preventing') issues.push("Not Vegan");
                      if (labels['Allergen-Safe']?.impact_raw?.includes('negatively') || labels['Allergen-Safe']?.impact === 'preventing') issues.push("Allergen");
                      if (labels['Eco-Friendly']?.impact_raw?.includes('negatively') || labels['Eco-Friendly']?.impact === 'preventing') issues.push("Not Eco");

                      if (issues.length > 0) {
                        statusText = issues.join(", ");
                        statusColor = "bg-rose-100 text-rose-700";
                        StatusIcon = AlertTriangle;
                      }

                      const source = labels['Halal']?.source || 'unknown';
                      const attn = labels['Halal']?.attention_weight || 0;

                      return (
                        <tr key={idx} className="hover:bg-slate-50 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900 capitalize">
                            {ingredient}
                            {/* <div className="text-xs text-slate-500 font-normal mt-0.5">Model Attention: {attn.toFixed(1)}%</div> */}
                          </td>
                          <td className="px-6 py-4 text-sm max-w-[150px]">
                            <span className={`inline-flex flex-wrap items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-medium ${statusColor}`}>
                              <StatusIcon className="w-3.5 h-3.5 flex-shrink-0" />
                              <span className="leading-tight">{statusText}</span>
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600 capitalize">
                            {source}
                          </td>
                          <td className="px-6 py-4 text-sm text-slate-600 leading-relaxed max-w-md">
                            <div className="space-y-3">
                              {Object.entries(labels).map(([l, d]) => (
                                <div key={l} className="flex flex-col gap-1 text-xs">
                                  <span className="font-bold text-slate-800">{l}:</span>
                                  <span className="text-slate-600">{d.reasoning}</span>
                                </div>
                              ))}
                            </div>
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
