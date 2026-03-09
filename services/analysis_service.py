from services.search_service import SearchService
from services.ai_service import AIService
from utils.validators import format_sector_for_search, truncate_text
import logging
import time

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for coordinating market analysis"""
    
    def __init__(self, gemini_api_key: str):
        """
        Initialize analysis service
        
        Args:
            gemini_api_key: Google Gemini API key
        """
        self.search_service = SearchService()
        self.ai_service = AIService(gemini_api_key)
        logger.info("Analysis service initialized")
    
    def analyze_sector(self, sector: str) -> dict:
        """
        Perform complete sector analysis
        
        Args:
            sector: Sector name to analyze
            
        Returns:
            Dictionary with report and metadata
        """
        start_time = time.time()
        
        try:
            # Step 1: Search for market data
            logger.info(f"Starting analysis for sector: {sector}")
            search_query = format_sector_for_search(sector)
            search_results = self.search_service.search_sector_news(sector, max_results=10)
            
            if not search_results:
                logger.warning(f"No search results found for {sector}")
                return {
                    "report": self._generate_no_data_report(sector),
                    "metadata": {
                        "sources_found": 0,
                        "analysis_time": time.time() - start_time
                    }
                }
            
            # Step 2: Format search results for AI
            formatted_data = self._format_data_for_ai(search_results)
            
            # Step 3: Generate AI analysis
            report = self.ai_service.analyze_sector(sector, formatted_data)
            
            # Step 4: Post-process report
            report = self._post_process_report(report, sector)
            
            analysis_time = time.time() - start_time
            
            logger.info(f"Analysis completed for {sector} in {analysis_time:.2f}s")
            
            return {
                "report": report,
                "metadata": {
                    "sources_found": len(search_results),
                    "analysis_time": round(analysis_time, 2)
                }
            }
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            return {
                "report": self._generate_error_report(sector, str(e)),
                "metadata": {
                    "sources_found": 0,
                    "analysis_time": time.time() - start_time,
                    "error": str(e)
                }
            }
    
    def _format_data_for_ai(self, search_results: list) -> str:
        """
        Format search results for AI consumption
        
        Args:
            search_results: List of search results
            
        Returns:
            Formatted string
        """
        formatted = []
        
        for i, result in enumerate(search_results, 1):
            formatted.append(f"\n{'='*80}")
            formatted.append(f"Source {i}: {result['title']}")
            formatted.append(f"{'='*80}")
            formatted.append(f"{result['body']}")
            formatted.append(f"URL: {result['url']}\n")
        
        full_text = "\n".join(formatted)
        
        # Truncate if too long (Gemini has token limits)
        return truncate_text(full_text, max_length=15000)
    
    def _post_process_report(self, report: str, sector: str) -> str:
        """
        Post-process the generated report
        
        Args:
            report: Raw report from AI
            sector: Sector name
            
        Returns:
            Cleaned report
        """
        # Add header if missing
        if not report.startswith("#"):
            report = f"# Market Analysis Report: {sector.title()}\n\n{report}"
        
        # Ensure proper markdown formatting
        report = report.strip()
        
        return report
    
    def _generate_no_data_report(self, sector: str) -> str:
        """Generate report when no data is found"""
        return f"""# Market Analysis Report: {sector.title()} Sector

## Notice
Unable to retrieve current market data for the {sector} sector at this time.

## Possible Reasons
- Limited online information for this specific sector
- Network connectivity issues
- Sector name may need clarification

## Recommendations
1. **Verify Sector Name**: Ensure the sector name is correctly spelled and commonly used
2. **Try Alternative Names**: Use alternative or more specific sector descriptions
3. **Check Spelling**: Common sectors include: pharmaceuticals, technology, agriculture, automotive, banking
4. **Try Again**: Temporary network issues may be resolved

## Available Sectors
Some well-covered Indian sectors include:
- Pharmaceuticals and Healthcare
- Information Technology
- Agriculture and Agritech
- Automotive and Electric Vehicles
- Banking and Financial Services
- Textiles and Apparel
- Renewable Energy
- E-commerce and Retail
- Real Estate and Construction
- Telecommunications

Please try again with a different sector name or check back later.

---
*Report generated with limited data availability*
"""
    
    def _generate_error_report(self, sector: str, error: str) -> str:
        """Generate report when error occurs"""
        return f"""# Market Analysis Report: {sector.title()} Sector

## Service Temporarily Unavailable

We encountered an issue while generating the analysis for the {sector} sector.

## Technical Details
```
{error}
```

## What You Can Do
1. **Try Again**: The issue may be temporary
2. **Check API Keys**: Ensure your Gemini API key is configured correctly
3. **Verify Connectivity**: Check your internet connection
4. **Contact Support**: If the issue persists

## Alternative Options
- Use manual research through business news websites
- Consult industry reports and market analysis publications
- Check government statistics and sector-specific databases

---
*We apologize for the inconvenience. Please try again shortly.*
"""

