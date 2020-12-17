import eel

i=0
eel.init('html')
eel.start(
'connect.html',
     mode='chrome',
#        cmdline_args=['--start-fullscreen'],
block=False)

while(i<1000):
    eel.sleep(0.01)
    print(i)
    i+=1
