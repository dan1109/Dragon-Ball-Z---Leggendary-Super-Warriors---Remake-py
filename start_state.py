
class StartState:
    def __init__(self):
        self.message = "Start"
        self.message_visible = True
        self.timer = 0
        self.message_duration = 500  # Tempo in millisecondi per cui il messaggio è visibile

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.message_duration:
            self.message_visible = not self.message_visible
            self.timer = 0
