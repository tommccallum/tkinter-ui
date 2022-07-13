#!/usr/bin/env python3
import tkinter as tk
import os
import sys

# General gui outline
#   A root window
#     - A scrollbar
#     - A canvas
#       A subwindow
#       - A frame
#         - N buttons
def on_root_configure(e):
  print("root {}".format(e))
  #canvas.configure(width=e.width, height=e.height)
  #canvas.itemconfig(win, width=e.width, height=e.height)

root = tk.Tk()
root.title("A simple gui")
root.geometry("800x600")
# The following 2 rows make sure the container frame takes up the whole of the 
# window on resize.
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
#root.bind("<Configure>", on_root_configure)

# This container resizes automatically to the root size
container = tk.Frame(root)
container.grid(row=0,column=0, sticky="news")
container.config(bg="blue")
# these are required to resize the canvas to other container size
# the weight=1 makes sure that the canvas gets any excess width
container.columnconfigure(0, weight=1)
container.rowconfigure(0, weight=1)
#container.grid_propagate(False) # ???

canvas = tk.Canvas(container)
canvas.config(bg="red")
canvas.grid(row=0, column=0, sticky="news")
canvas.rowconfigure(0, weight=1)
canvas.columnconfigure(0, weight=1)

# Create the scrollbar, next to the canvas.  The scrollregion size comes from the 
# size of the scrollable_frame
v = tk.Scrollbar(container, orient="vertical")
v.grid(row=0, column=1, sticky="nes")

def on_scrollable_frame_configure(e):
  print("on_scrollable_frame_configure {}".format(e))
  # Q. Do have the scrollregion object properly set?
  print("scrollregion: {} {}".format(canvas.bbox("all"), scrollable_frame.bbox("all")))
  #canvas.configure(scrollregion=canvas.bbox("all"))
  canvas.configure(scrollregion=scrollable_frame.bbox("all"))

  # this basically does the same as using scrollable_frame.bbox("all")
  # but the scrollbar shows red which means the inner frame is scrolling
  size = [scrollable_frame.winfo_reqwidth(), scrollable_frame.winfo_reqheight()]
  #canvas.config(scrollregion="0 0 {} {}".format(size[0], size[1]))
  #if scrollable_frame.winfo_reqheight() != canvas.winfo_height():
  #  canvas.config(height=scrollable_frame.winfo_reqheight())


def on_container_configure(e):
  # when the window resizes this should be called to resize the
  # inner window based on the new canvas size
  print("on_container_configure {} {}".format(e.width, e.height))

  # This should only be adjusted for width. If we
  # do adjust for height we ruin the scrolling.
  canvas.itemconfig(win, width=e.width)

  # This resizes the canvas to the size of the root window.
  # We do NOT want to resize the inner window as that will
  # mean the viewport will not scroll and we will end up with
  # just the canvas background.
  canvas.config(width=e.width, height=e.height)

# this is the "viewport" into a part of the frame that the 
# scrollbar is allowing to be shown.
# A frame has no yview.
scrollable_frame = tk.Frame(canvas, bg="yellow")
# this is called when the frame is resized and will get it to recalculate the grid size
scrollable_frame.bind("<Configure>", on_scrollable_frame_configure)
# this allows our buttons to stretch across the canvas
scrollable_frame.columnconfigure(0, weight=1)

# this creates a window inside the canvas which we can use as a viewport
# it is set to appear in the top-left
win = canvas.create_window(0,0, window=scrollable_frame, anchor=tk.NW)
# this line tells the canvas to change when the scrollbar value is set
v.configure(command=canvas.yview)
canvas.configure(yscrollcommand=v.set)
# this is called when the container is resized so that the window inside the canvas resizes
container.bind("<Configure>", on_container_configure)


# Allow the user to add multiple buttons each one a row
rowCount = 1
buttons = []
def do_add_row():
  global buttons
  global rowCount
  bt = tk.Button(scrollable_frame, text="Press me {} of {}".format(rowCount, rowCount), command=do_add_row)
  bt.grid(row=rowCount-1, column=0, sticky="ew")
  buttons.append(bt)

  ii = 1
  for bt in buttons:
    bt.configure(text="Press me {} of {}".format(ii, rowCount))
    ii = ii + 1

  rowCount = rowCount + 1
  # this may be required as fix for our problem
  #scrollable_frame.update_idletasks()

bt = tk.Button(scrollable_frame, text="Press me {}".format(rowCount), command=do_add_row)
bt.grid(row=rowCount-1, column=0, sticky="ew")
rowCount = rowCount + 1
buttons.append(bt)

#canvas.configure(scrollregion=canvas.bbox("all"))

# run the main window loop
root.mainloop()
