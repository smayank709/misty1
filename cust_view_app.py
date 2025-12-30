import gradio as gr
import requests
import pandas as pd
from supabase import create_client

# --- 1. CONFIGURATION & ASSETS ---
SUPABASE_URL = "https://vgcxwpupdtyqzggiaydp.supabase.co"
SUPABASE_KEY = "sb_publishable_GZ0qyBF5Fw5cZDz-aK7JAQ_8ZRDv9i9"
LOGO_URL = "https://github.com/smayank709/misty1/blob/main/Gemini_Generated_Image_u53r2pu53r2pu53r.png?raw=true"
CSS_URL = "https://raw.githubusercontent.com/smayank709/misty1/refs/heads/main/style.css"

# Initialize Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch Custom CSS from GitHub
try:
    css_content = requests.get(CSS_URL).text
except:
    css_content = "" # Fallback if GitHub is unreachable

# --- 2. BACKEND FUNCTIONS ---

def get_customer_and_orders(phone_number):
    """Fetches customer name and order history."""
    if not phone_number or len(phone_number) < 10:
        return "Please enter a valid 10-digit mobile number.", pd.DataFrame()

    # Fetch Customer Name
    customer_res = supabase.table("customers").select("full_name").eq("phone", phone_number).execute()
    
    if not customer_res.data:
        return "Welcome! Please register at our store to view your history.", pd.DataFrame()
    
    name = customer_res.data[0]['full_name']
    greeting = f"## Namaste, {name} ji! \nGreat to see you again."

    # Fetch Orders
    orders_res = supabase.table("orders").select(
        "order_id, order_date, qty_kg, order_value_inr, status, products(sweet_name)"
    ).eq("cust_phone", phone_number).execute()
    
    if orders_res.data:
        df = pd.DataFrame(orders_res.data)
        # Flattening the products join
        df['Item'] = df['products'].apply(lambda x: x['sweet_name'] if x else "Artisanal Sweet")
        df = df[['order_id', 'order_date', 'Item', 'qty_kg', 'order_value_inr', 'status']]
        df.columns = ["Order ID", "Date", "Item", "Weight (kg)", "Total (₹)", "Status"]
    else:
        df = pd.DataFrame(columns=["Order ID", "Date", "Item", "Weight (kg)", "Total (₹)", "Status"])

    return greeting, df

def get_trending_products():
    """Retrieves top 4 best sellers."""
    orders_res = supabase.table("orders").select("qty_kg, products(sweet_name, variant_type, price_per_kg)").execute()
    
    if not orders_res.data:
        return pd.DataFrame(columns=["Sweet Name", "Collection", "Price (₹/kg)"])

    raw_df = pd.DataFrame(orders_res.data)
    raw_df['Sweet Name'] = raw_df['products'].apply(lambda x: x['sweet_name'])
    raw_df['Collection'] = raw_df['products'].apply(lambda x: x['variant_type'])
    raw_df['Price'] = raw_df['products'].apply(lambda x: x['price_per_kg'])
    
    trending = raw_df.groupby(['Sweet Name', 'Collection', 'Price'])['qty_kg'].sum().reset_index()
    trending = trending.sort_values(by='qty_kg', ascending=False).head(4)
    return trending[['Sweet Name', 'Collection', 'Price']]

# --- 3. UI LAYOUT (GRADIO) ---

with gr.Blocks(css=css_content, title="MishTee-Magic | Artisanal Sweets") as demo:
    
    # Header Section
    with gr.Column(elem_id="header_container"):
        gr.Image(LOGO_URL, show_label=False, container=False, width=280, interactive=False)
        gr.Markdown("<center><h3>Purity and Health in Every Bite</h3></center>")
    
    gr.HTML("<div style='margin-top: 30px;'></div>")

    # Welcome & Login Logic
    with gr.Row():
        with gr.Column(scale=1):
            pass 
        with gr.Column(scale=2):
            phone_input = gr.Textbox(
                label="Registered Mobile", 
                placeholder="91XXXXXXXX",
                max_lines=1
            )
            login_btn = gr.Button("ENTER THE MAGIC")
            greeting_output = gr.Markdown() # Placeholder for 'Namaste [Name] ji!'
        with gr.Column(scale=1):
            pass

    gr.HTML("<hr style='border: 0.5px solid #C06C5C; opacity: 0.2; margin: 40px 0;'>")

    # Data Display Tabs
    with gr.Tabs():
        with gr.TabItem("MY ORDER HISTORY"):
            order_table = gr.Dataframe(interactive=False)
            
        with gr.TabItem("TRENDING TODAY"):
            trending_table = gr.Dataframe(interactive=False)

    # Footer
    gr.Markdown("<center><small>MishTee-Magic Artisanal Sweets • A2 Purity • Organics</small></center>")

    # --- 4. EVENT TRIGGERS ---
    def on_login(phone):
        greeting, orders = get_customer_and_orders(phone)
        trending = get_trending_products()
        return greeting, orders, trending

    login_btn.click(
        fn=on_login,
        inputs=[phone_input],
        outputs=[greeting_output, order_table, trending_table]
    )

if __name__ == "__main__":
    demo.launch()
