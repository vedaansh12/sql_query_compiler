import cohere

co = cohere.Client("qdf4d0Dx2iIh597I8tttrmsswjLMxZ6aEKWSV3r8")  # Replace with your API key

def get_query_suggestion(user_query):
    prompt = f"Fix or suggest a correct SQL query based on: {user_query}"

    try:
        response = co.generate(
            model='command-r-plus',  # Or use 'command-nightly' if available
            prompt=prompt,
            max_tokens=100,
            temperature=0.5
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"AI error: {str(e)}"