import discord

class Embed():
    class Default(discord.Embed):
        def __init__(self, title = None, description = None):
            super().__init__(title=title, description=description, color=discord.Color.orange())
            self.set_image(url="https://www.dropbox.com/scl/fi/70b9ckjwrfilds65gbs11/gradient_bar.png?rlkey=922kwpi4t17lk0ju4ztbq6ofc&st=nb9saec1&dl=1")
            self.set_thumbnail(url="https://www.dropbox.com/scl/fi/a21ptajqddfkhilx1e4st/mi-2025.png?rlkey=29x0wvk1np17a3nvddth0jnyk&st=s6r4f2kr&dl=1")