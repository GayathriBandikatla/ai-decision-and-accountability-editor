import React, { useState } from 'react';
import { Menu, Search, Settings, Bell, User, Download, Plus, Filter, ChevronDown, Eye, EyeOff } from 'lucide-react';
import './EnterpriseApp.css';

export default function EnterpriseApp() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [darkMode, setDarkMode] = useState(true);
  const [expandedCard, setExpandedCard] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [transcript, setTranscript] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiUrl] = useState('https://patchamomma-api-509553055814.us-central1.run.app');

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
        throw new Error(errorData.detail || 'Failed to analyze');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.85) return 'rgb(16, 185, 129)';
    if (confidence >= 0.70) return 'rgb(251, 191, 36)';
    return 'rgb(239, 68, 68)';
  };

  const getPriorityBadge = (text) => {
    const lower = text.toLowerCase();
    if (lower.includes('high') || lower.includes('urgent') || lower.includes('critical')) return 'high';
    if (lower.includes('low')) return 'low';
    return 'medium';
  };

  const filteredDecisions = results?.decisions?.filter(d => {
    const matchSearch = d.text.toLowerCase().includes(searchQuery.toLowerCase());
    const matchFilter = filterStatus === 'all' || getPriorityBadge(d.text) === filterStatus;
    return matchSearch && matchFilter;
  }) || [];

  const filteredActions = results?.action_items?.filter(a => {
    const matchSearch = a.text.toLowerCase().includes(searchQuery.toLowerCase());
    return matchSearch;
  }) || [];

  if (!results) {
    return (
      <div className={`app ${darkMode ? 'dark' : ''}`}>
        <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
        <MainContent>
          <Header setSidebarOpen={setSidebarOpen} darkMode={darkMode} setDarkMode={setDarkMode} />
          <UploadArea onAnalyze={handleAnalyze} loading={loading} error={error} />
        </MainContent>
      </div>
    );
  }

  const decisionCount = results?.stats?.decision_count || 0;
  const actionCount = results?.stats?.action_count || 0;
  const ownerCount = results?.stats?.owner_count || 0;
  const highPriorityCount = results?.decisions?.filter(d => getPriorityBadge(d.text) === 'high').length || 0;

  return (
    <div className={`app ${darkMode ? 'dark' : ''}`}>
      <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
      <MainContent>
        <Header setSidebarOpen={setSidebarOpen} darkMode={darkMode} setDarkMode={setDarkMode} />

        <div className="dashboard-content">
          {/* Summary Stats */}
          <div className="stats-grid">
            <StatCard icon="🎯" label="Decisions" value={decisionCount} color="#3B82F6" />
            <StatCard icon="✅" label="Action Items" value={actionCount} color="#10B981" />
            <StatCard icon="👥" label="Owners" value={ownerCount} color="#8B5CF6" />
            <StatCard icon="⚡" label="High Priority" value={highPriorityCount} color="#F59E0B" />
          </div>

          {/* Filters & Search */}
          <div className="filters-section">
            <div className="search-bar">
              <Search size={20} />
              <input
                type="text"
                placeholder="Search decisions and actions..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <div className="filter-tabs">
              <button
                className={`filter-btn ${filterStatus === 'all' ? 'active' : ''}`}
                onClick={() => setFilterStatus('all')}
              >
                All
              </button>
              <button
                className={`filter-btn ${filterStatus === 'high' ? 'active' : ''}`}
                onClick={() => setFilterStatus('high')}
              >
                High Priority
              </button>
              <button
                className={`filter-btn ${filterStatus === 'medium' ? 'active' : ''}`}
                onClick={() => setFilterStatus('medium')}
              >
                Medium
              </button>
              <button
                className={`filter-btn ${filterStatus === 'low' ? 'active' : ''}`}
                onClick={() => setFilterStatus('low')}
              >
                Low
              </button>
            </div>
          </div>

          {/* Tabs */}
          <div className="tabs-section">
            <div className="tabs">
              <button className="tab active">📊 Decisions ({decisionCount})</button>
              <button className="tab">✓ Action Items ({actionCount})</button>
              <button className="tab">🔗 Dependencies</button>
              <button className="tab">⚠️ Validation</button>
            </div>
          </div>

          {/* Decisions List */}
          <div className="decisions-list">
            {filteredDecisions.map((decision, idx) => (
              <DecisionCard
                key={idx}
                decision={decision}
                index={idx}
                expanded={expandedCard === idx}
                onToggle={() => setExpandedCard(expandedCard === idx ? null : idx)}
                confidenceColor={getConfidenceColor(decision.confidence)}
                priority={getPriorityBadge(decision.text)}
              />
            ))}
          </div>

          {/* Action Items List */}
          {filteredActions.length > 0 && (
            <div className="action-items-section">
              <h3>Action Items</h3>
              <div className="action-items-list">
                {filteredActions.map((action, idx) => (
                  <ActionItemCard key={idx} action={action} index={idx} />
                ))}
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="action-buttons">
            <button className="btn btn-primary" onClick={() => {
              const dataStr = JSON.stringify(results, null, 2);
              const blob = new Blob([dataStr], { type: 'application/json' });
              const url = URL.createObjectURL(blob);
              const link = document.createElement('a');
              link.href = url;
              link.download = `analysis-${new Date().toISOString().split('T')[0]}.json`;
              link.click();
            }}>
              <Download size={18} /> Download Report
            </button>
            <button className="btn btn-secondary" onClick={() => setResults(null)}>
              ← Analyze Another
            </button>
          </div>
        </div>
      </MainContent>
    </div>
  );
}

function Sidebar({ sidebarOpen, setSidebarOpen }) {
  const menuItems = [
    { icon: '📊', label: 'Dashboard' },
    { icon: '🔍', label: 'Audits' },
    { icon: '🎯', label: 'Decisions' },
    { icon: '📈', label: 'Reports' },
    { icon: '⚙️', label: 'Settings' },
  ];

  return (
    <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
      <div className="sidebar-header">
        <div className="logo">
          <span className="logo-icon">🎯</span>
          {sidebarOpen && <span>Patchamomma</span>}
        </div>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item, idx) => (
          <a key={idx} href="#" className="nav-item">
            <span>{item.icon}</span>
            {sidebarOpen && <span>{item.label}</span>}
          </a>
        ))}
      </nav>
    </div>
  );
}

function MainContent({ children }) {
  return <div className="main-content">{children}</div>;
}

function Header({ setSidebarOpen, darkMode, setDarkMode }) {
  return (
    <header className="header">
      <div className="header-left">
        <button className="menu-btn" onClick={() => setSidebarOpen(prev => !prev)}>
          <Menu size={24} />
        </button>
        <h1>AI Decision & Accountability Auditor</h1>
      </div>
      <div className="header-right">
        <Bell size={24} className="icon-btn" />
        <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? '☀️' : '🌙'}
        </button>
        <User size={24} className="icon-btn" />
      </div>
    </header>
  );
}

function StatCard({ icon, label, value, color }) {
  return (
    <div className="stat-card" style={{ borderLeftColor: color }}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-info">
        <div className="stat-label">{label}</div>
        <div className="stat-value" style={{ color }}>{value}</div>
      </div>
    </div>
  );
}

function UploadArea({ onAnalyze, loading, error }) {
  const [text, setText] = useState('');

  return (
    <div className="upload-area">
      {error && <div className="error-banner">{error}</div>}
      <div className="upload-content">
        <div className="upload-icon">📝</div>
        <h2>Upload Meeting Transcript</h2>
        <p>Paste or upload your meeting transcript to analyze decisions and action items</p>
        <textarea
          className="transcript-input"
          placeholder="Paste your meeting transcript here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={10}
        />
        <div className="upload-stats">
          <span>{text.length} characters • {Math.ceil(text.length / 5)} words</span>
          {text.length >= 50 && <span className="ready">✓ Ready to analyze</span>}
        </div>
        <button
          className="btn btn-primary btn-large"
          onClick={() => onAnalyze(text)}
          disabled={loading || text.length < 50}
        >
          {loading ? '🔄 Analyzing...' : '🚀 Analyze Transcript'}
        </button>
      </div>
    </div>
  );
}

function DecisionCard({ decision, index, expanded, onToggle, confidenceColor, priority }) {
  const priorityColors = {
    high: '#EF4444',
    medium: '#F59E0B',
    low: '#6B7280',
  };

  return (
    <div className="decision-card">
      <div className="card-header">
        <div className="card-id">#{index + 1}</div>
        <div className="card-title">{decision.text}</div>
        <div className="card-badges">
          <span className={`badge priority-${priority}`}>
            {priority.toUpperCase()}
          </span>
          <span className="badge confidence">
            {Math.round(decision.confidence * 100)}% Confident
          </span>
        </div>
      </div>
      <div className="card-confidence">
        <div className="confidence-ring" style={{
          background: `conic-gradient(${confidenceColor} 0deg ${decision.confidence * 360}deg, #e5e7eb ${decision.confidence * 360}deg)`
        }}>
          <div className="confidence-inner">
            {Math.round(decision.confidence * 100)}%
          </div>
        </div>
      </div>
      {expanded && (
        <div className="card-details">
          <div className="detail-row">
            <span className="label">Evidence:</span>
            <span className="value">{decision.evidence_text || 'N/A'}</span>
          </div>
          <div className="detail-row">
            <span className="label">Timestamp:</span>
            <span className="value">{decision.evidence_timestamp || 'N/A'}</span>
          </div>
        </div>
      )}
      <button className="expand-btn" onClick={onToggle}>
        {expanded ? '▼ Hide Details' : '▶ View Details'}
      </button>
    </div>
  );
}

function ActionItemCard({ action, index }) {
  return (
    <div className="action-item-card">
      <div className="action-header">
        <div className="action-id">#{index + 1}</div>
        <div className="action-text">{action.text}</div>
      </div>
      <div className="action-info">
        {action.owner && <span className="owner">👤 {action.owner}</span>}
        {action.deadline && <span className="deadline">📅 {action.deadline}</span>}
        {action.priority && <span className={`priority priority-${action.priority}`}>{action.priority}</span>}
      </div>
    </div>
  );
}
