"""
Personal Finance Tracker with AI Features
A CLI-based application for tracking expenses with intelligent insights

Author: Finance Tracker
Purpose: Learning tool for personal finance management
Features: Transaction management, visualization, AI advisor
"""

import csv
import os
from datetime import datetime
import warnings

# Data analysis and visualization libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Replit

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION AND GLOBAL VARIABLES
# ============================================================================

# CSV file name for storing transactions
CSV_FILE = "transactions.csv"

# Column headers for the CSV file
CSV_HEADERS = ["Date", "Category", "Amount", "Description"]


# ============================================================================
# CSV FILE MANAGEMENT FUNCTIONS
# ============================================================================

def initialize_csv():
    """
    Creates the CSV file with headers if it doesn't exist.
    This ensures the application can run without any setup.
    """
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
        print(f"✓ Created new transactions file: {CSV_FILE}")
    else:
        print(f"✓ Found existing transactions file: {CSV_FILE}")


def add_transaction():
    """
    Adds a new transaction to the CSV file.
    Prompts user for: Date, Category, Amount, and Description.
    Validates input to ensure data quality.
    """
    print("\n" + "="*50)
    print("ADD NEW TRANSACTION")
    print("="*50)
    
    # Get transaction date (default to today)
    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date_input == "":
        transaction_date = datetime.now().strftime("%Y-%m-%d")
    else:
        # Basic date validation
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            transaction_date = date_input
        except ValueError:
            print("❌ Invalid date format. Using today's date.")
            transaction_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get category
    print("\nSuggested categories: Food, Transport, Shopping, Entertainment, Bills, Healthcare, Other")
    category = input("Enter category: ").strip()
    if category == "":
        category = "Other"
    
    # Get amount with validation
    while True:
        amount_input = input("Enter amount ($): ").strip()
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("❌ Amount must be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("❌ Invalid amount. Please enter a number.")
    
    # Get description
    description = input("Enter description: ").strip()
    if description == "":
        description = "No description"
    
    # Write to CSV file
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([transaction_date, category, amount, description])
    
    print(f"\n✓ Transaction added successfully!")
    print(f"  Date: {transaction_date}")
    print(f"  Category: {category}")
    print(f"  Amount: ${amount:.2f}")
    print(f"  Description: {description}")


def view_transactions():
    """
    Displays all transactions from the CSV file in a formatted table.
    Shows transaction number, date, category, amount, and description.
    """
    print("\n" + "="*50)
    print("ALL TRANSACTIONS")
    print("="*50)
    
    # Read transactions from CSV
    transactions = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        transactions = list(reader)
    
    # Check if there are any transactions
    if len(transactions) == 0:
        print("\n📭 No transactions found. Add your first transaction!")
        return
    
    # Display transactions in a formatted table
    print(f"\n{'No.':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<30}")
    print("-" * 80)
    
    for idx, transaction in enumerate(transactions, 1):
        date = transaction['Date']
        category = transaction['Category']
        amount = float(transaction['Amount'])
        description = transaction['Description']
        
        # Truncate description if too long
        if len(description) > 27:
            description = description[:27] + "..."
        
        print(f"{idx:<5} {date:<12} {category:<15} ${amount:<9.2f} {description:<30}")
    
    print("-" * 80)
    print(f"Total transactions: {len(transactions)}")


# ============================================================================
# SPENDING SUMMARY FUNCTIONS
# ============================================================================

def spending_summary():
    """
    Displays a comprehensive spending summary including:
    - Total spending
    - Category-wise breakdown with percentages
    - Average transaction amount
    - Highest spending category
    """
    print("\n" + "="*50)
    print("SPENDING SUMMARY")
    print("="*50)
    
    # Load transactions using pandas for easier analysis
    try:
        df = pd.read_csv(CSV_FILE)
    except pd.errors.EmptyDataError:
        print("\n📭 No transactions found. Add some transactions first!")
        return
    
    # Check if dataframe is empty
    if df.empty or len(df) == 0:
        print("\n📭 No transactions found. Add some transactions first!")
        return
    
    # Calculate total spending
    total_spending = df['Amount'].sum()
    
    # Calculate category-wise spending
    category_summary = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    
    # Calculate average transaction
    avg_transaction = df['Amount'].mean()
    
    # Find highest spending category
    top_category = category_summary.index[0] if len(category_summary) > 0 else "N/A"
    
    # Display summary
    print(f"\n💰 Total Spending: ${total_spending:.2f}")
    print(f"📊 Average Transaction: ${avg_transaction:.2f}")
    print(f"🔝 Top Category: {top_category}")
    print(f"📝 Total Transactions: {len(df)}")
    
    print("\n" + "-"*50)
    print("CATEGORY-WISE BREAKDOWN")
    print("-"*50)
    print(f"{'Category':<20} {'Amount':<15} {'Percentage':<10}")
    print("-"*50)
    
    for category, amount in category_summary.items():
        percentage = (amount / total_spending) * 100
        print(f"{category:<20} ${amount:<14.2f} {percentage:>5.1f}%")
    
    print("-"*50)


# ============================================================================
# VISUALIZATION FUNCTIONS (MATPLOTLIB)
# ============================================================================

def visualize_spending():
    """
    Creates visual charts of spending patterns:
    1. Pie Chart: Shows category-wise spending distribution
    2. Bar Chart: Shows spending by category
    Saves charts as PNG files for viewing.
    """
    print("\n" + "="*50)
    print("SPENDING VISUALIZATION")
    print("="*50)
    
    # Load transactions
    try:
        df = pd.read_csv(CSV_FILE)
    except pd.errors.EmptyDataError:
        print("\n📭 No transactions found. Add some transactions first!")
        return
    
    if df.empty or len(df) == 0:
        print("\n📭 No transactions found. Add some transactions first!")
        return
    
    # Calculate category-wise spending
    category_spending = df.groupby('Category')['Amount'].sum()
    
    # Create figure with two subplots (pie chart and bar chart)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. PIE CHART
    # Shows percentage distribution of spending across categories
    colors = plt.cm.Set3(range(len(category_spending)))
    ax1.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%',
            colors=colors, startangle=90)
    ax1.set_title('Spending Distribution by Category', fontsize=14, fontweight='bold')
    
    # 2. BAR CHART
    # Shows actual amounts spent in each category
    bars = ax2.bar(category_spending.index, category_spending.values, color=colors)
    ax2.set_xlabel('Category', fontsize=12)
    ax2.set_ylabel('Amount ($)', fontsize=12)
    ax2.set_title('Spending by Category', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.2f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    # Save the chart
    chart_filename = 'spending_chart.png'
    plt.savefig(chart_filename, dpi=100, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Visualization created successfully!")
    print(f"📊 Chart saved as: {chart_filename}")
    print(f"💡 Tip: Download the file to view the charts")


# ============================================================================
# AI ADVISOR FUNCTION
# ============================================================================

def ai_advisor():
    """
    AI-powered financial advisor that analyzes spending patterns
    and provides personalized money-saving tips based on:
    - Dominant spending category
    - Spending frequency
    - Average transaction amounts
    
    This uses rule-based logic to provide intelligent recommendations.
    """
    print("\n" + "="*50)
    print("AI FINANCIAL ADVISOR")
    print("="*50)
    
    # Load transactions
    try:
        df = pd.read_csv(CSV_FILE)
    except pd.errors.EmptyDataError:
        print("\n📭 No transactions found. Add some transactions first!")
        return
    
    if df.empty or len(df) == 0:
        print("\n📭 No transactions found. Add some transactions first!")
        return
    
    # Analyze spending patterns
    category_spending = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    top_category = category_spending.index[0]
    top_amount = category_spending.values[0]
    total_spending = df['Amount'].sum()
    top_percentage = (top_amount / total_spending) * 100
    
    print(f"\n🤖 AI Analysis Complete!")
    print(f"\n📊 Your dominant spending category: {top_category}")
    print(f"💰 Amount spent: ${top_amount:.2f} ({top_percentage:.1f}% of total)")
    
    # AI-powered recommendations based on category
    print("\n💡 PERSONALIZED MONEY-SAVING TIPS:")
    print("-" * 50)
    
    tips = {
        'Food': [
            "🍳 Cook at home more often - can save up to 60% compared to eating out",
            "📝 Plan your meals weekly to reduce impulse purchases",
            "🛒 Buy groceries in bulk for non-perishable items",
            "💧 Drink water instead of beverages when dining out"
        ],
        'Transport': [
            "🚌 Consider public transport or carpooling to reduce costs",
            "🚴 Use bike or walk for short distances - good for health too!",
            "⛽ Maintain your vehicle regularly to improve fuel efficiency",
            "📱 Use ride-sharing apps to compare prices before booking"
        ],
        'Shopping': [
            "🛍️ Wait 24 hours before making non-essential purchases",
            "💳 Use cashback and rewards programs",
            "🏷️ Compare prices online before buying",
            "📅 Shop during sales and use discount codes"
        ],
        'Entertainment': [
            "📺 Consider sharing streaming subscriptions with family",
            "🎮 Look for free or low-cost entertainment alternatives",
            "🎟️ Use student/senior discounts if applicable",
            "🏠 Host game nights at home instead of going out"
        ],
        'Bills': [
            "💡 Switch to energy-efficient appliances to lower electricity bills",
            "📞 Review and negotiate your subscription services annually",
            "🌡️ Adjust thermostat settings to save on heating/cooling",
            "📊 Track usage patterns to identify saving opportunities"
        ],
        'Healthcare': [
            "💊 Ask for generic medications when possible",
            "🏥 Use preventive care to avoid costly treatments",
            "💰 Check if your insurance covers wellness programs",
            "🔍 Compare prices at different pharmacies"
        ]
    }
    
    # Get tips for the dominant category
    category_tips = tips.get(top_category, [
        "📊 Track your expenses regularly to identify patterns",
        "💰 Set a monthly budget for this category",
        "🎯 Try to reduce spending by 10-15% next month",
        "📱 Use apps to find better deals and discounts"
    ])
    
    for i, tip in enumerate(category_tips, 1):
        print(f"{i}. {tip}")
    
    print("\n🎯 General Advice:")
    print("   • Follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings")
    print("   • Build an emergency fund (3-6 months of expenses)")
    print("   • Review your spending weekly to stay on track")


# ============================================================================
# MAIN MENU AND APPLICATION FLOW
# ============================================================================

def display_menu():
    """
    Displays the main menu options for the user.
    """
    print("\n" + "="*50)
    print("PERSONAL FINANCE TRACKER WITH AI")
    print("="*50)
    print("1. Add New Transaction")
    print("2. View All Transactions")
    print("3. Spending Summary")
    print("4. Visualize Spending (Charts)")
    print("5. AI Financial Advisor")
    print("6. Exit")
    print("="*50)


def main():
    """
    Main function that runs the application.
    Handles menu selection and program flow.
    """
    print("\n" + "="*60)
    print("🎯 WELCOME TO PERSONAL FINANCE TRACKER WITH AI!")
    print("="*60)
    print("Track expenses • Get AI insights • Manage your money")
    print("="*60 + "\n")
    
    # Initialize CSV file
    initialize_csv()
    
    # Main application loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            spending_summary()
        elif choice == "4":
            visualize_spending()
        elif choice == "5":
            ai_advisor()
        elif choice == "6":
            print("\n" + "="*50)
            print("👋 Thank you for using Finance Tracker!")
            print("Stay financially smart! 💰")
            print("="*50 + "\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-6.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
