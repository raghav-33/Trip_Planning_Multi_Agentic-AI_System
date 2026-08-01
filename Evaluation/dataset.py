import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "MultiAgent_TravelPlanner_Evaluation"


# -------------------------------------------------------------------
# Paste ALL your 50 examples here
# -------------------------------------------------------------------
examples = [
    {
    "inputs": {
        "query": "Plan a 4-day Goa trip from Amritsar under Rs 20,000."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Goa",
            "origin": "Amritsar",
            "duration": "4 days",
            "budget": "Rs 20000",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a 5-day Kerala trip from Delhi under Rs 35,000."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Kerala",
            "origin": "Delhi",
            "duration": "5 days",
            "budget": "Rs 35000",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a 3-day Jaipur trip under Rs 15,000."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Jaipur",
            "origin": "",
            "duration": "3 days",
            "budget": "Rs 15000",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a 6-day Kashmir vacation from Mumbai under Rs 50,000."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "weather_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Kashmir",
            "origin": "Mumbai",
            "duration": "6 days",
            "budget": "Rs 50000",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a weekend trip to Rishikesh from Chandigarh."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Rishikesh",
            "origin": "Chandigarh",
            "duration": "Weekend",
            "budget": "",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a budget trip to Manali under Rs 18,000."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Manali",
            "origin": "",
            "duration": "",
            "budget": "Rs 18000",
            "travel_style": "Budget",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a family vacation to Shimla for 5 days."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "weather_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Shimla",
            "origin": "",
            "duration": "5 days",
            "budget": "",
            "travel_style": "Family",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a Goa backpacking trip from Pune."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Goa",
            "origin": "Pune",
            "duration": "",
            "budget": "",
            "travel_style": "Backpacking",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a spiritual trip to Varanasi."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Varanasi",
            "origin": "",
            "duration": "",
            "budget": "",
            "travel_style": "Spiritual",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a 7-day Rajasthan tour under Rs 45,000."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Rajasthan",
            "origin": "",
            "duration": "7 days",
            "budget": "Rs 45000",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a luxury honeymoon to Paris for 7 days from Delhi."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Paris",
            "origin": "Delhi",
            "duration": "7 days",
            "budget": "",
            "travel_style": "Luxury",
            "special_preferences": [
                "Honeymoon"
            ]
        }
    }
},
{
    "inputs": {
        "query": "Plan a Europe trip from Mumbai under Rs 2 lakh."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Europe",
            "origin": "Mumbai",
            "duration": "",
            "budget": "Rs 2 lakh",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a Switzerland vacation for 10 days."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Switzerland",
            "origin": "",
            "duration": "10 days",
            "budget": "",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a Singapore trip from Chennai under Rs 60000."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Singapore",
            "origin": "Chennai",
            "duration": "",
            "budget": "Rs 60000",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a New York vacation during Christmas."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "weather_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "New York",
            "origin": "",
            "duration": "Christmas",
            "budget": "",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a Dubai family vacation from Delhi under Rs 1 lakh."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Dubai",
            "origin": "Delhi",
            "duration": "",
            "budget": "Rs 100000",
            "travel_style": "Family",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a Bali honeymoon."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Bali",
            "origin": "",
            "duration": "",
            "budget": "",
            "travel_style": "",
            "special_preferences": [
                "Honeymoon"
            ]
        }
    }
},
{
    "inputs": {
        "query": "Plan a Maldives luxury trip under Rs 4 lakh."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Maldives",
            "origin": "",
            "duration": "",
            "budget": "Rs 4 lakh",
            "travel_style": "Luxury",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a London trip from Bangalore."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "London",
            "origin": "Bangalore",
            "duration": "",
            "budget": "",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a Tokyo vacation in spring."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "weather_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Tokyo",
            "origin": "",
            "duration": "Spring",
            "budget": "",
            "travel_style": "",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a 6-day family trip to Kashmir from Delhi under Rs 80,000."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Kashmir",
            "origin": "Delhi",
            "duration": "6 days",
            "budget": "Rs 80000",
            "travel_style": "Family",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a honeymoon trip to Bali for 7 days from Mumbai."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Bali",
            "origin": "Mumbai",
            "duration": "7 days",
            "budget": "",
            "travel_style": "Luxury",
            "special_preferences": ["Honeymoon"]
        }
    }
},
{
    "inputs": {
        "query": "Business trip to Hyderabad for 2 days."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Hyderabad",
            "origin": "",
            "duration": "2 days",
            "budget": "",
            "travel_style": "Business",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan my anniversary vacation to Maldives."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Maldives",
            "origin": "",
            "duration": "",
            "budget": "",
            "travel_style": "Luxury",
            "special_preferences": ["Anniversary"]
        }
    }
},
{
    "inputs": {
        "query": "Suggest hotels for my business conference in Pune."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Pune",
            "origin": "",
            "duration": "",
            "budget": "",
            "travel_style": "Business",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a family trip to Jaipur next month."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "weather_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Jaipur",
            "origin": "",
            "duration": "next month",
            "budget": "",
            "travel_style": "Family",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Luxury honeymoon in Switzerland under Rs 5 lakh."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Switzerland",
            "origin": "",
            "duration": "",
            "budget": "Rs 5 lakh",
            "travel_style": "Luxury",
            "special_preferences": ["Honeymoon"]
        }
    }
},
{
    "inputs": {
        "query": "Business trip from Bangalore to Chennai tomorrow."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Chennai",
            "origin": "Bangalore",
            "duration": "tomorrow",
            "budget": "",
            "travel_style": "Business",
            "special_preferences": []
        }
    }
},
{
    "inputs": {
        "query": "Plan a Goa bachelor trip for 5 friends."
    },
    "outputs": {
        "selected_agents": [
            "hotel_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Goa",
            "origin": "",
            "duration": "",
            "budget": "",
            "travel_style": "Group",
            "special_preferences": ["Bachelor Trip"]
        }
    }
},
{
    "inputs": {
        "query": "Family vacation to Singapore for 5 days under Rs 2 lakh."
    },
    "outputs": {
        "selected_agents": [
            "flight_agent",
            "hotel_agent",
            "budget_agent",
            "itinerary_agent"
        ],
        "trip_constraints": {
            "destination": "Singapore",
            "origin": "",
            "duration": "5 days",
            "budget": "Rs 2 lakh",
            "travel_style": "Family",
            "special_preferences": []
        }
    }
}

]


def create_dataset():

    # ----------------------------------------------------
    # Check if dataset already exists
    # ----------------------------------------------------

    if client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset '{DATASET_NAME}' already exists.")

        dataset = client.read_dataset(
            dataset_name=DATASET_NAME
        )

    else:

        dataset = client.create_dataset(
            dataset_name=DATASET_NAME,
            description="Benchmark dataset for Multi-Agent Travel Planner Evaluation"
        )

        print(f"Created dataset: {DATASET_NAME}")

    # ----------------------------------------------------
    # Avoid duplicate uploads
    # ----------------------------------------------------

    existing_examples = list(
        client.list_examples(dataset_id=dataset.id)
    )

    if len(existing_examples) > 0:
        print(
            f"Dataset already contains {len(existing_examples)} examples."
        )
        print("Skipping upload.")
        return

    # ----------------------------------------------------
    # Upload examples
    # ----------------------------------------------------

    print("\nUploading examples...\n")

    for i, example in enumerate(examples, start=1):

        client.create_example(
            dataset_id=dataset.id,
            inputs=example["inputs"],
            outputs=example["outputs"],
        )

        print(f"Uploaded Example {i}")

    print("\n===================================")
    print("Dataset uploaded successfully!")
    print(f"Total examples: {len(examples)}")
    print("===================================")


if __name__ == "__main__":
    create_dataset()