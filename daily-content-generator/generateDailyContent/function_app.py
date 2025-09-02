import azure.functions as func
import datetime
import logging
from services.user_data_access import get_active_users, create_daily_content
from services.ai_generator import generate_personalized_content

app = func.FunctionApp()

@app.schedule(schedule="0 0 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def generateDailyContent(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        microsecond=0).isoformat()

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function started at %s', utc_timestamp)
    
    try:
        # Get all active users
        users = get_active_users()
        
        for user in users:
            try:
                # Generate personalized content
                content = generate_personalized_content(
                    user_name=f"{user.first_name} {user.last_name}",
                    birth_details=user.birth_details,
                    preferences=user.preferences
                )
                
                # Save content to database
                create_daily_content(user.id, content)
                
                logging.info(f"Generated daily content for user {user.id}")
                
            except Exception as e:
                logging.error(f"Error generating content for user {user.id}: {str(e)}")
                continue
                
        logging.info(f"Daily content generation completed at {utc_timestamp}")
        
    except Exception as e:
        logging.error(f"Error in daily content generation: {str(e)}")
        raise
