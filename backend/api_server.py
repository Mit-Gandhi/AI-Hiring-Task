from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from typing import List
import uvicorn
from pydantic import BaseModel
import main_file as generator
from pathlib import Path

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store generated PDFs data in memory
generated_pdfs = []

class GenerationRequest(BaseModel):
    role: str
    num_candidates: int

@app.post("/api/generate")
async def generate_profiles(request: GenerationRequest):
    global generated_pdfs
    generated_pdfs = []  # Clear previous data
    
    try:
        # Initialize the generator with your API key
        profile_generator = generator.CandidateProfileGenerator()
        assessment_generator = generator.UniqueAssessmentGenerator(generator.GEMINI_API_KEY)
        behavioral_analyzer = generator.BehavioralAnalyzer(generator.GEMINI_API_KEY)
        market_analyzer = generator.MarketIntelligenceAgent(generator.GEMINI_API_KEY)
        criteria_evaluator = generator.CriteriaEvaluator(generator.GEMINI_API_KEY)
        pdf_generator = generator.PDFGenerator()

        # Create output directories
        os.makedirs("candidate_profiles", exist_ok=True)
        os.makedirs("pdf_reports", exist_ok=True)

        all_candidates = []
        all_assessments = []
        all_evaluations = []
        generated_pdfs = []

        for i in range(1, request.num_candidates + 1):
            # Generate candidate profile
            candidate_profile = profile_generator.generate_profile(i)
            candidate_name = candidate_profile["personal_info"]["name"]

            # Generate assessment
            assessment = assessment_generator.generate_assessment_for_candidate(
                request.role, candidate_profile, i
            )

            # Generate behavioral analysis
            behavioral_analysis = behavioral_analyzer.analyze_candidate(candidate_profile, request.role)

            # Generate evaluation
            evaluation = criteria_evaluator.evaluate_candidate(
                candidate_profile, assessment, behavioral_analysis, request.role
            )

            # Prepare PDF info without generating
            safe_name = "".join(c for c in candidate_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            pdf_filename = f"{safe_name}_{request.role.replace(' ', '_')}_assessment.pdf"

            generated_pdfs.append({
                "filename": pdf_filename,
                "candidateName": candidate_name,
                "score": evaluation["overall_score"],
                "profile": candidate_profile,
                "assessment": assessment,
                "behavioral_analysis": behavioral_analysis
            })

            all_candidates.append(candidate_profile)
            all_assessments.append(assessment)
            all_evaluations.append(evaluation)

        return {
            "status": "success",
            "message": f"Generated {request.num_candidates} profiles",
            "pdfs": generated_pdfs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{filename}")
async def download_pdf(filename: str):
    try:
        # Get cached candidate data
        candidate_data = next(
            (pdf for pdf in generated_pdfs if pdf["filename"] == filename),
            None
        )
        
        if not candidate_data:
            raise HTTPException(status_code=404, detail="Candidate data not found")
        
        # Create PDF on-demand
        pdf_path = os.path.join("pdf_reports", filename)
        pdf_generator = generator.PDFGenerator()
        
        pdf_generator.generate_candidate_pdf(
            candidate_data["profile"],
            candidate_data["assessment"],
            candidate_data["behavioral_analysis"],
            pdf_path
        )
        
        response = FileResponse(pdf_path, filename=filename)
        
        # Clean up the file after sending
        def cleanup(response):
            try:
                os.remove(pdf_path)
            except:
                pass
            return response
        
        response.background = cleanup
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market-analysis")
async def get_market_analysis():
    try:
        market_analyzer = generator.MarketIntelligenceAgent(generator.GEMINI_API_KEY)
        common_roles = [
            "Software Engineer",
            "Data Scientist",
            "Frontend Engineer",
            "Backend Engineer",
            "DevOps Engineer",
            "ML Engineer",
            "Product Manager",
            "Sales Engineer",
            "Solutions Architect"
        ]
        
        analyses = {}
        for role in common_roles:
            analysis = market_analyzer.analyze_market_trends(role)
            analyses[role] = analysis
        
        return {
            "status": "success",
            "analyses": analyses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download-all")
async def download_all_pdfs():
    # Create a zip file of all PDFs
    import zipfile
    from datetime import datetime
    
    zip_filename = f"all_assessments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = os.path.join("pdf_reports", zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for pdf in os.listdir("pdf_reports"):
            if pdf.endswith(".pdf"):
                pdf_path = os.path.join("pdf_reports", pdf)
                zip_file.write(pdf_path, pdf)
    
    return FileResponse(zip_path, filename=zip_filename)

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
