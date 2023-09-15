import subprocess

def stream_iptv(iptv_url):
    try:
        # Command to run MPV with the provided IPTV URL
        command = ["mpv", iptv_url]

        # Start the MPV player
        subprocess.Popen(command)

        # Wait for the user to press Enter to stop the player
        input("Press Enter to stop the IPTV stream...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace 'YOUR_IPTV_URL_HERE' with the actual IPTV URL you want to stream
    iptv_url = "https://iptv-org.github.io/iptv/countries/in.m3u"
    
    stream_iptv(iptv_url)

