from flexx import app, ui, event
import os

class IRS(ui.Widget):

    def init(self):

        with ui.FormLayout() as self.form:
            self.song = ui.LineEdit(placeholder_text="Song Name")
            self.artist = ui.LineEdit(placeholder_text="Artist Name")
            self.submit = ui.Button(text="Submit")
            self.output = ui.Label(text="")
            ui.Widget(flex=2)

    """@event.connect("submit.mouse_click", "artist.submit")
    def _button_clicked(self, *events):
        self.output.text = os.system('irs -a "%s" -s "%s"' % (self.artist.text, self.song.text))
"""

if __name__ == '__main__':
    m = app.launch(IRS)
    app.run()
