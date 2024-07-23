import streamlit as st
from streamlit_chat import message
import requests

# Set up Streamlit page configuration
st.set_page_config(
    page_title="SQL Query Chatbot",
    page_icon=":robot:"
)

API_URL = "http://127.0.0.1:5000/query"  # Update with your Flask server URL

st.header("SQL Query Chatbot")

# Initialize session state
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query_load(query):
    try:
        response = requests.post(API_URL, json=query)
        response.raise_for_status()
        print("Response status code:", response.status_code)  # Debug print
        print("Response content:", response.content)  # Debug print
        response_json = response.json()
        # Access the nested "output" key
        return response_json.get("response", {}).get("output", "No response")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        print("RequestException:", e)  # Debug print
        return "Error: Request failed"
    except ValueError:
        st.error("Received a non-JSON response from the server.")
        print("Non-JSON response:", response.text)  # Debug print
        return "Error: Non-JSON response from server"

def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text 

# Get user input
user_input = get_text()

if user_input:
    # Load the query response
    output = query_load({"question": user_input})
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# Display chat messages
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

# Allow submission using the Enter key
st.write("""
    <script type="text/javascript">
        const input = document.querySelector('input[type="text"]');
        input.addEventListener('keydown', function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                document.querySelector('button[type="submit"]').click();
            }
        });
    </script>
""", unsafe_allow_html=True)
