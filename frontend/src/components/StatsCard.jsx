import React from 'react';

const colorClasses = {
  blue: 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-600 dark:text-blue-400',
  green: 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800 text-emerald-600 dark:text-emerald-400',
  purple: 'bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-800 text-purple-600 dark:text-purple-400',
  red: 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-600 dark:text-red-400',
};

export default function StatsCard({ icon, label, value, color = 'blue' }) {
  const classes = colorClasses[color] || colorClasses.blue;

  return (
    <div className={`card border ${classes} space-y-2`}>
      <div className="text-3xl">{icon}</div>
      <p className="text-sm font-semibold text-slate-600 dark:text-slate-400">{label}</p>
      <p className="text-3xl font-bold text-slate-900 dark:text-white">{value}</p>
    </div>
  );
}
