import streamlit as st
import requests
import json
import time

# Phone.com API details - Using Streamlit secrets
ACCOUNT_ID = st.secrets["ACCOUNT_ID"]
EXTENSION_ID = st.secrets["EXTENSION_ID"]
API_URL = f"https://api.phone.com/v4/accounts/{ACCOUNT_ID}/extensions/{EXTENSION_ID}/sms"
API_TOKEN = st.secrets["API_TOKEN"]
SENDER_NUMBER = st.secrets["SENDER_NUMBER"]
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

# Streamlit app title
st.title("Bulk SMS Sender (Phone.com)")

# --- Input Fields ---

# Input for recipient phone numbers
st.subheader("Enter Recipient Phone Numbers (one per line)")
recipient_input = st.text_area("Phone Numbers (e.g., +1234567890)", height=200)
recipients = [num.strip() for num in recipient_input.split("\n") if num.strip()]

# Input for message content
message = st.text_area("Enter Your Message", height=150)

# Display current recipient count
st.write(f"Current Recipient Count: {len(recipients)}")

# --- Batching and Rate Limiting ---
batch_size = 25
delay_seconds = 2.1

# Send button
if st.button("Send SMS"):
    if not recipients or not message:  # Simplified check
        st.error("Please enter recipient phone numbers and a message.")
    else:
        # --- Batching Logic ---
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i + batch_size]

            # Prepare payload
            payload = {
                "from": SENDER_NUMBER,  # Use the hardcoded sender
                "to": batch,
                "text": message
            }

            try:
                # Send request to Phone.com API
                response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
                response.raise_for_status()

                if response.status_code in (200, 201):
                    st.success(f"Batch {i // batch_size + 1} sent successfully!")
                    st.write(response.json())
                else:
                    st.error(f"Failed to send batch {i // batch_size + 1}: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred sending batch {i // batch_size + 1}: {str(e)}")

            # --- Rate Limiting ---
            time.sleep(delay_seconds)

        st.success("All batches processed!")

# Display current recipients for review
if recipients:
    st.subheader("Recipients to Send To:")
    for recipient in recipients:
        st.write(recipient)