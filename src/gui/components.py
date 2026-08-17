import customtkinter as ctk


class MarqueeFooter(ctk.CTkFrame):
    """Componente de rodapé com texto em rolagem contínua."""

    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master, fg_color="#1E3A8A", corner_radius=8, height=45, **kwargs
        )
        self.raw_text = text
        self.pos = 0

        self.label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#F8FAFC",
        )
        self.label.pack(fill="x", pady=8)
        self.animate()

    def animate(self):
        full_text = self.raw_text * 3
        visible = full_text[self.pos : self.pos + 60]
        self.label.configure(text=visible)
        self.pos = (self.pos + 1) % len(full_text)
        self.after(160, self.animate)