import React, { useState, useEffect } from 'react';
import { 
  Building2, 
  User, 
  Users, 
  Briefcase, 
  GraduationCap, 
  IndianRupee, 
  Percent, 
  Calendar, 
  ShieldCheck, 
  ShieldAlert, 
  Clock, 
  MapPin,
  TrendingUp,
  FileSpreadsheet,
  CheckCircle2,
  XCircle,
  HelpCircle,
  ArrowRight,
  TrendingDown
} from 'lucide-react';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

function App() {
  const [activeTab, setActiveTab] = useState('new'); // 'new', 'history'
  const [stats, setStats] = useState({
    total_applications: 0,
    approval_rate: 0,
    approved_count: 0,
    rejected_count: 0,
    average_income: 0,
    average_loan_amount: 0
  });
  const [history, setHistory] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);
  const [explanations, setExplanations] = useState([]);
  const [loadingExplain, setLoadingExplain] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    gender: 'Male',
    married: 'Yes',
    dependents: 0,
    education: 'Graduate',
    self_employed: 'No',
    applicant_income: 5000,
    coapplicant_income: 0,
    loan_amount: 120,
    loan_amount_term: 360,
    credit_history: 1.0,
    property_area: 'Semiurban'
  });

  // Fetch Dashboard Stats and History
  const fetchData = async () => {
    try {
      const statsRes = await fetch(`${API_BASE_URL}/stats`);
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }
      
      const historyRes = await fetch(`${API_BASE_URL}/history`);
      if (historyRes.ok) {
        const historyData = await historyRes.json();
        setHistory(historyData);
      }
    } catch (err) {
      console.error("Error fetching data:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'dependents' || name === 'applicant_income' || name === 'coapplicant_income' || name === 'loan_amount' || name === 'loan_amount_term' || name === 'credit_history' 
        ? parseFloat(value) 
        : value
    }));
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setPredictionResult(null);
    setExplanations([]);

    try {
      const res = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!res.ok) {
        throw new Error("Prediction request failed");
      }

      const data = await res.json();
      setPredictionResult(data);

      // Get explanations for this prediction
      setLoadingExplain(true);
      const explainRes = await fetch(`${API_BASE_URL}/explain/${data.id}`);
      if (explainRes.ok) {
        const explainData = await explainRes.json();
        setExplanations(explainData.explanations);
      }
      setLoadingExplain(false);
      
      // Refresh statistics and history list
      fetchData();
    } catch (err) {
      console.error(err);
      alert("Error processing loan application. Is the backend API running?");
    } finally {
      setSubmitting(false);
    }
  };

  const handleResetForm = () => {
    setPredictionResult(null);
    setExplanations([]);
  };

  return (
    <div className="app-container">
      <div className="bg-glow-1"></div>
      <div className="bg-glow-2"></div>

      <header className="app-header">
        <div className="logo-container">
          <div className="logo-icon">
            <Building2 size={28} />
          </div>
          <div>
            <h1>TrustFlow</h1>
            <p style={{ fontSize: '0.9rem' }}>AI-Powered Credit & Loan Intelligence</p>
          </div>
        </div>
        
        <div className="tab-container" style={{ marginBottom: 0 }}>
          <button 
            className={`tab-btn ${activeTab === 'new' ? 'active' : ''}`}
            onClick={() => setActiveTab('new')}
          >
            New Assessment
          </button>
          <button 
            className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            History & Logs
          </button>
        </div>
      </header>

      {/* Metrics Section */}
      <section className="metrics-grid">
        <div className="metric-card">
          <div className="metric-title">Total Evaluated</div>
          <div className="metric-value">{stats.total_applications}</div>
          <p style={{ fontSize: '0.8rem' }}>Lifetime evaluations logged</p>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Approval Index</div>
          <div className="metric-value metric-accent">
            {(stats.approval_rate * 100).toFixed(1)}%
          </div>
          <p style={{ fontSize: '0.8rem' }}>Overall approval percentage</p>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Avg Income</div>
          <div className="metric-value">
            ₹{Math.round(stats.average_income).toLocaleString()}/mo
          </div>
          <p style={{ fontSize: '0.8rem' }}>Combined main applicant avg</p>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Avg Requested</div>
          <div className="metric-value">
            ₹{Math.round(stats.average_loan_amount * 1000).toLocaleString()}
          </div>
          <p style={{ fontSize: '0.8rem' }}>Average loan request size</p>
        </div>
      </section>

      {activeTab === 'new' ? (
        <div className="main-content">
          {/* Card 1: Application Form */}
          <div className="card">
            <div className="card-title">
              <FileSpreadsheet className="metric-accent" />
              <h2>Applicant Profile</h2>
            </div>
            
            {!predictionResult ? (
              <form onSubmit={handleFormSubmit}>
                <div className="form-grid">
                  <div className="form-group">
                    <label><User size={16} /> Gender</label>
                    <select name="gender" value={formData.gender} onChange={handleInputChange}>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label><Users size={16} /> Married</label>
                    <select name="married" value={formData.married} onChange={handleInputChange}>
                      <option value="Yes">Yes</option>
                      <option value="No">No</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label><Users size={16} /> Dependents</label>
                    <select name="dependents" value={formData.dependents} onChange={handleInputChange}>
                      <option value={0}>None</option>
                      <option value={1}>1</option>
                      <option value={2}>2</option>
                      <option value={3}>3 or more</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label><GraduationCap size={16} /> Education</label>
                    <select name="education" value={formData.education} onChange={handleInputChange}>
                      <option value="Graduate">Graduate</option>
                      <option value="Not Graduate">Not Graduate</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label><Briefcase size={16} /> Self Employed</label>
                    <select name="self_employed" value={formData.self_employed} onChange={handleInputChange}>
                      <option value="No">No</option>
                      <option value="Yes">Yes</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label><MapPin size={16} /> Property Area</label>
                    <select name="property_area" value={formData.property_area} onChange={handleInputChange}>
                      <option value="Urban">Urban</option>
                      <option value="Semiurban">Semiurban</option>
                      <option value="Rural">Rural</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label><IndianRupee size={16} /> Monthly Income (₹)</label>
                    <input 
                      type="number" 
                      name="applicant_income" 
                      value={formData.applicant_income} 
                      onChange={handleInputChange}
                      min="0"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label><IndianRupee size={16} /> Co-applicant Income (₹)</label>
                    <input 
                      type="number" 
                      name="coapplicant_income" 
                      value={formData.coapplicant_income} 
                      onChange={handleInputChange}
                      min="0"
                    />
                  </div>

                  <div className="form-group">
                    <label><IndianRupee size={16} /> Loan Amount (₹ Thousands)</label>
                    <input 
                      type="number" 
                      name="loan_amount" 
                      value={formData.loan_amount} 
                      onChange={handleInputChange}
                      min="1"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label><Clock size={16} /> Loan Term (months)</label>
                    <select name="loan_amount_term" value={formData.loan_amount_term} onChange={handleInputChange}>
                      <option value={120}>10 Years (120 mo)</option>
                      <option value={180}>15 Years (180 mo)</option>
                      <option value={240}>20 Years (240 mo)</option>
                      <option value={300}>25 Years (300 mo)</option>
                      <option value={360}>30 Years (360 mo)</option>
                      <option value={480}>40 Years (480 mo)</option>
                    </select>
                  </div>

                  <div className="form-group full-width">
                    <label><ShieldCheck size={16} /> Credit History Standard</label>
                    <select name="credit_history" value={formData.credit_history} onChange={handleInputChange}>
                      <option value={1.0}>Meets credit guidelines (Good score / no defaults)</option>
                      <option value={0.0}>Does not meet guidelines (Low score / historical defaults)</option>
                    </select>
                  </div>
                </div>

                <button type="submit" className="button" style={{ width: '100%' }} disabled={submitting}>
                  {submitting ? "Analyzing Profile..." : (
                    <>
                      Verify Loan Approval <ArrowRight size={18} />
                    </>
                  )}
                </button>
              </form>
            ) : (
              <div className="result-container">
                <div className={`result-header ${predictionResult.prediction === 1 ? 'approved' : 'rejected'}`}>
                  <div className={`result-badge ${predictionResult.prediction === 1 ? 'approved' : 'rejected'}`}>
                    {predictionResult.prediction === 1 ? "PRE-APPROVED" : "REJECTED"}
                  </div>
                  
                  <div className="meter-wrapper">
                    <div className={`meter-circle ${predictionResult.prediction === 1 ? 'approved' : 'rejected'}`}>
                      <span className="meter-value">{(predictionResult.probability * 100).toFixed(0)}%</span>
                      <span className="meter-label">APPROVAL SCORE</span>
                    </div>
                  </div>

                  <p style={{ fontSize: '0.95rem', marginTop: '12px' }}>
                    {predictionResult.prediction === 1 
                      ? "Congratulations! The profile fits structural parameters for high-probability loan recovery."
                      : "The model has identified critical risk dimensions that fall outside standard approval parameters."}
                  </p>
                </div>

                <button onClick={handleResetForm} className="button" style={{ background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: 'var(--text-primary)' }}>
                  Submit Another Profile
                </button>
              </div>
            )}
          </div>

          {/* Card 2: Explainability & Metrics */}
          <div className="card">
            <div className="card-title">
              <TrendingUp className="metric-accent" />
              <h2>AI Explainability & Risk Analysis</h2>
            </div>
            
            {!predictionResult ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '300px', color: 'var(--text-secondary)' }}>
                <HelpCircle size={48} style={{ strokeWidth: 1, marginBottom: '16px' }} />
                <p style={{ textAlign: 'center', maxWidth: '300px' }}>Fill out the applicant profile and click verify to see automated model explainability.</p>
              </div>
            ) : (
              <div>
                <div style={{ marginBottom: '24px' }}>
                  <h3 style={{ marginBottom: '8px' }}>Decision Parameters</h3>
                  <p style={{ fontSize: '0.9rem' }}>
                    The classification is determined using a Logistic Regression model trained with an Stratified Split (F1: 90.8%). Below are the feature impacts calculated for this decision:
                  </p>
                </div>
                
                {loadingExplain ? (
                  <p>Loading decision explanation...</p>
                ) : (
                  <div className="explanations-list">
                    {explanations.map((item, idx) => (
                      <div key={idx} className={`explain-item ${item.impact.toLowerCase()}`}>
                        <div className={`explain-icon-wrapper ${item.impact.toLowerCase()}`}>
                          {item.impact === 'Positive' ? <CheckCircle2 size={18} /> : <XCircle size={18} />}
                        </div>
                        <div>
                          <div className="explain-title">{item.factor}</div>
                          <div className="explain-desc">{item.description}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      ) : (
        /* History & Logs Panel */
        <div className="card">
          <div className="card-title">
            <Clock className="metric-accent" />
            <h2>Historical Records & Logs</h2>
          </div>
          
          <p style={{ marginBottom: '20px' }}>Real-time logs of applicants processed, along with backend classifications and confidence levels.</p>
          
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Time Logged</th>
                  <th>Gender / Married</th>
                  <th>Education</th>
                  <th>Property</th>
                  <th>Income</th>
                  <th>Request</th>
                  <th>Credit</th>
                  <th>Outcome</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                {history.length === 0 ? (
                  <tr>
                    <td colSpan="9" style={{ textAlign: 'center', padding: '40px' }}>No records logged yet. Run a few assessments!</td>
                  </tr>
                ) : (
                  history.map((record) => (
                    <tr key={record.id}>
                      <td>{new Date(record.applied_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
                      <td>{record.gender || 'N/A'}, Married: {record.married || 'N/A'}</td>
                      <td>{record.education}</td>
                      <td>{record.property_area}</td>
                      <td>₹{record.applicant_income.toLocaleString()}</td>
                      <td>₹{(record.loan_amount * 1000).toLocaleString()}</td>
                      <td>{record.credit_history === 1.0 ? 'Meets' : 'No'}</td>
                      <td>
                        <span className={`badge ${record.status.toLowerCase()}`}>
                          {record.status}
                        </span>
                      </td>
                      <td>{(record.probability * 100).toFixed(0)}%</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
