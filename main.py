import json
import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.modalview import ModalView
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.screenmanager import NoTransition
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.image import Image

class CreditsModal(ModalView):
    terms_text = StringProperty("")  # Define the terms_text property

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)  # Modal size
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.load_terms()  # Load terms from JSON

        # Scrollable content
        scroll_view = ScrollView(size_hint=(None, None), size=('210dp', '250dp'), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        content = Label(
            text=self.terms_text,  # Set text from JSON
            size_hint=(None, None),
            width=scroll_view.width,
            font_size='16sp',
            halign='left',
            valign='top',
            color=(0.72, 0.53, 0.04, 1),
            text_size=(scroll_view.width, None)  # Enable text wrapping
        )
        
        content.bind(size=content.setter('text_size'))  # Adjust text wrapping
        content.bind(texture_size=self.adjust_height)  # Dynamically adjust height
        scroll_view.add_widget(content)
        self.add_widget(scroll_view)

    def load_terms(self):
        """Load terms from a config.json file."""
        try:
            with open("config/menu.json", "r") as f:
                data = json.load(f)
                self.terms_text = data.get("credits", "No terms available.")
        except Exception as e:
            self.terms_text = "Failed to load terms. Please try again later."
            print(f"Error loading terms: {e}")

    def adjust_height(self, instance, value):
        """Adjust the height of the label based on its content."""
        instance.height = instance.texture_size[1]

class TermsModal(ModalView):
    terms_text = StringProperty("")  # Define the terms_text property

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)  # Modal size
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.load_terms()  # Load terms from JSON

        # Scrollable content
        scroll_view = ScrollView(size_hint=(None, None), size=('210dp', '250dp'), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        content = Label(
            text=self.terms_text,  # Set text from JSON
            size_hint=(None, None),
            width=scroll_view.width,
            font_size='16sp',
            halign='left',
            valign='top',
            color=(0.72, 0.53, 0.04, 1),
            text_size=(scroll_view.width, None)  # Enable text wrapping
        )
        
        content.bind(size=content.setter('text_size'))  # Adjust text wrapping
        content.bind(texture_size=self.adjust_height)  # Dynamically adjust height
        scroll_view.add_widget(content)
        self.add_widget(scroll_view)

    def load_terms(self):
        """Load terms from a config.json file."""
        try:
            with open("config/menu.json", "r") as f:
                data = json.load(f)
                self.terms_text = data.get("terms_and_privacy", "No terms available.")
        except Exception as e:
            self.terms_text = "Failed to load terms. Please try again later."
            print(f"Error loading terms: {e}")

    def adjust_height(self, instance, value):
        """Adjust the height of the label based on its content."""
        instance.height = instance.texture_size[1]
        
class SplashScreen(Screen):
    progress = NumericProperty(0)
    
    def on_enter(self):
        self.progress = 0
        self.event = Clock.schedule_interval(self.update_progress, 0.1)
        
    def update_progress(self, dt):
        self.progress += 0.033
        if self.progress >= 1:
            self.event.cancel()
            self.switch_to_main()
            
    def switch_to_main(self, *args):
        self.manager.current = 'dashboard'

class VolumeControl(ModalView):
    pass

class MenuModal(ModalView):
    pass
    
class QuitConfirmationModal(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)  # Modal size
        self.background_color = (0, 0, 0, 0)  # Transparent background
    
# ------------------------------------------------------------------------------------------

class LetterOfTruth(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shake_flags = {}  # Dictionary to track animation states for each button
        self.is_animation_running = False  # Global flag to allow only one animation at a time
        self.random_letter = RandomLetter()  # Instance of RandomLetter modal
        self.random_letter.bind(on_dismiss=self.check_parrot_modal)  # Bind dismissal of random modal

    def open_random_letter(self):
        """Opens the random letter modal."""
        self.random_letter.open()

    def show_parrot_message(self, *args):
        """Displays the parrot message modal."""
        parrot_modal = ParrotMessage()
        parrot_modal.open()

    def shake_chest(self, button):
        """Handles the chest animation and modal logic."""
        # Prevent re-opening a chest
        if button.background_normal == 'data/images/open_chest.png':
            return

        # Prevent starting a new animation while another is running
        if self.is_animation_running:
            return

        # Initialize the button-specific flag if it doesn't exist
        if button not in self.shake_flags:
            self.shake_flags[button] = False

        # Prevent animating a button already in progress
        if self.shake_flags[button]:
            return

        # Set the global and button-specific flags
        self.is_animation_running = True
        self.shake_flags[button] = True

        # Update the button to the "opened" chest image
        button.background_normal = 'data/images/open_chest.png'
        button.background_down = 'data/images/open_chest_down.png'

        # Define the shake animation
        distance = 10
        initial_duration = 0.3
        shake_animation = (
            Animation(pos=(button.x - distance, button.y), duration=initial_duration) +
            Animation(pos=(button.x + distance, button.y), duration=initial_duration) +
            Animation(pos=(button.x, button.y), duration=initial_duration)
        )

        # Increment the opened chests counter
        app = App.get_running_app()
        app.opened_chests_count += 1

        # Reset flags and handle modal display when the animation completes
        def on_animation_complete(*args):
            self.is_animation_running = False  # Reset the global flag
            self.shake_flags[button] = False  # Reset the flag for this button

            # If it's the last chest, show the parrot message with a delay
            if app.opened_chests_count == 8:
                Clock.schedule_once(self.show_parrot_message, 0.5)  # Add a 0.5-second delay
            else:
                # Open the random letter modal
                self.open_random_letter()

        # Bind the animation completion to the reset function
        shake_animation.bind(on_complete=on_animation_complete)

        # Start the animation
        shake_animation.start(button)

    def check_parrot_modal(self, *args):
        """Check if the parrot modal needs to be displayed after random letter modal."""
        app = App.get_running_app()
        if app.opened_chests_count == 8:
            self.show_parrot_message()
        
class RandomLetter(ModalView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent background
        
    def play_random_sounds(*args):
        sound_files = [
            "data/audiofx/boost1.mp3",
            "data/audiofx/boost2.mp3",
            "data/audiofx/boost3.mp3",
            "data/audiofx/boost4.mp3",
            "data/audiofx/boost5.mp3"
        ]
        # Select 5 random sounds
        selected_sound = random.choice(sound_files)
        
        sound = SoundLoader.load(selected_sound)
        
        if sound:
            sound.play()
        
class ParrotMessage(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent background        
        
# ------------------------------------------------------------------------------------------
        
class AdventureAcademy(Screen):
    animals_data = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_level = 0  # Default level (index 0)
        self.selected_button = None
        self.first_click = None
        self.load_level_data(self.current_level)
        self.background_color = (0, 0, 0, 0)  # Transparent background

    def load_level_data(self, level):
        """Load level data from the JSON file."""
        try:
            with open("config/adventure.json", "r") as f:
                data = json.load(f)

            # Retrieve animals_data and current_level_data
            self.animals_data = data.get("animals", [])

            # Load the data for the specified level
            if 0 <= level < len(self.animals_data):
                level_data = self.animals_data[level]
                self.correct_answer = level_data["correct_answer"]

                # Set the image source and play its sound
                self.ids.centered_image.source = f"data/images/{level_data['image']}"
                self.ids.centered_image.reload()

                # Reset and create options
                self.reset_selection()
                self.create_option_buttons(level_data["option"], level_data["option_sound"])
            else:
                print("Invalid level number")

        except Exception as e:
            print(f"Error loading level data: {e}")

    def create_option_buttons(self, options, sounds):
        """Create or update option buttons dynamically based on the data."""
        self.reset_selection()

        for i, (answer, sound) in enumerate(zip(options, sounds)):
            btn = self.ids.get(f"option_button_{i}")
            if not btn:
                continue

            # Set the background images for normal and down states
            btn.background_normal = f"data/images/{answer}"
            btn.background_down = f"data/images/{answer}"

            # Set the sound file for the button
            btn.sound_file = f"data/audiofx/{sound}"

            # Remove any widgets added to the button previously
            btn.clear_widgets()

            # Ensure the button has the correct size
            btn.size_hint = (None, None)
            btn.size = (400, 200)  # Adjust button size as needed

    def on_touch_down(self, touch):
        """Override on_touch_down to detect touches on the centered image."""
        centered_image = self.ids.centered_image

        # Convert the touch coordinates to the widget's local coordinate space
        if centered_image.collide_point(*centered_image.to_widget(*touch.pos)):
            # Play the sound associated with the image
            self.play_centered_image_sound()
            return True  # Consume the touch event

        # Allow other widgets to process the touch
        return super().on_touch_down(touch)

    def play_centered_image_sound(self):
        """Play the sound associated with the centered image."""
        try:
            # Get the sound file path for the centered image
            level_data = self.animals_data[self.current_level]
            sound_file = f"data/audiofx/{level_data['image_sound']}"
            self.play_sound(sound_file)
        except KeyError:
            print("Error: 'image_sound' key is missing in level data.")
        except Exception as e:
            print(f"Error playing centered image sound: {e}")

    def on_option_button_click(self, instance):
        """Handle option button click."""
        if self.selected_button:
            self.selected_button.background_color = (1, 1, 1, 1)
        self.selected_button = instance
        instance.background_color = (1, 0, 0, 1)

        if self.first_click == instance:
            self.handle_answer()
        else:
            self.first_click = instance
            self.play_sound(instance.sound_file)

    def handle_answer(self):
        """Handle double-click on option buttons."""
        # Get the image source of the selected button (e.g., 'r.png')
        selected_button_image = self.selected_button.background_normal.split("/")[-1]  # Extract the image name (e.g., 'r.png')

        # Compare the selected button's image name to the correct answer
        if selected_button_image == self.correct_answer:
            # Play one of five random sounds
            random_sounds = [
                "data/audiofx/correct1.mp3",
                "data/audiofx/correct2.mp3",
                "data/audiofx/correct3.mp3",
                "data/audiofx/correct4.mp3",
                "data/audiofx/correct5.mp3",
            ]
            self.play_sound(random.choice(random_sounds))

            # Increment the level and check if there are more levels
            self.current_level += 1
            if self.current_level < len(self.animals_data):
                self.load_level_data(self.current_level)  # Load the next level
            else:
                # If no more levels, show the ParrotMessage modal
                self.show_parrot_message()
        else:
            self.animate_incorrect_answer(self.selected_button)
            self.play_sound("data/audiofx/wrong_answer.mp3")
            self.reset_selection()

    def show_parrot_message(self):
        """Display the ParrotMessage modal."""
        parrot_modal = ParrotMessage()
        parrot_modal.open()

    def animate_incorrect_answer(self, button):
        """Create a shake animation for incorrect answers."""
        # Store the button's original x position
        original_x = button.x

        # Define the shake animation
        shake = (
            Animation(x=original_x - 10, duration=0.05) +  # Move left
            Animation(x=original_x + 10, duration=0.05) +  # Move right
            Animation(x=original_x, duration=0.05)         # Return to original position
        )
        shake.start(button)

    def play_sound(self, sound_file):
        """Play the specified sound."""
        sound = SoundLoader.load(sound_file)
        if sound:
            sound.play()

    def reset_selection(self):
        """Reset the selection and button states."""
        self.selected_button = None
        self.first_click = None
        for i in range(4):  # Assuming 4 options
            btn = self.ids.get(f"option_button_{i}")
            if btn:
                btn.background_color = (1, 1, 1, 1)
# ------------------------------------------------------------------------------------------

class PlayGround(Screen):
    pass
    
# ------------------------------------------------------------------------------------------
    
class DashboardScreen(Screen):
    screen_order = ['letter_of_truth', 'adventure_academy', 'playground']
    current_index = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_modal = MenuModal()
        self.terms_modal = TermsModal()
        self.credits_modal = CreditsModal()
        self.volume_control = VolumeControl()
        self.show_screen_by_index(self.current_index)  # Show the default screen

    def show_screen_by_index(self, index):
        content_area = self.ids.content_area
        content_area.clear_widgets()

        screen_name = self.screen_order[index]
        self.change_background(screen_name)

        if screen_name == 'letter_of_truth':
            content_area.add_widget(LetterOfTruth())
        elif screen_name == 'adventure_academy':
            content_area.add_widget(AdventureAcademy())
        elif screen_name == 'playground':
            content_area.add_widget(PlayGround())

    def navigate_screen(self, direction):
        """Navigate to the next or previous screen."""
        if direction == 'next':
            self.current_index = (self.current_index + 1) % len(self.screen_order)
        elif direction == 'previous':
            self.current_index = (self.current_index - 1) % len(self.screen_order)
        
        self.show_screen_by_index(self.current_index)

    def switch_screen(self, screen_name):
        """Switch to a specific screen."""
        if screen_name == 'menu':
            self.menu_modal.open()

    def open_terms_modal(self):
        self.terms_modal.open()

    def open_credits_modal(self):
        self.credits_modal.open()

    def open_volume_control(self):
        self.volume_control.open()
        
    def open_chest_demo_modal(self):
        self.chest_demo_modal.open()

    def change_background(self, screen_name):
        if screen_name == 'letter_of_truth':
            image_path = 'data/images/dashboard.png'
        elif screen_name == 'adventure_academy':
            image_path = 'data/images/dashboard1.png'
        elif screen_name == 'playground':
            image_path = 'data/images/dashboard2.png'
        else:
            image_path = 'data/images/dashboard.png'

        # Check if 'dashboard_background' is in the ids
        if 'dashboard_background' in self.ids:
            background_widget = self.ids.dashboard_background

            # Check if there is a Rectangle already in the canvas
            if background_widget.canvas.before.children:
                # Update the existing Rectangle's source
                background_widget.canvas.before.children[-1].source = image_path
            else:
                # If no Rectangle exists, create a new one
                with background_widget.canvas.before:
                    Color(1, 1, 1, 1)  # Reset to white
                    Rectangle(
                        size=background_widget.size,
                        pos=background_widget.pos,
                        source=image_path
                    )
        else:
            print("dashboard_background ID not found in self.ids")
            
# ------------------------------------------------------------------------------------------

class MainApp(App):
    bgm_volume = NumericProperty(50)  # Background music volume
    sfx_volume = NumericProperty(50)  # Sound effect volume    
    quit_confirmation_open = False  # Flag to track if quit confirmation is open
    back_button_timer = None  # Timer for back button double-click prevention
    displayed_label = StringProperty("")  # Bindable property for the label text
    random_letters = ListProperty()  # List of all random letters
    current_data = ListProperty()  # Current data list
    
    displayed_label_audio = StringProperty("")
    opened_chests_count = NumericProperty(0)

    def build(self):
        # Load and play background music
        self.background_music = SoundLoader.load('data/audio/bg_fun_sound.mp3')
        self.sound_fx = SoundLoader.load('data/audiofx/select.mp3')
        self.sound_fx1 = SoundLoader.load('data/audiofx/close.mp3')
        self.sound_fx2 = SoundLoader.load('data/audiofx/chest_click.mp3')
        self.sound_fx3 = SoundLoader.load('data/audiofx/adventure_click.mp3')
        self.sound_fx4 = SoundLoader.load('data/audiofx/playground_click.mp3')
        self.load_chest_data()
        self.opened_chests_count = 0
        
        self.play_chest_sound_label = SoundLoader.load('data/audiofx/'+self.displayed_label_audio)
        
        # Bind the back button event
        Window.bind(on_keyboard=self.on_back_button)

        # Set initial sound effects volume
        self.set_sound_effects_volume(0.5)

        # Play background music if loaded
        if self.background_music:
            self.background_music.loop = True  # Make the music loop
            self.background_music.volume = 0.5  # Set volume to 50%
            self.background_music.play()

        # Screen manager setup
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

    def set_sound_effects_volume(self, volume):
        """Set the volume for all sound effects."""
        if self.sound_fx:
            self.sound_fx.volume = volume
        if self.sound_fx1:
            self.sound_fx1.volume = volume
        if self.sound_fx2:
            self.sound_fx2.volume = volume
        if self.sound_fx3:
            self.sound_fx3.volume = volume
        if self.sound_fx4:
            self.sound_fx4.volume = volume
        if self.play_chest_sound_label:
            self.play_chest_sound_label = volume

    def reset_quit_flag(self, dt):
        """Reset the quit confirmation flag if the user doesn't double-click within the timeout."""
        self.quit_confirmation_open = False

    def on_stop(self):
        # Stop the music when the app closes
        if self.background_music:
            self.background_music.stop()

    def adjust_volume_bgm(self, value):
        self.bgm_volume = value  # Update the background music volume
        if self.background_music:
            self.background_music.volume = value / 100  # Update the volume in the music player

    def adjust_volume_sfx(self, value):
        self.sfx_volume = value  # Update the sound effect volume
        self.set_sound_effects_volume(value / 100)

    def play_click_sound(self):
        if self.sound_fx:
            self.sound_fx.play()
            
    def play_close_sound(self):
        if self.sound_fx1:
            self.sound_fx1.play()
            
    def play_chest_sound(self):
        if self.sound_fx2:
            self.sound_fx2.play()
            
    def play_adventure_click(self):
        if self.sound_fx3:
            self.sound_fx3.play()
            
    def play_playground_click(self):
        if self.sound_fx4:
            self.sound_fx4.play()                       

    def on_back_button(self, window, key, *args):
        if key == 27:  # Android back button key code
            if not self.quit_confirmation_open:
                self.show_quit_confirmation()
                self.quit_confirmation_open = True  # Set the flag to True when the modal is open

                # Start a timer to reset the flag if no second press happens within 2 seconds
                if self.back_button_timer:
                    self.back_button_timer.cancel()
                self.back_button_timer = Clock.schedule_once(self.reset_quit_flag, 2)  # 2 seconds timeout

            return True  # Prevent the default back button behavior
        return False

    def show_quit_confirmation(self):
        """Show the quit confirmation modal."""
        quit_modal = QuitConfirmationModal()
        quit_modal.bind(on_dismiss=self.on_quit_modal_dismiss)  # Reset flag when modal is dismissed
        quit_modal.open()

    def on_quit_modal_dismiss(self, instance):
        """Reset the flag when the quit modal is dismissed."""
        self.quit_confirmation_open = False

    def quit_app(self):
        """Quit the app."""
        App.get_running_app().stop()
    
    def load_chest_data(self):
        """Load chest data from the JSON file."""
        try:
            with open("config/config.json", "r") as f:
                data = json.load(f)

            # Retrieve random_letters and current_data
            self.random_letters = data.get("random_letters", [])
            self.current_data = data.get("current_data", [])

            # If current_data is empty, refill it with random_letters
            if not self.current_data:
                self.current_data = self.random_letters[:]
                self.save_current_data_to_json()

        except Exception as e:
            print(f"Error loading chest data: {e}")

    def save_current_data_to_json(self):
        """Save the current data to the JSON file."""
        try:
            with open("config/config.json", "w") as f:
                data = {
                    "random_letters": self.random_letters,
                    "current_data": self.current_data
                }
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving chest data: {e}")

    def show_random_letter(self):
        """Display a random letter and remove it from current_data."""
        if self.current_data:
            # Select a random item
            selected_item = random.choice(self.current_data)
            self.displayed_label = selected_item["label"]  # Update the label with the selected letter
            self.displayed_label_audio = selected_item["audiofx"]

            # Remove the selected item from current_data
            self.current_data.remove(selected_item)

            # Save the updated current_data back to the JSON file
            self.save_current_data_to_json()
        else:
            self.load_chest_data()  # Reload data from the JSON file
            selected_item = random.choice(self.current_data)
            self.displayed_label = selected_item["label"]  
            self.displayed_label_audio = selected_item["audiofx"]
            
    def chest_label_sound(self):
        sound_path = 'data/audiofx/' + self.    displayed_label_audio
        self.play_chest_sound_label = SoundLoader.load(sound_path)
        if self.play_chest_sound_label:
            self.play_chest_sound_label.play()

# Run the app
if __name__ == '__main__':
    MainApp().run()