import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Function to load data

def load_data(filepath, encoding='ascii'):
    df = pd.read_csv(filepath, encoding=encoding)
    return df

# Function to assign headers

def assign_headers(df, headers):
    df.columns = headers
    return df

# Function to clean and preprocess data

def preprocess_data(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Hour'] = df['Timestamp'].dt.hour
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()
    return df

# Function to filter fraud data

def filter_fraud(df):
    return df[df['IsFraud'] == 1]

# Function to create dashboard

def create_fraud_dashboard(fraud_df, output_html='fraud_dashboard.html'):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Fraud by Hour of Day', 'Fraud by Day of Week', 'Top Sender Accounts', 'Top Receiver Accounts')
    )

    # Fraud by Hour
    hour_counts = fraud_df['Hour'].value_counts().sort_index()
    fig.add_trace(go.Bar(x=hour_counts.index, y=hour_counts.values, name='Fraud by Hour'), row=1, col=1)

    # Fraud by Day
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = fraud_df['DayOfWeek'].value_counts().reindex(day_order)
    fig.add_trace(go.Bar(x=day_order, y=day_counts.values, name='Fraud by Day'), row=1, col=2)

    # Top Senders
    top_senders = fraud_df['SenderName'].value_counts().head(10)
    fig.add_trace(go.Bar(x=top_senders.index, y=top_senders.values, name='Top Senders'), row=2, col=1)

    # Top Receivers
    top_receivers = fraud_df['ReceiverName'].value_counts().head(10)
    fig.add_trace(go.Bar(x=top_receivers.index, y=top_receivers.values, name='Top Receivers'), row=2, col=2)

    fig.update_layout(height=700, width=1000, title_text='Fraud Analysis Dashboard')
    fig.write_html(output_html)
    return output_html

# Example usage
# Load data

def main():
    df = load_data('sindh_microfinance_transactions.csv')
    headers = ['TransactionID', 'Timestamp', 'SenderName', 'SenderAccount', 'ReceiverName', 'ReceiverAccount', 'Amount', 'PaymentMethod', 'TransactionType', 'IsFraud']
    df = assign_headers(df, headers)
    df = preprocess_data(df)
    fraud_df = filter_fraud(df)
    create_fraud_dashboard(fraud_df)

# Run main

main()