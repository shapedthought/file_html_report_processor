import pandas as pd
import hashlib
import PySimpleGUI as sg
from cryptography.fernet import Fernet
import json

# sg.theme('DefaultNoMoreNagging')
sg.theme('Default1')


class Gui:
    """Create the GUI"""

    def __init__(self):
        self.menu_def = [['Help', 'About...']]

        self.layout = [
            [sg.Menu(self.menu_def)],
            [sg.Radio('Import HTML', group_id="selectors", default=True, key='import_select', enable_events=True),
             sg.Radio('Import File', group_id="selectors", key='export_select', enable_events=True)],
            [sg.Text('Import HTML', size=(16, 1)), sg.InputText(key='import_html'),
             sg.FileBrowse(key='html_file_path')],
            [sg.Text('Import File', size=(16, 1)), sg.InputText(key='import_text', disabled=True),
             sg.FileBrowse(key='text_file_path', disabled=True)],
            [sg.Text('Key', size=(16, 1)), sg.InputText(password_char='*', disabled=True, key='encypt_key')],
            # [sg.Output(size=(20, 10))],
            [sg.Submit('Submit', key='SUBMIT'), sg.Cancel('Cancel', key='CANCEL')]]

        self.window = sg.Window('FCV Packager', self.layout)


class HtmlConvert:

    def __int__(self):
        pass

    def run_convert(self, values):
        import_data = pd.read_html(values['import_html'])

        data = import_data[0].fillna(0)

        data['Filename'] = data['Filename'].apply(self.hash_func)

        data = data.drop(['Full Path', 'File Owner'], axis=1)
        data['First Event Time'] = pd.to_datetime(data['First Event Time'])
        data['Last Event Time'] = pd.to_datetime(data['Last Event Time'])
        data['Modified Time'] = pd.to_datetime(data['Modified Time'])
        data['Created Time'] = pd.to_datetime(data['Created Time'])

        key = Fernet.generate_key()
        fernet = Fernet(key)
        with open('filekey.key', 'wb') as file_key:
            file_key.write(key)

        data_json = data.to_json().encode("utf-8")
        encrypted = fernet.encrypt(data_json)

        with open('data_encrypted.txt', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        sg.popup('Data Exported!')

    def unencrypt(self, values):
        with open(values['import_text'], 'rb') as encrypted_file:
            encrypted = encrypted_file.read()

        fernet = Fernet(values['encypt_key'])

        decrypted = fernet.decrypt(encrypted).decode('utf-8')

        data_json = json.loads(decrypted)

        with open('decypted_file.json', 'w') as json_file:
            json.dump(data_json, json_file)

        sg.popup('JSON file saved!')

    def hash_func(self, file_name):
        hash_val = hashlib.sha256()
        encoded_string = file_name.encode('utf-8')
        hash_val.update(encoded_string)
        return_value = hash_val.hexdigest()
        return return_value


class main():
    g = Gui()
    s = HtmlConvert()
    import_html = True

    while True:
        event, values = g.window.Read()
        if event is None or event == 'CANCEL':
            break
        if event == 'SUBMIT':
            if import_html and not values['import_html']:
                sg.popup_error('We need the HTML file!')
            elif import_html and values['import_html']:
                s.run_convert(values)
            if not import_html and not values['import_text'] and not values['encypt_key']:
                sg.popup_error('Check inputs')
            elif not import_html and values['import_text'] and values['encypt_key']:
                s.unencrypt(values)
        if event == 'export_select':
            if import_html:
                g.window['import_html'].update(disabled=True)
                g.window['html_file_path'].update(disabled=True)

                g.window['import_text'].update(disabled=False)
                g.window['text_file_path'].update(disabled=False)

                g.window['encypt_key'].update(disabled=False)
                import_html = False
        if event == 'import_select':
            if not import_html:
                g.window['import_html'].update(disabled=False)
                g.window['html_file_path'].update(disabled=False)

                g.window['import_text'].update(disabled=True)
                g.window['text_file_path'].update(disabled=True)

                g.window['encypt_key'].update(disabled=True)
                import_html = True
        if event == 'About...':
            sg.popup('Created by Ed howard @ Veeam; edward.x.howard@veeam.com')

