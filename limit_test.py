from gpiozero import Button
import time

# Setup button with debounce (e.g., 200ms)
LIMIT_SWITCH = Button(18, pull_up=False, bounce_time=0.2)

def main():
    print("Waiting for limit switch press...")
    try:
        while True:
            LIMIT_SWITCH.wait_for_press()
            print("Pressed!")
            LIMIT_SWITCH.wait_for_release()
            print("Released!")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting program.")

if __name__ == "__main__":
    main()
