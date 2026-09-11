import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

export default function DecisionsTab({ decisions }) {
  const [expandedId, setExpandedId] = useState(null);

  if (!decisions || decisions.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-600 dark:text-slate-400">No decisions extracted</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {decisions.map((decision, idx) => (
        <div
          key={idx}
          className="border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden"
        >
          <button
            onClick={() => setExpandedId(expandedId === idx ? null : idx)}
            className="w-full p-4 text-left hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors flex items-start justify-between gap-3"
          >
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold text-slate-500 dark:text-slate-400">#{idx + 1}</span>
                <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                  decision.confidence >= 0.8
                    ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300'
                    : decision.confidence >= 0.6
                    ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300'
                    : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300'
                }`}>
                  {(decision.confidence * 100).toFixed(0)}% confident
                </span>
              </div>
              <p className="text-slate-900 dark:text-white font-semibold line-clamp-2">
                {decision.text}
              </p>
            </div>
            <ChevronDown
              className={`w-5 h-5 text-slate-400 flex-shrink-0 transition-transform ${
                expandedId === idx ? 'rotate-180' : ''
              }`}
            />
          </button>

          {expandedId === idx && (
            <div className="border-t border-slate-200 dark:border-slate-800 p-4 bg-slate-50 dark:bg-slate-800/50 space-y-4">
              {/* Evidence */}
              <div>
                <p className="text-sm font-semibold text-slate-600 dark:text-slate-400 mb-2">📋 Evidence</p>
                <div className="bg-white dark:bg-slate-900 p-3 rounded border border-slate-200 dark:border-slate-700">
                  <p className="text-sm text-slate-700 dark:text-slate-300 italic">"{decision.evidence_text}"</p>
                  {decision.evidence_speaker && (
                    <p className="text-xs text-slate-500 dark:text-slate-500 mt-2">
                      — {decision.evidence_speaker}
                      {decision.evidence_timestamp && ` at ${decision.evidence_timestamp}`}
                    </p>
                  )}
                </div>
              </div>

              {/* Metadata */}
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-slate-600 dark:text-slate-400 font-semibold">Speaker</p>
                  <p className="text-slate-900 dark:text-white">
                    {decision.evidence_speaker || '—'}
                  </p>
                </div>
                <div>
                  <p className="text-slate-600 dark:text-slate-400 font-semibold">Timestamp</p>
                  <p className="text-slate-900 dark:text-white">
                    {decision.evidence_timestamp || '—'}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
