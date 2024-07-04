import json
import datetime

def validate(slots):
    valid_cities = ['mumbai', 'delhi', 'bangalore', 'hyderabad','chennai','surat','pune','jaipur','lucknow','indore','munnar','visakhapatanam','agra','srinagar','jaisalmer','manali','kashmir','goa']
    
    if not slots['Location']:
        return {
            'isValid': False,
            'violatedSlot': 'Location',
            'message': 'Please provide a location.'
        }        
        
    if slots['Location']['value']['originalValue'].lower() not in valid_cities:
        return {
            'isValid': False,
            'violatedSlot': 'Location',
            'message': f'We currently support only {", ".join(valid_cities)} as valid destinations.'
        }
        
    if not slots['CheckInDate']:
        return {
            'isValid': False,
            'violatedSlot': 'CheckInDate',
            'message': 'Please provide a check-in date.'
        }
        
    if not slots['Nights']:
        return {
            'isValid': False,
            'violatedSlot': 'Nights',
            'message': 'Please provide the number of nights.'
        }
        
    if not slots['RoomType']:
        return {
            'isValid': False,
            'violatedSlot': 'RoomType',
            'message': 'What type of room would you like to book? We have Classic, Duplex, Suite, Queen Rooms, Junior Suite, Deluxe Rooms, Presidential Suites, and Rooms with a View.'
        }

    return {'isValid': True}
    
def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    validation_result = validate(slots)
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit': validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": validation_result.get('message', 'There was an error with your input.')
                    }
                ]
            }
            return response
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
            return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        room_type = slots['RoomType']['value']['originalValue']
        check_in_date = slots['CheckInDate']['value']['originalValue']
        number_of_nights = int(slots['Nights']['value']['originalValue'])
        location = slots['Location']['value']['originalValue']
        
        room_prices = {
            'Classic': 1000,
            'Duplex': 1500,
            'Suite': 3000,
            'Queen Rooms': 1200,
            'Junior Suite': 1800,
            'Deluxe Rooms': 2500,
            'Presidential Suites': 5000,
            'Rooms with a View': 3000
        }
        
        price_per_night = room_prices.get(room_type, 100)
        total_price = price_per_night * number_of_nights 
        
        confirmation_message = (
            f"Your booking for a {room_type} at {location} for {number_of_nights} nights starting on {check_in_date} "
            f"has been confirmed. The total price is Inr {total_price}/-."
        )
        
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name': intent,
                    'slots': slots,
                    'state': 'Fulfilled'
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": confirmation_message
                }
            ]
        }
        return response
