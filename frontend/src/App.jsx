import React, { useState } from 'react';
import { Moon, Sun, AlertCircle, CheckCircle, Upload } from 'lucide-react';
import ResultsPanel from './components/ResultsPanel';
import './App.css';

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [apiUrl] = useState('https://patchamomma-api-kxd7wnyafa-uc.a.run.app');

  const handleAnalyze = async (text) => {
    if (!text || text.trim().length < 50) {
      setError('Transcript must be at least 50 characters long');
      return;
    }

    setTranscript(text);
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch(`${apiUrl}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript_text: text }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze transcript');
      }

      const data = await response.json();
      setResults(data);
      setError(null);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing the transcript');
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setTranscript(event.target.result);
      };
      reader.readAsText(files[0]);
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    if (!darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  const downloadResults = () => {
    if (!results) return;
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `analysis-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  const clearResults = () => {
    setResults(null);
    setTranscript('');
    setError(null);
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900 transition-colors">
        {/* Header */}
        <header className="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                  🎯 AI Decision & Accountability Auditor
                </h1>
                <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                  Extract decisions, action items, and dependencies from meetings using AI
                </p>
              </div>
              <button
                onClick={toggleDarkMode}
                className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition"
              >
                {darkMode ? <Sun size={24} /> : <Moon size={24} />}
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Error Alert */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="font-semibold text-red-900 dark:text-red-100">Error</p>
                <p className="text-red-700 dark:text-red-200 text-sm">{error}</p>
              </div>
            </div>
          )}

          {/* Results or Upload */}
          {results ? (
            <div className="space-y-6">
              {/* Success Alert */}
              <div className="p-4 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="font-semibold text-emerald-900 dark:text-emerald-100">Analysis Complete</p>
                  <p className="text-emerald-700 dark:text-emerald-200 text-sm">
                    Found {results.stats.decision_count} decisions, {results.stats.action_count} action items, and {results.stats.dependency_count} dependencies
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 flex-wrap">
                <button
                  onClick={downloadResults}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition flex items-center gap-2"
                >
                  📥 Download Results (JSON)
                </button>
                <button
                  onClick={clearResults}
                  className="px-6 py-2 bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-white rounded-lg font-semibold hover:bg-slate-300 dark:hover:bg-slate-600 transition"
                >
                  ← Analyze Another
                </button>
              </div>

              {/* Results Panel */}
              <ResultsPanel data={results} />
            </div>
          ) : (
            <>
              {/* Upload Area with Drag & Drop */}
              <div
                className={`border-2 border-dashed rounded-2xl p-12 text-center transition ${
                  dragActive
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <Upload size={48} className="mx-auto mb-4 text-slate-400" />
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                  Upload Your Meeting Transcript
                </h2>
                <p className="text-slate-600 dark:text-slate-400 mb-6">
                  Drag and drop a file, paste text, or use the input below to analyze decisions and action items
                </p>

                <textarea
                  className="w-full h-64 p-4 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
                  placeholder="Paste your meeting transcript here or drag and drop a file..."
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                />

                <div className="text-sm text-slate-600 dark:text-slate-400 mb-6">
                  {transcript.length} characters • {Math.ceil(transcript.length / 5)} words
                  {transcript.length >= 50 && <span className="text-green-600 dark:text-green-400 font-semibold"> ✓ Ready to analyze</span>}
                </div>

                <button
                  onClick={() => handleAnalyze(transcript)}
                  disabled={loading || transcript.length < 50}
                  className={`px-8 py-3 rounded-lg font-semibold text-white transition text-lg ${
                    loading || transcript.length < 50
                      ? 'bg-slate-400 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                >
                  {loading ? '🔄 Analyzing...' : '🚀 Analyze Transcript'}
                </button>

                <p className="text-xs text-slate-500 dark:text-slate-400 mt-4">
                  💡 Tip: Drag and drop a text file here for quick upload
                </p>
              </div>

              {/* Features */}
              <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="card bg-white dark:bg-slate-800 p-6 rounded-lg border border-slate-200 dark:border-slate-700">
                  <div className="text-3xl mb-2">🎯</div>
                  <h3 className="font-bold text-slate-900 dark:text-white">Decision Extraction</h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">
                    Automatically identify all decisions made in your meetings with confidence scoring.
                  </p>
                </div>
                <div className="card bg-white dark:bg-slate-800 p-6 rounded-lg border border-slate-200 dark:border-slate-700">
                  <div className="text-3xl mb-2">✅</div>
                  <h3 className="font-bold text-slate-900 dark:text-white">Action Items</h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">
                    Extract tasks, assignments, deadlines, and priority levels automatically.
                  </p>
                </div>
                <div className="card bg-white dark:bg-slate-800 p-6 rounded-lg border border-slate-200 dark:border-slate-700">
                  <div className="text-3xl mb-2">🔗</div>
                  <h3 className="font-bold text-slate-900 dark:text-white">Dependencies</h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">
                    Map relationships between decisions and actions to prevent conflicts.
                  </p>
                </div>
                <div className="card bg-white dark:bg-slate-800 p-6 rounded-lg border border-slate-200 dark:border-slate-700">
                  <div className="text-3xl mb-2">⚠️</div>
                  <h3 className="font-bold text-slate-900 dark:text-white">Validation</h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">
                    Detect duplicates, missing owners, unrealistic deadlines, and conflicts.
                  </p>
                </div>
                <div className="card bg-white dark:bg-slate-800 p-6 rounded-lg border border-slate-200 dark:border-slate-700">
                  <div className="text-3xl mb-2">🔍</div>
                  <h3 className="font-bold text-slate-900 dark:text-white">Evidence Tracing</h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">
                    Every decision is linked back to the exact transcript excerpt.
                  </p>
                </div>
                <div className="card bg-white dark:bg-slate-800 p-6 rounded-lg border border-slate-200 dark:border-slate-700">
                  <div className="text-3xl mb-2">⚡</div>
                  <h3 className="font-bold text-slate-900 dark:text-white">AI-Powered</h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">
                    Uses Gemini 3.6 Flash for fast, accurate analysis of any meeting.
                  </p>
                </div>
              </div>
            </>
          )}
        </main>

        {/* Footer */}
        <footer className="mt-16 border-t border-slate-200 dark:border-slate-800 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-slate-600 dark:text-slate-400 text-sm">
            <p>AI Decision & Accountability Auditor © 2024</p>
          </div>
        </footer>
      </div>
    </div>
  );
}
