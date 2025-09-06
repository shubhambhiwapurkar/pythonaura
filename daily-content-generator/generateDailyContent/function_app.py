import azure.functions as func
import datetime
import logging
from services.user_data_access import get_active_users, create_daily_content, get_user_by_id
from services.ai_generator import generate_personalized_content

app = func.FunctionApp()

# Timer-triggered function for daily batch processing
@app.schedule(schedule="0 5 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def dailyContentGenerator(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info("Daily scheduled generation is running.")
    
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


# HTTP-triggered function for on-demand content generation
@app.route(route="generate-content", auth_level=func.AuthLevel.FUNCTION)
def onDemandContentGenerator(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function processed a request.')

    user_id = req.params.get('user_id')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('user_id')

    if not user_id:
        return func.HttpResponse(
             "Please pass a user_id on the query string or in the request body",
             status_code=400
        )

    logging.info(f"Processing request for user_id: {user_id}")

    try:
        user = get_user_by_id(user_id)
        if not user:
            return func.HttpResponse(f"User with id {user_id} not found.", status_code=404)
        
        if not user.birth_details:
            return func.HttpResponse(f"User {user_id} has no birth details.", status_code=400)

        # Generate and save content
        content = generate_personalized_content(
            user_name=f"{user.first_name} {user.last_name}",
            birth_details=user.birth_details,
            preferences=getattr(user, 'preferences', {})
        )
        create_daily_content(user.id, content)
        
        logging.info(f"Successfully generated content for user {user.id}")
        return func.HttpResponse(f"Successfully generated content for user {user.id}", status_code=200)

    except Exception as e:
        logging.error(f"Error processing request for user {user_id}: {str(e)}")
        return func.HttpResponse("Failed to generate content.", status_code=500)
