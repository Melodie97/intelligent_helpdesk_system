from fastapi import FastAPI, HTTPException
from src.core.help_desk_system import HelpDeskSystem
from src.core.state import HelpDeskRequest, HelpDeskResponse
from config.settings import Config
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(title="Intelligent Help Desk System", version="1.0.0")
    config = Config()
    help_desk = HelpDeskSystem()

    @app.post("/support", response_model=HelpDeskResponse)
    async def process_support_request(request: HelpDeskRequest):
        """Process a help desk support request"""
        try:
            response = help_desk.process_request(request)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}

    @app.get("/categories")
    async def get_categories():
        """Get available request categories"""
        return {"categories": list(help_desk.classifier.categories.keys())}

    @app.get("/config")
    async def get_config():
        """Get current system configuration"""
        return config.get_provider_info()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://helpdesk-ui-three.vercel.app/"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app