import os, requests
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_dungeon_spec(prompt_paragraph: str):
    system_user_content = f"""
        Parse the following short dungeon prompt into strict JSON that exactly matches the schema provided in response_format. Use the mapping rules described below for number_of_rooms and difficulty. Output ONLY the JSON that conforms to the schema.

        PROMPT: "{prompt_paragraph}"
        
        Mapping rules:

        - Rooms: 'lots', 'many', 'complex', 'labyrinth' => prefer 6-7; 'several', 'medium' => 4-5; 'few', 'small', 'tiny' => 2-3.
          If 'dangerous','deadly','lethal' appear, add +1 to +3 rooms (clamp to 9). If 'super easy' appears, subtract 1-2 (clamp min 2).
        - Theme: temple words (altar, shrine, priest, sanctum) => 'temple'. castle words (keep, battlement, throne, fortress) => 'castle'. Default 'castle' if ambiguous.
        - Difficulty: map tone to 1..5:
          'super dangerous'/'deadly' -> 5
          'dangerous'/'spooky' -> 4
          'medium' -> 3
          'easy' -> 2
          'very easy' -> 1

        Return JSON only (no commentary).
        """

    payload = {
        "model": "gpt-5-nano",
        "messages": [
            {"role": "user", "content": system_user_content}
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "dungeon_spec",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "number_of_rooms": {"type": "integer", "minimum": 3, "maximum": 15},
                        "theme": {"type": "string", "enum": ["castle", "temple"]},
                        "difficulty": {"type": "integer", "minimum": 1, "maximum": 5}
                    },
                    "required": ["number_of_rooms", "theme", "difficulty"],
                    "additionalProperties": False
                }
            }
        }
    }
    full_response = requests.post(url, headers=headers, json=payload).json()
    
    # return full_response.json()
    
    content = full_response['choices'][0]['message']['content']
    
    # parse JSON string into dict
    dungeon_spec = json.loads(content)
    
    # just the three values as a tuple
    return (
        dungeon_spec['number_of_rooms'],
        dungeon_spec['theme'],
        dungeon_spec['difficulty']
    )