import React, { useState } from 'react';
import { ChevronDown, Calendar, User } from 'lucide-react';

export default function ActionsTab({ actions }) {
  const [expandedId, setExpandedId] = useState(null);

  if (!actions || actions.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-600 dark:text-slate-400">No action items extracted</p>
      </div>
    );
  }

  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300';
      case 'medium':
        return 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300';
      case 'low':
        return 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300';
      default:
        return 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300';
    }
  };

  return (
    <div className="space-y-3">
      {actions.map((action, idx) => (
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
                <span className={`px-2 py-0.5 rounded text-xs font-semibold capitalize ${getPriorityColor(action.priority)}`}>
                  {action.priority} priority
                </span>
                {action.status && (
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                    action.status === 'completed'
                      ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
                  }`}>
                    {action.status}
                  </span>
                )}
              </div>
              <p className="text-slate-900 dark:text-white font-semibold line-clamp-2">
                {action.text}
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
              {/* Owner and Deadline */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400 font-semibold text-sm mb-2">
                    <User className="w-4 h-4" />
                    Owner
                  </div>
                  <p className="text-slate-900 dark:text-white">
                    {action.owner ? (
                      <span className="px-2 py-1 bg-white dark:bg-slate-900 rounded border border-slate-200 dark:border-slate-700 inline-block text-sm">
                        {action.owner}
                      </span>
                    ) : (
                      <span className="text-slate-400 italic">Unassigned</span>
                    )}
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400 font-semibold text-sm mb-2">
                    <Calendar className="w-4 h-4" />
                    Deadline
                  </div>
                  <p className="text-slate-900 dark:text-white">
                    {action.deadline ? (
                      <span className="px-2 py-1 bg-white dark:bg-slate-900 rounded border border-slate-200 dark:border-slate-700 inline-block text-sm">
                        {action.deadline}
                      </span>
                    ) : (
                      <span className="text-slate-400 italic">No deadline</span>
                    )}
                  </p>
                </div>
              </div>

              {/* Evidence */}
              <div>
                <p className="text-sm font-semibold text-slate-600 dark:text-slate-400 mb-2">📋 Evidence</p>
                <div className="bg-white dark:bg-slate-900 p-3 rounded border border-slate-200 dark:border-slate-700">
                  <p className="text-sm text-slate-700 dark:text-slate-300 italic">"{action.evidence_text}"</p>
                </div>
              </div>

              {/* Related Decision */}
              {action.related_decision_id && (
                <div>
                  <p className="text-sm font-semibold text-slate-600 dark:text-slate-400 mb-2">🔗 Related Decision</p>
                  <p className="text-sm text-primary-600 dark:text-primary-400">
                    {action.related_decision_id}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
