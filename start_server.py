from jujitsu_library import jujitsu_server, usually_choose_treasure

# To create a server, pass in a chooser function the server should use in 
# deciding what card to play.
app = jujitsu_server(usually_choose_treasure)

# This causes the program to go into an infinite loop, waiting for players
# to connect. When they do, the server replies to them with its choice for
# which card to play.
app.run(host="0.0.0.0", port=5555, debug=True)

