from jujitsu_library import jujitsu, human_player, create_remote_player

# Connects to a jujitsu server running on this computer. If you know the IP 
# address and port for a different computer running a jujitsu server, 
# you can connect to that server by entering its address below.
remote = create_remote_player("http://localhost:5555/jujitsu", 5555)

# You could replace the human player with your own chooser function here
# to test your program against the server.
jujitsu(human_player, remote, "Player", "The computer")