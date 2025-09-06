import httpx
from datetime import datetime, date
from bson import ObjectId
from app.core.config import get_settings
from app.models.dailycontent import DailyContent, Content
from app.models.user import User
from app.models.birthchart import BirthChart

settings = get_settings()

class DailyContentService:
    @staticmethod
    async def get_or_generate_daily_content(user: User) -> dict:
        """Get cached daily content or generate new one."""
        today = date.today()
        user_id = ObjectId(str(user.id))

        # Try to get cached content for today
        cached_content = DailyContent.objects(
            user=user_id,
            date=today
        ).first()

        if cached_content:
            return {
                "dailyAffirmation": cached_content.content.horoscope,
                "dailyChartInsight": cached_content.content.guidance,
                "keyTransits": [
                    {
                        "transit": "Current Transits",
                        "description": cached_content.content.horoscope
                    }
                ],
                "exploreTopic": "How do today's planetary alignments affect your path?"
            }

        # Get user's birth chart for context
        birth_chart = BirthChart.objects(user=user.id).first()
        if not birth_chart:
            # Return generic content if no birth chart exists
            return {
                "dailyAffirmation": "Trust in the cosmic flow of life.",
                "keyTransits": [
                    {
                        "transit": "Moon's Journey",
                        "description": "The Moon guides our emotional tides."
                    }
                ],
                "dailyChartInsight": "Create your birth chart to receive personalized insights.",
                "exploreTopic": "What celestial insights await in your birth chart?"
            }

        try:
            # Call Azure Function for personalized content
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://cosmicapp-daily-content.azurewebsites.net/api/generateDailyContent",
                    json={
                        "userId": str(user.id),
                        "birthData": birth_chart.birth_data,
                        "chartData": birth_chart.chart_data
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    content_data = response.json()
                    
                    # Save to cache
                    new_content = DailyContent(
                        user=user_id,
                        date=today,
                        content=Content(
                            horoscope=content_data["affirmation"],
                            guidance=content_data["insight"]
                        )
                    ).save()

                    return {
                        "dailyAffirmation": content_data["affirmation"],
                        "keyTransits": content_data.get("transits", []),
                        "dailyChartInsight": content_data["insight"],
                        "exploreTopic": content_data.get("topic", "How do today's planetary alignments affect your path?")
                    }

        except Exception as e:
            print(f"Error generating daily content: {str(e)}")
            
        # Return fallback content if generation fails
        return {
            "dailyAffirmation": "The stars align to guide your journey today.",
            "keyTransits": [
                {
                    "transit": "Celestial Guidance",
                    "description": "Trust in the cosmic wisdom that surrounds you."
                }
            ],
            "dailyChartInsight": "Every moment holds potential for growth and transformation.",
            "exploreTopic": "What cosmic messages are speaking to you today?"
        }
