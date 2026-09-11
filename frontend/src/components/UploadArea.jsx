import React, { useState } from 'react';
import { Upload, FileText, Loader } from 'lucide-react';

export default function UploadArea({ onAnalyze, loading }) {
  const [transcript, setTranscript] = useState('');
  const [isDragging, setIsDragging] = useState(false);

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        setTranscript(event.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setTranscript(event.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleAnalyze = () => {
    onAnalyze(transcript);
  };

  const charCount = transcript.length;
  const wordCount = transcript.trim().split(/\s+/).filter(w => w.length > 0).length;
  const minChars = 50;
  const isValid = charCount >= minChars;

  return (
    <div className="space-y-6">
      {/* Upload Card */}
      <div
        className={`card p-8 transition-all ${
          isDragging
            ? 'border-primary-500 dark:border-primary-400 bg-primary-50 dark:bg-primary-900/20 shadow-lg'
            : ''
        }`}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="flex items-center justify-center mb-6">
          <Upload className="w-12 h-12 text-primary-600 dark:text-primary-400" />
        </div>

        <h2 className="text-2xl font-bold text-center mb-2">Upload Your Meeting Transcript</h2>
        <p className="text-center text-slate-600 dark:text-slate-400 mb-6">
          Drag and drop or paste your meeting transcript to analyze decisions, action items, and dependencies.
        </p>

        {/* Textarea */}
        <textarea
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          placeholder="Paste your meeting transcript here... (minimum 50 characters)"
          className="input-field h-48 mb-4 font-mono text-sm resize-none"
        />

        {/* Character Count */}
        <div className="flex items-center justify-between mb-6 text-sm">
          <div className="text-slate-600 dark:text-slate-400">
            <span className={charCount >= minChars ? 'text-emerald-600 dark:text-emerald-400 font-semibold' : ''}>
              {charCount}
            </span>
            {' '}characters • {wordCount} words
          </div>
          {isValid && (
            <span className="text-emerald-600 dark:text-emerald-400 font-semibold">✓ Ready to analyze</span>
          )}
        </div>

        {/* File Input */}
        <div className="mb-6">
          <input
            type="file"
            accept=".txt,.json,.pdf"
            onChange={handleFileInput}
            className="hidden"
            id="file-input"
          />
          <label
            htmlFor="file-input"
            className="inline-flex items-center gap-2 px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-50 rounded-lg font-semibold hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors cursor-pointer"
          >
            <FileText className="w-5 h-5" />
            Or upload a file
          </label>
        </div>

        {/* Analyze Button */}
        <button
          onClick={handleAnalyze}
          disabled={!isValid || loading}
          className="w-full btn-primary py-3 text-lg font-bold flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader className="w-5 h-5 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              🚀 Analyze Transcript
            </>
          )}
        </button>
      </div>

      {/* Sample Transcripts */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">💡 Tip</h3>
        <p className="text-blue-800 dark:text-blue-200 text-sm">
          Include speaker names and timestamps for best results. Example: "PM: Let's use React by next Friday. Dev: Agreed, I'll set it up."
        </p>
      </div>
    </div>
  );
}
