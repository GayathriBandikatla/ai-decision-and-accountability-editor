import React, { useState } from 'react';
import { ChevronDown, AlertCircle, CheckCircle } from 'lucide-react';
import DecisionsTab from './tabs/DecisionsTab';
import ActionsTab from './tabs/ActionsTab';
import DependenciesTab from './tabs/DependenciesTab';
import ValidationTab from './tabs/ValidationTab';
import StatsCard from './StatsCard';

export default function ResultsPanel({ data }) {
  const [activeTab, setActiveTab] = useState('decisions');

  if (!data) return null;

  const stats = data.stats || {};
  const validation = data.validation || {};
  const conflicts = data.conflicts || {};

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          icon="🎯"
          label="Decisions"
          value={stats.decision_count || 0}
          color="blue"
        />
        <StatsCard
          icon="✅"
          label="Action Items"
          value={stats.action_count || 0}
          color="green"
        />
        <StatsCard
          icon="👥"
          label="Owners"
          value={stats.owner_count || 0}
          color="purple"
        />
        <StatsCard
          icon="⚡"
          label="High Priority"
          value={stats.high_priority_count || 0}
          color="red"
        />
      </div>

      {/* Issues Summary */}
      {(validation.decisions?.issue_count > 0 || conflicts.conflict_count > 0) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {validation.decisions?.issue_count > 0 && (
            <div className="card border-l-4 border-amber-500 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-amber-900 dark:text-amber-100">
                  {validation.decisions.issue_count} Decision Issue(s)
                </p>
                <p className="text-amber-700 dark:text-amber-200 text-sm">
                  Check validation tab for details
                </p>
              </div>
            </div>
          )}

          {conflicts.conflict_count > 0 && (
            <div className="card border-l-4 border-red-500 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-red-900 dark:text-red-100">
                  {conflicts.conflict_count} Potential Conflict(s)
                </p>
                <p className="text-red-700 dark:text-red-200 text-sm">
                  Check validation tab for details
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tabs */}
      <div className="card p-0 overflow-hidden">
        <div className="border-b border-slate-200 dark:border-slate-800 flex overflow-x-auto">
          {[
            { id: 'decisions', label: 'Decisions', icon: '🎯' },
            { id: 'actions', label: 'Action Items', icon: '✅' },
            { id: 'dependencies', label: 'Dependencies', icon: '🔗' },
            { id: 'validation', label: 'Validation', icon: '⚠️' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-4 font-semibold border-b-2 transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? 'text-primary-600 dark:text-primary-400 border-primary-600 dark:border-primary-400'
                  : 'text-slate-600 dark:text-slate-400 border-transparent hover:text-slate-900 dark:hover:text-slate-50'
              }`}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'decisions' && <DecisionsTab decisions={data.decisions || []} />}
          {activeTab === 'actions' && <ActionsTab actions={data.action_items || []} />}
          {activeTab === 'dependencies' && <DependenciesTab dependencies={data.dependencies || []} />}
          {activeTab === 'validation' && (
            <ValidationTab validation={validation} conflicts={conflicts} />
          )}
        </div>
      </div>
    </div>
  );
}
