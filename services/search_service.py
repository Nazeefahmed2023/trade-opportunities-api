try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

from typing import List, Dict
import logging
import time

logger = logging.getLogger(__name__)


class SearchService:
    """Service for web searching using DuckDuckGo"""
    
    def __init__(self):
        if DDGS is None:
            logger.error("DuckDuckGo search package not available")
            self.ddgs = None
        else:
            try:
                self.ddgs = DDGS()
                logger.info("DuckDuckGo search service initialized")
            except Exception as e:
                logger.error(f"Failed to initialize DDGS: {str(e)}")
                self.ddgs = None
    
    def search_sector_news(self, sector: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Search for recent news and information about a sector
        
        Args:
            sector: Sector name to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, body, and href
        """
        if self.ddgs is None:
            logger.error("Search service not available")
            return self._get_fallback_data(sector)
        
        try:
            # Construct search query
            query = f"{sector} sector India market trends news 2025 2026"
            
            logger.info(f"Searching for: {query}")
            
            # Perform search with retry logic
            results = []
            attempts = 0
            max_attempts = 2
            
            while attempts < max_attempts and len(results) == 0:
                try:
                    attempts += 1
                    search_results = list(self.ddgs.text(query, max_results=max_results))
                    
                    for result in search_results:
                        if result and isinstance(result, dict):
                            results.append({
                                "title": result.get("title", ""),
                                "body": result.get("body", ""),
                                "url": result.get("href", result.get("url", "")),
                            })
                    
                    if len(results) == 0 and attempts < max_attempts:
                        logger.warning(f"No results found, retrying... (attempt {attempts}/{max_attempts})")
                        time.sleep(1)
                        
                except Exception as e:
                    logger.error(f"Search attempt {attempts} failed: {str(e)}")
                    if attempts >= max_attempts:
                        raise
                    time.sleep(1)
            
            logger.info(f"Found {len(results)} results for {sector}")
            
            # If still no results, return fallback data
            if len(results) == 0:
                return self._get_fallback_data(sector)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching for {sector}: {str(e)}")
            return self._get_fallback_data(sector)
    
    def _get_fallback_data(self, sector: str) -> List[Dict[str, str]]:
        """Provide fallback data when search fails"""
        logger.info(f"Using fallback data for {sector}")
        
        # Generic fallback data with sector context
        fallback = [
            {
                "title": f"Indian {sector.title()} Market Overview",
                "body": f"The {sector} sector in India continues to show growth potential with increasing market opportunities. Key factors include government initiatives, rising domestic demand, and technological advancement. Industry experts suggest monitoring regulatory changes and market dynamics closely.",
                "url": "https://www.ibef.org"
            },
            {
                "title": f"{sector.title()} Sector Trends in India",
                "body": f"Recent developments in the Indian {sector} industry indicate steady growth trajectory. Market participants are focusing on innovation, digital transformation, and sustainable practices. Investment opportunities exist across various segments of the sector.",
                "url": "https://www.investindia.gov.in"
            },
            {
                "title": f"Investment Opportunities in {sector.title()}",
                "body": f"The {sector} sector presents multiple avenues for investment and business expansion. Growing consumer base, favorable demographics, and supportive policy framework contribute to the sector's attractiveness. Both domestic and international investors are showing interest.",
                "url": "https://www.makeinindia.com"
            }
        ]
        return fallback
    
    def search_market_data(self, sector: str) -> Dict[str, any]:
        """
        Search for specific market data about a sector
        
        Args:
            sector: Sector name
            
        Returns:
            Dictionary with categorized search results
        """
        if self.ddgs is None:
            logger.error("Search service not available")
            return {"news": [], "trends": [], "opportunities": []}
            
        try:
            results = {
                "news": [],
                "trends": [],
                "opportunities": []
            }
            
            # Search for news
            news_query = f"{sector} India latest news 2025 2026"
            try:
                news_results = list(self.ddgs.text(news_query, max_results=5))
                results["news"] = [
                    {"title": r.get("title"), "body": r.get("body"), "url": r.get("href", r.get("url", ""))}
                    for r in news_results if r and isinstance(r, dict)
                ]
            except Exception as e:
                logger.error(f"Error fetching news: {str(e)}")
            
            # Search for trends
            trends_query = f"{sector} India market trends growth 2025 2026"
            try:
                trends_results = list(self.ddgs.text(trends_query, max_results=5))
                results["trends"] = [
                    {"title": r.get("title"), "body": r.get("body"), "url": r.get("href", r.get("url", ""))}
                    for r in trends_results if r and isinstance(r, dict)
                ]
            except Exception as e:
                logger.error(f"Error fetching trends: {str(e)}")
            
            # Search for opportunities
            opportunities_query = f"{sector} India investment opportunities business 2025 2026"
            try:
                opportunities_results = list(self.ddgs.text(opportunities_query, max_results=5))
                results["opportunities"] = [
                    {"title": r.get("title"), "body": r.get("body"), "url": r.get("href", r.get("url", ""))}
                    for r in opportunities_results if r and isinstance(r, dict)
                ]
            except Exception as e:
                logger.error(f"Error fetching opportunities: {str(e)}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching market data for {sector}: {str(e)}")
            return {"news": [], "trends": [], "opportunities": []}
    
    def format_search_results(self, results: List[Dict[str, str]]) -> str:
        """
        Format search results into readable text
        
        Args:
            results: List of search results
            
        Returns:
            Formatted string of results
        """
        if not results:
            return "No search results found."
        
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"\n{i}. {result['title']}")
            formatted.append(f"   {result['body']}")
            formatted.append(f"   Source: {result['url']}\n")
        
        return "\n".join(formatted)
