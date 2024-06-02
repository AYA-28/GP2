import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.exceptions import NotFittedError

# Set page configuration
st.set_page_config(page_title="Malicious Node Predictor",
                   layout="wide",
                   page_icon="🛡️")

# Getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# Loading the saved models
models = {
    'svm_model': pickle.load(open(os.path.join(working_dir, 'svm_model.pkl'), 'rb')),
    'RF_model': pickle.load(open(os.path.join(working_dir, 'rf_model.pkl'), 'rb')),
    'ANN_model': pickle.load(open(os.path.join(working_dir, 'ann_model.pkl'), 'rb')),
    'LINEAR_model': pickle.load(open(os.path.join(working_dir, 'linear_model.pkl'), 'rb'))
}

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        'Malicious Nodes Prediction System',
        ['svm_model', 'RF_model', 'ANN_model', 'LINEAR_model'],
        menu_icon='shield',
        icons=['lock', 'lock', 'lock', 'lock'],
        default_index=0
    )

# Define the input fields
def get_user_input():
    cols = st.columns(3)
    inputs = [
        'Node_ID', 'IP_Address', 'Packet_Rate', 'Packet_Drop_Rate',
        'Packet_Duplication_Rate', 'Signal_Strength', 'SNR', 'Battery_Level',
        'Number_of_Neighbors', 'Route_Request_Frequency', 'Route_Reply_Frequency',
        'Data_Reception_Frequency', 'CPU_Usage', 'Memory_Usage', 'Bandwidth'
    ]
    user_input = []
    for i, label in enumerate(inputs):
        with cols[i % 3]:
            value = st.text_input(label)
            user_input.append(value)
    return user_input

# Prediction function
def predict(model, user_input):
    try:
        # Handle empty strings and convert to float
        user_input = [float(x.strip()) if x.strip() else 0.0 for x in user_input]
        # Check if model is fitted
        if not hasattr(model, "predict"):
            raise NotFittedError(f"This {selected} instance is not fitted yet.")
        prediction = model.predict([user_input])
        if prediction[0] == 1:
            return 'The node is malicious'
        else:
            return 'The node is not malicious'
    except ValueError as e:
        st.error(f"Error converting input to float: {e}")
    except NotFittedError as e:
        st.error(f"Model not fitted error: {e}")
    return ''

# Malicious Node Prediction Page
if selected in models:
    st.title(f'{selected} Prediction using ML')
    user_input = get_user_input()
    if st.button('Test Result'):
        diagnosis = predict(models[selected], user_input)
        st.success(diagnosis)


