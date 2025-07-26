from kivy.clock import mainthread
from kivy.logger import Logger, LOG_LEVELS
from kivy.metrics import dp
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import discordapi
import logging
import rpc
import settings
import webview

import time

Logger.setLevel(LOG_LEVELS["debug"])
logging.getLogger("requests").setLevel(logging.INFO)
logging.getLogger("websockets").setLevel(logging.INFO)

if platform == "android":
    from kivymd.toast import toast
    from android_notify import Notification
else:
    from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
    def toast(text):
        MDSnackbar(
            MDSnackbarText(
                text = text,
            ),
            y = dp(24),
            pos_hint = {"center_x": 0.5},
            size_hint_x = 0.5,
        ).open()
    
TAG = "DBTools App" + ": "

class DBTools(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"Running on {platform}")

        self.webviewScreen = None
        self.currentRPCSession: rpc.RPCSession = None
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Darkgreen"
        self.ScreenRoot = MDScreen(
            MDBoxLayout(
                MDLabel(
                    id = "status",
                    text = "Login to Discord to start RPC",
                    font_style = "Title",
                    halign = "center",
                    pos_hint = {"center_x": 0.5},
                    adaptive_height = True
                ),
                MDButton(
                    MDButtonText(
                        text = "Notify Test"
                    ),
                    on_press = self.notifyTest,
                    pos_hint = {"center_x": 0.5}
                ),
                MDButton(
                    MDButtonText(
                        id = "LoginToDiscordText",
                        text = "Login to Discord"
                    ),
                    on_press = self.loginToDiscordCallback,
                    id = "LoginToDiscordButton",
                    pos_hint = {"center_x": 0.5}
                ),
                MDButton(
                    MDButtonText(
                        id = "StartRPCText",
                        text = "Start RPC"
                    ),
                    on_press = self.startRPC,
                    id = "StartRPCButton",
                    pos_hint = {"center_x": 0.5}
                ),
                id = "meow",
                spacing = dp(5),
                orientation = "vertical",
                adaptive_height = True,
                pos_hint = {"center_x": 0.5, "center_y": 0.5}
            )
        )
        self.Screen = self.ScreenRoot.get_ids()
        return self.ScreenRoot
    
    def on_start(self):
        if settings.getSetting("token"):
            Logger.debug(TAG + "Logged into discord, applying username to gui")
            self.applyUsernameAndCallback()
        print(self.Screen.meow.height, self.Screen.meow.line_width, self.Screen.meow.pos)
    
    @mainthread
    def notifyTest(self, *args):
        if platform != "android":
            toast("Please run this on android")
            return
        
        Logger.debug(TAG + "Creating notification object")
        notification = Notification(
            title = "Connected to server",
            message = "Located at Pyongyang, NK"
        )
        notification.addLine("Place ID: 142823291")
        notification.addLine("Job ID: 123e4567-e89b-12d3-a456-426614174000")
        notification.addLine("UDMUX IP: 128.116.12.34")

        Logger.debug(TAG + "Sending out notification")
        notification.send()
    
    def applyUsernameAndCallback(self):
        Logger.debug(TAG + "Getting username")
        username = discordapi.getUsername(settings.getSetting("token"))
        if not username:
            Logger.error(TAG + "A problem has occurred.. O_O")
            return
        
        Logger.debug(TAG + f"Username is {username}, putting it to text and setting callback")
        self.Screen.status.text = f"Logged in as {username}"
        self.Screen.LoginToDiscordText.text = "Logout of Discord"
        self.Screen.LoginToDiscordButton.on_press = self.logoutOfDiscordCallback

    @mainthread
    def loginToDiscordCallback(self, *args):
        if settings.getSetting("token"): return
        if self.webviewScreen: return
        if platform != "android":
            toast("Please run this on android")
            return
        
        Logger.debug(TAG + "Creating webview")
        self.webviewScreen = webview.DiscordLoginWebView()
        self.webviewScreen.onLoginCompleted = self._onLoginCompleted
        Logger.debug(TAG + "Starting webview")
        self.webviewScreen.startWebview()
        
    
    def _onLoginCompleted(self, token):
        Logger.debug(TAG + "Done logging in, setting token and applying username")
        settings.setSetting("token", token)
        self.applyUsernameAndCallback()

    @mainthread
    def logoutOfDiscordCallback(self, *args):
        if not settings.getSetting("token"): return
        Logger.debug(TAG + "Logging out of discord")
        discordapi.logout(settings.getSetting("token"))

        Logger.debug(TAG + "Setting token to None")
        settings.setSetting("token", None)

        Logger.debug(TAG + "Changing callbacks and text")
        self.Screen.status.text = "Login to Discord to start RPC"
        self.Screen.LoginToDiscordText.text = "Login to Discord"
        self.Screen.LoginToDiscordButton.on_press = self.loginToDiscordCallback

    @mainthread
    def startRPC(self, *args):
        if self.currentRPCSession: return
        token = settings.getSetting("token")
        if not token:
            toast("Login to Discord to start RPC!")
            return
        
        Logger.debug(TAG + "Getting MP of cute kitty >_<")
        mpOfCuteKitty = discordapi.getMPOfUrls(
            token = token,
            applicationId = rpc.models.BLOXSTRAP_APPLICATION_ID,
            urls = ["https://media.tenor.com/k0VpFy4zjkIAAAAM/joy-snow-day.gif"]
        )[0]
        Logger.debug(TAG + f"Media Proxy URL is {mpOfCuteKitty}")

        Logger.info(TAG + "Starting RPC")
        self.currentRPCSession = rpc.RPCSession(token)
        self.currentRPCSession.start()
        self.currentRPCSession.changeRPC(rpc.models.ChangeRPCPayload(
            name = "FemboyStrap",
            details = "Playing femboy obby",
            state = "by drake",
            timeStart = time.time() * 1000,
            largeImage = mpOfCuteKitty,
            largeText = "cute cat",
            smallImage = mpOfCuteKitty,
            smallText = "cute cat right?",
            buttons = [rpc.models.Button(
                label = "Check out DroidBlox",
                url = "https://github.com/meowstrapper/DroidBlox"
            )]
        ))

        Logger.debug(TAG + "Changing text and button callback")
        self.Screen.StartRPCText.text = "Stop RPC"
        self.Screen.StartRPCButton.on_press = self.stopRPC

    @mainthread
    def stopRPC(self, *args):
        if not self.currentRPCSession: return
        Logger.info(TAG + "Stopping RPC")
        self.currentRPCSession.removeRPC()
        self.currentRPCSession.stop()
        self.currentRPCSession = None

        Logger.debug(TAG + "Changing text and button callback")
        self.Screen.StartRPCText.text = "Start RPC"
        self.Screen.StartRPCButton.on_press = lambda: self.startRPC()
DBTools().run()