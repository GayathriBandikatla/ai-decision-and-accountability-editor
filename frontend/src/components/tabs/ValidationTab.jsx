import React, { useState } from 'react';
import { AlertCircle, CheckCircle } from 'lucide-react';

export default function ValidationTab({ validation, conflicts }) {
  const [expandedSection, setExpandedSection] = useState('decisions');

  const decisionIssues = validation?.decisions?.issues || [];
  const actionIssues = validation?.actions?.issues || [];
  const conflictList = conflicts?.conflicts || [];
  const hasIssues = decisionIssues.length > 0 || actionIssues.length > 0 || conflictList.length > 0;

  const getIssueIcon = (type) => {
    const icons = {
      duplicate: '🔄',
      low_confidence: '⚠️',
      missing_evidence: '❓',
      missing_speaker: '👤',
      vague_decision: '🤔',
      missing_owner: '👤',
      ambiguous_owner: '❓',
      missing_deadline: '📅',
      past_deadline: '⏰',
      unrealistic_deadline: '⚠️',
      vague_action: '🤔',
      duplicate_action: '🔄',
      contradictory_decisions: '⚡',
      unowned_critical_task: '🚨',
      unclear_responsibility: '❓',
      orphaned_action: '🔗',
    };
    return icons[type] || '⚠️';
  };

  const getIssueSeverity = (type) => {
    const high = ['contradictory_decisions', 'unowned_critical_task', 'past_deadline', 'missing_owner'];
    const medium = ['low_confidence', 'missing_deadline', 'ambiguous_owner', 'unclear_responsibility'];
    if (high.includes(type)) return 'high';
    if (medium.includes(type)) return 'medium';
    return 'low';
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800';
      case 'medium':
        return 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800';
      default:
        return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800';
    }
  };

  if (!hasIssues) {
    return (
      <div className="text-center py-12">
        <CheckCircle className="w-16 h-16 text-emerald-600 dark:text-emerald-400 mx-auto mb-4" />
        <p className="text-xl font-semibold text-emerald-900 dark:text-emerald-100">No Issues Found!</p>
        <p className="text-emerald-700 dark:text-emerald-200 mt-2">
          All decisions and action items passed validation checks.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Decision Issues */}
      {decisionIssues.length > 0 && (
        <div>
          <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
            🎯 Decision Issues ({decisionIssues.length})
          </h3>
          <div className="space-y-2">
            {decisionIssues.map((issue, idx) => (
              <div
                key={idx}
                className={`card border p-4 flex gap-3 ${getSeverityColor(getIssueSeverity(issue.type))}`}
              >
                <span className="text-2xl flex-shrink-0">{getIssueIcon(issue.type)}</span>
                <div className="flex-1">
                  <p className="font-semibold text-slate-900 dark:text-white capitalize">
                    {issue.type.replace(/_/g, ' ')}
                  </p>
                  <p className="text-sm text-slate-700 dark:text-slate-300 mt-1">
                    {issue.message}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Issues */}
      {actionIssues.length > 0 && (
        <div>
          <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
            ✅ Action Item Issues ({actionIssues.length})
          </h3>
          <div className="space-y-2">
            {actionIssues.map((issue, idx) => (
              <div
                key={idx}
                className={`card border p-4 flex gap-3 ${getSeverityColor(getIssueSeverity(issue.type))}`}
              >
                <span className="text-2xl flex-shrink-0">{getIssueIcon(issue.type)}</span>
                <div className="flex-1">
                  <p className="font-semibold text-slate-900 dark:text-white capitalize">
                    {issue.type.replace(/_/g, ' ')}
                  </p>
                  <p className="text-sm text-slate-700 dark:text-slate-300 mt-1">
                    {issue.message}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Conflicts */}
      {conflictList.length > 0 && (
        <div>
          <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
            ⚡ Potential Conflicts ({conflictList.length})
          </h3>
          <div className="space-y-2">
            {conflictList.map((conflict, idx) => (
              <div
                key={idx}
                className={`card border p-4 flex gap-3 ${getSeverityColor(getIssueSeverity(conflict.type))}`}
              >
                <span className="text-2xl flex-shrink-0">{getIssueIcon(conflict.type)}</span>
                <div className="flex-1">
                  <p className="font-semibold text-slate-900 dark:text-white capitalize">
                    {conflict.type.replace(/_/g, ' ')}
                  </p>
                  <p className="text-sm text-slate-700 dark:text-slate-300 mt-1">
                    {conflict.message}
                  </p>
                  {conflict.decision_a_text && (
                    <div className="mt-2 pt-2 border-t border-slate-300 dark:border-slate-600 text-xs space-y-1">
                      <p><strong>A:</strong> {conflict.decision_a_text}</p>
                      <p><strong>B:</strong> {conflict.decision_b_text}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Statistics */}
      <div className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-800">
        <h3 className="text-lg font-bold mb-4">📊 Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="card border border-slate-200 dark:border-slate-800">
            <p className="text-sm text-slate-600 dark:text-slate-400">Total Issues</p>
            <p className="text-2xl font-bold text-slate-900 dark:text-white">
              {decisionIssues.length + actionIssues.length + conflictList.length}
            </p>
          </div>
          <div className="card border border-slate-200 dark:border-slate-800">
            <p className="text-sm text-slate-600 dark:text-slate-400">Decision Issues</p>
            <p className="text-2xl font-bold text-slate-900 dark:text-white">{decisionIssues.length}</p>
          </div>
          <div className="card border border-slate-200 dark:border-slate-800">
            <p className="text-sm text-slate-600 dark:text-slate-400">Action Issues</p>
            <p className="text-2xl font-bold text-slate-900 dark:text-white">{actionIssues.length}</p>
          </div>
          <div className="card border border-slate-200 dark:border-slate-800 col-span-2 md:col-span-1">
            <p className="text-sm text-slate-600 dark:text-slate-400">Conflicts</p>
            <p className="text-2xl font-bold text-slate-900 dark:text-white">{conflictList.length}</p>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">💡 Recommendations</h4>
        <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
          {decisionIssues.some(i => i.type === 'missing_evidence') && (
            <li>• Ensure all decisions have supporting evidence from the transcript</li>
          )}
          {actionIssues.some(i => i.type === 'missing_owner') && (
            <li>• Assign owners to all action items for accountability</li>
          )}
          {actionIssues.some(i => i.type === 'missing_deadline') && (
            <li>• Add deadlines to high-priority action items</li>
          )}
          {conflictList.some(c => c.type === 'contradictory_decisions') && (
            <li>• Review and reconcile contradictory decisions</li>
          )}
        </ul>
      </div>
    </div>
  );
}
