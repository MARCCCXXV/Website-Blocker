#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, simpledialog
import platform
import os
import ctypes
import sys
import subprocess
import threading
import time


class FocusBlockerApp:  
    def __init__(self, root):
        self.root = root
        self.root.title("Lock in Button")
        self.root.geometry("300x200")
        self.root.configure(bg="#FFCC55")
        self.root.resizable(True, True)
        self.root.overrideredirect(False)  # remove border
        
        # Timer state
        self.blocking = False
        self.time_remaining = 0
        self.timer_thread = None
        self.selected_time = 30  # Default 30 minutes
        
        # Get hosts path
        self.hosts_path = self.get_hosts_path()
        
        # Websites to block
        self.websites = [
            "instagram.com",
            "youtube.com",
            "tiktok.com"
        ]
        
        self.create_widgets()
        self.create_context_menu()

    def start_move(self, event):
        """Record starting position when click begins."""
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        """Move window as mouse drags."""
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")        
    
    def create_widgets(self):
        # Main frame for centering
        main_frame = tk.Frame(self.root, bg="#FFCC55")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Timer display (only shows when blocking)
        self.timer_display = tk.Label(
            main_frame,
            text="",
            font=("Courier New", 32, "bold"),
            bg="#FFCC55",
            fg="#E74C3C"
        )
        self.timer_display.pack(pady=(0, 20))
        
        # Canvas for hand-drawn button
        self.canvas = tk.Canvas(
            main_frame,
            width=250,
            height=120,
            bg="#FFCC55",
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.draw_button()
        
        # Bind right-click to context menu
        self.root.bind("<Button-3>", self.show_context_menu)
        self.canvas.bind("<Button-3>", self.show_context_menu)
        
    def create_context_menu(self):
        """Create right-click context menu."""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        
        # Time submenu
        time_menu = tk.Menu(self.context_menu, tearoff=0)
        time_menu.add_command(label="15 minutes", command=lambda: self.set_time(15))
        time_menu.add_command(label="30 minutes", command=lambda: self.set_time(30))
        time_menu.add_command(label="1 hour", command=lambda: self.set_time(60))
        time_menu.add_command(label="2 hours", command=lambda: self.set_time(120))
        
        self.context_menu.add_cascade(label="Set Timer", menu=time_menu)
        self.context_menu.add_command(label="View Blocked Sites", command=self.show_blocked_sites)
        self.context_menu.add_command(label=" Add Website", command=self.add_website)
        self.context_menu.add_command(label="Remove Website", command=self.remove_website)
        self.context_menu.add_separator()
        
        self.context_menu.add_command(label="About", command=self.show_about)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Exit", command=self.root.quit)
        
    def show_context_menu(self, event):
        """Display context menu on right-click."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def set_time(self, minutes):
        """Set the focus timer duration."""
        if not self.blocking:
            self.selected_time = minutes
    
    def show_blocked_sites(self):
        """Show list of websites that will be blocked."""
        sites_list = "\n".join(f"• {site}" for site in self.websites)
        messagebox.showinfo(
            "Blocked Websites",
            f"These websites will be blocked:\n\n{sites_list}"
        )
    
    def add_website(self):
        """Add a website to the block list."""
        if self.blocking:
            messagebox.showwarning("Blocking Active", "Cannot modify list while blocking is active")
            return
        
        website = simpledialog.askstring(
            "Add Website",
            "Enter website to block (e.g., example.com):"
        )
        if website:
            website = website.strip().lower()
            if website not in self.websites:
                self.websites.append(website)
                messagebox.showinfo("Added", f"{website} added to block list")
            else:
                messagebox.showinfo("Already Listed", f"{website} is already in the block list")
    
    def remove_website(self):
        """Remove a website from the block list."""
        if self.blocking:
            messagebox.showwarning("Blocking Active", "Cannot modify list while blocking is active")
            return
        
        if not self.websites:
            messagebox.showinfo("Empty List", "No websites in the block list")
            return
        
        # Create a selection window
        select_window = tk.Toplevel(self.root)
        select_window.title("Remove Website")
        select_window.geometry("300x400")
        select_window.configure(bg="#FFCC55")
        
        tk.Label(
            select_window,
            text="Select website to remove:",
            font=("Arial", 11, "bold"),
            bg="#FFCC55"
        ).pack(pady=10)
        
        listbox = tk.Listbox(select_window, font=("Arial", 10), height=15)
        listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        for site in self.websites:
            listbox.insert(tk.END, site)
        
        def remove_selected():
            selection = listbox.curselection()
            if selection:
                site = listbox.get(selection[0])
                self.websites.remove(site)
                messagebox.showinfo("Removed", f"{site} removed from block list")
                select_window.destroy()
        
        tk.Button(
            select_window,
            text="Remove Selected",
            command=remove_selected,
            font=("Arial", 10),
            bg="#E74C3C",
            fg="white",
            padx=20,
            pady=5
        ).pack(pady=10)

    
    def show_about(self):
        """Show about information."""
        about_text = f"""Focus Blocker

A simple tool to help you stay focused by temporarily blocking distracting websites.

Current Timer: {self.selected_time} minutes
Websites in List: {len(self.websites)}

Right-click anywhere for options."""
        
        messagebox.showinfo("About Focus Blocker", about_text)
        
    def draw_button(self):

        self.canvas.delete("all")
        
        if not self.blocking:
            # Draw "LOCK IN" button
            points = [
                30, 20,
                32, 18,
                220, 22,
                218, 25,
                220, 95,
                218, 98,
                32, 94,
                30, 92,
                30, 20
            ]
            self.button_shape = self.canvas.create_polygon(
                points,
                fill="#3498DB",
                outline="#2C3E50",
                width=3,
                smooth=True
            )
            
            self.button_text = self.canvas.create_text(
                125, 58,
                text="LOCK IN",
                font=("Comic Sans MS", 18, "bold"),
                fill="white"
            )
            
            # Bind click events
            self.canvas.tag_bind(self.button_shape, "<Button-1>", self.on_button_click)
            self.canvas.tag_bind(self.button_text, "<Button-1>", self.on_button_click)
            self.canvas.tag_bind(self.button_shape, "<Enter>", self.on_button_hover)
            self.canvas.tag_bind(self.button_text, "<Enter>", self.on_button_hover)
            self.canvas.tag_bind(self.button_shape, "<Leave>", self.on_button_leave)
            self.canvas.tag_bind(self.button_text, "<Leave>", self.on_button_leave)
            
        else:
            # Draw "STOP EARLY" button
            points = [
                30, 20,
                32, 18,
                220, 22,
                218, 25,
                220, 95,
                218, 98,
                32, 94,
                30, 92,
                30, 20
            ]
            self.button_shape = self.canvas.create_polygon(
                points,
                fill="#E74C3C",
                outline="#2C3E50",
                width=3,
                smooth=True
            )
            
            self.button_text = self.canvas.create_text(
                125, 58,
                text="STOP EARLY",
                font=("Comic Sans MS", 18, "bold"),
                fill="white"
            )
            
            self.canvas.tag_bind(self.button_shape, "<Button-1>", self.on_button_click)
            self.canvas.tag_bind(self.button_text, "<Button-1>", self.on_button_click)
            self.canvas.tag_bind(self.button_shape, "<Enter>", self.on_button_hover)
            self.canvas.tag_bind(self.button_text, "<Enter>", self.on_button_hover)
            self.canvas.tag_bind(self.button_shape, "<Leave>", self.on_button_leave)
            self.canvas.tag_bind(self.button_text, "<Leave>", self.on_button_leave)
            
    
    def on_button_hover(self, event):
        if not self.blocking:
            self.canvas.itemconfig(self.button_shape, fill="#2980B9")
        else:
            self.canvas.itemconfig(self.button_shape, fill="#C0392B")
    
    def on_button_leave(self, event):
        if not self.blocking:
            self.canvas.itemconfig(self.button_shape, fill="#3498DB")
        else:
            self.canvas.itemconfig(self.button_shape, fill="#E74C3C")
    
    def on_button_click(self, event):
        if not self.blocking:
            self.start_blocking()
        else:
            self.stop_blocking()
    
    def start_blocking(self):
        """Start the blocking timer."""
        if not self.check_admin():
            messagebox.showerror(
                "Permission Error",
                "Please run this program as administrator to block websites."
            )
            return
        
        self.blocking = True
        self.time_remaining = self.selected_time * 60  # Convert to seconds
        
        # Block websites
        for website in self.websites:
            self.block_website(website)
        
        self.draw_button()
        
        # Start timer thread
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
    
    def stop_blocking(self):
        """Stop blocking and unblock websites."""
        self.blocking = False
        
        # Unblock websites
        for website in self.websites:
            self.unblock_website(website)
        
        self.timer_display.config(text="")
        self.draw_button()
    
    def run_timer(self):
        """Run the countdown timer."""
        while self.blocking and self.time_remaining > 0:
            hours = self.time_remaining // 3600
            minutes = (self.time_remaining % 3600) // 60
            seconds = self.time_remaining % 60
            
            if hours > 0:
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                time_str = f"{minutes:02d}:{seconds:02d}"
            
            self.timer_display.config(text=time_str)
            
            time.sleep(1)
            self.time_remaining -= 1
        
        if self.blocking:  # Timer completed naturally
            self.stop_blocking()
            messagebox.showinfo("Time's Up!", "Great job staying focused! Websites are now unblocked.")
    
    def block_website(self, website):
        """Add website to hosts file."""
        try:
            domains = self.get_domain_variants(website)
            with open(self.hosts_path, "a") as file:
                for domain in domains:
                    file.write(f"127.0.0.1 {domain}\n")
                file.flush()
            self.flush_dns()
        except Exception as e:
            print(f"Error blocking {website}: {e}")
    
    def unblock_website(self, website):
        """Remove website from hosts file."""
        try:
            domains = self.get_domain_variants(website)
            
            with open(self.hosts_path, "r") as file:
                lines = file.readlines()
            
            with open(self.hosts_path, "w") as file:
                for line in lines:
                    stripped = line.strip()
                    should_keep = True
                    for domain in domains:
                        if stripped == f"127.0.0.1 {domain}":
                            should_keep = False
                            break
                    if should_keep:
                        file.write(line)
                file.flush()
            
            self.flush_dns()
        except Exception as e:
            print(f"Error unblocking {website}: {e}")
    
    def get_domain_variants(self, website):
        """Get www and non-www versions."""
        if website.startswith("www."):
            return [website[4:], website]
        else:
            return [website, f"www.{website}"]
    
    def flush_dns(self):
        """Flush DNS cache."""
        try:
            if platform.system() == "Windows":
                subprocess.run(["ipconfig", "/flushdns"], 
                             capture_output=True, check=False)
        except Exception:
            pass
    
    def get_hosts_path(self):
        """Get hosts file path."""
        if platform.system() == "Windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        else:
            return "/etc/hosts"
    
    def check_admin(self):
        """Check if running with admin privileges."""
        try:
            if platform.system() == "Windows":
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False


if __name__ == "__main__":
    # Check admin BEFORE creating any windows
    if platform.system() == "Windows":
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                # Use pythonw.exe to avoid console window
                python_exe = sys.executable
                if python_exe.endswith('python.exe'):
                    python_exe = python_exe.replace('python.exe', 'pythonw.exe')
                
                # Relaunch with admin privileges
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", python_exe,
                    f'"{sys.argv[0]}"',
                    None, 1
                )
                sys.exit()
        except Exception as e:
            pass
    
    root = tk.Tk()
    app = FocusBlockerApp(root)
    root.mainloop()