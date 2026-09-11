import React from 'react';
import { ArrowRight } from 'lucide-react';

export default function DependenciesTab({ dependencies }) {
  if (!dependencies || dependencies.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-600 dark:text-slate-400">No dependencies detected</p>
      </div>
    );
  }

  const getRelationshipIcon = (relationship) => {
    switch (relationship?.toLowerCase()) {
      case 'blocks':
        return '🚫';
      case 'depends_on':
        return '⬅️';
      case 'conflicts_with':
        return '⚡';
      case 'enables':
        return '✅';
      default:
        return '→';
    }
  };

  const getRelationshipColor = (relationship) => {
    switch (relationship?.toLowerCase()) {
      case 'blocks':
        return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-700 dark:text-red-300';
      case 'depends_on':
        return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-700 dark:text-blue-300';
      case 'conflicts_with':
        return 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-300';
      case 'enables':
        return 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300';
      default:
        return 'bg-slate-50 dark:bg-slate-900/20 border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300';
    }
  };

  return (
    <div className="space-y-3">
      {dependencies.map((dep, idx) => (
        <div
          key={idx}
          className={`card border flex items-center gap-4 ${getRelationshipColor(dep.relationship)}`}
        >
          <div className="flex-1 text-right pr-2">
            <div className="font-semibold text-slate-900 dark:text-white">{dep.source_id}</div>
            <p className="text-xs text-slate-600 dark:text-slate-400">Source</p>
          </div>

          <div className="flex flex-col items-center gap-1">
            <span className="text-2xl">{getRelationshipIcon(dep.relationship)}</span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 whitespace-nowrap">
              {dep.relationship.replace('_', ' ')}
            </span>
            <span className="text-xs text-slate-600 dark:text-slate-400">
              {(dep.confidence * 100).toFixed(0)}%
            </span>
          </div>

          <div className="flex-1 pl-2">
            <div className="font-semibold text-slate-900 dark:text-white">{dep.target_id}</div>
            <p className="text-xs text-slate-600 dark:text-slate-400">Target</p>
          </div>
        </div>
      ))}

      {/* Legend */}
      <div className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-800">
        <p className="text-sm font-semibold text-slate-600 dark:text-slate-400 mb-3">Relationship Types</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
          <div className="flex items-center gap-2">
            <span>🚫</span>
            <p><strong>Blocks:</strong> Source prevents target from happening</p>
          </div>
          <div className="flex items-center gap-2">
            <span>⬅️</span>
            <p><strong>Depends On:</strong> Source requires target to be done first</p>
          </div>
          <div className="flex items-center gap-2">
            <span>⚡</span>
            <p><strong>Conflicts:</strong> Source contradicts target</p>
          </div>
          <div className="flex items-center gap-2">
            <span>✅</span>
            <p><strong>Enables:</strong> Source makes target possible or easier</p>
          </div>
        </div>
      </div>
    </div>
  );
}
