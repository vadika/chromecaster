import pychromecast


def discover_chromecasts():
    """Discover and return all available Chromecast devices."""
    chromecasts, browser = pychromecast.get_chromecasts()
    pychromecast.discovery.stop_discovery(browser)
    return chromecasts


def list_chromecasts(chromecasts):
    """Print all discovered Chromecast devices and return them."""
    print("Available Chromecast devices:")
    for idx, cc in enumerate(chromecasts):
        print(f"{idx + 1}: {cc.device.friendly_name} (IP: {cc.host})")
    return chromecasts


def control_media(chromecast, action):
    """Control media playback on a specified Chromecast device."""
    cast = chromecast
    cast.wait()
    media_controller = cast.media_controller

    if action == 'play':
        media_url = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
        media_controller.play_media(media_url, 'video/mp4')
        media_controller.block_until_active()
        print("Media is playing...")
    elif action == 'pause':
        media_controller.pause()
        print("Media is paused.")
    elif action == 'stop':
        media_controller.stop()
        print("Media playback stopped.")


def main_menu():
    chromecasts = discover_chromecasts()
    if not chromecasts:
        print("No Chromecast devices found.")
        return

    chromecasts = list_chromecasts(chromecasts)
    choice = input("Choose a Chromecast device by number (or 'exit' to quit): ")

    if choice.lower() == 'exit':
        return

    try:
        device_choice = int(choice) - 1
        if device_choice < 0 or device_choice >= len(chromecasts):
            raise ValueError("Invalid selection.")
        selected_device = chromecasts[device_choice]
        print(f"Selected: {selected_device.device.friendly_name}")
    except ValueError as e:
        print(e)
        return

    while True:
        print("\nAvailable actions:")
        print("1: Play Media")
        print("2: Pause Media")
        print("3: Stop Media")
        print("4: Exit")

        action_choice = input("Select an action: ")

        if action_choice == '1':
            control_media(selected_device, 'play')
        elif action_choice == '2':
            control_media(selected_device, 'pause')
        elif action_choice == '3':
            control_media(selected_device, 'stop')
        elif action_choice == '4':
            break
        else:
            print("Invalid choice. Please select a valid action.")


if __name__ == "__main__":
    main_menu()
