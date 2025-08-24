# Library Management System  

A FastAPI-based system for managing a library, with Docker support.  

## Quick Start (Docker)  

1. **Build and Run**  
   ```bash
   # Build image
   docker build -t library-app .
   
   # Run container
   docker run -d -p 8000:80 --name library-container library-app
   ```
   > If you see permission errors, run with `sudo` or add your user to the `docker` group.  

2. **Access the app**  
   - API: [http://localhost:8000](http://localhost:8000)  
   - Docs: [http://localhost:8000/docs](http://localhost:8000/docs)  

## Key Endpoints  

- `/` → Welcome info  
- `/docs` → Swagger docs    
- `/auth/*` → Authentication  
- `/users/*` → Users  
- `/books/*` → Books  
- `/loans/*` → Loans  
- `/orders/*` → Orders  
- `/statistics/*` → Stats  

## Local Development  

1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

2. Run the app:  
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```  

3. Open [http://localhost:8000](http://localhost:8000)  
