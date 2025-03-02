# backend/queue/order_queue.py

from queue import Queue

# Creating an order queue
order_queue = Queue()

# Function to add an order to the queue
def add_order(order):
    order_queue.put(order)
    print(f"Order added: {order}")

# Function to process an order
def process_order():
    if not order_queue.empty():
        order = order_queue.get()
        print(f"Processing order: {order}")
        return order
    else:
        print("No orders to process.")
        return None
