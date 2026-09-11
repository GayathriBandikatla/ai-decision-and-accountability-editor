import React from 'react';
import { Moon, Sun } from 'lucide-react';

export default function Header({ darkMode, onToggleDarkMode }) {
  return (
    <header className="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="text-3xl">🎯</div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Patchamomma</h1>
            <p className="text-sm text-slate-600 dark:text-slate-400">AI Decision & Accountability Auditor</p>
          </div>
        </div>

        <button
          onClick={onToggleDarkMode}
          className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          aria-label="Toggle dark mode"
        >
          {darkMode ? (
            <Sun className="w-5 h-5 text-slate-900 dark:text-yellow-400" />
          ) : (
            <Moon className="w-5 h-5 text-slate-600" />
          )}
        </button>
      </div>
    </header>
  );
}
