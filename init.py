import configparser
from nicegui import ui
from pathlib import Path
from saveGen import generateSave


BASE_DIR = Path(__file__).resolve().parents[0]

def userInitCheck():
    save_dir = BASE_DIR / "Saves"
    config_dir = BASE_DIR / "config.ini"

    def hasNoSave(folderPath):
        folder = Path(folderPath)

        if not folder.is_dir():
            return False
        
        contents = list(folder.iterdir())

        return len(contents) == 1
    
    is_empty = hasNoSave(save_dir)
    is_config = config_dir.exists()

    if is_empty and not is_config:
        with ui.dialog() as dialog:
            with ui.card().classes('w-[1400px] !max-w-full flex justify-center items-center'):
                ui.label("There are no save files present. Enter your name to create a new profile:").style('font-size: 30px')
                name_input = ui.input(label='Name')

                def create_profile():
                    name = name_input.value.strip()

                    config = configparser.ConfigParser()
                    config['SAVES'] = {
                        'Profile': name
                    }

                    if not name:
                        return

                    with open(BASE_DIR / 'config.ini', 'w') as configfile:
                        config.write(configfile)

                    generateSave(name)
                    ui.notify('Profile Created!')
                    ui.navigate.reload()
                    dialog.close()

                ui.button("Create Profile!", on_click=create_profile)

        dialog.open()
