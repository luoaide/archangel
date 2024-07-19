# The Network Architecture

Skydios x14 
Teal II x6
DJI x14



Each box runs:
1. ZeroTierOne (need to develop interface for access management)
2. 

# Security
Streams are not encrypted.
All packets are encryptede


# Static IP Architecture
Naming SOP = Acquatic Mammals
Muskrat[1 - 14] = DJI (20 series)
Walrus[1 - X] = PUMA (30 series)
Dolphin[1 - 6] = Teal (40 series)
Beaver[1 - 14] = Skydio (50 series)
Orca [1 - 4] = PDW (60 series)

Each box has a label with its:
ZeroTier VLAN IP Address + DNS Name
DHCP Server Address
ZeroTier Address
TAK Server Address (?)
mediaMTX Ports... address?

# SYSTEM DIAGRAM

+-----------------+   +-----------------+   +-----------------+   +-----------------+
| UAS CONTROLLER  |   | DJI CONTROLLER  |   | UAS CONTROLLER  |   | UAS CONTROLLER  |  
|   *DHCP_ADDR    |   |   +ZeroTier-One |   |   *DHCP_ADDR    |   |   *DHCP_ADDR    |
+-----------------+   +-----------------+   +-----------------+   +-----------------+
         ||                   ||                    ||                  ||
         ||                   ||                    ||                  ||
         ||                   ||                    ||                  ||
         ||                   ||                    ||                  ||
+--[RTSP:8554]----+   +--[RTMP:8000]----+   +--[RTSP:8554]----+   +--[RTSP:8554]----+          +---------------------------+
| ARCHANGEL BOX   |   | ARCHANGEL BOX   |   | ARCHANGEL BOX   |   | ARCHANGEL BOX   |          | ARCHANGEL WEBSERVER       |
|   +ZeroTier-One |===|   +ZeroTier-One |===|   +ZeroTier-One |===|   +ZeroTier-One |=={API}==>|   IP: archangel.webserver |
|   +DHCP_SERVER  |   |   +DHCP_SERVER  |   |   +DHCP_SERVER  |   |   +DHCP_SERVER  |          |   +ZT_NETWORKCONTROLLER   |
|   +MEDIAMTX     |   |   +MEDIAMTX     |   |   +MEDIAMTX     |   |   +MEDIAMTX     |          |   +DNS_SERVER             |
+-[UDP-Multicast]-+   +-[UDP-Multicast]-+   +-[UDP-Multicast]-+   +-[UDP-Multicast]-+          +-[uWSGI Web Server: 5000]--+
         ||    \\         //  ||  \\                                          ||                         /\ + [API ENDPOINTS]
         ||     \\       //   ||   \\                                         ||                         ||
         ||      \\     //    ||    \\                                        ||                         ||
         ||       \\   //     ||     \\                                       ||                         ||
         ||        \\ //      ||      \\========={Live Streams}=========\\    ||                         ||
         ||         \V/       ||                                        ||    ||                         || {Live Stream State}
         ||        // \\      ||                                        ||    ||                         ||
         ||       //   \\     ||                                        ||    ||                         ||
         \/      \/     \/    \/                                        \/    \/                         ||
+-------------------+   +-------------------+                    +-------------------+                   ||
| ARCHANGEL C2 NODE |   | ARCHANGEL C2 NODE |                    | ARCHANGEL C2 NODE |                   ||
|   +ZeroTier-One   |   |   +ZeroTier-One   |                    |   +zeroTier-One   |                   ||
|   +mediaMTX       |===|   +mediaMTX       |========{API}=======|   +mediaMTX       |===================//
+-------------------+   +-------------------+                    +-------------------+

# NODE DIAGRAM

N

# Hardware Requirements
https://ninkear.com/products/ninkear-mini-pc-n9-intel-yang-n95-processor-3-4ghz-8gb-ddr4-256gb-ssd-dual-frequency-wifi-gigabit-lan-bluetooth-4-2-window-11-mini-computer?gad_source=1&gclid=CjwKCAjw7NmzBhBLEiwAxrHQ-aLUcNRyzMiokEmTYVNNGHXCmLokJIvsA3m1lZCckapc6jXFUB7OSxoCioMQAvD_BwE

https://fit-iot.com/web/products/fitlet3/

https://simplynuc.com/product/nuc13oxi5/

https://www.newegg.com/asus-pn52-bb7000x1td-nl/p/N82E16856110279?Item=N82E16856110279

https://us.dfi.com/product/index/1545

https://us.dfi.com/product/index/1637


TAK Server

# MEDIA STREAMING
all Nodes have an IP
All nodes, when streaming, publish their feed to https://node-ip:8889/feed

TOCs are different nodes. They are configured to replicate (mirror) RTSP streams to TOC-specific URL mapping
in order to enable UDP multicast across the ad-hoc network instead of WebRTC connections to each of the 
edge nodes.

A TOC subscribes (with its instance of mediaMTX server, to the RTSP stream from each of the remotes)

Then the GUI maps each of those urls to a player. That way the C2 Node Server can be beefier and handle those concurrent streams. Need laptops for this...running ubuntu would be nice.

Need to build a good mediaMTX config file for the server.

TRY HLS to see performance comparisons with WebRTC.

Big question... when proxying streams and loading the website on thefed at the same time, the video stream sucks, but serving the website and querying the proxied stream from aiden-air is near real-time. Is this a different in graphics cards? Or is there something about proxying to localhost and also requesting feeds from localhost that degrades performance?

# SETUP EDGE NODE
zerotier setup info is in /var/etc/zerotier-one

This should all be a dockerfile so that the generic node is a docker image with a config file
1. Install OS: Ubuntu 22.0.4
2. Create archangel user (what are the permissions?)
2. Download ZeroTier One
    curl -s https://install.zerotier.com | sudo bash
2. Get ZeroTier One Address with
    sudo zerotier-cli info
5. Request to join ZeroTier Network
6. Authorize the new now with the Zero Tier Network Controller
7. Configure ZeroTier to run on start
8. in ~/archangel download mediaMTX wiht:
9. Upload the custom mediamtx-node.yml file into the location.
10. Upload the API calling script into the same location.
11. Ensure the API script has execution permissions for user archangel
12. Install DHCP server (dnsmasq)
13. Upload the custom configuration for dnsmasq
14. Disallow all ip traffic from all ports on any public-facing interface.s
15. Install mediaMTX from https://github.com/bluenviron/mediamtx/releases with wget
16. tar -xvzf medi...


# SETUP WEBSERVER
To get DNS to work... sigh.... I
1. systemd-resolv was running and listening on port 53... so I turned that off and hid it
2. Then I editted /etc/resolv.conf with the nameservers (which I think ended up not being necessary)
3. Then I added the local=/archangel/ to /etc/dnsmasq.conf so that all requests for archangel TLD would
    reference the /etc/hosts on the server
4. So now I need to put the entire architecture into /etc/hosts on the server
5. Question for myself? Why am I bothering asking for the "name" on the /network page when I already have decided who
    is named what with my hard-coded DNS mapping? Is that just creating room for error and people messing up?
