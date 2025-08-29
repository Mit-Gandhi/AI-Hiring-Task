import React, { useState } from 'react';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Paper,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Alert,
  MenuItem,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Grid,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import { Download as DownloadIcon, ExpandMore as ExpandMoreIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const roles = [
  "Software Engineer",
  "Data Scientist",
  "Frontend Engineer",
  "Backend Engineer",
  "DevOps Engineer",
  "ML Engineer",
  "Product Manager",
  "Sales Engineer",
  "Solutions Architect"
];

function App() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [role, setRole] = useState('');
  const [numCandidates, setNumCandidates] = useState('');
  const [pdfs, setPdfs] = useState([]);
  const [error, setError] = useState('');
  const [marketAnalyses, setMarketAnalyses] = useState(null);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);

  const handleGenerateClick = () => {
    setStep(2);
  };

  const handleMarketAnalysisClick = async () => {
    setLoadingAnalysis(true);
    setError('');
    try {
      const response = await axios.get(`${API_BASE_URL}/market-analysis`);
      setMarketAnalyses(response.data.analyses);
      setStep(4);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error fetching market analysis');
    } finally {
      setLoadingAnalysis(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/generate`, {
        role,
        num_candidates: parseInt(numCandidates)
      });

      setPdfs(response.data.pdfs);
      setStep(3);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (filename) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/download/${filename}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Error downloading file');
    }
  };

  const handleDownloadAll = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/download-all`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'all_assessments.zip');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Error downloading files');
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8, mb: 4 }}>
        {step === 1 && (
          <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="h4" component="h1" gutterBottom>
              AI-Powered Candidate Assessment Generator
            </Typography>
            <Typography variant="body1" sx={{ mb: 4 }}>
              Generate detailed candidate profiles and assessments using AI
            </Typography>
            <Grid container spacing={2} justifyContent="center">
              <Grid item>
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleGenerateClick}
                >
                  Generate & Analyze
                </Button>
              </Grid>
              <Grid item>
                <Button
                  variant="outlined"
                  size="large"
                  onClick={handleMarketAnalysisClick}
                  disabled={loadingAnalysis}
                >
                  {loadingAnalysis ? <CircularProgress size={24} /> : 'Market Analysis'}
                </Button>
              </Grid>
            </Grid>
          </Paper>
        )}

        {step === 2 && (
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Configure Generation Settings
            </Typography>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            <form onSubmit={handleSubmit}>
              <TextField
                select
                fullWidth
                label="Select Role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                margin="normal"
                required
              >
                {roles.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
              <TextField
                fullWidth
                label="Number of Candidates"
                type="number"
                value={numCandidates}
                onChange={(e) => setNumCandidates(e.target.value)}
                margin="normal"
                required
                inputProps={{ min: 1, max: 20 }}
              />
              <Button
                type="submit"
                variant="contained"
                fullWidth
                sx={{ mt: 3 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Generate Profiles'}
              </Button>
            </form>
          </Paper>
        )}

        {step === 4 && (
          <Paper elevation={3} sx={{ p: 4 }}>
            <Box sx={{ mb: 3, display: 'flex', alignItems: 'center' }}>
              <IconButton onClick={() => setStep(1)} sx={{ mr: 2 }}>
                <ArrowBackIcon />
              </IconButton>
              <Typography variant="h5" component="h2">
                Market Analysis
              </Typography>
            </Box>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            {marketAnalyses && Object.entries(marketAnalyses).map(([role, analysis]) => (
              <Accordion key={role} sx={{ mb: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="h6">{role}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Card variant="outlined" sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="subtitle1" color="primary" gutterBottom>
                        Market Demand
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {analysis.market_demand}
                      </Typography>

                      <Typography variant="subtitle1" color="primary" gutterBottom>
                        Key Skills in Demand
                      </Typography>
                      <Box sx={{ mb: 2 }}>
                        {analysis.key_skills_in_demand.map((skill, index) => (
                          <Chip
                            key={index}
                            label={skill}
                            sx={{ m: 0.5 }}
                            variant="outlined"
                          />
                        ))}
                      </Box>

                      <Typography variant="subtitle1" color="primary" gutterBottom>
                        Salary Insights
                      </Typography>
                      <Typography variant="body2" paragraph>
                        Range: {analysis.salary_insights.range}
                      </Typography>
                      <Typography variant="body2" component="div">
                        Factors:
                        <ul>
                          {analysis.salary_insights.factors.map((factor, index) => (
                            <li key={index}>{factor}</li>
                          ))}
                        </ul>
                      </Typography>

                      <Typography variant="subtitle1" color="primary" gutterBottom>
                        Market Trends
                      </Typography>
                      <ul>
                        {analysis.market_trends.map((trend, index) => (
                          <li key={index}>
                            <Typography variant="body2">{trend}</Typography>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                </AccordionDetails>
              </Accordion>
            ))}
          </Paper>
        )}

        {step === 3 && (
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Generated Profiles
            </Typography>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            <List>
              {pdfs.map((pdf, index) => (
                <ListItem key={index} divider={index !== pdfs.length - 1}>
                  <ListItemText
                    primary={pdf.candidateName}
                    secondary={`Overall Score: ${pdf.score.toFixed(1)}%`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      onClick={() => handleDownload(pdf.filename)}
                    >
                      <DownloadIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
            <Button
              variant="contained"
              fullWidth
              onClick={handleDownloadAll}
              sx={{ mt: 3 }}
            >
              Download All PDFs
            </Button>
            <Button
              variant="outlined"
              fullWidth
              onClick={() => {
                setStep(1);
                setPdfs([]);
                setRole('');
                setNumCandidates('');
              }}
              sx={{ mt: 2 }}
            >
              Start Over
            </Button>
          </Paper>
        )}
      </Box>
    </Container>
  );
}

export default App;
