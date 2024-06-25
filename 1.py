import tkinter as tk
from tkinter import ttk

def item_selected(event):
    print("Selected.")

def item_opened(event):
    print("Opened.")

def item_closed(event):
    print("Closed.")

root = tk.Tk()
root.title("Treeview in Tk")
treeview = ttk.Treeview()
# Create a new tag with certain event hanlders.
treeview.tag_bind("mytag", "<<TreeviewSelect>>", item_selected)
treeview.tag_bind("mytag", "<<TreeviewOpen>>", item_opened)
treeview.tag_bind("mytag", "<<TreeviewClose>>", item_closed)
# Create two items with the previous tag.
item = treeview.insert("", tk.END, text="Item 1", tags=("mytag",))
treeview.insert(item, tk.END, text="Subitem 1", tags=("mytag",))
treeview.pack()
root.mainloop()