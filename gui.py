import os
from tkinterdnd2 import DND_FILES, TkinterDnD
import core
import customtkinter as ctk
from PIL import Image


class OCDFileRenamer(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

        self.title("OCD File Renamer")
        self.geometry(f"{1280}x{750}")

        self.selected_file = ""
        self.queue = []

        # Define weights for categories
        self.weights = {
            "Lo-fi": 1,
            "Acoustic": 2,
            "Tropical": 3,
        }

        # Initialize output directory
        self.output_directory = ""

        # Drag and drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

        self.create_gui()

    def create_gui(self):
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                       size=(26, 26))
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                             size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                             size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                       dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                       size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                       dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                       size=(20, 20))
        self.add_user_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="OCD File Renamer",
                                                   compound="left",
                                                   font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="Home",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.add_remove_categories = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                   border_spacing=10, text="Categories",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.chat_image, anchor="w",
                                                   command=self.add_remove_categories_event)
        self.add_remove_categories.grid(row=2, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                             text="Settings",
                                             fg_color="transparent", text_color=("gray10", "gray90"),
                                             hover_color=("gray70", "gray30"),
                                             image=self.add_user_image, anchor="w",
                                             command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")

        self.home_window()  # Window 1
        self.category_window()  # Window 2
        self.settings_window()  # Window 3

        # Set default value for scaling
        self.scaling_optionemenu.set("100%")

        # Select default frame
        self.select_frame_by_name("home")

    def home_window(self):
        # Create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Top frame
        self.home_top_frame = ctk.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.home_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Browse Button
        self.browse_button = ctk.CTkButton(self.home_top_frame, text="Browse", image=self.image_icon_image,
                                           command=self.browse_file)
        self.browse_button.grid(row=0, column=0, padx=5, pady=5)

        # Selected File Display
        self.file_display = ctk.CTkLabel(self.home_top_frame, text="")
        self.file_display.grid(row=0, column=1, padx=5, pady=5)

        # Categories button frame
        self.button_frame = ctk.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)

        self.categories = core.load_categories()  # Load categories from a configuration file
        self.categories.sort(key=lambda x: x.lower())

        self.buttons = []
        row = 0
        col = 0
        for category in self.categories:
            button = ctk.CTkButton(self.button_frame, text=category,
                                   command=lambda c=category: self.add_to_queue(c))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)
            col += 1
            if col == 6:
                col = 0
                row += 1

        # Create a frame to group the custom text entry and output directory
        self.custom_text_frame = ctk.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.custom_text_frame.grid(row=2, column=0, padx=10, pady=10)

        # Output Directory Browse Button
        self.output_directory_browse_button = ctk.CTkButton(self.custom_text_frame, text="Output Directory",
                                                            image=self.image_icon_image,
                                                            command=self.browse_output_directory)
        self.output_directory_browse_button.grid(row=0, column=0, padx=5, pady=5)

        # Output Directory Entry
        self.output_directory_entry = ctk.CTkEntry(self.custom_text_frame, width=150)
        self.output_directory_entry.grid(row=0, column=1, padx=5, pady=5)

        # Custom Text Entry Label
        self.custom_text_label = ctk.CTkLabel(self.custom_text_frame, text="Custom text entry: ")
        self.custom_text_label.grid(row=0, column=2, padx=5, pady=5)

        # Custom Text Entry
        self.custom_text_entry = ctk.CTkEntry(self.custom_text_frame, width=150)
        self.custom_text_entry.grid(row=0, column=3, padx=10, pady=10)

        # Rename File Button
        self.rename_button = ctk.CTkButton(self.custom_text_frame, text="Rename File",
                                           command=self.rename_files)
        self.rename_button.grid(row=0, column=4, padx=5, pady=5)

        # Create a frame to group the folder operations frame
        self.folder_operations_frame = ctk.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.folder_operations_frame.grid(row=3, column=0, padx=10, pady=10)

        # Checkbox to enable/disable resetting the Output Directory
        self.reset_output_directory_var = ctk.BooleanVar(value=False)  # Default not to reset
        self.reset_output_directory_checkbox = ctk.CTkCheckBox(self.folder_operations_frame,
                                                               text="Reset Output Directory",
                                                               variable=self.reset_output_directory_var)
        self.reset_output_directory_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable moving the file up one folder
        self.move_up_var = ctk.BooleanVar(value=False)
        self.move_up_checkbox = ctk.CTkCheckBox(self.folder_operations_frame, text="Move Up One Folder",
                                                variable=self.move_up_var)
        self.move_up_checkbox.grid(row=0, column=1, padx=5, pady=5)

        # Checkbox for the text moving feature
        self.move_text_var = ctk.BooleanVar()
        self.move_text_var.set(True)  # Default to enabled
        self.move_text_checkbox = ctk.CTkCheckBox(self.folder_operations_frame, text="Move Text",
                                                  variable=self.move_text_var,
                                                  onvalue=True, offvalue=False)
        self.move_text_checkbox.grid(row=0, column=2, padx=5, pady=5)

        # Placement Label
        self.placement_label = ctk.CTkLabel(self.folder_operations_frame, text="Placement:")
        self.placement_label.grid(row=0, column=3, padx=10, pady=5)

        # Variable to track the user's placement choice (prefix or suffix)
        self.placement_choice = ctk.StringVar()
        self.placement_choice.set("suffix")  # Default to suffix

        # Radio button for prefix
        self.prefix_radio = ctk.CTkRadioButton(self.folder_operations_frame, text="Prefix",
                                               variable=self.placement_choice,
                                               value="prefix")
        self.prefix_radio.grid(row=0, column=4, padx=5, pady=5)

        # Radio button for suffix
        self.suffix_radio = ctk.CTkRadioButton(self.folder_operations_frame, text="Suffix",
                                               variable=self.placement_choice,
                                               value="suffix")
        self.suffix_radio.grid(row=0, column=5, padx=5, pady=5)

        # Create a frame to group the misc. buttons
        self.button_group_frame = ctk.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.button_group_frame.grid(row=5, column=0, padx=10, pady=10)

        # Undo Button
        self.undo_button = ctk.CTkButton(self.button_group_frame, text="Undo", command=self.undo_last)
        self.undo_button.grid(row=0, column=0, padx=10, pady=10)

        # Clear Button
        self.clear_button = ctk.CTkButton(self.button_group_frame, text="Clear", command=self.clear_selection)
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)

        # Move to Trash Button
        self.trash_button = ctk.CTkButton(self.button_group_frame, text="Move to Trash",
                                          command=self.move_to_trash)
        self.trash_button.grid(row=0, column=2, padx=10, pady=10)

        # Select Last Used File Button
        self.last_used_file_button = ctk.CTkButton(self.button_group_frame, text="Select Last Used File",
                                                   command=self.load_last_used_file)
        self.last_used_file_button.grid(row=0, column=3, padx=10, pady=10)

        # Create a frame to display the last used file
        self.last_used_frame = ctk.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.last_used_frame.grid(row=6, column=0, padx=5, pady=5)

        # Last Used File Label
        self.last_used_display_label = ctk.CTkLabel(self.last_used_frame, text="Last used file:")
        self.last_used_display_label.grid(row=0, column=0, padx=5, pady=5)

        # Last Used File Display
        self.last_used_display = ctk.CTkLabel(self.last_used_frame, text="")
        self.last_used_display.grid(row=0, column=1, padx=5, pady=5)

        # Create a frame to display messages
        self.message_label_frame = ctk.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.message_label_frame.grid(row=7, column=0, padx=10, pady=10)

        # Message Label
        self.message_label = ctk.CTkLabel(self.message_label_frame, text="")
        self.message_label.grid(row=0, column=0, padx=10, pady=10)

    def category_window(self):
        # Create add/remove categories frame
        self.category_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.category_frame.grid_columnconfigure(0, weight=1)

        # Top frame
        self.cat_top_frame = ctk.CTkFrame(self.category_frame, corner_radius=0, fg_color="transparent")
        self.cat_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Add/Remove Categories Label
        self.file_label = ctk.CTkLabel(self.cat_top_frame, text="Add/Remove Categories",
                                       font=ctk.CTkFont(size=15, weight="bold"))
        self.file_label.grid(row=0, column=0, padx=5, pady=5)

        # Categories button frame
        self.button_frame = ctk.CTkFrame(self.cat_top_frame, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)

        self.categories = core.load_categories()  # Load categories from a configuration file
        self.categories.sort(key=lambda x: x.lower())

        self.buttons = []
        row = 0
        col = 0
        for category in self.categories:
            button = ctk.CTkButton(self.button_frame, text=category, hover=False)
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)
            col += 1
            if col == 6:
                col = 0
                row += 1

        # Cat frame
        self.cat_frame = ctk.CTkFrame(self.cat_top_frame, corner_radius=0, fg_color="transparent")
        self.cat_frame.grid(row=2, column=0, padx=10, pady=10)

        # Add Category Entry
        self.category_entry = ctk.CTkEntry(self.cat_frame, width=705)
        self.category_entry.grid(row=0, column=0, padx=20, pady=10)

        # Add Category Button
        self.add_category_button = ctk.CTkButton(self.cat_frame, text="Add Category",
                                                 command=self.add_category)
        self.add_category_button.grid(row=0, column=1, padx=20, pady=10)

        # Remove Category Entry
        self.remove_category_entry = ctk.CTkEntry(self.cat_frame, width=705)
        self.remove_category_entry.grid(row=1, column=0, padx=20, pady=10)

        # Remove Category Button
        self.remove_category_button = ctk.CTkButton(self.cat_frame, text="Remove Category",
                                                    command=self.remove_category)
        self.remove_category_button.grid(row=1, column=1, padx=20, pady=10)

        # Create a frame to display messages
        self.message_label_frame = ctk.CTkFrame(self.cat_frame, corner_radius=0, fg_color="transparent")
        self.message_label_frame.grid(row=3, column=0, padx=10, pady=10)

        # Message Label
        self.message_label = ctk.CTkLabel(self.message_label_frame, text="")
        self.message_label.grid(row=0, column=0, padx=10, pady=10)

    def settings_window(self):
        # Create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # Top frame
        self.settings_top_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.settings_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Settings label
        self.settings_label = ctk.CTkLabel(self.settings_top_frame, text="Settings",
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.settings_label.grid(row=0, column=0, padx=5, pady=5)

        # Checkbox to enable/disable open on drop behavior
        self.open_on_drop_var = ctk.BooleanVar(value=False)
        self.open_on_drop_switch = ctk.CTkSwitch(self.settings_top_frame, text="Open File on Drag and Drop",
                                                 variable=self.open_on_drop_var)
        self.open_on_drop_switch.grid(row=1, column=0, padx=10, pady=10)

        # Checkbox to enable/disable for duplicate removal
        self.remove_duplicates_var = ctk.BooleanVar(value=True)
        self.remove_duplicates_switch = ctk.CTkSwitch(self.settings_top_frame,
                                                      text="Remove Duplicates",
                                                      variable=self.remove_duplicates_var)
        self.remove_duplicates_switch.grid(row=1, column=1, padx=10, pady=10)

        # Select light or dark label
        self.appearance_mode_label = ctk.CTkLabel(self.settings_top_frame, text="Appearance:")
        self.appearance_mode_label.grid(row=2, column=0, padx=10, pady=10)

        # Select light or dark mode
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.settings_top_frame,
                                                      values=["Light", "Dark", "System"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=2, column=1, padx=10, pady=10)

        # Select scaling label
        self.scaling_label = ctk.CTkLabel(self.settings_top_frame, text="UI Scaling:")
        self.scaling_label.grid(row=3, column=0, padx=10, pady=10)

        # Select scaling level
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.settings_top_frame,
                                                     values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=3, column=1, padx=10, pady=10)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.add_remove_categories.configure(
            fg_color=("gray75", "gray25") if name == "add_remove_categories" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "add_remove_categories":
            self.category_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.category_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def add_remove_categories_event(self):
        self.select_frame_by_name("add_remove_categories")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def browse_output_directory(self):
        core.browse_output_directory(self)

    def move_to_trash(self):
        core.move_to_trash(self)

    def load_last_used_file(self):
        core.load_last_used_file(self)

    def on_drop(self, event):
        core.on_drop(self, event)

    def add_to_queue(self, category):
        core.add_to_queue(self, category)

    def update_file_display(self):
        core.update_file_display(self)

    def undo_last(self):
        core.undo_last(self)

    def clear_selection(self):
        core.clear_selection(self)

    def add_category(self):
        core.add_category(self)

    def remove_category(self):
        core.remove_category(self)

    def refresh_category_buttons(self):
        core.refresh_category_buttons(self)

    def load_categories(self):
        core.load_categories()

    def save_categories(self):
        core.save_categories(self)

    def rename_files(self):
        core.rename_files(self)

    def handle_rename_success(self, new_path):
        core.handle_rename_success(self, new_path)

    def browse_file(self):
        core.browse_file(self)

    def construct_new_name(self, base_name, weighted_categories, custom_text, extension):
        return core.construct_new_name(self, base_name, weighted_categories, custom_text, extension)

    def move_text(self, name):
        return core.move_text(name)

    def sanitize_file_name(self, name):
        return core.sanitize_file_name(name)

    def show_message(self, message, error=False):
        core.show_message(self, message, error)


if __name__ == "__main__":
    app = OCDFileRenamer()
    app.mainloop()
