from jujitsu_library import jujitsu, human_player, create_remote_player

# Connects to a jujitsu server running on this computer. If you know the IP 
# address and port for a different computer running a jujitsu server, 
# you can connect to that server by entering its address instead of 'localhost'
# below.
remote = create_remote_player("http://localhost", 5555)

# You could replace the human player with your own chooser function here
# to test your program against the server.
human_name = raw_input("What is your name? ")
jujitsu(human_player, remote, human_name, "The computer")
