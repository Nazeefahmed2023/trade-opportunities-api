import google.generativeai as genai
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI analysis using Google Gemini"""
    
    def __init__(self, api_key: str):
        """
        Initialize AI service
        
        Args:
            api_key: Google Gemini API key
        """
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("Gemini AI service initialized with gemini-2.5-flash")
    
    def analyze_sector(self, sector: str, market_data: str) -> str:
        """
        Analyze sector using AI
        
        Args:
            sector: Sector name
            market_data: Collected market data and news
            
        Returns:
            AI-generated analysis report in markdown format
        """
        try:
            prompt = self._create_analysis_prompt(sector, market_data)
            
            logger.info(f"Generating AI analysis for {sector}")
            
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("Empty response from AI")
            
            logger.info(f"AI analysis generated successfully for {sector}")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating AI analysis: {str(e)}")
            return self._generate_fallback_report(sector, market_data)
    
    def _create_analysis_prompt(self, sector: str, market_data: str) -> str:
        """
        Create detailed prompt for AI analysis
        
        Args:
            sector: Sector name
            market_data: Market data
            
        Returns:
            Formatted prompt
        """
        prompt = f"""You are a senior financial analyst specializing in Indian markets with 15+ years of experience. Analyze the {sector} sector in India using the data provided below and create a comprehensive, well-structured market analysis report.

MARKET DATA AND NEWS:
{market_data}

Generate a professional markdown report following this EXACT structure:

# 📊 Market Analysis Report: {sector.title()} Sector in India

---

## 🎯 Executive Summary

Provide a compelling 4-5 sentence overview covering:
- Current market position and size
- Growth trajectory and momentum
- Key opportunity highlights
- Overall investment sentiment

---

## 📈 Current Market Overview

### Market Size & Valuation
- Current market size (estimate if exact data unavailable)
- Year-over-year growth rate
- Market maturity stage

### Key Market Players
1. **Leader 1** - Market share and position
2. **Leader 2** - Market share and position
3. **Leader 3** - Market share and position
4. Other significant players

### Recent Developments (Last 6 Months)
- Major announcements, mergers, partnerships
- Significant policy changes
- Notable market movements

---

## 🔥 Key Market Trends

### 1. [Primary Trend Title]
**Impact:** High/Medium/Low
**Description:** Detailed explanation of the trend
**Timeline:** When this trend is expected to peak

### 2. [Secondary Trend Title]
**Impact:** High/Medium/Low
**Description:** Detailed explanation
**Timeline:** Expected duration

### 3. [Additional Trends...]
Continue for 3-5 major trends

---

## 💼 Trade Opportunities

### 🌟 High-Priority Opportunities

#### Opportunity 1: [Specific Opportunity Name]
- **Description:** What the opportunity entails
- **Target Segment:** Who should pursue this
- **Investment Range:** Estimated capital required
- **Expected ROI:** Potential returns timeline
- **Risk Level:** 🟢 Low / 🟡 Medium / 🔴 High
- **Action Steps:** 3-4 concrete steps to pursue

#### Opportunity 2: [Name]
[Same structure as above]

#### Opportunity 3: [Name]
[Same structure as above]

### 🚀 Emerging High-Growth Segments

1. **[Segment Name]**
   - Growth Rate: X% annually
   - Market Size: Current and projected
   - Key Success Factors

2. **[Segment Name]**
   [Same format]

---

## 📊 Market Drivers & Catalysts

### Positive Drivers ✅
1. **Economic Factors**
   - GDP growth impact
   - Consumer spending trends
   - Income levels

2. **Policy & Regulatory**
   - Government initiatives
   - Regulatory changes
   - Incentives and subsidies

3. **Technology & Innovation**
   - Digital transformation
   - Automation trends
   - R&D investments

4. **Demand Dynamics**
   - Consumer behavior shifts
   - Demographic advantages
   - Market expansion factors

---

## ⚠️ Challenges & Risk Assessment

### Critical Risks 🔴
1. **[Risk Category]**
   - Description
   - Likelihood: High/Medium/Low
   - Mitigation strategies

### Moderate Concerns 🟡
1. **[Challenge]**
   - Impact analysis
   - Management approach

### Competitive Landscape
- Market concentration
- Entry barriers
- Competitive intensity

---

## 💹 Investment Outlook & Ratings

### Short-Term (0-6 months)
**Rating:** ⭐⭐⭐⭐⭐ (1-5 stars)
**Sentiment:** Bullish/Neutral/Bearish
**Key Factors:** List 3-4 factors influencing short-term outlook

### Medium-Term (6-18 months)
**Rating:** ⭐⭐⭐⭐⭐
**Sentiment:** Bullish/Neutral/Bearish
**Key Factors:** List 3-4 factors

### Long-Term (18+ months)
**Rating:** ⭐⭐⭐⭐⭐
**Sentiment:** Bullish/Neutral/Bearish
**Key Factors:** List 3-4 factors

---

## 🎯 Strategic Recommendations

### For Investors
1. **[Recommendation 1]**
   - Rationale
   - Expected outcome
   - Risk considerations

2. **[Recommendation 2]**
   [Same format]

### For Business Owners & Entrepreneurs
1. **[Recommendation 1]**
   - Implementation strategy
   - Resource requirements
   - Success metrics

2. **[Recommendation 2]**
   [Same format]

### For Market Entrants
1. **[Recommendation 1]**
   - Entry strategy
   - Competitive positioning
   - Timeline

---

## 📚 Data Sources

Based on analysis of:
- Market research data
- Recent news and developments
- Industry reports
- Government publications
- Expert analyses

**Key Sources Referenced:**
List specific sources from the market data provided

---

## ⚖️ Important Disclaimer

**Investment Risk Notice:** This report is for informational purposes only and does not constitute financial advice. Market conditions can change rapidly. Investors should:
- Conduct their own due diligence
- Consult with certified financial advisors
- Consider their risk tolerance and investment objectives
- Review all regulatory requirements

**Data Accuracy:** Analysis is based on publicly available information current as of the report generation date. Market dynamics may have evolved since then.

---

**📅 Report Generated:** {self._get_current_date()}  
**🏢 Sector:** {sector.title()}  
**🇮🇳 Market:** India  
**📊 Analysis Type:** Comprehensive Market Intelligence Report

---

*For questions or detailed analysis requests, please consult with market specialists.*

---

INSTRUCTIONS FOR GENERATION:
- Be specific with numbers and data when available from the market data provided
- If exact figures aren't available, provide reasonable estimates with disclaimers
- Use the actual market data sources provided to support your analysis
- Make recommendations actionable and practical
- Maintain professional tone throughout
- Use emojis strategically for visual organization (as shown above)
- Ensure all sections are complete and well-detailed
- Format tables properly if needed
- Bold important terms and figures
"""
        return prompt
    
    def _generate_fallback_report(self, sector: str, market_data: str) -> str:
        """
        Generate basic fallback report if AI fails
        
        Args:
            sector: Sector name
            market_data: Market data
            
        Returns:
            Basic markdown report
        """
        sources_section = ""
        if market_data and len(market_data.strip()) > 50:
            sources_section = f"""
## 📰 Available Market Data & Sources

{market_data}

---
"""
        else:
            sources_section = """
## ⚠️ Data Availability Notice

Unable to retrieve current market data for the {sector} sector at this time.

### Possible Reasons
- 🔍 Limited online information for this specific sector
- 🌐 Network connectivity issues
- 📝 Sector name may need clarification

---
"""
        
        return f"""# 📊 Market Analysis Report: {sector.title()} Sector

---

## ⚠️ Important Notice

**Limited Analysis Available**

This is a basic report generated due to temporary AI service limitations. The full AI-powered analysis is currently unavailable, but we've compiled available market data below.

**For a comprehensive analysis, please try again in a few minutes.**

---

{sources_section}

## 📈 Sector Overview

The **{sector} sector** in India is an important part of the economy with ongoing developments and market activity.

### General Market Characteristics
- Active market with multiple players
- Subject to regulatory oversight
- Influenced by economic and policy factors
- Growing consumer/business interest

---

## 💡 Next Steps & Recommendations

### 1. 🔍 Deep Dive Research
- Review the market data sources listed above
- Explore sector-specific trade publications
- Analyze competitor activities
- Study recent government policies

### 2. 📊 Data Gathering
- Collect financial reports from key players
- Track market size and growth metrics
- Monitor consumer trends
- Identify emerging technologies

### 3. 🤝 Expert Consultation
- Connect with industry veterans
- Engage market research firms
- Attend sector-specific conferences
- Join relevant trade associations

### 4. 📱 Stay Updated
- Subscribe to sector newsletters
- Follow industry thought leaders
- Monitor regulatory announcements
- Track international market trends

---

## 🎯 Suggested Focus Areas

Based on general Indian market dynamics, consider exploring:

1. **Digital Transformation Opportunities**
   - Technology adoption rates
   - E-commerce integration potential
   - Digital payment systems

2. **Policy & Regulatory Landscape**
   - Recent government initiatives
   - Compliance requirements
   - Available subsidies and incentives

3. **Competitive Analysis**
   - Market leaders and challengers
   - Competitive advantages
   - Market share distribution

4. **Consumer Insights**
   - Target demographics
   - Buying behavior patterns
   - Price sensitivity analysis

5. **Supply Chain Dynamics**
   - Sourcing strategies
   - Distribution networks
   - Logistics optimization

---

## 📚 Additional Resources

### Recommended Data Sources
- Ministry websites and official publications
- Industry associations and trade bodies
- Market research reports (Nielsen, Gartner, etc.)
- Business news portals (Economic Times, Business Standard)
- International trade organizations

### Key Metrics to Track
- Market size (current and projected)
- Growth rates (CAGR)
- Investment flows (FDI, VC funding)
- Employment trends
- Export-import data

---

## ⚖️ Disclaimer

**Information Notice:** This report provides general information only and does not constitute financial, investment, or business advice. 

**Action Required:** Conduct thorough due diligence and consult with certified professionals before making any investment or business decisions.

**Data Currency:** Information is based on publicly available data as of the report generation date. Market conditions evolve rapidly.

---

**📅 Report Generated:** {self._get_current_date()}  
**🏢 Sector:** {sector.title()}  
**🇮🇳 Market:** India  
**📄 Report Type:** Basic Market Overview (AI Analysis Pending)

---

**🔄 For Full Analysis:** Please retry in a few minutes when AI services are available for comprehensive insights, trade opportunities, and strategic recommendations.

---
"""
    
    def _get_current_date(self) -> str:
        """Get current date formatted"""
        return datetime.now().strftime("%B %d, %Y")

