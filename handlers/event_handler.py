import os
from utils.get_all_files import get_all_files


def setup_events(bot):
    event_folders = get_all_files(
        os.path.join(os.path.dirname(__file__), "..", "events"), folders_only=True
    )

    for event_folder in event_folders:
        event_files = get_all_files(event_folder)
        event_files.sort()

        event_name = os.path.basename(event_folder)

        @bot.event
        async def on_event(arg):
            for event_file in event_files:
                event_function = __import__(
                    event_file.replace("/", ".").replace("\\", ".").replace(".py", ""),
                    fromlist=["execute"],
                )
                await event_function.execute(bot, arg)
